from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models.organizer_application_model import OrganizerApplication
from schemas.organizer_application_schema import OrganizerApplicationCreate, OrganizerApplicationOut
from core.security import get_current_user
from models.user_model import User

router = APIRouter(prefix="/organizer", tags=["Organizer Application"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/apply")
def apply_organizer(
    data: OrganizerApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if user already applied
    existing = db.query(OrganizerApplication).filter(
        OrganizerApplication.user_id == current_user.id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="You already have a pending application")

    application = OrganizerApplication(
        user_id=current_user.id,
        **data.dict()
    )
    db.add(application)
    db.commit()
    db.refresh(application)

    return {"message": "Application submitted successfully"}

@router.get("/my-application")
def get_my_application(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    application = db.query(OrganizerApplication).filter(
        OrganizerApplication.user_id == current_user.id
    ).first()

    if not application:
        raise HTTPException(
            status_code=404,
            detail="You have not applied for organizer yet"
        )

    return {
        "name": application.name,
        "email": application.email,
        "status": application.status,
        "applied_at": application.created_at
    }