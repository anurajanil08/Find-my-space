from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# Existing schemas (keep yours, but ensure they match)
class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Optional[str] = "USER"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# --- New Schemas for OTP & Reset ---

class VerifyOTP(BaseModel):
    email: EmailStr
    otp_code: str = Field(..., min_length=6, max_length=6)

class ForgotPassword(BaseModel):
    email: EmailStr

class ResetPassword(BaseModel):
    email: EmailStr
    otp_code: str
    new_password: str
    confirm_password: str

    # Optional: Add a check to ensure passwords match
    def check_passwords(self):
        if self.new_password != self.confirm_password:
            raise ValueError("Passwords do not match")



