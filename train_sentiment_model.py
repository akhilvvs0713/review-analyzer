import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import os

from database import SessionLocal
from models import Review

# --- Step 1: pull data from PostgreSQL, not the raw CSV ---
db = SessionLocal()
reviews = db.query(Review).filter(Review.rating.isnot(None)).all()
db.close()

texts = [r.review_text for r in reviews]
ratings = [r.rating for r in reviews]

print(f"Total labeled reviews: {len(texts)}")


# --- Step 2: derive sentiment labels from star ratings ---
def rating_to_sentiment(rating):
    if rating <= 2:
        return "negative"
    elif rating == 3:
        return "neutral"
    else:
        return "positive"

labels = [rating_to_sentiment(r) for r in ratings]

print("Label distribution:")
print(pd.Series(labels).value_counts())


# --- Step 3: split into train and test sets ---
X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.2, random_state=42
)


# --- Step 4: vectorize text (TF-IDF) ---
vectorizer = TfidfVectorizer(max_features=3000, stop_words="english")
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)


# --- Step 5: train the model ---
model = LogisticRegression(max_iter=1000, class_weight="balanced")
model.fit(X_train_vec, y_train)


# --- Step 6: evaluate ---
predictions = model.predict(X_test_vec)
print("\nModel performance:")
print(classification_report(y_test, predictions, zero_division=0))


# --- Step 7: save model + vectorizer ---
os.makedirs("ml_models", exist_ok=True)
joblib.dump(model, "ml_models/sentiment_model.pkl")
joblib.dump(vectorizer, "ml_models/sentiment_vectorizer.pkl")

print("\nModel saved to ml_models/sentiment_model.pkl")