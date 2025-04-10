from fastapi import APIRouter
from pydantic import BaseModel
from database.db import SessionLocal
from database.models import User

router = APIRouter(prefix="/users", tags=["Users"])

class UserCreate(BaseModel):
    name: str
    age: int
    height_cm: float
    weight_kg: float
    gender: str  # "male" or "female"
    goal: str     # "cut", "bulk", "maintain"
    diet_type: str  # "vegetarian", "non-vegetarian"
    activity_level: str  # "sedentary", "light", "moderate", "active", "very_active"

@router.post("/")
def create_user(user: UserCreate):
    db = SessionLocal()
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created", "user_id": new_user.id}