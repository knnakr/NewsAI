"""
Pydantic schemas for user authentication and profile management.
"""
from datetime import datetime
from typing import Optional, List
import uuid
from pydantic import BaseModel, EmailStr, field_validator, ConfigDict


class RegisterRequest(BaseModel):
    """Request schema for user registration."""
    email: EmailStr
    password: str
    display_name: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        """Validate password minimum length."""
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v

    @field_validator("display_name")
    @classmethod
    def validate_display_name(cls, v):
        """Validate display name minimum length."""
        if len(v) < 2:
            raise ValueError("Display name must be at least 2 characters")
        return v


class LoginRequest(BaseModel):
    """Request schema for user login."""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Response schema for authentication tokens."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds


class UserResponse(BaseModel):
    """Response schema for user profile."""
    id: uuid.UUID
    email: str
    display_name: str
    role: str
    email_verified_at: Optional[datetime] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UpdateUserRequest(BaseModel):
    """Request schema for updating user profile."""
    display_name: Optional[str] = None

    @field_validator("display_name")
    @classmethod
    def validate_display_name(cls, v):
        """Validate display name minimum length if provided."""
        if v is not None and len(v) < 2:
            raise ValueError("Display name must be at least 2 characters")
        return v


class UserPreferencesResponse(BaseModel):
    """Response schema for user preferences."""
    language: str
    ai_tone: str
    news_categories: List[str]
    email_digest: bool

    model_config = ConfigDict(from_attributes=True)


class UpdatePreferencesRequest(BaseModel):
    """Request schema for updating user preferences."""
    language: Optional[str] = None
    ai_tone: Optional[str] = None
    news_categories: Optional[List[str]] = None
    email_digest: Optional[bool] = None

    @field_validator("ai_tone")
    @classmethod
    def validate_ai_tone(cls, v):
        if v is None:
            return v
        allowed = {"neutral", "formal", "casual"}
        if v not in allowed:
            raise ValueError("Invalid ai_tone")
        return v
