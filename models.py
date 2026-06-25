
from sqlalchemy import Column, Integer, String
from database import Base

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String)
    quantity = Column(Integer)
    status = Column(String, default="placed")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from database import Base

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    role = Column(String)        # "user" or "assistant"
    content = Column(String)
    created_at = Column(DateTime, server_default=func.now())
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String, index=True)       # from asins
    product_name = Column(String)                  # from name
    review_text = Column(String)                   # from reviews.text
    review_title = Column(String)                  # from reviews.title
    rating = Column(Float)                          # from reviews.rating
    sentiment = Column(String, nullable=True)        # we'll fill this in Day 12
    is_fake = Column(Boolean, default=False)         # we'll fill this in Day 13
    helpful_count = Column(Integer, default=0)       # from reviews.numHelpful
    recommend = Column(Boolean, nullable=True)       # from reviews.doRecommend
    username = Column(String, nullable=True)
    review_date = Column(String, nullable=True)