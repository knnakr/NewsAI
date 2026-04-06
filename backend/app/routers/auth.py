from datetime import datetime, timedelta, timezone
import secrets

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from pydantic import BaseModel, ConfigDict, EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db
from app.models.user import PasswordResetToken, User
from app.schemas.user import LoginRequest, RegisterRequest, TokenResponse, UserResponse
from app.services.auth_service import login_user, logout_user, refresh_tokens, register_user
from app.utils.security import hash_password, hash_token


router = APIRouter()


class ForgotPasswordRequest(BaseModel):
	email: EmailStr

	model_config = ConfigDict(
		json_schema_extra={"example": {"email": "user@example.com"}}
	)


class ResetPasswordRequest(BaseModel):
	token: str
	password: str

	model_config = ConfigDict(
		json_schema_extra={
			"example": {
				"token": "reset-token-value",
				"password": "newsecurepass123",
			}
		}
	)


@router.post(
	"/register",
	response_model=UserResponse,
	status_code=status.HTTP_201_CREATED,
	summary="Register user",
	description="Yeni kullanıcı oluşturur ve profil kaydını döndürür.",
)
async def post_register(payload: RegisterRequest, db: AsyncSession = Depends(get_db)) -> UserResponse:
	user = await register_user(payload.email, payload.password, payload.display_name, db)
	return UserResponse.model_validate(user)


@router.post(
	"/login",
	response_model=TokenResponse,
	status_code=status.HTTP_200_OK,
	summary="Login user",
	description="Kimlik doğrular, access token ve refresh cookie döndürür.",
)
async def post_login(
	payload: LoginRequest,
	response: Response,
	db: AsyncSession = Depends(get_db),
) -> TokenResponse:
	access_token, refresh_token_plain = await login_user(payload.email, payload.password, db)
	response.set_cookie(
		key="refresh_token",
		value=refresh_token_plain,
		httponly=True,
		samesite="lax",
	)
	return TokenResponse(
		access_token=access_token,
		token_type="bearer",
		expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
	)


@router.post(
	"/refresh",
	response_model=TokenResponse,
	status_code=status.HTTP_200_OK,
	summary="Refresh access token",
	description="Refresh cookie'deki token ile yeni access token üretir.",
)
async def post_refresh(
	response: Response,
	refresh_token: str | None = Cookie(default=None),
	db: AsyncSession = Depends(get_db),
) -> TokenResponse:
	if not refresh_token:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token bulunamadi")

	new_access_token, new_refresh_token = await refresh_tokens(refresh_token, db)
	response.set_cookie(
		key="refresh_token",
		value=new_refresh_token,
		httponly=True,
		samesite="lax",
	)
	return TokenResponse(
		access_token=new_access_token,
		token_type="bearer",
		expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
	)


@router.post(
	"/logout",
	status_code=status.HTTP_200_OK,
	summary="Logout user",
	description="Refresh cookie'yi revoke eder ve istemciden siler.",
)
async def post_logout(
	response: Response,
	refresh_token: str | None = Cookie(default=None),
	db: AsyncSession = Depends(get_db),
) -> dict[str, str]:
	if refresh_token:
		await logout_user(refresh_token, db)
	response.delete_cookie("refresh_token")
	return {"detail": "Cikis yapildi"}


@router.post(
	"/forgot-password",
	status_code=status.HTTP_200_OK,
	summary="Request password reset",
	description="Var olan kullanıcı için şifre sıfırlama akışını başlatır.",
)
async def post_forgot_password(
	payload: ForgotPasswordRequest,
	db: AsyncSession = Depends(get_db),
) -> dict[str, str]:
	result = await db.execute(select(User).where(User.email == payload.email))
	user = result.scalar_one_or_none()

	if user:
		plain_token = secrets.token_urlsafe(32)
		token = PasswordResetToken(
			user_id=user.id,
			token_hash=hash_token(plain_token),
			expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
		)
		db.add(token)
		await db.commit()

	return {"detail": "E-posta varsa sifre sifirlama adimlari gonderilecektir"}


@router.post(
	"/reset-password",
	status_code=status.HTTP_200_OK,
	summary="Reset password",
	description="Doğrulanan reset token ile kullanıcı şifresini günceller.",
)
async def post_reset_password(
	payload: ResetPasswordRequest,
	db: AsyncSession = Depends(get_db),
) -> dict[str, str]:
	now = datetime.now(timezone.utc)
	token_hash_value = hash_token(payload.token)
	result = await db.execute(
		select(PasswordResetToken).where(
			PasswordResetToken.token_hash == token_hash_value,
			PasswordResetToken.used_at.is_(None),
			PasswordResetToken.expires_at > now,
		)
	)
	token = result.scalar_one_or_none()

	if not token:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Gecersiz veya suresi dolmus token")

	user_result = await db.execute(select(User).where(User.id == token.user_id))
	user = user_result.scalar_one_or_none()
	if not user:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Kullanici bulunamadi")

	user.hashed_password = hash_password(payload.password)
	token.used_at = now
	await db.commit()

	return {"detail": "Sifre basariyla guncellendi"}
