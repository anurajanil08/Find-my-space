from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database import SessionLocal
from models.user_model import User
from schemas.user_schema import UserRegister, UserLogin
from core.security import hash_password, verify_password, create_access_token, generate_otp, send_otp_email

router = APIRouter(prefix="/auth", tags=["Auth"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(user: UserRegister, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    otp = generate_otp()
    hashed_pw = hash_password(user.password)

    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_pw,
        role=user.role,
        otp_code=otp,
        otp_expiry=datetime.utcnow() + timedelta(minutes=5), # Valid for 5 mins
        is_verified=False
    )

    db.add(new_user)
    db.commit()
    
    # Send email in the background
    background_tasks.add_task(send_otp_email, user.email, otp)

    return {"message": "Registration successful. Please check your email for the OTP."}

@router.post("/verify-otp")
def verify_otp(email: str, otp: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    
    if not user or user.otp_code != otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    
    if datetime.utcnow() > user.otp_expiry:
        raise HTTPException(status_code=400, detail="OTP has expired")

    user.is_verified = True
    user.otp_code = None  # Clear OTP after use
    db.commit()
    
    return {"message": "Account verified successfully"}

@router.post("/forgot-password")
def forgot_password(email: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    otp = generate_otp()
    user.otp_code = otp
    user.otp_expiry = datetime.utcnow() + timedelta(minutes=10)
    db.commit()

    background_tasks.add_task(send_otp_email, email, otp)
    return {"message": "Password reset OTP sent to email"}



@router.post("/reset-password")
def reset_password(email: str, otp: str, new_password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email, user.otp_code == otp).first()
    
    if not user or datetime.utcnow() > user.otp_expiry:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    user.password = hash_password(new_password)
    user.otp_code = None
    db.commit()
    
    return {"message": "Password updated successfully"}


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user.is_verified:
        raise HTTPException(status_code=401, detail="Please verify your email first.")
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token(
        data={
            "user_id": db_user.id,
            "role": db_user.role
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": db_user.role
    }
