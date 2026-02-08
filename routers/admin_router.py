from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models.user_model import User
from models.theatre_model import Theatre
from models.booking_model import Booking
from schemas.user_schema import UserRegister
from schemas.theatre_schema import TheatreCreate
from core.security import hash_password, admin_required

router = APIRouter(prefix="/admin", tags=["Admin"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/bookings")
def get_all_bookings(db: Session = Depends(get_db), admin: User = Depends(admin_required)):
    bookings = db.query(Booking).all()
    return bookings



@router.post("/theatres")
def create_theatre(theatre: TheatreCreate, current_user = Depends(admin_required)):
    # Only admin can access
    db = SessionLocal()
    new_theatre = Theatre(name=theatre.name, location=theatre.location, organizer_id=None)
    db.add(new_theatre)
    db.commit()
    db.refresh(new_theatre)
    db.close()
    return {"message": "Theatre created", "theatre": new_theatre.name}


@router.post("/organizers")
def create_organizer(user: UserRegister, db: Session = Depends(get_db), admin: User = Depends(admin_required)):

    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    hashed_pw = hash_password(user.password)
    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_pw,
        role="ORGANIZER",
        is_active=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": f"Organizer {new_user.name} created successfully"}


@router.put("/organizers/{organizer_id}/approve")
def approve_organizer(organizer_id: int, approve: bool, db: Session = Depends(get_db), admin: User = Depends(admin_required)):

    organizer = db.query(User).filter(User.id == organizer_id, User.role == "ORGANIZER").first()
    if not organizer:
        raise HTTPException(status_code=404, detail="Organizer not found")

    organizer.is_active = approve
    db.commit()
    return {"message": f"Organizer {organizer.name} {'approved' if approve else 'blocked'}"}

