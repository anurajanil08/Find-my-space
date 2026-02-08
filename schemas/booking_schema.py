from pydantic import BaseModel
from datetime import datetime

class BookingCreate(BaseModel):
    user_id: int
    theatre_id: int
    tickets: int = 1

class BookingResponse(BaseModel):
    id: int
    user_id: int
    theatre_id: int
    tickets: int
    booking_time: datetime

    class Config:
        orm_mode = True
