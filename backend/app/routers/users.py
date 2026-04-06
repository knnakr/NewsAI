from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User, UserPreferences
from app.schemas.user import (
	UpdatePreferencesRequest,
	UpdateUserRequest,
	UserPreferencesResponse,
	UserResponse,
)


router = APIRouter(prefix="/users", tags=["users"])


@router.get(
	"/me",
	response_model=UserResponse,
	status_code=status.HTTP_200_OK,
	summary="Get current user",
	description="Giriş yapmış kullanıcının profil bilgilerini döndürür.",
)
async def get_me(current_user: User = Depends(get_current_user)) -> UserResponse:
	return UserResponse.model_validate(current_user)


@router.patch(
	"/me",
	response_model=UserResponse,
	status_code=status.HTTP_200_OK,
	summary="Update current user",
	description="Giriş yapmış kullanıcının display name alanını günceller.",
)
async def patch_me(
	payload: UpdateUserRequest,
	current_user: User = Depends(get_current_user),
	db: AsyncSession = Depends(get_db),
) -> UserResponse:
	if payload.display_name is not None:
		current_user.display_name = payload.display_name
		await db.commit()
		await db.refresh(current_user)
	return UserResponse.model_validate(current_user)


@router.delete(
	"/me",
	status_code=status.HTTP_200_OK,
	summary="Delete current user",
	description="Giriş yapmış kullanıcının hesabını siler.",
)
async def delete_me(
	current_user: User = Depends(get_current_user),
	db: AsyncSession = Depends(get_db),
) -> dict[str, str]:
	await db.delete(current_user)
	await db.commit()
	return {"detail": "Hesap silindi"}


@router.get(
	"/me/preferences",
	response_model=UserPreferencesResponse,
	status_code=status.HTTP_200_OK,
	summary="Get user preferences",
	description="Giriş yapmış kullanıcının tercihlerini döndürür.",
)
async def get_preferences(
	current_user: User = Depends(get_current_user),
	db: AsyncSession = Depends(get_db),
) -> UserPreferencesResponse:
	preferences = await db.get(UserPreferences, current_user.id)
	if not preferences:
		preferences = UserPreferences(user_id=current_user.id)
		db.add(preferences)
		await db.commit()
		await db.refresh(preferences)
	return UserPreferencesResponse.model_validate(preferences)


@router.patch(
	"/me/preferences",
	response_model=UserPreferencesResponse,
	status_code=status.HTTP_200_OK,
	summary="Update user preferences",
	description="Kullanıcının dil, ton ve haber tercihlerini günceller.",
)
async def patch_preferences(
	payload: UpdatePreferencesRequest,
	current_user: User = Depends(get_current_user),
	db: AsyncSession = Depends(get_db),
) -> UserPreferencesResponse:
	preferences = await db.get(UserPreferences, current_user.id)
	if not preferences:
		preferences = UserPreferences(user_id=current_user.id)
		db.add(preferences)

	if payload.language is not None:
		preferences.language = payload.language
	if payload.ai_tone is not None:
		preferences.ai_tone = payload.ai_tone
	if payload.news_categories is not None:
		preferences.news_categories = payload.news_categories
	if payload.email_digest is not None:
		preferences.email_digest = payload.email_digest

	await db.commit()
	await db.refresh(preferences)
	return UserPreferencesResponse.model_validate(preferences)
