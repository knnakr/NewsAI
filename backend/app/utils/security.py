"""
Security utilities for password hashing, JWT tokens, and token management.
"""
from werkzeug.security import generate_password_hash, check_password_hash
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
import hashlib
import secrets
from app.config import settings


def hash_password(plain: str) -> str:
    """
    Hash a plain text password using PBKDF2-SHA256.
    
    Args:
        plain: Plain text password
    
    Returns:
        Hashed password string
    """
    return generate_password_hash(plain, method="pbkdf2:sha256")


def verify_password(plain: str, hashed: str) -> bool:
    """
    Verify a plain text password against a hash.
    
    Args:
        plain: Plain text password to verify
        hashed: Hashed password to compare against
    
    Returns:
        True if password matches, False otherwise
    """
    return check_password_hash(hashed, plain)


def create_access_token(user_id: str) -> str:
    """
    Create a JWT access token.
    
    Args:
        user_id: User ID to encode in token
    
    Returns:
        JWT access token string
    """
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": user_id, "exp": expire}
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token() -> tuple[str, str]:
    """
    Create a refresh token pair (plain, hashed).
    
    Returns:
        Tuple of (plain_token, hashed_token)
    """
    plain = secrets.token_urlsafe(32)
    return plain, hash_token(plain)


def decode_access_token(token: str) -> dict:
    """
    Decode and validate a JWT access token.
    
    Args:
        token: JWT token string
    
    Returns:
        Decoded payload dictionary
    
    Raises:
        JWTError: If token is invalid or expired
    """
    return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])


def hash_token(plain: str) -> str:
    """
    Hash a token using SHA256 for database storage.
    
    Args:
        plain: Plain token string
    
    Returns:
        SHA256 hash of token
    """
    return hashlib.sha256(plain.encode()).hexdigest()
