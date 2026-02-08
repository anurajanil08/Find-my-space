from fastapi import APIRouter, Depends
from core.security import admin_required
from schemas.theatre_schema import TheatreCreate
from models.theatre_model import Theatre
from database import SessionLocal

router = APIRouter(prefix="/admin", tags=["Admin"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



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