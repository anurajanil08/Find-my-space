from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from database import SessionLocal
from models.user_model import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme)):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id = payload.get("user_id")
        role = payload.get("role")

        if user_id is None or role is None:
            raise HTTPException(status_code=401, detail="Invalid token")

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    db = SessionLocal()

    user = db.query(User).filter(User.id == user_id).first()

    db.close()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


def admin_required(current_user: User = Depends(get_current_user)):
    """Allow access only if the user is ADMIN"""
    if current_user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

def organizer_required(current_user: User = Depends(get_current_user)):
    """Allow access only if the user is ORGANIZER"""
    if current_user.role != "ORGANIZER":
        raise HTTPException(status_code=403, detail="Organizer access required")
    return current_user

def user_required(current_user: User = Depends(get_current_user)):
    """Allow access only if the user is a normal USER"""
    if current_user.role != "USER":
        raise HTTPException(status_code=403, detail="User access required")
    return current_user

