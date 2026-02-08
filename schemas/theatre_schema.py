from pydantic import BaseModel

class TheatreCreate(BaseModel):
    name: str
    location: str
