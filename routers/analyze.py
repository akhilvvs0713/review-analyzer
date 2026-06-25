from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import joblib
import os
import sys
from auth import get_current_user
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_db
from auth import get_current_user

router = APIRouter()

# load ONCE when server starts — not inside the route function
model = joblib.load("ml_models/sentiment_model.pkl")
vectorizer = joblib.load("ml_models/sentiment_vectorizer.pkl")


class ReviewInput(BaseModel):
    review_text: str
    rating: float | None = None


def check_fake_signals(review_text: str, rating: float | None):
    """Same logic from Day 13, reused as a live-check function."""
    score = 0
    reasons = []

    word_count = len(review_text.split())
    if word_count < 5:
        score += 1
        reasons.append("review is very short")

    exclamations = review_text.count("!")
    caps_words = sum(1 for w in review_text.split() if w.isupper() and len(w) > 2)
    if exclamations >= 3 or caps_words >= 3:
        score += 1
        reasons.append("excessive punctuation or capitalization")

    negative_words = ["bad", "terrible", "worst", "hate", "broken", "disappointed", "awful"]
    positive_words = ["great", "love", "amazing", "excellent", "perfect", "best"]
    text_lower = review_text.lower()
    has_negative = any(w in text_lower for w in negative_words)
    has_positive = any(w in text_lower for w in positive_words)

    if rating is not None:
        if rating >= 4 and has_negative and not has_positive:
            score += 2
            reasons.append("rating-text sentiment mismatch")
        if rating <= 2 and has_positive and not has_negative:
            score += 2
            reasons.append("rating-text sentiment mismatch")

    return {"is_suspicious": score >= 2, "score": score, "reasons": reasons}


@router.post("/reviews/analyze")
def analyze_review(body: ReviewInput, current_user: dict = Depends(get_current_user)):
    vec = vectorizer.transform([body.review_text])
    sentiment = model.predict(vec)[0]
    confidence = model.predict_proba(vec).max()

    fake_check = check_fake_signals(body.review_text, body.rating)

    return {
        "sentiment": sentiment,
        "confidence": round(float(confidence), 3),
        "fake_check": fake_check,
        "analyzed_by": current_user["email"]
    }
from models import Review
from cache import get_cache, set_cache


@router.get("/products/{product_id}/summary")
def product_summary(product_id: str, db: Session = Depends(get_db)):
    cache_key = f"summary:{product_id}"
    cached = get_cache(cache_key)
    if cached:
        return cached

    reviews = db.query(Review).filter(Review.product_id == product_id).all()

    if not reviews:
        return {"error": "No reviews found for this product"}

    total = len(reviews)
    sentiment_counts = {"positive": 0, "negative": 0, "neutral": 0}
    fake_count = 0

    for r in reviews:
        if r.sentiment in sentiment_counts:
            sentiment_counts[r.sentiment] += 1
        if r.is_fake:
            fake_count += 1

    result = {
        "product_id": product_id,
        "total_reviews": total,
        "sentiment_breakdown": {
            k: round(v / total * 100, 1) for k, v in sentiment_counts.items()
        },
        "suspicious_reviews": fake_count,
        "suspicious_percentage": round(fake_count / total * 100, 1)
    }

    set_cache(cache_key, result, expire_seconds=300)
    return result
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


@router.get("/products/{product_id}/ai-summary")
def ai_summary(product_id: str, db: Session = Depends(get_db)):
    cache_key = f"ai_summary:{product_id}"
    cached = get_cache(cache_key)
    if cached:
        return cached

    reviews = db.query(Review).filter(Review.product_id == product_id).limit(20).all()

    if not reviews:
        return {"error": "No reviews found for this product"}

    review_texts = "\n".join([f"- {r.review_text}" for r in reviews if r.review_text])

    prompt = f"""Here are customer reviews for a product:

{review_texts}

Write a short summary (3-4 sentences) covering:
1. What customers liked
2. What customers complained about
Keep it factual and based only on the reviews above."""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    result = {
        "product_id": product_id,
        "reviews_analyzed": len(reviews),
        "ai_summary": response.choices[0].message.content
    }

    set_cache(cache_key, result, expire_seconds=600)
    return result