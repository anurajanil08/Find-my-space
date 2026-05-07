from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from database import Base


class OrganizerApplication(Base):
    __tablename__ = "organizer_applications"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    address = Column(String, nullable=True)
    bank_details = Column(String, nullable=True)
    aadhar_number = Column(String, nullable=False, unique=True)
    pan_number = Column(String, nullable=False, unique=True)


    status = Column(String, default="PENDING")  # PENDING / APPROVED / REJECTED

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    # reviewed_at = Column(DateTime, nullable=True)
    # reapply_allowed_at = Column(DateTime, nullable=True)