from fastapi import APIRouter
from pydantic import BaseModel
from app.db.mongo import db

router = APIRouter()

users_collection = db["users"]


class RegisterRequest(BaseModel):
    user_id: str
    password: str


@router.post("/register")
def register(data: RegisterRequest):

    existing_user = users_collection.find_one({
        "user_id": data.user_id
    })

    if existing_user:
        return {
            "success": False,
            "message": "User ID already exists"
        }

    users_collection.insert_one({
        "user_id": data.user_id,
        "password": data.password
    })

    return {
        "success": True,
        "message": "User registered successfully"
    }


@router.post("/login")
def login(data: RegisterRequest):

    user = users_collection.find_one({
        "user_id": data.user_id
    })

    if not user:
        return {
            "success": False,
            "message": "User not found"
        }

    if user["password"] != data.password:
        return {
            "success": False,
            "message": "Wrong password"
        }

    return {
        "success": True,
        "message": "Login successful",
        "user_id": user["user_id"]
    }