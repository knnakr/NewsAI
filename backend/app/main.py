import logging
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.database import AsyncSessionLocal, get_db
from app.middleware.logging import logging_middleware
from app.middleware.rate_limiter import rate_limit_middleware
from app.routers import auth, conversations, fact_check, news, users
from app.utils.cache import run_cleanup

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("newsai")

scheduler = AsyncIOScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup_event()
    try:
        yield
    finally:
        await shutdown_event()


app = FastAPI(
    title="News AI API",
    description="AI-powered news platform with CrewAI agents (News Crew + Fact Check Crew)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {"name": "auth", "description": "Kayıt, giriş, token yönetimi"},
        {"name": "users", "description": "Kullanıcı profili ve tercihler"},
        {"name": "conversations", "description": "Chat konuşmaları ve News Crew"},
        {"name": "fact-check", "description": "Fact Check Crew"},
        {"name": "news", "description": "Haber feed, trending, kategori, kayıt"},
    ],
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(rate_limit_middleware)
app.middleware("http")(logging_middleware)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router)
app.include_router(conversations.router)
app.include_router(fact_check.router)
app.include_router(news.router)


async def startup_event() -> None:
    async def scheduled_cleanup() -> None:
        async with AsyncSessionLocal() as db:
            await run_cleanup(db)

    scheduler.add_job(scheduled_cleanup, trigger="interval", hours=6)
    scheduler.start()


async def shutdown_event() -> None:
    if scheduler.running:
        scheduler.shutdown()


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={"detail": jsonable_encoder(exc.errors())}
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Sunucu hatası"}
    )


@app.get(
    "/health",
    summary="Health check",
    description="Veritabanı bağlantısını doğrulayan sağlık kontrolü endpoint'i.",
    status_code=200,
)
async def health_check(db: AsyncSession = Depends(get_db)) -> dict[str, str]:
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception:
        return {"status": "degraded", "database": "disconnected"}
