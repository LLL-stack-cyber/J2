from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr, Field

from backend.services.auth_service import AuthService

router = APIRouter()
auth_service = AuthService()


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str = Field(min_length=2)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


@router.post("/register")
def register(payload: RegisterRequest) -> dict:
    return auth_service.register_user(payload.email, payload.full_name)


@router.post("/login")
def login(payload: LoginRequest) -> dict:
    res = auth_service.login_user(payload.email, payload.password)
    
    # Check if the result is an error and raise HTTPException if needed
    if res.get("status") == "error":
        raise HTTPException(
            status_code=res.get("code", 400),
            detail=res.get("message")
        )

    return res
