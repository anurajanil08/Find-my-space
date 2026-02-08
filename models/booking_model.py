from sqlalchemy import Column, Integer, ForeignKey, DateTime
from database import Base
from datetime import datetime

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    theatre_id = Column(Integer, ForeignKey("theatres.id"))
    booking_time = Column(DateTime, default=datetime.utcnow)
    tickets = Column(Integer, default=1)
