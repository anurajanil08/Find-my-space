from fastapi import FastAPI
from routers.auth_router import router as auth_router
from routers.admin_router import router as admin_router
from routers.organizer_application_router import router as organizer_router
from database import Base, engine
from models import *


Base.metadata.create_all(bind=engine)
app = FastAPI(title="Find your space")
app.include_router(admin_router)
app.include_router(auth_router)
app.include_router(organizer_router)

@app.get("/")
def root():
    return {"message": "Backend is running 🚀"}
