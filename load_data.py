import pandas as pd
from database import SessionLocal, engine, Base
from models import Review

Base.metadata.create_all(bind=engine)

df = pd.read_csv("data/raw_reviews.csv")

# keep only rows where review text actually exists
df = df.dropna(subset=["reviews.text"])

db = SessionLocal()


def clean_bool(value):
    if pd.isna(value):
        return None
    return bool(value)


def clean_float(value):
    if pd.isna(value):
        return None
    return float(value)


def clean_int(value):
    if pd.isna(value):
        return 0
    return int(value)


def clean_str(value, default="unknown"):
    if pd.isna(value):
        return default
    return str(value)


count = 0
for _, row in df.iterrows():
    review = Review(
        product_id=clean_str(row.get("asins")),
        product_name=clean_str(row.get("name")),
        review_text=clean_str(row.get("reviews.text"), default=""),
        review_title=clean_str(row.get("reviews.title"), default=""),
        rating=clean_float(row.get("reviews.rating")),
        helpful_count=clean_int(row.get("reviews.numHelpful")),
        recommend=clean_bool(row.get("reviews.doRecommend")),
        username=clean_str(row.get("reviews.username"), default="anonymous"),
        review_date=clean_str(row.get("reviews.date"), default="")
    )
    db.add(review)
    count += 1

db.commit()
db.close()

print(f"Loaded {count} reviews into PostgreSQL")