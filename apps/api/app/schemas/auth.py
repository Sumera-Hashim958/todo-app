"""Pydantic schemas for authentication endpoints"""
from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from typing import Optional
import re


class UserRegisterRequest(BaseModel):
    """Request schema for user registration"""
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """
        Validate password strength:
        - Min 8 characters
        - At least 1 uppercase letter
        - At least 1 lowercase letter
        - At least 1 number
        """
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")

        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")

        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")

        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one number")

        return v


class UserLoginRequest(BaseModel):
    """Request schema for user login"""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """User data in API responses"""
    id: int
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


class AuthResponse(BaseModel):
    """Response schema for authentication endpoints (register/login)"""
    user: UserResponse
    token: str


class LogoutResponse(BaseModel):
    """Response schema for logout endpoint"""
    message: str
