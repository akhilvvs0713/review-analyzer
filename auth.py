import bcrypt
from datetime import datetime, timedelta
from jose import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

SECRET_KEY = "your-secret-key-keep-this-safe"
ALGORITHM = "HS256"
EXPIRE_MINUTES = 30

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode('utf-8'), hashed.encode('utf-8'))

def create_token(data: dict):
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(minutes=EXPIRE_MINUTES)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = verify_token(token)
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")