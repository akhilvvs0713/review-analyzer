from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_db
from models import User
from schemas.user import UserSignup, UserLogin
from auth import hash_password, verify_password, create_token

router = APIRouter()

@router.post("/signup")
def signup(user: UserSignup, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(
        email=user.email,
        password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    return {"message": "Account created successfully"}

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_token({"user_id": db_user.id, "email": db_user.email})
    return {"access_token": token, "token_type": "bearer"}
