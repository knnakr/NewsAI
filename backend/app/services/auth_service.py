"""Authentication service layer for register/login/refresh/logout flows."""
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.user import RefreshToken, User
from app.utils.security import (
	create_access_token,
	create_refresh_token,
	hash_password,
	hash_token,
	verify_password,
)


LOCK_DURATION_MINUTES = 15
MAX_FAILED_ATTEMPTS = 5


async def register_user(email: str, password: str, display_name: str, db: AsyncSession) -> User:
	"""Create a new email/password user if email is unique."""
	existing = await db.execute(select(User).where(User.email == email))
	if existing.scalar_one_or_none():
		raise HTTPException(
			status_code=status.HTTP_409_CONFLICT,
			detail="Bu email zaten kullaniliyor",
		)

	user = User(
		email=email,
		hashed_password=hash_password(password),
		display_name=display_name,
	)
	db.add(user)
	await db.commit()
	await db.refresh(user)
	return user


async def login_user(email: str, password: str, db: AsyncSession) -> tuple[str, str]:
	"""Authenticate user and issue a new access/refresh token pair."""
	result = await db.execute(select(User).where(User.email == email))
	user = result.scalar_one_or_none()
	if not user:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="E-posta veya sifre hatali",
		)

	now = datetime.now(timezone.utc)
	if user.locked_until and user.locked_until > now:
		raise HTTPException(status_code=423, detail="Hesap gecici olarak kilitlendi")

	if not user.hashed_password or not verify_password(password, user.hashed_password):
		user.failed_login_count += 1
		if user.failed_login_count >= MAX_FAILED_ATTEMPTS:
			user.locked_until = now + timedelta(minutes=LOCK_DURATION_MINUTES)
		await db.commit()
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="E-posta veya sifre hatali",
		)

	user.failed_login_count = 0
	user.locked_until = None

	plain_refresh, hashed_refresh = create_refresh_token()
	token = RefreshToken(
		user_id=user.id,
		token_hash=hashed_refresh,
		expires_at=now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
	)
	db.add(token)
	await db.commit()

	return create_access_token(str(user.id)), plain_refresh


async def refresh_tokens(old_token_plain: str, db: AsyncSession) -> tuple[str, str]:
	"""Rotate refresh token and return a new access/refresh pair."""
	token_hash_value = hash_token(old_token_plain)
	result = await db.execute(select(RefreshToken).where(RefreshToken.token_hash == token_hash_value))
	token = result.scalar_one_or_none()

	now = datetime.now(timezone.utc)
	if not token or token.revoked_at or token.expires_at < now:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Gecersiz refresh token",
		)

	token.revoked_at = now
	plain_new, hashed_new = create_refresh_token()
	new_token = RefreshToken(
		user_id=token.user_id,
		token_hash=hashed_new,
		expires_at=now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
	)
	db.add(new_token)
	await db.commit()

	return create_access_token(str(token.user_id)), plain_new


async def logout_user(token_plain: str, db: AsyncSession) -> None:
	"""Revoke refresh token if it exists."""
	token_hash_value = hash_token(token_plain)
	result = await db.execute(select(RefreshToken).where(RefreshToken.token_hash == token_hash_value))
	token = result.scalar_one_or_none()
	if token:
		token.revoked_at = datetime.now(timezone.utc)
		await db.commit()
