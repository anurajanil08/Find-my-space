from fastapi import FastAPI
from routers.auth_router import router as auth_router

app = FastAPI(title="Find your space")

app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "Backend is running 🚀"}
