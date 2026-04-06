import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.fact_check import FactCheck
from app.models.user import User
from app.schemas.fact_check import FactCheckRequest, FactCheckResponse
from app.services.fact_check_service import check_claim
from app.utils.security import decode_access_token


router = APIRouter(prefix="/fact-check", tags=["fact-check"])
optional_bearer = HTTPBearer(auto_error=False)


async def get_optional_user(
	credentials: HTTPAuthorizationCredentials | None = Depends(optional_bearer),
	db: AsyncSession = Depends(get_db),
) -> User | None:
	if credentials is None:
		return None

	try:
		payload = decode_access_token(credentials.credentials)
		user_id = payload.get("sub")
	except Exception:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Geçersiz token",
		)

	result = await db.execute(select(User).where(User.id == user_id))
	user = result.scalar_one_or_none()
	if user is None:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Kullanıcı bulunamadı",
		)
	return user


@router.post(
	"",
	response_model=FactCheckResponse,
	status_code=status.HTTP_200_OK,
	summary="Create fact check",
	description="İddiayı Fact Check Crew ile doğrular ve sonucu kaydeder.",
)
async def post_fact_check(
	payload: FactCheckRequest,
	current_user: User | None = Depends(get_optional_user),
	db: AsyncSession = Depends(get_db),
) -> FactCheckResponse:
	user_id = current_user.id if current_user else None
	try:
		fact_check = await check_claim(payload.claim, user_id, db)
	except Exception as exc:
		error_text = str(exc).lower()
		if "rate_limit_exceeded" in error_text or "ratelimiterror" in error_text:
			raise HTTPException(
				status_code=status.HTTP_429_TOO_MANY_REQUESTS,
				detail="AI servisinde yoğunluk var. Lütfen birkaç saniye sonra tekrar deneyin.",
			) from exc
		raise HTTPException(
			status_code=status.HTTP_502_BAD_GATEWAY,
			detail=f"AI servis hatası: {exc}",
		) from exc
	return FactCheckResponse.model_validate(fact_check)


@router.get(
	"/history",
	response_model=list[FactCheckResponse],
	status_code=status.HTTP_200_OK,
	summary="List fact-check history",
	description="Giriş yapmış kullanıcının fact-check geçmişini listeler.",
)
async def get_fact_check_history(
	current_user: User = Depends(get_current_user),
	db: AsyncSession = Depends(get_db),
) -> list[FactCheckResponse]:
	result = await db.execute(
		select(FactCheck)
		.where(FactCheck.user_id == current_user.id)
		.order_by(FactCheck.created_at.desc())
	)
	items = list(result.scalars().all())
	return [FactCheckResponse.model_validate(item) for item in items]


@router.get(
	"/{fact_check_id}",
	response_model=FactCheckResponse,
	status_code=status.HTTP_200_OK,
	summary="Get fact check",
	description="Kullanıcıya ait tek bir fact-check kaydını döndürür.",
)
async def get_fact_check(
	fact_check_id: uuid.UUID,
	current_user: User = Depends(get_current_user),
	db: AsyncSession = Depends(get_db),
) -> FactCheckResponse:
	result = await db.execute(
		select(FactCheck).where(
			FactCheck.id == fact_check_id,
			FactCheck.user_id == current_user.id,
		)
	)
	fact_check = result.scalar_one_or_none()
	if fact_check is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fact check kaydı bulunamadı")
	return FactCheckResponse.model_validate(fact_check)
