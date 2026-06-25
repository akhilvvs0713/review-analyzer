import pandas as pd
from database import SessionLocal
from models import Review

db = SessionLocal()
reviews = db.query(Review).all()


def build_duplicate_signal(reviews):
    """
    Returns a set of review_texts that appear under MORE THAN ONE
    distinct username — a real fraud signal, not scraping noise.
    """
    text_to_usernames = {}
    for r in reviews:
        text_to_usernames.setdefault(r.review_text, set()).add(r.username)

    return {text for text, usernames in text_to_usernames.items() if len(usernames) > 1}


def is_duplicate_text(review_text, duplicate_set):
    return review_text in duplicate_set


def is_too_short(review_text, min_words=5):
    """Genuine reviews usually have some detail. Very short reviews are weak signals."""
    return len(review_text.split()) < min_words


def has_excessive_punctuation(review_text):
    """Fake/spam reviews often overuse exclamation marks or caps for emphasis."""
    exclamations = review_text.count("!")
    caps_words = sum(1 for word in review_text.split() if word.isupper() and len(word) > 2)
    return exclamations >= 3 or caps_words >= 3


def rating_text_mismatch(rating, review_text):
    """A 5-star rating with negative-sounding words, or 1-star with glowing words, is suspicious."""
    negative_words = ["bad", "terrible", "worst", "hate", "broken", "disappointed", "awful"]
    positive_words = ["great", "love", "amazing", "excellent", "perfect", "best"]

    text_lower = review_text.lower()
    has_negative = any(word in text_lower for word in negative_words)
    has_positive = any(word in text_lower for word in positive_words)

    if rating is None:
        return False
    if rating >= 4 and has_negative and not has_positive:
        return True
    if rating <= 2 and has_positive and not has_negative:
        return True
    return False


# build duplicate signal once, outside the loop
duplicate_across_users = build_duplicate_signal(reviews)

flagged_count = 0
signal_counts = {"duplicate": 0, "short": 0, "punctuation": 0, "mismatch": 0}

for review in reviews:
    score = 0

    if is_duplicate_text(review.review_text, duplicate_across_users):
        score += 2
        signal_counts["duplicate"] += 1

    if is_too_short(review.review_text):
        score += 1
        signal_counts["short"] += 1

    if has_excessive_punctuation(review.review_text):
        score += 1
        signal_counts["punctuation"] += 1

    if rating_text_mismatch(review.rating, review.review_text):
        score += 2
        signal_counts["mismatch"] += 1

    review.is_fake = score >= 2

    if review.is_fake:
        flagged_count += 1

db.commit()
db.close()

print(f"Total reviews: {len(reviews)}")
print(f"Flagged as suspicious: {flagged_count}")
print(f"Percentage flagged: {round(flagged_count / len(reviews) * 100, 2)}%")
print("\nSignal breakdown:")
for signal, count in signal_counts.items():
    print(f"{signal}: {count}")