from pydantic import BaseModel
from typing import Optional


class OrganizerApplicationCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str]
    address: Optional[str]
    bank_details: Optional[str]


class OrganizerApplicationOut(BaseModel):
    id: int
    user_id: int
    name: str
    email: str
    status: str

    class Config:
        from_attributes = True