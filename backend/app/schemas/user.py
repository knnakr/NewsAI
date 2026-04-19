"""
Pydantic schemas for user authentication and profile management.
"""
from datetime import datetime
from typing import Optional, List, Literal
import uuid
from pydantic import BaseModel, EmailStr, field_validator, ConfigDict


class RegisterRequest(BaseModel):
    """Request schema for user registration."""
    email: EmailStr
    password: str
    display_name: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "password": "securepass123",
                "display_name": "John Doe",
            }
        }
    )

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

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "password": "securepass123",
            }
        }
    )


class TokenResponse(BaseModel):
    """Response schema for authentication tokens."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "eyJhbGciOi...",
                "token_type": "bearer",
                "expires_in": 900,
            }
        }
    )


class UserResponse(BaseModel):
    """Response schema for user profile."""
    id: uuid.UUID
    email: str
    display_name: str
    role: str
    email_verified_at: Optional[datetime] = None
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "11111111-1111-1111-1111-111111111111",
                "email": "user@example.com",
                "display_name": "John Doe",
                "role": "user",
                "email_verified_at": None,
                "created_at": "2026-04-05T12:00:00Z",
            }
        },
    )


class UpdateUserRequest(BaseModel):
    """Request schema for updating user profile."""
    display_name: Optional[str] = None

    model_config = ConfigDict(
        json_schema_extra={"example": {"display_name": "Updated Name"}}
    )

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
    orchestrator: Literal["crewai", "langgraph"]
    news_categories: List[str]
    email_digest: bool

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "language": "Turkish",
                "ai_tone": "neutral",
                "orchestrator": "crewai",
                "news_categories": ["world", "technology"],
                "email_digest": False,
            }
        },
    )


class UpdatePreferencesRequest(BaseModel):
    """Request schema for updating user preferences."""
    language: Optional[str] = None
    ai_tone: Optional[str] = None
    orchestrator: Optional[Literal["crewai", "langgraph"]] = None
    news_categories: Optional[List[str]] = None
    email_digest: Optional[bool] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "language": "English",
                "ai_tone": "formal",
                "orchestrator": "langgraph",
                "news_categories": ["technology"],
                "email_digest": True,
            }
        }
    )

    @field_validator("ai_tone")
    @classmethod
    def validate_ai_tone(cls, v):
        if v is None:
            return v
        allowed = {"neutral", "formal", "casual"}
        if v not in allowed:
            raise ValueError("Invalid ai_tone")
        return v
