import joblib
from database import SessionLocal
from models import Review

model = joblib.load("ml_models/sentiment_model.pkl")
vectorizer = joblib.load("ml_models/sentiment_vectorizer.pkl")

db = SessionLocal()
reviews = db.query(Review).all()

for review in reviews:
    vec = vectorizer.transform([review.review_text])
    prediction = model.predict(vec)[0]
    review.sentiment = prediction

db.commit()
db.close()

print(f"Updated sentiment for {len(reviews)} reviews")