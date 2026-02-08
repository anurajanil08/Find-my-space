from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class Theatre(Base):
    __tablename__ = "theatres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    location = Column(String)
    organizer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
