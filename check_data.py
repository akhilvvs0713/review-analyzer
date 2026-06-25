from database import SessionLocal
from models import Review

db = SessionLocal()
results = db.query(Review.product_id, Review.product_name).distinct().limit(5).all()
db.close()

for r in results:
    print(r.product_id, "-", r.product_name)