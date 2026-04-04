# News AI — Project Roadmap (Backend)

**Proje:** News AI — AI Ajanlı Haber Platformu  
**Phase 1:** Infrastructure & Database (1 hafta)  
**Phase 2:** Authentication & User Management (1.5 hafta)  
**Phase 3:** CrewAI Core (2 hafta)  
**Phase 4:** News Feed & Cache System (1 hafta)  
**Phase 5:** Fact Check Engine (1 hafta)  
**Phase 6:** User Features — Saved Articles & Preferences (1 hafta)  
**Phase 7:** Trending & Category Pages (1 hafta)  
**Phase 8:** Testing, Security & Polish (1 hafta)  

---

## 📋 İçindekiler

### Phase 1: Infrastructure & Database
- [Phase 1 Overview](#-phase-1-overview)
- [Week 1: Project Setup, Docker & Database](#-week-1-project-setup-docker--database)
- [Phase 1 Success Metrics](#-phase-1-success-metrics)

### Phase 2: Authentication & User Management
- [Phase 2 Overview](#-phase-2-overview)
- [Week 2: Auth System (JWT + Refresh Token)](#-week-2-auth-system-jwt--refresh-token)
- [Week 3 (ilk yarı): User Endpoints & Email Verification](#-week-3-ilk-yarı-user-endpoints--email-verification)
- [Phase 2 Success Metrics](#-phase-2-success-metrics)

### Phase 3: CrewAI Core
- [Phase 3 Overview](#-phase-3-overview)
- [Week 3 (ikinci yarı): CrewAI Altyapısı & Tool Sistemi](#-week-3-ikinci-yarı-crewai-altyapısı--tool-sistemi)
- [Week 4: Chat Endpoint'leri & Konuşma Yönetimi](#-week-4-chat-endpointleri--konuşma-yönetimi)
- [Phase 3 Success Metrics](#-phase-3-success-metrics)

### Phase 4: News Feed & Cache System
- [Phase 4 Overview](#-phase-4-overview)
- [Week 5: NewsAPI Entegrasyonu & Cache Sistemi](#-week-5-newsapi-entegrasyonu--cache-sistemi)
- [Phase 4 Success Metrics](#-phase-4-success-metrics)

### Phase 5: Fact Check Engine
- [Phase 5 Overview](#-phase-5-overview)
- [Week 6: Fact Check Crew & Endpoint'leri](#-week-6-fact-check-crew--endpointleri)
- [Phase 5 Success Metrics](#-phase-5-success-metrics)

### Phase 6: User Features
- [Phase 6 Overview](#-phase-6-overview)
- [Week 7: Saved Articles & User Preferences](#-week-7-saved-articles--user-preferences)
- [Phase 6 Success Metrics](#-phase-6-success-metrics)

### Phase 7: Trending & Category Pages
- [Phase 7 Overview](#-phase-7-overview)
- [Week 8: Trending Sistemi & Kategori Endpoint'leri](#-week-8-trending-sistemi--kategori-endpointleri)
- [Phase 7 Success Metrics](#-phase-7-success-metrics)

### Phase 8: Testing, Security & Polish
- [Phase 8 Overview](#-phase-8-overview)
- [Week 9: Testing, Security Hardening & Dokümantasyon](#-week-9-testing-security-hardening--dokümantasyon)
- [Phase 8 Success Metrics](#-phase-8-success-metrics)

---

## 🎯 Phase 1 Overview

### Scope

**Dahil:**
- Python/FastAPI proje iskeleti
- Docker & Docker Compose altyapısı (FastAPI + PostgreSQL)
- Pydantic Settings ile environment yönetimi
- PostgreSQL veritabanı (11 tablo, tüm ENUM'lar, index'ler, trigger'lar)
- SQLAlchemy async ORM modelleri
- Alembic migration sistemi
- Health check endpoint'i
- Logging altyapısı

**Hariç:**
- Authentication (Phase 2)
- CrewAI mantığı (Phase 3+)
- Business logic endpoint'leri (Phase 4+)
- Frontend entegrasyonu

### Definition of Done

Phase 1 tamamlanmış sayılır eğer:
- [ ] Docker container'lar çalışıyor (FastAPI + PostgreSQL)
- [ ] Tüm 11 tablo oluşturuldu, tüm ENUM type'lar tanımlı
- [ ] Trigger'lar aktif (user_preferences otomatik oluşuyor, updated_at'ler çalışıyor)
- [ ] SQLAlchemy async modelleri hazır ve ilişkiler tanımlı
- [ ] Alembic migration'ları çalışıyor
- [ ] `GET /health` endpoint aktif ve DB bağlantısını doğruluyor
- [ ] Logging altyapısı kurulu
- [ ] `schema.sql` container başlangıcında otomatik yükleniyor
- [ ] Phase 1 testleri geçiyor (`pytest tests/test_health.py tests/test_models.py`)

---

## 📅 Week 1: Project Setup, Docker & Database

**Hedef:** Proje iskeleti, Docker altyapısı, schema yükleme, ORM modelleri

---

### Task 1.1: Project Directory Structure

**Tahmini Süre:** 1 saat

**Durum:** ✅ TAMAMLANDI

**Yapılacaklar:**
- [x] Proje klasör yapısını oluştur:
  ```
  news-ai/
  ├── backend/           # FastAPI (bu klasörün içi aşağıda)
  ├── frontend/          # Next.js (ROADMAP_FRONTEND.md)
  ├── docs/
  │   ├── ROADMAP_BACKEND.md
  │   ├── ROADMAP_FRONTEND.md
  │   └── DATABASE.md
  ├── schema.sql
  ├── docker-compose.yml
  ├── .env.example
  └── README.md

  backend/ içi:
  ├── app/
  │   ├── __init__.py
  │   ├── main.py
  │   ├── config.py
  │   ├── database.py
  │   ├── dependencies.py
  │   ├── models/
  │   │   ├── __init__.py
  │   │   ├── user.py
  │   │   ├── conversation.py
  │   │   ├── fact_check.py
  │   │   └── news.py
  │   ├── schemas/
  │   │   ├── __init__.py
  │   │   ├── user.py
  │   │   ├── conversation.py
  │   │   ├── fact_check.py
  │   │   └── news.py
  │   ├── routers/
  │   │   ├── __init__.py
  │   │   ├── auth.py
  │   │   ├── users.py
  │   │   ├── conversations.py
  │   │   ├── fact_check.py
  │   │   ├── news.py
  │   │   └── trending.py
  │   ├── services/
  │   │   ├── __init__.py
  │   │   ├── auth_service.py
  │   │   ├── crew_service.py
  │   │   ├── news_service.py
  │   │   ├── fact_check_service.py
  │   │   └── cache_service.py
  │   ├── crew/
  │   │   ├── __init__.py
  │   │   ├── news_crew.py
  │   │   ├── fact_check_crew.py
  │   │   ├── agents/
  │   │   │   ├── __init__.py
  │   │   │   ├── news_fetcher.py
  │   │   │   ├── news_analyst.py
  │   │   │   ├── fact_checker.py
  │   │   │   └── verdict_agent.py
  │   │   ├── tasks/
  │   │   │   ├── __init__.py
  │   │   │   ├── news_tasks.py
  │   │   │   └── fact_check_tasks.py
  │   │   ├── tools/
  │   │   │   ├── __init__.py
  │   │   │   ├── web_search.py
  │   │   │   ├── fetch_news.py
  │   │   │   ├── fetch_trending.py
  │   │   │   ├── fact_check_search.py
  │   │   │   └── summarize.py
  │   │   └── prompts/
  │   │       ├── __init__.py
  │   │       ├── news_prompts.py
  │   │       └── fact_check_prompts.py
  │   ├── middleware/
  │   │   ├── __init__.py
  │   │   ├── logging.py
  │   │   └── rate_limiter.py
  │   └── utils/
  │       ├── __init__.py
  │       ├── security.py
  │       └── cache.py
  ├── alembic/
  │   ├── versions/
  │   └── env.py
  ├── tests/
  │   ├── __init__.py
  │   ├── conftest.py
  │   ├── test_health.py
  │   ├── test_models.py
  │   ├── test_auth.py
  │   ├── test_crew.py
  │   ├── test_news.py
  │   ├── test_fact_check.py
  │   └── test_e2e.py
  ├── schema.sql
  ├── Dockerfile
  ├── .env.example
  ├── .gitignore
  ├── alembic.ini
  ├── pytest.ini
  └── requirements.txt
  ```
- [x] Root `.gitignore` oluştur (`.env`, `__pycache__`, `.pytest_cache`, `*.pyc` dahil)

---

### Task 1.2: Environment Configuration

**Tahmini Süre:** 1 saat

**Durum:** ✅ TAMAMLANDI

**Yapılacaklar:**
- [x] `.env.example` dosyasını projeye koy:
  ```
  DATABASE_URL=postgresql+asyncpg://newsai:newsai@db:5432/newsai
  GROQ_API_KEY=your_groq_api_key
  TAVILY_API_KEY=your_tavily_api_key
  NEWS_API_KEY=your_newsapi_key
  JWT_SECRET=your_jwt_secret_min_32_chars
  JWT_ALGORITHM=HS256
  ACCESS_TOKEN_EXPIRE_MINUTES=15
  REFRESH_TOKEN_EXPIRE_DAYS=30
  ENVIRONMENT=development
  ALLOWED_ORIGINS=["http://localhost:3000"]
    GROQ_MODEL_DEFAULT=groq/compound-mini
    GROQ_MODEL_REASONING=groq/compound
  ARTICLE_CACHE_TTL_HOURS=6
  ```
- [x] `app/config.py` oluştur:
  ```python
  from pydantic_settings import BaseSettings
  from typing import Literal

  class Settings(BaseSettings):
      DATABASE_URL: str

      GROQ_API_KEY: str
      TAVILY_API_KEY: str
      NEWS_API_KEY: str

      JWT_SECRET: str
      JWT_ALGORITHM: str = "HS256"
      ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
      REFRESH_TOKEN_EXPIRE_DAYS: int = 30

      ENVIRONMENT: Literal["development", "production"] = "development"
      ALLOWED_ORIGINS: list[str] = ["http://localhost:3000"]

    GROQ_MODEL_DEFAULT: str = "groq/compound-mini"
    GROQ_MODEL_REASONING: str = "groq/compound"

      ARTICLE_CACHE_TTL_HOURS: int = 6

      class Config:
          env_file = ".env"

  settings = Settings()
  ```

---

### Task 1.3: Docker Setup

**Tahmini Süre:** 2 saat

**Durum:** ✅ TAMAMLANDI

**Yapılacaklar:**
- [x] `backend/Dockerfile` oluştur:
  ```dockerfile
  FROM python:3.12-slim

  WORKDIR /app

  COPY requirements.txt .
  RUN pip install --no-cache-dir -r requirements.txt

  COPY . .

  EXPOSE 8001

  CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
  ```
- [x] `docker-compose.yml` root'ta oluştur:
  ```yaml
  services:
    api:
      build: ./backend
      ports:
        - "8001:8001"
      environment:
        DATABASE_URL: postgresql+asyncpg://newsai:newsai@db:5432/newsai
      env_file:
        - ./backend/.env
      depends_on:
        db:
          condition: service_healthy
      volumes:
        - ./backend:/app

    db:
      image: postgres:16-alpine
      environment:
        POSTGRES_USER: newsai
        POSTGRES_PASSWORD: newsai
        POSTGRES_DB: newsai
      ports:
        - "5433:5432"
      volumes:
        - ./backend/schema.sql:/docker-entrypoint-initdb.d/schema.sql
        - pgdata:/var/lib/postgresql/data
      healthcheck:
        test: ["CMD-SHELL", "pg_isready -U newsai"]
        interval: 5s
        timeout: 5s
        retries: 5

  volumes:
    pgdata:
  ```
- [x] `backend/.dockerignore` oluştur:
  ```
  __pycache__
  .pytest_cache
  .env
  *.pyc
  alembic/versions/
  ```
- [x] `docker compose up -d` çalıştır, `api` ve `db` container'ların `healthy` olduğunu doğrula

---

### Task 1.4: FastAPI Application Foundation

**Tahmini Süre:** 2 saat

**Durum:** ✅ TAMAMLANDI

**Yapılacaklar:**
- [x] `requirements.txt` oluştur:
  ```
  fastapi>=0.115.0
  uvicorn[standard]>=0.32.0
  sqlalchemy[asyncio]>=2.0.36
  asyncpg>=0.30.0
  alembic>=1.14.0
  pydantic>=2.10.0
  pydantic-settings>=2.6.0
  python-jose[cryptography]>=3.3.0
  passlib[bcrypt]>=1.7.4
  python-multipart>=0.0.12
  httpx>=0.28.0
  groq>=0.13.0
  tavily-python>=0.5.0
  crewai>=0.80.0
  crewai-tools>=0.17.0
  apscheduler>=3.10.0
  pytest>=8.0.0
  pytest-asyncio>=0.23.0
  pytest-cov>=5.0.0
  httpx>=0.28.0
  ```
- [x] `app/main.py` oluştur:
  ```python
  from fastapi import FastAPI
  from fastapi.middleware.cors import CORSMiddleware
  from app.config import settings

  app = FastAPI(
      title="News AI API",
      description="AI-powered news platform with CrewAI agents",
      version="1.0.0",
  )

  app.add_middleware(
      CORSMiddleware,
      allow_origins=settings.ALLOWED_ORIGINS,
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
  )

  @app.get("/health")
  async def health_check():
      # DB bağlantısını doğrula
      ...
  ```
- [x] `app/database.py` oluştur:
  ```python
  from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
  from app.config import settings

  engine = create_async_engine(settings.DATABASE_URL, echo=False)
  AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

  async def get_db():
      async with AsyncSessionLocal() as session:
          yield session
  ```
- [x] `app/dependencies.py` oluştur (`get_current_user` dependency için placeholder)

---

### Task 1.5: SQLAlchemy ORM Modelleri

**Tahmini Süre:** 3 saat

**Durum:** ✅ TAMAMLANDI

**Yapılacaklar:**
- [x] `app/models/user.py` oluştur (`User`, `RefreshToken`, `PasswordResetToken`, `EmailVerificationToken`, `UserPreferences` modelleri):
  ```python
  import uuid
  from datetime import datetime
  from sqlalchemy import String, Boolean, Integer, DateTime, ForeignKey, Enum as SAEnum, Text
  from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
  from sqlalchemy.dialects.postgresql import UUID, JSONB

  class Base(DeclarativeBase):
      pass

  class User(Base):
      __tablename__ = "users"
      id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
      email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
      hashed_password: Mapped[str | None] = mapped_column(String(255))
      display_name: Mapped[str] = mapped_column(String(100), nullable=False)
      role: Mapped[str] = mapped_column(SAEnum("user", "admin", name="user_role"), default="user")
      auth_provider: Mapped[str] = mapped_column(SAEnum("email", "google", "github", name="auth_provider"), default="email")
      email_verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
      failed_login_count: Mapped[int] = mapped_column(Integer, default=0)
      locked_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
      created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
      updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

      preferences: Mapped["UserPreferences"] = relationship(back_populates="user", uselist=False)
      conversations: Mapped[list["Conversation"]] = relationship(back_populates="user")
      refresh_tokens: Mapped[list["RefreshToken"]] = relationship(back_populates="user")

  class UserPreferences(Base):
      __tablename__ = "user_preferences"
      user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
      language: Mapped[str] = mapped_column(String(10), default="Turkish")
      ai_tone: Mapped[str] = mapped_column(SAEnum("neutral", "formal", "casual", name="ai_tone"), default="neutral")
      news_categories: Mapped[list] = mapped_column(JSONB, default=list)
      email_digest: Mapped[bool] = mapped_column(Boolean, default=False)
      updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

      user: Mapped["User"] = relationship(back_populates="preferences")

  class RefreshToken(Base):
      __tablename__ = "refresh_tokens"
      id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
      user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
      token_hash: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
      expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
      revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
      created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

      user: Mapped["User"] = relationship(back_populates="refresh_tokens")
  ```
- [x] `app/models/conversation.py` oluştur (`Conversation`, `Message`, `AgentToolCall` modelleri):
  ```python
  class Conversation(Base):
      __tablename__ = "conversations"
      id: Mapped[uuid.UUID] = ...
      user_id: Mapped[uuid.UUID] = ...
      title: Mapped[str | None] = ...
      is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
      created_at: Mapped[datetime] = ...
      updated_at: Mapped[datetime] = ...

      user: Mapped["User"] = relationship(back_populates="conversations")
      messages: Mapped[list["Message"]] = relationship(back_populates="conversation", cascade="all, delete")

  class Message(Base):
      __tablename__ = "messages"
      id: Mapped[uuid.UUID] = ...
      conversation_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("conversations.id", ondelete="CASCADE"))
      role: Mapped[str] = mapped_column(SAEnum("user", "assistant", "system", name="message_role"))
      content: Mapped[str] = mapped_column(Text, nullable=False)
      sources: Mapped[list | None] = mapped_column(JSONB)
      created_at: Mapped[datetime] = ...

      conversation: Mapped["Conversation"] = relationship(back_populates="messages")
      tool_calls: Mapped[list["AgentToolCall"]] = relationship(back_populates="message", cascade="all, delete")

  class AgentToolCall(Base):
      __tablename__ = "agent_tool_calls"
      id: Mapped[uuid.UUID] = ...
      message_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("messages.id", ondelete="CASCADE"))
      tool_name: Mapped[str] = mapped_column(SAEnum("web_search", "fetch_news_by_category", "fetch_trending", "fact_check_search", "summarize_article", name="agent_tool"))
      input_params: Mapped[dict] = mapped_column(JSONB, default=dict)
      output_result: Mapped[str | None] = mapped_column(Text)
      duration_ms: Mapped[int | None] = mapped_column(Integer)
      is_success: Mapped[bool] = mapped_column(Boolean, default=True)
      error_message: Mapped[str | None] = mapped_column(Text)
      created_at: Mapped[datetime] = ...

      message: Mapped["Message"] = relationship(back_populates="tool_calls")
  ```
- [x] `app/models/fact_check.py` oluştur (`FactCheck` modeli)
- [x] `app/models/news.py` oluştur (`SavedArticle`, `ArticleCache` modelleri)
- [x] `app/models/__init__.py` içinde `Base` ve tüm modelleri export et

---

### Task 1.6: Alembic Migration Setup

**Tahmini Süre:** 1 saat

**Durum:** ✅ TAMAMLANDI

**Yapılacaklar:**
- [x] `alembic init alembic` komutuyla alembic başlat
- [x] `alembic/env.py` güncelle:
  ```python
  from app.config import settings
  from app.models import Base

  # Async engine için
  from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

  config.set_main_option(
      "sqlalchemy.url",
      settings.DATABASE_URL.replace("+asyncpg", "")
  )
  target_metadata = Base.metadata
  ```
- [x] `alembic.ini` içindeki `sqlalchemy.url` satırını kaldır (env.py'den alınacak)
- [x] İlk migration oluştur:
  ```
  alembic revision --autogenerate -m "initial_schema"
  ```
- [x] Migration uygula:
  ```
  alembic upgrade head
  ```
- [x] `alembic current` → head revision gösteriyor mu doğrula

> **Not:** `schema.sql` Docker başlangıcında tabloları oluşturur; Alembic yeni migration'lar için kullanılır. İlk `alembic revision` boş kalabilir (`schema.sql` ile tablo zaten hazır), sadece revision takibi yapılır.

---

### Task 1.7: Logging Altyapısı

**Tahmini Süre:** 1 saat

**Durum:** ✅ TAMAMLANDI

**Yapılacaklar:**
- [x] `app/middleware/logging.py` oluştur:
  ```python
  import time
  import logging
  from fastapi import Request

  logger = logging.getLogger("newsai")

  async def logging_middleware(request: Request, call_next):
      start = time.time()
      response = await call_next(request)
      duration = (time.time() - start) * 1000
      logger.info(
          f"{request.method} {request.url.path} → {response.status_code} ({duration:.0f}ms)"
      )
      return response
  ```
- [x] `app/main.py`'ye logging config ve middleware ekle:
  ```python
  import logging
  from app.middleware.logging import logging_middleware

  logging.basicConfig(
      level=logging.INFO,
      format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
  )

  app.middleware("http")(logging_middleware)
  ```
- [x] `docker compose logs -f api` ile her request'in loglandığını doğrula

> **Ekstra:** Test First yaklaşımıyla `tests/test_logging.py` oluşturuldu. Middleware'in HTTP method, path, status code, duration logladığı testlendi.

---

### Task 1.8: Phase 1 Testleri

**Tahmini Süre:** 2 saat

**Durum:** ✅ YAPILDI

> **TDD Notu:** Bu task'taki testler Phase 1 implementasyonunu doğrular. Her testin önce yazılıp sonra implementasyonun buna göre tamamlanması beklenir.

**Yapılacaklar:**
- [x] `tests/conftest.py` oluştur (pytest fixtures: event_loop, db, client)
- [x] `pytest.ini` oluştur (asyncio_mode=auto, testpaths=tests)
- [x] `tests/test_health.py` oluştur (4 test: status code, schema, connection status)
- [x] `tests/test_models.py` oluştur (6 test: tables, triggers, enums, constraints)
- [x] `pytest tests/test_health.py tests/test_models.py -v` çalıştır → **10/10 testler geçti** ✅

> **Ekstra:** 
> - Database triggers (user_preferences, conversation.updated_at) implementasyonu tamamlandı
> - conftest.py'de triggers otomatik oluşturuluyor
> - Health endpoint dependency injection kullanıyor (test override uyumlu)


---

### 📊 Phase 1 Success Metrics

- [x] `docker compose up -d` sonrası her iki servis `healthy`
- [x] `GET http://localhost:8001/health` → `{"status": "ok", "database": "connected"}`
- [x] `docker compose exec db psql -U newsai -d newsai -c "\dt"` → 11 tablo görünüyor
- [x] `alembic current` → head revision gösteriyor (`2_add_triggers`)
- [x] Yeni kullanıcı INSERT edildiğinde `user_preferences` satırı otomatik oluşuyor
- [x] Logging middleware her request'i kaydediyor
- [x] `pytest tests/test_health.py tests/test_models.py` → tüm testler geçiyor (10/10 ✅)

---

## 🎯 Phase 2 Overview

### Scope

**Dahil:**
- JWT access token + refresh token sistemi
- Kayıt, giriş, çıkış endpoint'leri
- Token rotation
- E-posta doğrulama token sistemi
- Şifre sıfırlama akışı
- Brute force koruması
- `GET /users/me` profil endpoint'i
- Pydantic request/response şemaları

**Hariç:**
- OAuth (Google/GitHub) — sonraki versiyon
- E-posta gönderimi (SMTP) — opsiyonel
- Admin endpoint'leri (Phase 8)

### Definition of Done

- [ ] Kayıt → giriş → token yenileme → çıkış akışı uçtan uca çalışıyor
- [ ] Access token 15 dakika, refresh token 30 gün geçerli
- [ ] 5 hatalı girişte hesap 15 dakika kilitlenir
- [ ] Korumalı endpoint'lere geçersiz token ile 401 dönüyor
- [ ] `GET /users/me` doğru kullanıcı bilgisini döndürüyor
- [ ] `pytest tests/test_auth.py` → tüm testler geçiyor, coverage >= %85

---

## 📅 Week 2: Auth System (JWT + Refresh Token)

**Hedef:** Tam auth akışı, token yönetimi, brute force koruması

---

### Task 2.1: Security Utilities

**Tahmini Süre:** 1 saat

**Durum:** ✅ YAPILDI

**Yapılacaklar:**
- [x] Test önce — `tests/test_auth.py` dosyasını oluştur ve security util testlerini yaz (8 testler)
- [x] `app/utils/security.py` oluştur:
  - [x] `hash_password(plain: str) -> str` — PBKDF2-SHA256 hashing
  - [x] `verify_password(plain: str, hashed: str) -> bool` — password validation
  - [x] `create_access_token(user_id: str) -> str` — JWT token creation (15 min expiry)
  - [x] `create_refresh_token() -> tuple[str, str]` — refresh token pair
  - [x] `decode_access_token(token: str) -> dict` — JWT decoding
  - [x] `hash_token(plain: str) -> str` — SHA256 hashing for DB storage
- [x] `app/dependencies.py` güncelle:
  - [x] `get_current_user()` dependency implementation (bearer token extraction + user lookup)
- [x] `pytest tests/test_auth.py -v` çalıştır → **8/8 testler geçti** ✅

> **Ekstra Not:** 
> - PBKDF2-SHA256 kullanıldı (bağımsız, built-in passlib scheme)
> - HTTPBearer security scheme kullanılıyor (HTTPAuthorizationCredentials)
> - get_current_user 401 Unauthorized döndürüyor (invalid/expired token, not found user)

---

### Task 2.2: Auth Schemas

**Tahmini Süre:** 1 saat

**Durum:** ✅ YAPILDI

**Yapılacaklar:**
- [x] Test önce — `tests/test_auth.py`'e schema validation testleri ekle:
  ```python
  from pydantic import ValidationError
  from app.schemas.user import RegisterRequest, LoginRequest

  def test_register_request_rejects_short_password():
      with pytest.raises(ValidationError):
          RegisterRequest(email="a@b.com", password="short", display_name="Test")

  def test_register_request_rejects_invalid_email():
      with pytest.raises(ValidationError):
          RegisterRequest(email="not-an-email", password="validpass123", display_name="Test")

  def test_register_request_rejects_short_display_name():
      with pytest.raises(ValidationError):
          RegisterRequest(email="a@b.com", password="validpass123", display_name="T")

  def test_register_request_valid():
      req = RegisterRequest(email="a@b.com", password="validpass123", display_name="Test User")
      assert req.email == "a@b.com"

  def test_login_request_requires_email_and_password():
      with pytest.raises(ValidationError):
          LoginRequest(email="a@b.com")
  ```
- [x] `app/schemas/user.py` oluştur:
  ```python
  from pydantic import BaseModel, EmailStr, field_validator, ConfigDict
  from datetime import datetime
  import uuid

  class RegisterRequest(BaseModel):
      email: EmailStr
      password: str
      display_name: str

      @field_validator("password")
      @classmethod
      def password_min_length(cls, v: str) -> str:
          if len(v) < 8:
              raise ValueError("Şifre en az 8 karakter olmalı")
          return v

      @field_validator("display_name")
      @classmethod
      def display_name_min_length(cls, v: str) -> str:
          if len(v) < 2:
              raise ValueError("İsim en az 2 karakter olmalı")
          return v

  class LoginRequest(BaseModel):
      email: EmailStr
      password: str

  class TokenResponse(BaseModel):
      access_token: str
      token_type: str = "bearer"
      expires_in: int

  class UserResponse(BaseModel):
      id: uuid.UUID
      email: str
      display_name: str
      role: str
      email_verified_at: datetime | None
      created_at: datetime
      model_config = ConfigDict(from_attributes=True)

  class UpdateUserRequest(BaseModel):
      display_name: str | None = None

  class UserPreferencesResponse(BaseModel):
      language: str
      ai_tone: str
      news_categories: list
      email_digest: bool
      model_config = ConfigDict(from_attributes=True)

  class UpdatePreferencesRequest(BaseModel):
      language: str | None = None
      ai_tone: str | None = None
      news_categories: list | None = None
      email_digest: bool | None = None
  ```

---

### Task 2.3: Auth Service

**Tahmini Süre:** 2 saat

**Durum:** ✅ YAPILDI

**Yapılacaklar:**
- [x] Test önce — `tests/test_auth.py`'e servis testleri ekle:
  ```python
  from app.services.auth_service import register_user, login_user, refresh_tokens, logout_user

  async def test_register_creates_user_in_db(db):
      user = await register_user("test@example.com", "password123", "Test User", db)
      assert user.id is not None
      assert user.email == "test@example.com"
      assert user.hashed_password != "password123"

  async def test_register_creates_user_preferences(db):
      await register_user("pref@example.com", "password123", "Pref User", db)
      result = await db.execute(
          text("SELECT COUNT(*) FROM user_preferences WHERE user_id = "
               "(SELECT id FROM users WHERE email = 'pref@example.com')")
      )
      assert result.scalar() == 1

  async def test_register_duplicate_email_raises_409(db):
      await register_user("dup@example.com", "password123", "User", db)
      with pytest.raises(HTTPException) as exc:
          await register_user("dup@example.com", "password123", "User2", db)
      assert exc.value.status_code == 409

  async def test_login_valid_credentials_returns_tokens(db):
      await register_user("login@example.com", "password123", "Login User", db)
      access_token, refresh_token = await login_user("login@example.com", "password123", db)
      assert isinstance(access_token, str)
      assert isinstance(refresh_token, str)

  async def test_login_wrong_password_returns_401(db):
      await register_user("fail@example.com", "password123", "Fail User", db)
      with pytest.raises(HTTPException) as exc:
          await login_user("fail@example.com", "wrongpassword", db)
      assert exc.value.status_code == 401

  async def test_brute_force_locks_account_after_5_attempts(db):
      await register_user("brute@example.com", "password123", "Brute User", db)
      for _ in range(5):
          try:
              await login_user("brute@example.com", "wrong", db)
          except HTTPException:
              pass
      with pytest.raises(HTTPException) as exc:
          await login_user("brute@example.com", "password123", db)
      assert exc.value.status_code == 423

  async def test_refresh_tokens_rotates_refresh_token(db):
      await register_user("refresh@example.com", "password123", "Refresh User", db)
      _, old_refresh = await login_user("refresh@example.com", "password123", db)
      new_access, new_refresh = await refresh_tokens(old_refresh, db)
      assert new_refresh != old_refresh
      assert isinstance(new_access, str)

  async def test_refresh_with_revoked_token_raises_401(db):
      await register_user("revoke@example.com", "password123", "Revoke User", db)
      _, refresh = await login_user("revoke@example.com", "password123", db)
      await logout_user(refresh, db)
      with pytest.raises(HTTPException) as exc:
          await refresh_tokens(refresh, db)
      assert exc.value.status_code == 401
  ```
- [x] `app/services/auth_service.py` oluştur:
  ```python
  from sqlalchemy.ext.asyncio import AsyncSession
  from sqlalchemy import select
  from fastapi import HTTPException, status
  from datetime import datetime, timezone, timedelta
  import uuid
  from app.models.user import User, RefreshToken
  from app.utils.security import hash_password, verify_password, create_access_token, create_refresh_token, hash_token
  from app.config import settings

  LOCK_DURATION_MINUTES = 15
  MAX_FAILED_ATTEMPTS = 5

  async def register_user(email: str, password: str, display_name: str, db: AsyncSession) -> User:
      existing = await db.execute(select(User).where(User.email == email))
      if existing.scalar_one_or_none():
          raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Bu email zaten kullanılıyor")
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
      result = await db.execute(select(User).where(User.email == email))
      user = result.scalar_one_or_none()
      if not user:
          raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="E-posta veya şifre hatalı")
      if user.locked_until and user.locked_until > datetime.now(timezone.utc):
          raise HTTPException(status_code=423, detail="Hesap geçici olarak kilitlendi")
      if not verify_password(password, user.hashed_password):
          user.failed_login_count += 1
          if user.failed_login_count >= MAX_FAILED_ATTEMPTS:
              user.locked_until = datetime.now(timezone.utc) + timedelta(minutes=LOCK_DURATION_MINUTES)
          await db.commit()
          raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="E-posta veya şifre hatalı")
      user.failed_login_count = 0
      user.locked_until = None
      plain_refresh, hashed_refresh = create_refresh_token()
      token = RefreshToken(
          user_id=user.id,
          token_hash=hashed_refresh,
          expires_at=datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
      )
      db.add(token)
      await db.commit()
      return create_access_token(str(user.id)), plain_refresh

  async def refresh_tokens(old_token_plain: str, db: AsyncSession) -> tuple[str, str]:
      token_hash = hash_token(old_token_plain)
      result = await db.execute(select(RefreshToken).where(RefreshToken.token_hash == token_hash))
      token = result.scalar_one_or_none()
      if not token or token.revoked_at or token.expires_at < datetime.now(timezone.utc):
          raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Geçersiz refresh token")
      token.revoked_at = datetime.now(timezone.utc)
      plain_new, hashed_new = create_refresh_token()
      new_token = RefreshToken(
          user_id=token.user_id,
          token_hash=hashed_new,
          expires_at=datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
      )
      db.add(new_token)
      await db.commit()
      return create_access_token(str(token.user_id)), plain_new

  async def logout_user(token_plain: str, db: AsyncSession) -> None:
      token_hash = hash_token(token_plain)
      result = await db.execute(select(RefreshToken).where(RefreshToken.token_hash == token_hash))
      token = result.scalar_one_or_none()
      if token:
          token.revoked_at = datetime.now(timezone.utc)
          await db.commit()
  ```
- [x] `.venv` ile doğrulama: `python -m pytest tests/test_auth.py -v` → **21/21 testler geçti** ✅

---

### Task 2.4: Auth Router

**Tahmini Süre:** 2 saat

**Durum:** ✅ YAPILDI

**Yapılacaklar:**
- [x] Test önce — `tests/test_auth.py`'e HTTP endpoint testleri ekle:
  ```python
  async def test_post_register_returns_201(client):
      response = await client.post("/auth/register", json={
          "email": "new@example.com", "password": "password123", "display_name": "New User"
      })
      assert response.status_code == 201
      assert "id" in response.json()
      assert "hashed_password" not in response.json()

  async def test_post_register_invalid_body_returns_422(client):
      response = await client.post("/auth/register", json={"email": "bad"})
      assert response.status_code == 422

  async def test_post_login_returns_access_token(client):
      await client.post("/auth/register", json={
          "email": "login2@example.com", "password": "password123", "display_name": "Login"
      })
      response = await client.post("/auth/login", json={
          "email": "login2@example.com", "password": "password123"
      })
      assert response.status_code == 200
      assert "access_token" in response.json()

  async def test_post_login_sets_refresh_cookie(client):
      await client.post("/auth/register", json={
          "email": "cookie@example.com", "password": "password123", "display_name": "Cookie"
      })
      response = await client.post("/auth/login", json={
          "email": "cookie@example.com", "password": "password123"
      })
      assert "refresh_token" in response.cookies

  async def test_post_refresh_rotates_token(client):
      await client.post("/auth/register", json={
          "email": "rot@example.com", "password": "password123", "display_name": "Rot"
      })
      login_resp = await client.post("/auth/login", json={
          "email": "rot@example.com", "password": "password123"
      })
      old_cookie = login_resp.cookies.get("refresh_token")
      refresh_resp = await client.post("/auth/refresh", cookies={"refresh_token": old_cookie})
      assert refresh_resp.status_code == 200
      assert refresh_resp.cookies.get("refresh_token") != old_cookie

  async def test_post_logout_revokes_refresh_token(client):
      await client.post("/auth/register", json={
          "email": "logout@example.com", "password": "password123", "display_name": "Logout"
      })
      login_resp = await client.post("/auth/login", json={
          "email": "logout@example.com", "password": "password123"
      })
      await client.post("/auth/logout", cookies=login_resp.cookies)
      refresh_resp = await client.post("/auth/refresh", cookies=login_resp.cookies)
      assert refresh_resp.status_code == 401

  async def test_register_duplicate_email_returns_409(client):
      await client.post("/auth/register", json={
          "email": "dup2@example.com", "password": "password123", "display_name": "Dup"
      })
      response = await client.post("/auth/register", json={
          "email": "dup2@example.com", "password": "password123", "display_name": "Dup2"
      })
      assert response.status_code == 409
  ```
- [x] `app/routers/auth.py` oluştur:
    - [x] `POST /auth/register` → 201, `UserResponse`
    - [x] `POST /auth/login` → `TokenResponse` + refresh token cookie (`httponly=True, samesite="lax"`)
    - [x] `POST /auth/refresh` → cookie'den refresh token oku, yeni access token + yeni cookie döndür
    - [x] `POST /auth/logout` → cookie'den refresh token oku, revoke et, cookie'yi sil
    - [x] `POST /auth/forgot-password` → `password_reset_tokens` tablosuna yaz
    - [x] `POST /auth/reset-password` → token doğrula, şifre güncelle
- [x] `app/main.py`'ye router'ı ekle:
  ```python
  from app.routers import auth
  app.include_router(auth.router, prefix="/auth", tags=["auth"])
  ```
- [x] `.venv` ile doğrulama: `python -m pytest tests/test_auth.py -v` → **28/28 testler geçti** ✅

---

## 📅 Week 3 (ilk yarı): User Endpoints & Email Verification

---

### Task 3.1: User Router

**Tahmini Süre:** 2 saat

**Durum:** ✅ YAPILDI

**Yapılacaklar:**
- [x] Test önce — `tests/test_auth.py`'e kullanıcı endpoint testleri ekle:
  ```python
  @pytest.fixture
  async def auth_headers(client) -> dict:
      await client.post("/auth/register", json={
          "email": "me@example.com", "password": "password123", "display_name": "Me User"
      })
      login_resp = await client.post("/auth/login", json={
          "email": "me@example.com", "password": "password123"
      })
      token = login_resp.json()["access_token"]
      return {"Authorization": f"Bearer {token}"}

  async def test_get_me_returns_current_user(client, auth_headers):
      response = await client.get("/users/me", headers=auth_headers)
      assert response.status_code == 200
      assert response.json()["email"] == "me@example.com"

  async def test_get_me_without_token_returns_401(client):
      response = await client.get("/users/me")
      assert response.status_code == 401

  async def test_get_me_with_invalid_token_returns_401(client):
      response = await client.get("/users/me", headers={"Authorization": "Bearer invalid.token.here"})
      assert response.status_code == 401

  async def test_get_me_response_excludes_hashed_password(client, auth_headers):
      response = await client.get("/users/me", headers=auth_headers)
      assert "hashed_password" not in response.json()

  async def test_patch_me_updates_display_name(client, auth_headers):
      response = await client.patch("/users/me", json={"display_name": "Updated Name"}, headers=auth_headers)
      assert response.status_code == 200
      assert response.json()["display_name"] == "Updated Name"

  async def test_get_preferences_returns_defaults(client, auth_headers):
      response = await client.get("/users/me/preferences", headers=auth_headers)
      assert response.status_code == 200
      data = response.json()
      assert data["language"] == "Turkish"
      assert data["ai_tone"] == "neutral"

  async def test_patch_preferences_updates_language(client, auth_headers):
      response = await client.patch("/users/me/preferences", json={"language": "English"}, headers=auth_headers)
      assert response.status_code == 200
      assert response.json()["language"] == "English"

  async def test_patch_preferences_invalid_ai_tone_returns_422(client, auth_headers):
      response = await client.patch("/users/me/preferences", json={"ai_tone": "aggressive"}, headers=auth_headers)
      assert response.status_code == 422
  ```
- [x] `app/routers/users.py` oluştur:
    - [x] `GET /users/me` → mevcut kullanıcı profili (`get_current_user` dependency)
    - [x] `PATCH /users/me` → display_name güncelle
    - [x] `DELETE /users/me` → hesabı sil
    - [x] `GET /users/me/preferences` → kullanıcı tercihleri
    - [x] `PATCH /users/me/preferences` → `language`, `ai_tone`, `news_categories`, `email_digest` güncelle
- [x] `app/main.py`'ye router ekle
- [x] `.venv` ile doğrulama: `python -m pytest tests/test_auth.py -v` → **36/36 testler geçti** ✅

---

### Task 3.2: Global Exception Handler

**Tahmini Süre:** 1 saat

**Durum:** ✅ YAPILDI

**Yapılacaklar:**
- [x] Test önce — `tests/test_auth.py`'e exception handler testleri ekle:
  ```python
  async def test_not_found_route_returns_404(client):
      response = await client.get("/nonexistent-route-xyz")
      assert response.status_code == 404

  async def test_validation_error_returns_422_with_detail(client):
      response = await client.post("/auth/register", json={"email": "bad-email"})
      assert response.status_code == 422
      assert "detail" in response.json()

  async def test_http_exception_returns_json_with_detail(client):
      response = await client.get("/users/me")
      assert response.status_code in (401, 403)
      assert "detail" in response.json()
  ```
- [x] `app/main.py`'ye exception handler'lar ekle:
  ```python
  from fastapi import Request
  from fastapi.responses import JSONResponse
  from fastapi.exceptions import RequestValidationError

  @app.exception_handler(HTTPException)
  async def http_exception_handler(request: Request, exc: HTTPException):
      return JSONResponse(
          status_code=exc.status_code,
          content={"detail": exc.detail}
      )

  @app.exception_handler(RequestValidationError)
  async def validation_exception_handler(request: Request, exc: RequestValidationError):
      return JSONResponse(
          status_code=422,
          content={"detail": exc.errors()}
      )

  @app.exception_handler(Exception)
  async def generic_exception_handler(request: Request, exc: Exception):
      logger.error(f"Unhandled exception: {exc}")
      return JSONResponse(
          status_code=500,
          content={"detail": "Sunucu hatası"}
      )
  ```

- [x] `.venv` ile doğrulama:
  - `python -m pytest tests/test_auth.py -v` → **39/39 testler geçti** ✅
  - `python -m pytest tests -v --tb=short` → **55/55 testler geçti** ✅

---

### Task 3.3: Auth Testleri (TDD Tamamlama)

**Tahmini Süre:** 2 saat

**Durum:** ✅ YAPILDI

**Yapılacaklar:**
- [x] `tests/test_auth.py` tüm test case'lerinin geçtiğini doğrula:
    - [x] `test_hash_password_returns_different_from_plain`
    - [x] `test_verify_password_correct`
    - [x] `test_verify_password_wrong`
    - [x] `test_create_access_token_returns_string`
    - [x] `test_decode_access_token_returns_user_id`
    - [x] `test_decode_invalid_token_raises`
    - [x] `test_hash_token_is_deterministic`
    - [x] `test_register_request_rejects_short_password`
    - [x] `test_register_request_rejects_invalid_email`
    - [x] `test_register_creates_user_in_db`
    - [x] `test_register_creates_user_preferences`
    - [x] `test_register_duplicate_email_raises_409`
    - [x] `test_login_valid_credentials_returns_tokens`
    - [x] `test_login_wrong_password_returns_401`
    - [x] `test_brute_force_locks_account_after_5_attempts`
    - [x] `test_refresh_tokens_rotates_refresh_token`
    - [x] `test_refresh_with_revoked_token_raises_401`
    - [x] `test_post_register_returns_201`
    - [x] `test_post_login_sets_refresh_cookie`
    - [x] `test_post_refresh_rotates_token`
    - [x] `test_post_logout_revokes_refresh_token`
    - [x] `test_get_me_returns_current_user`
    - [x] `test_get_me_without_token_returns_401`
    - [x] `test_get_me_response_excludes_hashed_password`
    - [x] `test_patch_preferences_updates_language`
    - [x] `test_patch_preferences_invalid_ai_tone_returns_422`
- [x] Coverage doğrulama (`.venv`):
    - `python -m pytest tests/test_auth.py --cov=app.routers.auth --cov=app.services.auth_service --cov=app.utils.security -v`
    - Sonuç: `50/50 passed`, toplam coverage **%97** ✅

> **Ekstra Testler (Task 3.3 coverage için eklendi):**
> - `test_post_refresh_without_cookie_returns_401`
> - `test_post_logout_without_cookie_returns_200`
> - `test_post_forgot_password_unknown_email_returns_generic_success`
> - `test_post_forgot_password_existing_email_creates_reset_token`
> - `test_post_reset_password_invalid_token_returns_400`
> - `test_post_reset_password_expired_token_returns_400`
> - `test_post_reset_password_valid_token_updates_password_and_marks_used`
> - `test_post_login_unit_sets_cookie_and_returns_token`
> - `test_post_refresh_unit_sets_cookie_and_returns_token`
> - `test_post_forgot_password_unit_user_exists_creates_token`
> - `test_post_reset_password_unit_success_updates_user_and_marks_token`

---

### 📊 Phase 2 Success Metrics

- [x] `POST /auth/register` → kayıt başarılı, `user_preferences` otomatik oluştu
- [x] `POST /auth/login` → access token + refresh token cookie döndü
- [x] `POST /auth/refresh` → eski token revoke edildi, yeni token döndü
- [x] 5 hatalı giriş → `locked_until` set edildi, 6. denemede 423
- [x] `GET /users/me` Bearer token olmadan → 401
- [x] `pytest tests/test_auth.py` → tüm testler geçiyor, coverage >= %85

---

## 🎯 Phase 3 Overview — CrewAI Core

### Mimari: İki Crew, Dört Agent

Bu projede tek bir ReAct agent yerine **CrewAI** kullanılıyor. İki ayrı crew tanımlanıyor:

```
┌─────────────────────────────────────────────────────────┐
│                    NEWS CREW                            │
│                                                         │
│   [NewsFetcherAgent] ──────► [NewsAnalystAgent]         │
│    Haber getirir              Özetler & yanıtlar        │
│    - web_search tool          - summarize_article tool  │
│    - fetch_news_by_category   - build_system_prompt     │
│    - fetch_trending tool      - kullanıcı tercihlerini  │
│                                 dikkate alır            │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                  FACT CHECK CREW                        │
│                                                         │
│   [FactCheckerAgent] ─────► [VerdictAgent]             │
│    İddiayı araştırır          Karar verir               │
│    - fact_check_search tool   - JSON formatında         │
│    - web_search tool            TRUE/FALSE/UNVERIFIED   │
│                                 + confidence_score      │
└─────────────────────────────────────────────────────────┘
```

### Crew Akışı

**News Crew** → Kullanıcı chat mesajı gönderdiğinde tetiklenir:
1. `NewsFetcherAgent` konuya uygun haberleri arar/getirir
2. `NewsAnalystAgent` ham sonuçları alıp anlamlı, kaynaklı bir yanıt üretir
3. Sonuç `messages` tablosuna kaydedilir, tool çağrıları `agent_tool_calls`'a yazılır

**Fact Check Crew** → `POST /fact-check` endpoint'i tetiklendiğinde çalışır:
1. `FactCheckerAgent` iddiayı birden fazla kaynakta araştırır
2. `VerdictAgent` bulguları değerlendirip yapılandırılmış karar döndürür
3. Sonuç `fact_checks` tablosuna kaydedilir

### Scope

**Dahil:**
- Groq API LLM entegrasyonu (CrewAI LLM olarak)
- Tavily web search tool'u (CrewAI tool formatında)
- News Crew: `NewsFetcherAgent` + `NewsAnalystAgent`
- Fact Check Crew: `FactCheckerAgent` + `VerdictAgent`
- Tool çağrılarını `agent_tool_calls` tablosuna kaydetme
- Konuşma endpoint'leri (CRUD)
- Mesaj endpoint'i (News Crew'u tetikler)
- Konuşma geçmişini DB'den okuyup context'e ekleme

**Hariç:**
- `fetch_news_by_category` ve `fetch_trending` tool'ları (Phase 4)
- Fact Check Crew endpoint entegrasyonu (Phase 5)

### Definition of Done

- [ ] Kullanıcı mesaj gönderdiğinde News Crew tetikleniyor
- [ ] `NewsFetcherAgent` Tavily ile web araması yapıyor
- [ ] `NewsAnalystAgent` sonuçları işleyip yanıt üretiyor
- [ ] Her tool çağrısı `agent_tool_calls` tablosuna kaydediliyor
- [ ] Konuşma geçmişi doğru şekilde context'e dahil ediliyor
- [ ] `pytest tests/test_crew.py` → tüm testler geçiyor, coverage >= %80

---

## 📅 Week 3 (ikinci yarı): CrewAI Altyapısı & Tool Sistemi

**Hedef:** Groq LLM bağlantısı, CrewAI tool'ları, News Crew agent'ları ve task tanımları

---

### Task 3.4: Groq LLM & CrewAI Kurulumu

**Tahmini Süre:** 1.5 saat

**Durum:** ✅ YAPILDI

**Yapılacaklar:**
- [x] Test önce — `tests/test_crew.py` oluştur, LLM bağlantı testleri yaz:
  ```python
  from unittest.mock import patch, MagicMock
  from app.crew.agents.news_fetcher import create_news_fetcher_agent
  from crewai import LLM

  def test_create_news_fetcher_agent_returns_agent():
      with patch("app.crew.agents.news_fetcher.LLM"):
          agent = create_news_fetcher_agent(MagicMock())
          assert agent is not None
          assert agent.role == "News Fetcher"

  def test_news_fetcher_agent_has_web_search_tool():
      with patch("app.crew.agents.news_fetcher.LLM"):
          agent = create_news_fetcher_agent(MagicMock())
          tool_names = [t.name for t in agent.tools]
          assert "web_search" in tool_names

  def test_news_fetcher_agent_has_max_iter_set():
      with patch("app.crew.agents.news_fetcher.LLM"):
          agent = create_news_fetcher_agent(MagicMock())
          assert agent.max_iter == 5
  ```
- [x] `app/crew/__init__.py` oluştur
- [x] Groq'u CrewAI LLM olarak yapılandır:
  ```python
  # app/crew/agents/news_fetcher.py
  from crewai import Agent, LLM
  from app.config import settings

  groq_llm = LLM(
      model=f"groq/{settings.GROQ_MODEL_DEFAULT}",
      api_key=settings.GROQ_API_KEY,
      temperature=0.3
  )
  ```
- [x] Hata durumlarını handle et: `RateLimitError`, `APIConnectionError`

> **Ekstra Testler (Roadmap dışı, güvenlik amaçlı):**
> - `test_create_groq_llm_handles_rate_limit_error`
> - `test_create_groq_llm_handles_api_connection_error`

---

### ⚠️ CRITICAL: CrewAI Tool Names & agent_tool ENUM Eşleşmesi

**DATABASE.md** ile uyum zorunlu — `BaseTool.name` ile `agent_tool` ENUM değerleri eşleşmelidir:

| CrewAI BaseTool.name | agent_tool ENUM | Kullanıcı |
|---|---|---|
| `web_search` | `web_search` | `NewsFetcherAgent`, `FactCheckerAgent` |
| `fetch_news_by_category` | `fetch_news_by_category` | `NewsFetcherAgent` (Phase 4) |
| `fetch_trending` | `fetch_trending` | `NewsFetcherAgent` (Phase 4) |
| `fact_check_search` | `fact_check_search` | `FactCheckerAgent` (Phase 5) |
| `summarize_article` | `summarize_article` | `NewsAnalystAgent` |

**Yeni tool ekleme adımları:**
1. `BaseTool` sınıfında `name = "tool_name"` tanımla
2. **schema.sql** ve **DATABASE.md** arasında `agent_tool` ENUM'a ekle
3. `app/crew/utils.py` içindeki `KNOWN_TOOLS` listesini güncelle

---

### Task 3.5: Tavily Web Search Tool (CrewAI Formatı)

**Tahmini Süre:** 1.5 saat

**Durum:** ✅ YAPILDI

**Yapılacaklar:**
- [x] Test önce — `tests/test_crew.py`'e tool testleri ekle:
  ```python
  from unittest.mock import AsyncMock, patch
  from app.crew.tools.web_search import WebSearchTool

  def test_web_search_tool_name_matches_enum():
      tool = WebSearchTool()
      assert tool.name == "web_search"

  def test_web_search_tool_has_description():
      tool = WebSearchTool()
      assert len(tool.description) > 0

  async def test_web_search_tool_arun_returns_list():
      with patch("app.crew.tools.web_search.AsyncTavilyClient") as mock_tavily:
          mock_instance = AsyncMock()
          mock_tavily.return_value = mock_instance
          mock_instance.search.return_value = {
              "results": [{"title": "Test", "url": "http://test.com", "content": "Test content"}]
          }
          tool = WebSearchTool()
          result = await tool._arun(query="test news")
          assert isinstance(result, list)
          assert len(result) == 1
          assert "title" in result[0]
          assert "url" in result[0]

  async def test_web_search_tool_returns_empty_on_no_results():
      with patch("app.crew.tools.web_search.AsyncTavilyClient") as mock_tavily:
          mock_instance = AsyncMock()
          mock_tavily.return_value = mock_instance
          mock_instance.search.return_value = {"results": []}
          tool = WebSearchTool()
          result = await tool._arun(query="obscure query")
          assert result == []
  ```
- [x] `app/crew/tools/web_search.py` oluştur:
  ```python
  from crewai.tools import BaseTool
  from tavily import AsyncTavilyClient
  from app.config import settings
  from pydantic import BaseModel, Field

  class WebSearchInput(BaseModel):
      query: str = Field(description="Arama sorgusu")
      max_results: int = Field(default=5)

  class WebSearchTool(BaseTool):
      name: str = "web_search"
      description: str = (
          "Web'de güncel haber, olay veya bilgi arar. "
          "Son gelişmeler için kullan."
      )
      args_schema: type[BaseModel] = WebSearchInput

      async def _arun(self, query: str, max_results: int = 5) -> list[dict]:
          tavily = AsyncTavilyClient(api_key=settings.TAVILY_API_KEY)
          response = await tavily.search(
              query=query,
              search_depth="advanced",
              max_results=max_results,
              include_answer=True
          )
          return [
              {"title": r["title"], "url": r["url"], "snippet": r["content"]}
              for r in response.get("results", [])
          ]
  ```

---

### Task 3.6: Summarize Article Tool (CrewAI Formatı)

**Tahmini Süre:** 1 saat

**Durum:** ✅ YAPILDI

**Yapılacaklar:**
- [x] Test önce — `tests/test_crew.py`'e eklendi:
  ```python
  from app.crew.tools.summarize import SummarizeArticleTool

  def test_summarize_tool_name_matches_enum():
      tool = SummarizeArticleTool()
      assert tool.name == "summarize_article"

  async def test_summarize_tool_arun_returns_string():
      with patch("app.crew.tools.summarize.httpx.AsyncClient") as mock_client:
          mock_response = MagicMock()
          mock_response.text = "<html><body>Article content here</body></html>"
          mock_client.return_value.__aenter__.return_value.get = AsyncMock(return_value=mock_response)
          tool = SummarizeArticleTool()
          result = await tool._arun(url="http://test.com/article")
          assert isinstance(result, str)

  async def test_summarize_tool_handles_fetch_error():
      with patch("app.crew.tools.summarize.httpx.AsyncClient") as mock_client:
          mock_client.return_value.__aenter__.return_value.get = AsyncMock(side_effect=Exception("fetch error"))
          tool = SummarizeArticleTool()
          result = await tool._arun(url="http://invalid.com")
          assert "hata" in result.lower() or result == ""
  ```
- [x] `app/crew/tools/summarize.py` oluşturuldu:
  ```python
  from crewai.tools import BaseTool
  from pydantic import BaseModel, Field
  import httpx

  class SummarizeInput(BaseModel):
      url: str = Field(description="Özetlenecek haber URL'i")

  class SummarizeArticleTool(BaseTool):
      name: str = "summarize_article"
      description: str = "Verilen URL'deki makaleyi çekip 3-4 cümlelik özet üretir."
      args_schema: type[BaseModel] = SummarizeInput

      async def _arun(self, url: str) -> str:
          try:
              async with httpx.AsyncClient(timeout=10.0) as client:
                  response = await client.get(url, follow_redirects=True)
                  # Ham HTML'den metin çıkar, Groq ile özetle
                  text = response.text[:5000]  # İlk 5000 karakter
                  return text  # TODO: Groq ile özet üret
          except Exception as e:
              return f"Makale yüklenemedi: {str(e)}"
  ```

---

### Task 3.7: News Crew Agent'ları

**Tahmini Süre:** 2 saat

**Durum:** ✅ YAPILDI

**Yapılacaklar:**
- [x] Test önce — `tests/test_crew.py`'e ekle:
  ```python
  def test_news_analyst_agent_goal_includes_language(mock_llm):
      agent = create_news_analyst_agent(mock_llm, "English", "formal")
      assert "English" in agent.goal

  def test_news_analyst_agent_goal_includes_tone(mock_llm):
      agent = create_news_analyst_agent(mock_llm, "Turkish", "casual")
      assert "casual" in agent.goal

  def test_news_analyst_agent_has_summarize_tool(mock_llm):
      agent = create_news_analyst_agent(mock_llm, "Turkish", "neutral")
      tool_names = [t.name for t in agent.tools]
      assert "summarize_article" in tool_names

  def test_news_fetcher_agent_backstory_mentions_tavily(mock_llm):
      agent = create_news_fetcher_agent(mock_llm)
      assert "Tavily" in agent.backstory or len(agent.backstory) > 0
  ```
- [x] `app/crew/agents/news_fetcher.py` oluştur:
  ```python
  from crewai import Agent, LLM
  from app.crew.tools.web_search import WebSearchTool

  def create_news_fetcher_agent(llm: LLM) -> Agent:
      return Agent(
          role="News Fetcher",
          goal="Kullanıcının sorusuyla ilgili güncel ve güvenilir haberleri bul.",
          backstory=(
              "Sen deneyimli bir araştırmacısın. "
              "Tavily arama motoru ile en güncel haberleri bulur, "
              "kaynaklarını belgelersin."
          ),
          tools=[WebSearchTool()],
          llm=llm,
          verbose=True,
          max_iter=5
      )
  ```
- [x] `app/crew/agents/news_analyst.py` oluştur:
  ```python
  from crewai import Agent, LLM
  from app.crew.tools.summarize import SummarizeArticleTool

  def create_news_analyst_agent(llm: LLM, language: str, ai_tone: str) -> Agent:
      return Agent(
          role="News Analyst",
          goal=(
              f"Getirilen haberleri analiz et ve kullanıcıya {language} dilinde, "
              f"{ai_tone} tonunda, kaynaklı bir yanıt üret."
          ),
          backstory=(
              "Sen tarafsız ve titiz bir haber analistsin. "
              "Her iddiayı kaynaklarla desteklersin, asla tahmin yürütmezsin."
          ),
          tools=[SummarizeArticleTool()],
          llm=llm,
          verbose=True
      )
  ```

  > **user_preferences entegrasyonu:** `language` ve `ai_tone` parametreleri **DATABASE.md**'deki `user_preferences` tablosundan gelir. Konuşma başlatılırken kullanıcının tercihlerine göre agent otomatik yapılandırılır.
  >
  > **Örnek flow:**
  > - Kullanıcı profili: `language="English"`, `ai_tone="formal"`
  > - Chat tetiklendiğinde: `create_news_analyst_agent(llm, "English", "formal")` çağrılır
  > - Agent'ın goal'u dinamik olur: *"...English dilinde, formal tonunda...*"

---

### Task 3.8: News Crew Task'ları ve Crew Tanımı

**Tahmini Süre:** 2 saat

**Durum:** ✅ YAPILDI

**Yapılacaklar:**
- [x] Test önce — `tests/test_crew.py`'e ekle:
  ```python
  from app.crew.tasks.news_tasks import create_fetch_task, create_analysis_task
  from unittest.mock import MagicMock

  def test_fetch_task_description_includes_user_message():
      agent = MagicMock()
      task = create_fetch_task(agent, "Tech news today", [])
      assert "Tech news today" in task.description

  def test_fetch_task_includes_conversation_history():
      agent = MagicMock()
      history = [{"role": "user", "content": "previous question"}]
      task = create_fetch_task(agent, "follow up", history)
      assert "previous question" in task.description

  def test_fetch_task_limits_history_to_10_messages():
      agent = MagicMock()
      history = [{"role": "user", "content": f"msg {i}"} for i in range(20)]
      task = create_fetch_task(agent, "new question", history)
      assert "msg 0" not in task.description
      assert "msg 19" in task.description

  def test_analysis_task_uses_fetch_task_as_context():
      agent = MagicMock()
      fetch_task = MagicMock()
      analysis_task = create_analysis_task(agent, fetch_task)
      assert fetch_task in analysis_task.context

  def test_build_news_crew_returns_crew_with_2_agents():
      with patch("app.crew.news_crew.LLM"):
          crew = build_news_crew()
          assert len(crew.agents) == 2
  ```
- [x] `app/crew/tasks/news_tasks.py` oluştur:
  ```python
  from crewai import Task

  def create_fetch_task(agent, user_message: str, conversation_history: list[dict]) -> Task:
      history_text = "\n".join(
          [f"{m['role']}: {m['content']}" for m in conversation_history[-10:]]
      )
      return Task(
          description=(
              f"Konuşma geçmişi:\n{history_text}\n\n"
              f"Kullanıcının son sorusu: {user_message}\n\n"
              "Bu soru için güncel haberleri ve bilgileri web'de ara. "
              "Kaynak URL'lerini mutlaka dahil et."
          ),
          expected_output="Haberlerin listesi: başlık, URL, kısa özet içermeli.",
          agent=agent
      )

  def create_analysis_task(agent, fetch_task: Task) -> Task:
      return Task(
          description=(
              "Önceki adımda bulunan haberleri analiz et. "
              "Kullanıcının sorusunu yanıtlayan, kaynaklı, net bir cevap oluştur. "
              "Her önemli iddia için kaynak URL belirt."
          ),
          expected_output=(
              "Kullanıcıya yönelik, kaynaklı, markdown formatında yanıt. "
              "Sonunda kaynaklar listesi bulunmalı."
          ),
          agent=agent,
          context=[fetch_task]
      )
  ```
- [x] `app/crew/news_crew.py` oluştur:
  ```python
  from crewai import Crew, Process, LLM
  from app.crew.agents.news_fetcher import create_news_fetcher_agent
  from app.crew.agents.news_analyst import create_news_analyst_agent
  from app.crew.tasks.news_tasks import create_fetch_task, create_analysis_task
  from app.config import settings

  def build_news_crew(language: str = "Turkish", ai_tone: str = "neutral") -> Crew:
      llm = LLM(
          model=f"groq/{settings.GROQ_MODEL_DEFAULT}",
          api_key=settings.GROQ_API_KEY
      )
      fetcher = create_news_fetcher_agent(llm)
      analyst = create_news_analyst_agent(llm, language, ai_tone)
      return Crew(
          agents=[fetcher, analyst],
          process=Process.sequential,
          verbose=True
      )

  async def run_news_crew(
      user_message: str,
      conversation_history: list[dict],
      language: str,
      ai_tone: str
  ) -> str:
      crew = build_news_crew(language, ai_tone)
      fetcher_agent = crew.agents[0]
      analyst_agent = crew.agents[1]
      fetch_task = create_fetch_task(fetcher_agent, user_message, conversation_history)
      analysis_task = create_analysis_task(analyst_agent, fetch_task)
      crew.tasks = [fetch_task, analysis_task]
      result = await crew.kickoff_async()
      return result.raw
  ```

> **Ekstra test (roadmape eklendi):**
> - [x] `test_run_news_crew_returns_result_raw` — `run_news_crew()` fonksiyonunun crew sonucundaki `raw` çıktıyı döndürdüğü doğrulandı.

---

### Task 3.9: Tool Çağrılarını DB'ye Kaydetme

**Tahmini Süre:** 1.5 saat

**Durum:** ✅ YAPILDI

**Yapılacaklar:**
- [x] Test önce — `tests/test_crew.py`'e ekle:
  ```python
  from app.crew.utils import set_tool_call_context, clear_tool_call_context, _context_stack

  def test_set_tool_call_context_stores_message_id():
      import uuid
      message_id = uuid.uuid4()
      set_tool_call_context(message_id, MagicMock(), uuid.uuid4())
      assert _context_stack["message_id"] == message_id

  def test_clear_tool_call_context_empties_stack():
      set_tool_call_context(MagicMock(), MagicMock(), MagicMock())
      clear_tool_call_context()
      assert _context_stack == {}

  async def test_tool_call_logged_to_agent_tool_calls_table(client, auth_headers, mock_crew):
      # mock_crew: News Crew'un mock'u — web_search çağrısı simüle edilir
      # Chat mesajı gönder
      # agent_tool_calls tablosunda kayıt oluştuğunu doğrula
      ...

  async def test_tool_call_failure_logged_with_is_success_false(db, mock_crew_with_error):
      # Tool hata fırlattığında is_success=False ile kaydedilmeli
      ...
  ```
- [x] CrewAI callback hook'larını kullanarak tool çağrılarını yakala:
  ```python
  # app/crew/hooks.py
  from crewai.utilities.events import crewai_event_bus
  from crewai.utilities.events.agent_events import ToolUsageFinishedEvent
  from app.models.conversation import AgentToolCall
  from app.crew.utils import _context_stack

  @crewai_event_bus.on(ToolUsageFinishedEvent)
  async def on_tool_used(source, event: ToolUsageFinishedEvent):
      if not _context_stack.get("message_id"):
          return
      message_id = _context_stack["message_id"]
      db = _context_stack["db"]
      known_tools = {"web_search", "fetch_news_by_category", "fetch_trending", "fact_check_search", "summarize_article"}
      tool_name = event.tool_name if event.tool_name in known_tools else None
      if tool_name is None:
          return
      tool_call = AgentToolCall(
          message_id=message_id,
          tool_name=tool_name,
          input_params=event.tool_input or {},
          output_result=str(event.tool_output),
          duration_ms=getattr(event, "duration_ms", None),
          is_success=not bool(getattr(event, "error", None)),
          error_message=str(event.error) if getattr(event, "error", None) else None
      )
      db.add(tool_call)
      await db.commit()
  ```
- [x] `app/crew/utils.py` oluştur:
  ```python
  from uuid import UUID
  from sqlalchemy.ext.asyncio import AsyncSession

  _context_stack: dict = {}

  def set_tool_call_context(message_id: UUID, db: AsyncSession, user_id: UUID):
      """CrewAI callback'lerinin mesaj context'ine erişmesi için."""
      _context_stack["message_id"] = message_id
      _context_stack["db"] = db
      _context_stack["user_id"] = user_id

  def clear_tool_call_context():
      _context_stack.clear()
  ```
- [x] Crew çalışması başında ve sonunda context yönetimi:
  ```python
  # app/services/crew_service.py içinde
  from app.crew.utils import set_tool_call_context, clear_tool_call_context

  set_tool_call_context(message.id, db, user_id)
  try:
      result = await crew.kickoff_async()
  finally:
      clear_tool_call_context()
  ```

---

### Task 3.10: Crew Service

**Tahmini Süre:** 1 saat

**Durum:** ✅ YAPILDI

**Yapılacaklar:**
- [x] Test önce — `tests/test_crew.py`'e ekle:
  ```python
  from app.services.crew_service import run_chat_crew

  async def test_run_chat_crew_returns_string_and_sources(mock_news_crew):
      result, sources = await run_chat_crew(
          user_message="Tech news?",
          conversation_history=[],
          user_preferences={"language": "Turkish", "ai_tone": "neutral"},
          db=MagicMock(),
          message_id=uuid.uuid4()
      )
      assert isinstance(result, str)
      assert isinstance(sources, list)

  async def test_run_chat_crew_uses_language_from_preferences(mock_news_crew):
      await run_chat_crew(
          user_message="News?",
          conversation_history=[],
          user_preferences={"language": "English", "ai_tone": "formal"},
          db=MagicMock(),
          message_id=uuid.uuid4()
      )
      # mock_news_crew'e "English" ve "formal" geçildiğini doğrula
      mock_news_crew.assert_called_with(language="English", ai_tone="formal")
  ```
- [x] `app/services/crew_service.py` oluştur:
  ```python
  from uuid import UUID
  from sqlalchemy.ext.asyncio import AsyncSession
  from app.crew.news_crew import run_news_crew
  from app.crew.utils import set_tool_call_context, clear_tool_call_context
  import re

  async def run_chat_crew(
      user_message: str,
      conversation_history: list[dict],
      user_preferences: dict,
      db: AsyncSession,
      message_id: UUID
  ) -> tuple[str, list[dict]]:
      language = user_preferences.get("language", "Turkish")
      ai_tone = user_preferences.get("ai_tone", "neutral")
      set_tool_call_context(message_id, db, None)
      try:
          result = await run_news_crew(user_message, conversation_history, language, ai_tone)
      finally:
          clear_tool_call_context()
      sources = _parse_sources_from_result(result)
      return result, sources

  def _parse_sources_from_result(result: str) -> list[dict]:
      """Markdown formatındaki URL'leri kaynak olarak çıkarır."""
      urls = re.findall(r'https?://[^\s\)]+', result)
      return [{"url": url} for url in urls[:10]]
  ```

---

## 📅 Week 4: Chat Endpoint'leri & Konuşma Yönetimi

**Hedef:** Konuşma CRUD, mesaj endpoint'i, News Crew entegrasyonu

---

### Task 4.1: Conversation Schemas

**Tahmini Süre:** 1 saat

**Durum:** ✅ YAPILDI

**Yapılacaklar:**
- [x] Test önce — `tests/test_crew.py`'e schema validation testleri ekle:
  ```python
  from app.schemas.conversation import MessageCreate, ConversationResponse
  from pydantic import ValidationError

  def test_message_create_rejects_empty_content():
      with pytest.raises(ValidationError):
          MessageCreate(content="")

  def test_message_create_rejects_too_long_content():
      with pytest.raises(ValidationError):
          MessageCreate(content="x" * 4001)

  def test_message_create_valid():
      msg = MessageCreate(content="What is the latest tech news?")
      assert msg.content == "What is the latest tech news?"
  ```
- [x] `app/schemas/conversation.py` oluştur:
  ```python
  from pydantic import BaseModel, Field, ConfigDict
  from datetime import datetime
  import uuid

  class ConversationCreate(BaseModel):
      title: str | None = None

  class ConversationUpdate(BaseModel):
      title: str = Field(min_length=1, max_length=200)

  class ConversationResponse(BaseModel):
      id: uuid.UUID
      title: str | None
      created_at: datetime
      updated_at: datetime
      model_config = ConfigDict(from_attributes=True)

  class MessageCreate(BaseModel):
      content: str = Field(min_length=1, max_length=4000)

  class MessageResponse(BaseModel):
      id: uuid.UUID
      role: str
      content: str
      sources: list[dict] | None
      created_at: datetime
      model_config = ConfigDict(from_attributes=True)

  class ConversationDetailResponse(ConversationResponse):
      messages: list[MessageResponse]
  ```

---

### Task 4.2: Conversation Router

**Tahmini Süre:** 3 saat

**Durum:** ✅ YAPILDI

**Yapılacaklar:**
- [x] Test önce — `tests/test_crew.py`'e endpoint testleri ekle:
  ```python
  async def test_post_conversations_creates_conversation(client, auth_headers):
      response = await client.post("/conversations", headers=auth_headers)
      assert response.status_code == 201
      assert "id" in response.json()

  async def test_get_conversations_returns_only_current_user(client, auth_headers, auth_headers_user2):
      await client.post("/conversations", headers=auth_headers)
      await client.post("/conversations", headers=auth_headers)
      await client.post("/conversations", headers=auth_headers_user2)
      response = await client.get("/conversations", headers=auth_headers)
      assert len(response.json()) == 2

  async def test_access_other_user_conversation_returns_403(client, auth_headers, auth_headers_user2):
      create_resp = await client.post("/conversations", headers=auth_headers_user2)
      conv_id = create_resp.json()["id"]
      response = await client.get(f"/conversations/{conv_id}", headers=auth_headers)
      assert response.status_code == 403

  async def test_delete_conversation_soft_deletes(client, auth_headers):
      create_resp = await client.post("/conversations", headers=auth_headers)
      conv_id = create_resp.json()["id"]
      await client.delete(f"/conversations/{conv_id}", headers=auth_headers)
      response = await client.get(f"/conversations/{conv_id}", headers=auth_headers)
      assert response.status_code == 404

  async def test_send_message_creates_user_and_assistant_messages(client, auth_headers, mock_crew_service):
      create_resp = await client.post("/conversations", headers=auth_headers)
      conv_id = create_resp.json()["id"]
      response = await client.post(
          f"/conversations/{conv_id}/messages",
          json={"content": "What is trending in tech?"},
          headers=auth_headers
      )
      assert response.status_code == 200
      assert response.json()["role"] == "assistant"

  async def test_conversation_history_included_in_crew_call(client, auth_headers, mock_crew_service):
      create_resp = await client.post("/conversations", headers=auth_headers)
      conv_id = create_resp.json()["id"]
      await client.post(f"/conversations/{conv_id}/messages", json={"content": "First question"}, headers=auth_headers)
      await client.post(f"/conversations/{conv_id}/messages", json={"content": "Follow up"}, headers=auth_headers)
      call_args = mock_crew_service.call_args
      assert len(call_args.kwargs["conversation_history"]) >= 2
  ```
- [x] `app/routers/conversations.py` oluştur:
    - [x] `GET /conversations` → kullanıcının aktif konuşmaları
    - [x] `POST /conversations` → yeni konuşma oluştur
    - [x] `GET /conversations/{id}` → konuşma + tüm mesajlar
    - [x] `PATCH /conversations/{id}` → title güncelle
    - [x] `DELETE /conversations/{id}` → soft delete
    - [x] `POST /conversations/{id}/archive`
    - [x] `POST /conversations/{id}/messages` → **Ana endpoint: News Crew'u tetikler**:
    1. Kullanıcı mesajını `messages` tablosuna ekle (`role='user'`)
    2. Konuşma geçmişini DB'den çek (son 20 mesaj)
    3. `run_chat_crew()` çağır (News Crew)
    4. Crew cevabını `messages` tablosuna ekle (`role='assistant'`, `sources` dolu)
    5. Konuşmanın `title`'ını ilk mesajdan üret (sadece ilk mesajda)
    6. `MessageResponse` döndür
    - [x] Başka kullanıcının konuşmasına erişim → 403

---

### Task 4.3: Streaming Desteği (Opsiyonel)

**Tahmini Süre:** 2 saat

**Durum:** ✅ YAPILDI

**Yapılacaklar:**
- [x] `POST /conversations/{id}/messages/stream` endpoint'i eklendi
- [x] CrewAI `step_callback` ile ara adım sonuçları SSE olarak gönderiliyor:
  ```
  data: {"event": "tool_start", "tool": "web_search"}
  data: {"event": "tool_end", "tool": "web_search"}
  data: {"token": "Bu"}
  data: [DONE]
  ```
- [x] Stream tamamlandıktan sonra tam mesaj DB'ye kaydediliyor

> **Ekstra test:** `test_send_message_stream_returns_sse_and_persists_assistant_message` eklendi.

---

### Task 4.4: Crew Testleri (TDD Tamamlama)

**Tahmini Süre:** 2 saat

**Durum:** ✅ YAPILDI

**Yapılacaklar:**
- [x] `tests/test_crew.py` tüm test case'lerinin geçtiğini doğrula:
    - [x] `test_create_news_fetcher_agent_returns_agent`
    - [x] `test_news_fetcher_agent_has_web_search_tool`
    - [x] `test_news_fetcher_agent_has_max_iter_set`
    - [x] `test_web_search_tool_name_matches_enum`
    - [x] `test_web_search_tool_arun_returns_list`
    - [x] `test_summarize_tool_name_matches_enum`
    - [x] `test_news_analyst_agent_goal_includes_language`
    - [x] `test_news_analyst_agent_goal_includes_tone`
    - [x] `test_fetch_task_description_includes_user_message`
    - [x] `test_fetch_task_includes_conversation_history`
    - [x] `test_fetch_task_limits_history_to_10_messages`
    - [x] `test_analysis_task_uses_fetch_task_as_context`
    - [x] `test_set_tool_call_context_stores_message_id`
    - [x] `test_clear_tool_call_context_empties_stack`
    - [x] `test_run_chat_crew_returns_string_and_sources`
    - [x] `test_send_message_creates_user_and_assistant_messages`
    - [x] `test_get_conversations_returns_only_current_user`
    - [x] `test_access_other_user_conversation_returns_403`
    - [x] `test_delete_conversation_soft_deletes`
    - [x] `test_conversation_history_included_in_crew_call`
    - [x] `test_max_iter_prevents_infinite_loop` (max_iter=5 ile sonsuz döngü engelleniyor)
- [x] `pytest tests/test_crew.py --cov=app/crew --cov=app/services/crew_service` → coverage >= %80

---

### 📊 Phase 3 Success Metrics

- [ ] `POST /conversations/{id}/messages` → News Crew tetikleniyor
- [ ] Haber sorusu sorulduğunda `NewsFetcherAgent` Tavily'i kullanıyor
- [ ] `NewsAnalystAgent` fetcher çıktısını alıp yanıt üretiyor
- [ ] `agent_tool_calls` tablosunda her tool çağrısı için kayıt oluşuyor
- [ ] Konuşma geçmişi fetch task context'ine dahil ediliyor
- [ ] Silinmiş konuşma GET isteğinde 404 dönüyor
- [ ] `pytest tests/test_crew.py` → tüm testler geçiyor, coverage >= %80

---

## 🎯 Phase 4 Overview

### Scope

**Dahil:**
- NewsAPI.org client
- Google News RSS parser
- `article_cache` tablosu üzerinde okuma/yazma
- `FetchNewsTool` ve `FetchTrendingTool` (CrewAI tool formatında)
- `NewsFetcherAgent`'a yeni tool'ların eklenmesi
- News Feed endpoint'leri
- Cache TTL yönetimi (6 saat)
- APScheduler ile periyodik cache temizliği

**Hariç:**
- Trending sistemi (Phase 7)

### Definition of Done

- [ ] `GET /news/feed` NewsAPI'den veya cache'den haber döndürüyor
- [ ] Aynı kategori 6 saat içinde tekrar istendiğinde NewsAPI çağrılmıyor
- [ ] `NewsFetcherAgent` artık `fetch_news_by_category` ve `fetch_trending` tool'larını kullanabiliyor
- [ ] Cache temizliği background task ile çalışıyor
- [ ] `pytest tests/test_news.py` → tüm testler geçiyor

---

## 📅 Week 5: NewsAPI Entegrasyonu & Cache Sistemi

---

### Task 5.1: NewsAPI Client

**Tahmini Süre:** 1.5 saat

**Durum:** ✅ YAPILDI

**Yapılacaklar:**
- [x] Test önce — `tests/test_news.py` oluştur:
  ```python
  import pytest
  from unittest.mock import AsyncMock, patch, MagicMock
  from app.services.news_service import fetch_from_newsapi, fetch_from_rss, get_or_fetch_articles

  async def test_fetch_from_newsapi_returns_article_list(mock_httpx):
      mock_httpx.return_value.__aenter__.return_value.get.return_value.json.return_value = {
          "articles": [
              {"title": "Test Article", "url": "http://test.com", "source": {"name": "Test Source"}, "publishedAt": "2024-01-01T00:00:00Z"}
          ]
      }
      result = await fetch_from_newsapi("technology")
      assert isinstance(result, list)
      assert len(result) == 1
      assert result[0]["title"] == "Test Article"
      assert result[0]["url"] == "http://test.com"

  async def test_fetch_from_newsapi_excludes_articles_without_url(mock_httpx):
      mock_httpx.return_value.__aenter__.return_value.get.return_value.json.return_value = {
          "articles": [
              {"title": "No URL", "url": None, "source": {"name": "Source"}, "publishedAt": "2024-01-01"},
              {"title": "Has URL", "url": "http://has.com", "source": {"name": "Source"}, "publishedAt": "2024-01-01"},
          ]
      }
      result = await fetch_from_newsapi("technology")
      assert len(result) == 1
      assert result[0]["title"] == "Has URL"

  async def test_fetch_from_newsapi_raises_on_http_error(mock_httpx):
      mock_httpx.return_value.__aenter__.return_value.get.return_value.raise_for_status.side_effect = Exception("HTTP Error")
      with pytest.raises(Exception):
          await fetch_from_newsapi("technology")

  async def test_rss_fallback_returns_list(mock_httpx):
      mock_httpx.return_value.__aenter__.return_value.get.return_value.text = (
          '<?xml version="1.0"?><rss><channel>'
          '<item><title>RSS Article</title><link>http://rss.com</link></item>'
          '</channel></rss>'
      )
      result = await fetch_from_rss("technology")
      assert isinstance(result, list)
  ```
- [x] `app/services/news_service.py` oluştur:
  ```python
  import httpx
  from app.config import settings

  async def fetch_from_newsapi(category: str, from_date: str | None = None) -> list[dict]:
      """NewsAPI.org /top-headlines endpoint'i çağırır."""
      async with httpx.AsyncClient() as client:
          resp = await client.get(
              "https://newsapi.org/v2/top-headlines",
              params={
                  "category": category,
                  "apiKey": settings.NEWS_API_KEY,
                  "pageSize": 20,
                  **({"from": from_date} if from_date else {})
              },
              timeout=10.0
          )
          resp.raise_for_status()
          articles = resp.json().get("articles", [])
          return [
              {
                  "title": a["title"],
                  "url": a["url"],
                  "source_name": a["source"]["name"],
                  "published_at": a["publishedAt"],
                  "category": category,
                  "ai_summary": None
              }
              for a in articles if a.get("url")
          ]

  async def fetch_from_rss(category: str) -> list[dict]:
      """Google News RSS fallback."""
      rss_url = f"https://news.google.com/rss/search?q={category}&hl=tr&gl=TR"
      async with httpx.AsyncClient() as client:
          resp = await client.get(rss_url, timeout=10.0)
          # XML parse et
          import xml.etree.ElementTree as ET
          root = ET.fromstring(resp.text)
          items = root.findall(".//item")
          return [
              {
                  "title": item.findtext("title", ""),
                  "url": item.findtext("link", ""),
                  "source_name": "Google News",
                  "published_at": item.findtext("pubDate"),
                  "category": category,
                  "ai_summary": None
              }
              for item in items[:20] if item.findtext("link")
          ]

  async def get_or_fetch_articles(category: str) -> list[dict]:
      """Cache'e bak, yoksa NewsAPI → RSS sırayla dene."""
      try:
          return await fetch_from_newsapi(category)
      except Exception:
          return await fetch_from_rss(category)
  ```

> **Ekstra test:** `test_get_or_fetch_articles_falls_back_to_rss_when_newsapi_fails` eklendi ve NewsAPI hata verince RSS fallback davranışı doğrulandı.

---

### Task 5.2: Cache Servisi

**Tahmini Süre:** 2 saat

**Durum:** ✅ YAPILDI

**Yapılacaklar:**
- [x] Test önce — `tests/test_news.py`'e ekle:
  ```python
  from app.utils.cache import get_cached_articles, set_cached_articles, build_cache_key
  from datetime import datetime, timezone, timedelta

  async def test_get_cached_articles_returns_none_when_no_cache(db):
      result = await get_cached_articles("technology:default", db)
      assert result is None

  async def test_set_and_get_cached_articles(db):
      articles = [{"title": "Test", "url": "http://test.com"}]
      await set_cached_articles("technology:default", articles, "technology", db)
      result = await get_cached_articles("technology:default", db)
      assert result == articles

  async def test_get_cached_articles_returns_none_when_expired(db):
      articles = [{"title": "Old", "url": "http://old.com"}]
      await set_cached_articles("tech:expired", articles, "technology", db)
      # Cache kaydını manuel olarak expire et
      await db.execute(text(
          "UPDATE article_cache SET expires_at = NOW() - INTERVAL '1 hour' WHERE cache_key = 'tech:expired'"
      ))
      await db.commit()
      result = await get_cached_articles("tech:expired", db)
      assert result is None

  async def test_request_count_increments_on_cache_hit(db):
      articles = [{"title": "Hit", "url": "http://hit.com"}]
      await set_cached_articles("tech:hit", articles, "technology", db)
      await get_cached_articles("tech:hit", db)
      await get_cached_articles("tech:hit", db)
      result = await db.execute(
          text("SELECT request_count FROM article_cache WHERE cache_key = 'tech:hit'")
      )
      count = result.scalar()
      assert count == 2

  async def test_build_cache_key_format():
      key = build_cache_key("technology", "today")
      assert key == "technology:today"
  ```
- [x] `app/utils/cache.py` oluştur:
  ```python
  from sqlalchemy.ext.asyncio import AsyncSession
  from sqlalchemy import select, text
  from app.models.news import ArticleCache
  from datetime import datetime, timezone, timedelta
  from app.config import settings
  import json

  def build_cache_key(category: str, period: str | None = None) -> str:
      return f"{category}:{period or 'default'}"

  async def get_cached_articles(cache_key: str, db: AsyncSession) -> list[dict] | None:
      """Geçerli cache kaydı varsa döndür, yoksa None."""
      result = await db.execute(
          select(ArticleCache).where(
              ArticleCache.cache_key == cache_key,
              ArticleCache.expires_at > datetime.now(timezone.utc)
          )
      )
      entry = result.scalar_one_or_none()
      if not entry:
          return None
      entry.request_count += 1
      await db.commit()
      return entry.articles_json

  async def set_cached_articles(
      cache_key: str, articles: list[dict], category: str, db: AsyncSession
  ) -> None:
      """Cache'e yaz, TTL hesapla."""
      expires_at = datetime.now(timezone.utc) + timedelta(hours=settings.ARTICLE_CACHE_TTL_HOURS)
      existing = await db.execute(
          select(ArticleCache).where(ArticleCache.cache_key == cache_key)
      )
      entry = existing.scalar_one_or_none()
      if entry:
          entry.articles_json = articles
          entry.expires_at = expires_at
      else:
          db.add(ArticleCache(
              cache_key=cache_key,
              category=category,
              articles_json=articles,
              expires_at=expires_at
          ))
      await db.commit()

  async def run_cleanup(db: AsyncSession) -> None:
      """Süresi dolmuş cache ve token kayıtlarını temizle."""
      await db.execute(text("SELECT cleanup_expired_cache()"))
      await db.commit()
  ```

---

### Task 5.3: News Feed Router

**Tahmini Süre:** 2 saat

**Durum:** ✅ YAPILDI

**Yapılacaklar:**
- [ ] Test önce — `tests/test_news.py`'e endpoint testleri ekle:
- [x] Test önce — `tests/test_news.py`'e endpoint testleri ekle:
  ```python
  async def test_get_news_feed_returns_article_list(client, mock_newsapi):
      response = await client.get("/news/feed?category=technology")
      assert response.status_code == 200
      assert isinstance(response.json(), list)

  async def test_get_news_feed_invalid_category_returns_422(client):
      response = await client.get("/news/feed?category=invalid_category_xyz")
      assert response.status_code == 422

  async def test_get_news_feed_uses_cache_on_second_request(client, mock_newsapi):
      await client.get("/news/feed?category=technology")
      await client.get("/news/feed?category=technology")
      # NewsAPI sadece bir kez çağrılmalı
      assert mock_newsapi.call_count == 1

  async def test_get_news_feed_does_not_require_auth(client, mock_newsapi):
      response = await client.get("/news/feed?category=technology")
      assert response.status_code != 401

  async def test_get_news_feed_response_has_required_fields(client, mock_newsapi):
      response = await client.get("/news/feed?category=technology")
      if response.json():
          article = response.json()[0]
          assert "title" in article
          assert "url" in article
          assert "category" in article
  ```
- [ ] `app/schemas/news.py` oluştur:
- [x] `app/schemas/news.py` oluştur:
  ```python
  from pydantic import BaseModel, ConfigDict
  from datetime import datetime
  import uuid

  class ArticleResponse(BaseModel):
      title: str
      url: str
      source_name: str
      published_at: str | None
      ai_summary: str | None
      category: str

  class SaveArticleRequest(BaseModel):
      title: str
      url: str
      source_name: str
      published_at: str | None = None
      category: str

  class SavedArticleResponse(ArticleResponse):
      id: uuid.UUID
      saved_at: datetime
      model_config = ConfigDict(from_attributes=True)
  ```
- [ ] `app/routers/news.py` oluştur:
- [x] `app/routers/news.py` oluştur:
  ```python
  from fastapi import APIRouter, Depends, Query
  from app.schemas.news import ArticleResponse, SaveArticleRequest, SavedArticleResponse
  from app.utils.cache import get_cached_articles, set_cached_articles, build_cache_key
  from app.services.news_service import get_or_fetch_articles
  from app.dependencies import get_current_user
  from app.database import get_db
  from typing import Literal

  router = APIRouter(prefix="/news", tags=["news"])

  @router.get("/feed", response_model=list[ArticleResponse])
  async def get_news_feed(
      category: Literal["world", "technology", "sports", "economy", "health", "science", "entertainment"] = Query(...),
      period: str | None = None,
      db = Depends(get_db)
  ):
      cache_key = build_cache_key(category, period)
      cached = await get_cached_articles(cache_key, db)
      if cached:
          return cached
      articles = await get_or_fetch_articles(category)
      await set_cached_articles(cache_key, articles, category, db)
      return articles
  ```

> **Ekstra test:** `test_get_news_feed_response_has_required_fields` eklendi ve router çıktısının schema uyumu doğrulandı.

---

### Task 5.4: FetchNewsTool & FetchTrendingTool (CrewAI Formatı)

**Tahmini Süre:** 1.5 saat

**Durum:** ✅ YAPILDI

**Yapılacaklar:**
- [x] Test önce — `tests/test_news.py`'e tool testleri ekle:
  ```python
  from app.crew.tools.fetch_news import FetchNewsTool
  from app.crew.tools.fetch_trending import FetchTrendingTool

  def test_fetch_news_tool_name_matches_enum():
      tool = FetchNewsTool()
      assert tool.name == "fetch_news_by_category"

  def test_fetch_trending_tool_name_matches_enum():
      tool = FetchTrendingTool()
      assert tool.name == "fetch_trending"

  async def test_fetch_news_tool_arun_returns_list(mock_get_or_fetch):
      mock_get_or_fetch.return_value = [{"title": "Test", "url": "http://test.com"}]
      tool = FetchNewsTool()
      result = await tool._arun(category="technology")
      assert isinstance(result, list)
      assert len(result) == 1

  async def test_fetch_news_tool_accepts_valid_categories():
      tool = FetchNewsTool()
      # Geçersiz kategori ile ValidationError fırlatmalı
      with pytest.raises(Exception):
          await tool._arun(category="invalid_cat")
  ```
- [x] `app/crew/tools/fetch_news.py` oluştur:
  ```python
  from crewai.tools import BaseTool
  from pydantic import BaseModel, Field
  from app.services.news_service import get_or_fetch_articles

  class FetchNewsInput(BaseModel):
      category: str = Field(
          description="Haber kategorisi",
          json_schema_extra={"enum": ["world","technology","sports","economy","health","science","entertainment"]}
      )
      from_date: str | None = Field(default=None, description="ISO tarih YYYY-MM-DD")

  class FetchNewsTool(BaseTool):
      name: str = "fetch_news_by_category"
      description: str = (
          "Belirli bir kategoride yapılandırılmış haber makalelerini getirir. "
          "Kullanıcı belirli bir konuda haber istediğinde kullan."
      )
      args_schema: type[BaseModel] = FetchNewsInput

      async def _arun(self, category: str, from_date: str | None = None) -> list[dict]:
          return await get_or_fetch_articles(category)
  ```
- [x] `app/crew/tools/fetch_trending.py` oluştur (benzer şekilde, `get_trending_articles` çağırır)
- [x] `NewsFetcherAgent`'a bu iki tool'u ekle:
  ```python
  tools=[WebSearchTool(), FetchNewsTool(), FetchTrendingTool()]
  ```
- [x] Tool çağrılarının `agent_tool_calls` tablosuna kaydedildiğini doğrula

> **Not:** `fetch_trending` için `get_trending_articles()` servis fonksiyonu eklendi ve araç üzerinden çağrıldığı doğrulandı.

---

### Task 5.5: Background Cache Cleanup

**Tahmini Süre:** 1 saat

**Durum:** ✅ YAPILDI

**Yapılacaklar:**
- [x] Test önce — `tests/test_news.py`'e ekle:
  ```python
  async def test_run_cleanup_deletes_expired_cache_entries(db):
      await set_cached_articles("expired:key", [], "technology", db)
      await db.execute(text(
          "UPDATE article_cache SET expires_at = NOW() - INTERVAL '1 hour' WHERE cache_key = 'expired:key'"
      ))
      await db.commit()
      await run_cleanup(db)
      result = await db.execute(text("SELECT COUNT(*) FROM article_cache WHERE cache_key = 'expired:key'"))
      assert result.scalar() == 0

  async def test_run_cleanup_keeps_valid_cache_entries(db):
      await set_cached_articles("valid:key", [], "technology", db)
      await db.commit()
      await run_cleanup(db)
      result = await db.execute(text("SELECT COUNT(*) FROM article_cache WHERE cache_key = 'valid:key'"))
      assert result.scalar() == 1
  ```
- [x] `app/main.py`'ye APScheduler ekle:
  ```python
  from apscheduler.schedulers.asyncio import AsyncIOScheduler
  from app.utils.cache import run_cleanup
  from app.database import AsyncSessionLocal

  scheduler = AsyncIOScheduler()

  @app.on_event("startup")
  async def startup_event():
      async def scheduled_cleanup():
          async with AsyncSessionLocal() as db:
              await run_cleanup(db)
      scheduler.add_job(scheduled_cleanup, "interval", hours=6)
      scheduler.start()

  @app.on_event("shutdown")
  async def shutdown_event():
      scheduler.shutdown()
  ```

> **Ekstra testler:**
> - [x] `test_startup_event_schedules_cleanup_job`
> - [x] `test_shutdown_event_stops_scheduler`

---

### Task 5.6: News Feed & Cache Testleri (TDD Tamamlama)

**Tahmini Süre:** 2 saat

**Durum:** ✅ YAPILDI

**Yapılacaklar:**
- [x] `tests/test_news.py` tüm test case'lerinin geçtiğini doğrula:
    - [x] `test_fetch_from_newsapi_returns_article_list`
    - [x] `test_fetch_from_newsapi_excludes_articles_without_url`
    - [x] `test_fetch_from_newsapi_raises_on_http_error`
    - [x] `test_rss_fallback_returns_list`
    - [x] `test_get_cached_articles_returns_none_when_no_cache`
    - [x] `test_set_and_get_cached_articles`
    - [x] `test_get_cached_articles_returns_none_when_expired`
    - [x] `test_request_count_increments_on_cache_hit`
    - [x] `test_get_news_feed_returns_article_list`
    - [x] `test_get_news_feed_invalid_category_returns_422`
    - [x] `test_get_news_feed_uses_cache_on_second_request`
    - [x] `test_fetch_news_tool_name_matches_enum`
    - [x] `test_fetch_trending_tool_name_matches_enum`
    - [x] `test_fetch_news_tool_arun_returns_list`
    - [x] `test_run_cleanup_deletes_expired_cache_entries`
    - [x] `test_run_cleanup_keeps_valid_cache_entries`
- [x] `pytest tests/test_news.py --cov=app.services.news_service --cov=app.utils.cache` → coverage >= %80 (sonuç: toplam %90)

---

### 📊 Phase 4 Success Metrics

- [ ] `GET /news/feed?category=technology&period=today` → article listesi döndürüyor
- [ ] Aynı istek 6 saat içinde tekrarlandığında `article_cache.request_count` artıyor
- [ ] NewsAPI limiti doluyken RSS fallback devreye giriyor
- [ ] Chat'te "teknoloji haberlerini getir" denilince `NewsFetcherAgent`, `fetch_news_by_category` tool'unu çağırıyor
- [ ] APScheduler her 6 saatte cleanup çalıştırıyor
- [x] `pytest tests/test_news.py` → tüm testler geçiyor

---

## 🎯 Phase 5 Overview — Fact Check Crew

### Mimari

```
POST /fact-check {"claim": "..."}
        │
        ▼
  FactCheckCrew.kickoff_async()
        │
   ┌────┴────────────────────────────┐
   │                                 │
[FactCheckerAgent]          [VerdictAgent]
 - fact_check_search tool    - Bulguları değerlendirir
 - web_search tool           - JSON: verdict + score + sources
 - Birden fazla kaynaktan    - Hiçbir zaman tahmin yapmaz
   araştırma yapar
   │
   └─► context olarak VerdictAgent'a geçer
```

### Scope

**Dahil:**
- `FactCheckCrew`: `FactCheckerAgent` + `VerdictAgent`
- `FactCheckSearchTool` (CrewAI formatında)
- Fact Check endpoint'leri
- Fact check geçmişi (kullanıcı bazlı)
- Güven skoru hesaplama

**Hariç:**
- Gerçek credibility scoring sistemi (şimdilik basit heuristic)

### Definition of Done

- [ ] `POST /fact-check` endpoint çalışıyor, TRUE/FALSE/UNVERIFIED döndürüyor
- [ ] Her fact check `fact_checks` tablosuna kaydediliyor
- [ ] Giriş yapmamış kullanıcı da fact check yapabiliyor (`user_id = NULL`)
- [ ] Geçmiş endpoint'i çalışıyor
- [ ] `pytest tests/test_fact_check.py` → tüm testler geçiyor, coverage >= %80

---

## 📅 Week 6: Fact Check Crew & Endpoint'leri

---

### Task 6.1: Fact Check Crew Agent'ları

**Tahmini Süre:** 2 saat

**Durum:** ✅ YAPILDI

**Yapılacaklar:**
- [x] Test önce — `tests/test_fact_check.py` oluştur:
  ```python
  from app.crew.tools.fact_check_search import FactCheckSearchTool
  from app.crew.agents.fact_checker import create_fact_checker_agent
  from app.crew.agents.verdict_agent import create_verdict_agent

  def test_fact_check_search_tool_name_matches_enum():
      tool = FactCheckSearchTool()
      assert tool.name == "fact_check_search"

  async def test_fact_check_search_tool_arun_returns_list(mock_tavily):
      mock_tavily.search.return_value = {
          "results": [{"title": "Check", "url": "http://factcheck.com", "content": "The claim is false"}]
      }
      tool = FactCheckSearchTool()
      result = await tool._arun(claim="The earth is flat")
      assert isinstance(result, list)

  def test_fact_checker_agent_has_both_tools(mock_llm):
      agent = create_fact_checker_agent(mock_llm)
      tool_names = [t.name for t in agent.tools]
      assert "fact_check_search" in tool_names
      assert "web_search" in tool_names

  def test_fact_checker_agent_has_max_iter(mock_llm):
      agent = create_fact_checker_agent(mock_llm)
      assert agent.max_iter == 5

  def test_verdict_agent_has_no_tools(mock_llm):
      agent = create_verdict_agent(mock_llm)
      assert len(agent.tools) == 0

  def test_verdict_agent_uses_reasoning_model():
      # VerdictAgent daha güçlü model kullanmalı
      with patch("app.crew.agents.verdict_agent.LLM") as mock_llm:
          create_verdict_agent(MagicMock())
          call_args = mock_llm.call_args
          assert settings.GROQ_MODEL_REASONING in str(call_args)
  ```
- [x] `app/crew/tools/fact_check_search.py` oluştur:
  ```python
  class FactCheckSearchTool(BaseTool):
      name: str = "fact_check_search"
      description: str = (
          "Bir iddiayı doğrulamak için özelleştirilmiş web araması yapar. "
          "Fact-checking için her zaman bu tool'u kullan."
      )

      async def _arun(self, claim: str) -> list[dict]:
          tavily = AsyncTavilyClient(api_key=settings.TAVILY_API_KEY)
          response = await tavily.search(
              query=f"fact check: {claim}",
              search_depth="advanced",
              max_results=5,
              include_answer=True
          )
          return [
              {"title": r["title"], "url": r["url"], "snippet": r["content"]}
              for r in response.get("results", [])
          ]
  ```
- [x] `app/crew/agents/fact_checker.py` oluştur:
  ```python
  def create_fact_checker_agent(llm: LLM) -> Agent:
      return Agent(
          role="Fact Checker",
          goal="İddiayı birden fazla bağımsız kaynakta araştır.",
          backstory=(
              "Sen şüpheci ve titiz bir araştırmacısın. "
              "Her iddiayı en az iki bağımsız kaynakla doğrularsın."
          ),
          tools=[FactCheckSearchTool(), WebSearchTool()],
          llm=llm,
          max_iter=5
      )
  ```
- [x] `app/crew/agents/verdict_agent.py` oluştur:
  ```python
  def create_verdict_agent(llm: LLM) -> Agent:
      return Agent(
          role="Verdict Agent",
          goal="Araştırma bulgularını değerlendirip yapılandırılmış karar ver.",
          backstory=(
              "Sen tarafsız bir hakem ve editörsün. "
              "Kanıtlara dayanarak TRUE/FALSE/UNVERIFIED kararı verirsin. "
              "Asla tahmin yapmazsın; kanıt yetersizse UNVERIFIED döndürürsün."
          ),
          tools=[],
          llm=LLM(
              model=f"groq/{settings.GROQ_MODEL_REASONING}",
              api_key=settings.GROQ_API_KEY
          )
      )
  ```

> **Doğrulama:** `pytest tests/test_fact_check.py -q` çalıştırıldı → **6/6 test geçti** ✅

---

### Task 6.2: Fact Check Task'ları ve Crew Tanımı

**Tahmini Süre:** 2 saat

**Durum:** ✅ TAMAMLANDI

**Yapılacaklar:**
- [x] Test önce — `tests/test_fact_check.py`'e ekle:
  ```python
  from app.crew.tasks.fact_check_tasks import create_research_task, create_verdict_task

  def test_research_task_description_includes_claim():
      agent = MagicMock()
      task = create_research_task(agent, "The earth is flat")
      assert "The earth is flat" in task.description

  def test_research_task_asks_for_multiple_sources():
      agent = MagicMock()
      task = create_research_task(agent, "test claim")
      assert "3" in task.description or "multiple" in task.description.lower() or "farklı" in task.description

  def test_verdict_task_uses_research_task_as_context():
      agent = MagicMock()
      research_task = MagicMock()
      task = create_verdict_task(agent, research_task)
      assert research_task in task.context

  def test_verdict_task_expected_output_is_json():
      agent = MagicMock()
      task = create_verdict_task(agent, MagicMock())
      assert "JSON" in task.expected_output or "json" in task.expected_output
  ```
- [x] `app/crew/tasks/fact_check_tasks.py` oluştur:
  ```python
  def create_research_task(agent, claim: str) -> Task:
      return Task(
          description=(
              f"Şu iddiayı araştır: '{claim}'\n\n"
              "- En az 3 farklı kaynakta ara\n"
              "- Bağımsız kaynakları önceliklendir\n"
              "- Her kaynağın URL'ini kaydet"
          ),
          expected_output="Kaynaklar listesi: başlık, URL, iddiayı destekleme/çürütme durumu.",
          agent=agent
      )

  def create_verdict_task(agent, research_task: Task) -> Task:
      return Task(
          description=(
              "Araştırma bulgularını değerlendirip şu JSON formatında yanıt ver:\n"
              '{"verdict": "TRUE|FALSE|UNVERIFIED", '
              '"explanation": "2-3 cümle", '
              '"confidence_score": 0.0-1.0, '
              '"sources": [{"title": "...", "url": "...", "snippet": "..."}]}'
          ),
          expected_output="Geçerli JSON, başka hiçbir şey yok.",
          agent=agent,
          context=[research_task]
      )
  ```
- [x] `app/crew/fact_check_crew.py` oluştur:
  ```python
  async def run_fact_check_crew(claim: str) -> dict:
      llm = LLM(model=f"groq/{settings.GROQ_MODEL_DEFAULT}", api_key=settings.GROQ_API_KEY)
      checker = create_fact_checker_agent(llm)
      verdict = create_verdict_agent(llm)
      research_task = create_research_task(checker, claim)
      verdict_task = create_verdict_task(verdict, research_task)
      crew = Crew(
          agents=[checker, verdict],
          tasks=[research_task, verdict_task],
          process=Process.sequential,
          verbose=True
      )
      result = await crew.kickoff_async()
      return json.loads(result.raw)
  ```

> **Doğrulama:** `pytest tests/test_fact_check.py -q` çalıştırıldı → **10/10 test geçti** ✅

---

### Task 6.3: Fact Check Servisi & Router

**Tahmini Süre:** 2 saat

**Durum:** ✅ YAPILDI

**Yapılacaklar:**
- [x] Test önce — `tests/test_fact_check.py`'e endpoint testleri ekle:
  ```python
  async def test_post_fact_check_returns_verdict(client, mock_fact_check_crew):
      mock_fact_check_crew.return_value = {
          "verdict": "FALSE",
          "explanation": "Multiple sources confirm this is false.",
          "confidence_score": 0.92,
          "sources": [{"title": "Fact Check", "url": "http://factcheck.com", "snippet": "..."}]
      }
      response = await client.post("/fact-check", json={"claim": "The earth is flat"})
      assert response.status_code == 200
      data = response.json()
      assert data["verdict"] in ("TRUE", "FALSE", "UNVERIFIED")
      assert 0.0 <= data["confidence_score"] <= 1.0

  async def test_fact_check_logged_with_null_user_id_when_anonymous(client, mock_fact_check_crew, db):
      mock_fact_check_crew.return_value = {"verdict": "FALSE", "explanation": "False", "confidence_score": 0.9, "sources": []}
      await client.post("/fact-check", json={"claim": "Anonymous claim"})
      result = await db.execute(text("SELECT user_id FROM fact_checks ORDER BY created_at DESC LIMIT 1"))
      user_id = result.scalar()
      assert user_id is None

  async def test_fact_check_logged_with_user_id_when_authenticated(client, auth_headers, mock_fact_check_crew, db):
      mock_fact_check_crew.return_value = {"verdict": "TRUE", "explanation": "True", "confidence_score": 0.8, "sources": []}
      await client.post("/fact-check", json={"claim": "Auth claim"}, headers=auth_headers)
      result = await db.execute(text("SELECT user_id FROM fact_checks ORDER BY created_at DESC LIMIT 1"))
      user_id = result.scalar()
      assert user_id is not None

  async def test_fact_check_history_requires_auth(client):
      response = await client.get("/fact-check/history")
      assert response.status_code == 401

  async def test_fact_check_history_returns_user_checks(client, auth_headers, mock_fact_check_crew):
      mock_fact_check_crew.return_value = {"verdict": "TRUE", "explanation": "t", "confidence_score": 0.5, "sources": []}
      await client.post("/fact-check", json={"claim": "Claim 1"}, headers=auth_headers)
      await client.post("/fact-check", json={"claim": "Claim 2"}, headers=auth_headers)
      response = await client.get("/fact-check/history", headers=auth_headers)
      assert response.status_code == 200
      assert len(response.json()) == 2

  async def test_false_claim_returns_false_verdict(client, mock_fact_check_crew):
      mock_fact_check_crew.return_value = {"verdict": "FALSE", "explanation": "False claim.", "confidence_score": 0.95, "sources": []}
      response = await client.post("/fact-check", json={"claim": "Known false claim"})
      assert response.json()["verdict"] == "FALSE"
  ```
- [x] `app/services/fact_check_service.py` oluştur:
  ```python
  async def check_claim(claim: str, user_id: uuid.UUID | None, db: AsyncSession) -> FactCheck:
      result = await run_fact_check_crew(claim)
      fact_check = FactCheck(
          user_id=user_id,
          claim=claim,
          verdict=result["verdict"],
          explanation=result["explanation"],
          confidence_score=result["confidence_score"],
          sources=result.get("sources", [])
      )
      db.add(fact_check)
      await db.commit()
      await db.refresh(fact_check)
      return fact_check
  ```
- [x] `app/routers/fact_check.py` oluştur:
    - [x] `POST /fact-check` → auth opsiyonel, Fact Check Crew çalıştır
    - [x] `GET /fact-check/history` → kullanıcının geçmişi (auth gerekli)
    - [x] `GET /fact-check/{id}` → tek kayıt

> **Ekstra testler (roadmap dışı ama gerekli doğrulama için eklendi):**
> - [x] `test_get_fact_check_by_id_returns_single_record`
> - [x] `test_get_fact_check_by_id_requires_auth`

> **Doğrulama:**
> - `pytest tests/test_fact_check.py -q` → **18/18 test geçti** ✅
> - `pytest tests/test_auth.py tests/test_fact_check.py -q` → **68/68 test geçti** ✅

---

### Task 6.4: Fact Check Testleri (TDD Tamamlama)

**Tahmini Süre:** 2 saat

**Durum:** ✅ TAMAMLANDI

**Yapılacaklar:**
- [x] `tests/test_fact_check.py` tüm test case'lerinin geçtiğini doğrula:
    - [x] `test_fact_check_search_tool_name_matches_enum`
    - [x] `test_fact_check_search_tool_arun_returns_list`
    - [x] `test_fact_checker_agent_has_both_tools`
    - [x] `test_fact_checker_agent_has_max_iter`
    - [x] `test_verdict_agent_has_no_tools`
    - [x] `test_verdict_agent_uses_reasoning_model`
    - [x] `test_research_task_description_includes_claim`
    - [x] `test_verdict_task_uses_research_task_as_context`
    - [x] `test_post_fact_check_returns_verdict`
    - [x] `test_fact_check_logged_with_null_user_id_when_anonymous`
    - [x] `test_fact_check_logged_with_user_id_when_authenticated`
    - [x] `test_fact_check_history_requires_auth`
    - [x] `test_fact_check_history_returns_user_checks`
    - [x] `test_false_claim_returns_false_verdict`
- [x] `pytest tests/test_fact_check.py --cov=app.crew.agents.fact_checker --cov=app.crew.agents.verdict_agent` → coverage >= %80

> **Doğrulama:** `pytest tests/test_fact_check.py --cov=app.crew.agents.fact_checker --cov=app.crew.agents.verdict_agent -q` çalıştırıldı → **18/18 test geçti**, coverage **%100** ✅

---

### 📊 Phase 5 Success Metrics

- [ ] `POST /fact-check` → Fact Check Crew tetikleniyor
- [ ] `FactCheckerAgent` birden fazla kaynakta araştırma yapıyor
- [ ] `VerdictAgent` yapılandırılmış JSON döndürüyor
- [ ] Her fact check `fact_checks` tablosuna kaydediliyor
- [ ] Giriş yapmadan fact check → `user_id = NULL` ile kaydediliyor
- [ ] `pytest tests/test_fact_check.py` → tüm testler geçiyor, coverage >= %80

---

## 🎯 Phase 6 Overview

### Scope

**Dahil:**
- Saved articles CRUD endpoint'leri
- User preferences endpoint'leri
- CrewAI agent davranışının `user_preferences`'e göre dinamik ayarlanması

**Hariç:**
- OAuth
- E-posta gönderimi

### Definition of Done

- [ ] Makale kaydetme/silme çalışıyor
- [ ] Kullanıcı tercihlerini güncelleyince agent dili ve tonu değişiyor
- [ ] Aynı makale iki kez kaydedilmeye çalışılınca 409
- [ ] Phase 6 testleri geçiyor

---

## 📅 Week 7: Saved Articles & User Preferences

---

### Task 7.1: Saved Articles Router

**Tahmini Süre:** 2 saat

**Durum:** ⬜ BEKLEMEDE

**Yapılacaklar:**
- [ ] Test önce — `tests/test_news.py`'e saved article testleri ekle:
  ```python
  async def test_save_article_returns_201(client, auth_headers):
      response = await client.post("/news/saved", json={
          "title": "Test Article", "url": "http://test.com/article",
          "source_name": "Test Source", "category": "technology"
      }, headers=auth_headers)
      assert response.status_code == 201
      assert "id" in response.json()

  async def test_save_same_article_twice_returns_409(client, auth_headers):
      article = {"title": "Dup", "url": "http://dup.com", "source_name": "Src", "category": "technology"}
      await client.post("/news/saved", json=article, headers=auth_headers)
      response = await client.post("/news/saved", json=article, headers=auth_headers)
      assert response.status_code == 409

  async def test_get_saved_articles_returns_only_current_user(client, auth_headers, auth_headers_user2):
      await client.post("/news/saved", json={"title": "A1", "url": "http://a1.com", "source_name": "S", "category": "technology"}, headers=auth_headers)
      await client.post("/news/saved", json={"title": "A2", "url": "http://a2.com", "source_name": "S", "category": "technology"}, headers=auth_headers_user2)
      response = await client.get("/news/saved", headers=auth_headers)
      assert len(response.json()) == 1
      assert response.json()[0]["title"] == "A1"

  async def test_delete_saved_article_removes_from_db(client, auth_headers):
      create_resp = await client.post("/news/saved", json={
          "title": "Del", "url": "http://del.com", "source_name": "S", "category": "technology"
      }, headers=auth_headers)
      article_id = create_resp.json()["id"]
      await client.delete(f"/news/saved/{article_id}", headers=auth_headers)
      response = await client.get("/news/saved", headers=auth_headers)
      assert len(response.json()) == 0

  async def test_save_article_requires_auth(client):
      response = await client.post("/news/saved", json={"title": "T", "url": "http://t.com", "source_name": "S", "category": "technology"})
      assert response.status_code == 401
  ```
- [ ] `app/routers/news.py`'ye saved article endpoint'leri ekle:
  - [ ] `GET /news/saved` → kullanıcının kaydettiği haberler
  - [ ] `POST /news/saved` → makale kaydet (URL + metadata)
  - [ ] `DELETE /news/saved/{id}` → kaydı sil
  - [ ] Aynı URL'yi iki kez kaydetme → 409 (UNIQUE constraint yakalanır)

---

### Task 7.2: User Preferences & Agent Entegrasyonu

**Tahmini Süre:** 1.5 saat

**Durum:** ⬜ BEKLEMEDE

**Yapılacaklar:**
- [ ] Test önce — `tests/test_auth.py`'e agent entegrasyon testleri ekle:
  ```python
  async def test_news_analyst_goal_changes_with_language_preference(client, auth_headers, mock_crew_service):
      await client.patch("/users/me/preferences", json={"language": "English"}, headers=auth_headers)
      await client.post("/conversations", headers=auth_headers)
      # mock_crew_service'e "English" geçildiğini doğrula
      call_args = mock_crew_service.call_args
      assert call_args.kwargs["user_preferences"]["language"] == "English"

  async def test_news_analyst_goal_changes_with_tone_preference(client, auth_headers, mock_crew_service):
      await client.patch("/users/me/preferences", json={"ai_tone": "formal"}, headers=auth_headers)
      # Chat mesajı gönder, tone kontrolü yap
      ...
  ```
- [ ] Konuşma mesajı gönderilirken kullanıcının tercihlerinin `crew_service`'e geçildiğini doğrula:
  ```python
  # app/routers/conversations.py mesaj endpoint'inde
  user_prefs = await db.get(UserPreferences, current_user.id)
  result, sources = await run_chat_crew(
      user_message=message_body.content,
      conversation_history=history,
      user_preferences={
          "language": user_prefs.language,
          "ai_tone": user_prefs.ai_tone,
      },
      db=db,
      message_id=user_message.id
  )
  ```

---

### Task 7.3: User Features Testleri (TDD Tamamlama)

**Tahmini Süre:** 1.5 saat

**Durum:** ⬜ BEKLEMEDE

**Yapılacaklar:**
- [ ] `tests/test_news.py` saved article test case'lerinin geçtiğini doğrula:
  - [ ] `test_save_article_returns_201`
  - [ ] `test_save_same_article_twice_returns_409`
  - [ ] `test_get_saved_articles_returns_only_current_user`
  - [ ] `test_delete_saved_article_removes_from_db`
  - [ ] `test_save_article_requires_auth`
- [ ] `tests/test_auth.py` preferences test case'lerinin geçtiğini doğrula:
  - [ ] `test_get_preferences_returns_defaults`
  - [ ] `test_patch_preferences_updates_language`
  - [ ] `test_patch_preferences_invalid_ai_tone_returns_422`
  - [ ] `test_news_analyst_goal_changes_with_language_preference`

---

### 📊 Phase 6 Success Metrics

- [ ] `POST /news/saved` → makale kaydediliyor
- [ ] Aynı makale tekrar kaydedilmeye çalışılınca 409
- [ ] `PATCH /users/me/preferences` ile `language=English` ayarlanınca agent İngilizce yanıt üretiyor
- [ ] `PATCH /users/me/preferences` ile `ai_tone=formal` ayarlanınca `NewsAnalystAgent` goal'u değişiyor
- [ ] Phase 6 testleri geçiyor

---

## 🎯 Phase 7 Overview

### Scope

**Dahil:**
- Trending endpoint'i
- Kategori sayfası endpoint'leri
- `FetchTrendingTool`'un `NewsFetcherAgent`'ta kullanımı

### Definition of Done

- [ ] `GET /news/trending` çalışıyor
- [ ] `GET /news/category/{category}` çalışıyor
- [ ] Agent "ne trending?" sorusuna `FetchTrendingTool` ile cevap veriyor
- [ ] Phase 7 testleri geçiyor

---

## 📅 Week 8: Trending Sistemi & Kategori Endpoint'leri

---

### Task 8.1: Trending Router

**Tahmini Süre:** 1.5 saat

**Durum:** ⬜ BEKLEMEDE

**Yapılacaklar:**
- [ ] Test önce — `tests/test_news.py`'e ekle:
  ```python
  async def test_get_trending_returns_article_list(client, mock_newsapi):
      response = await client.get("/news/trending")
      assert response.status_code == 200
      assert isinstance(response.json(), list)

  async def test_get_trending_with_topic_filter(client, mock_newsapi):
      response = await client.get("/news/trending?topic=technology")
      assert response.status_code == 200

  async def test_view_count_increments_on_trending_cache_hit(db, client, mock_newsapi):
      await client.get("/news/trending")
      await client.get("/news/trending")
      result = await db.execute(text("SELECT MAX(view_count) FROM article_cache"))
      count = result.scalar() or 0
      assert count >= 1
  ```
- [ ] `app/routers/news.py`'ye ekle:
  - [ ] `GET /news/trending` → `view_count DESC` sıralı makale listesi, opsiyonel `topic` filtresi
  - [ ] `view_count` cache hit'lerinden türetilir

---

### Task 8.2: Category Router

**Tahmini Süre:** 1.5 saat

**Durum:** ⬜ BEKLEMEDE

**Yapılacaklar:**
- [ ] Test önce — `tests/test_news.py`'e ekle:
  ```python
  async def test_get_category_news_returns_article_list(client, mock_newsapi):
      response = await client.get("/news/category/technology")
      assert response.status_code == 200
      assert isinstance(response.json(), list)

  async def test_get_category_news_invalid_category_returns_422(client):
      response = await client.get("/news/category/invalid_xyz")
      assert response.status_code == 422

  async def test_get_category_news_with_subcategory_filter(client, mock_newsapi):
      response = await client.get("/news/category/sports?subcategory=football")
      assert response.status_code == 200

  async def test_get_category_news_pagination(client, mock_newsapi):
      response = await client.get("/news/category/technology?page=1&page_size=5")
      assert response.status_code == 200
      assert len(response.json()) <= 5
  ```
- [ ] `app/routers/news.py`'ye ekle:
  - [ ] `GET /news/category/{category}` → kategori haberleri, opsiyonel `subcategory`, `page`, `page_size` parametreleri
  - [ ] Geçersiz kategori → 422

---

### Task 8.3: Trending & Category Testleri (TDD Tamamlama)

**Tahmini Süre:** 1 saat

**Durum:** ⬜ BEKLEMEDE

**Yapılacaklar:**
- [ ] `tests/test_news.py` trending & category test case'lerinin geçtiğini doğrula:
  - [ ] `test_get_trending_returns_article_list`
  - [ ] `test_get_trending_with_topic_filter`
  - [ ] `test_get_category_news_returns_article_list`
  - [ ] `test_get_category_news_invalid_category_returns_422`
  - [ ] `test_get_category_news_with_subcategory_filter`
  - [ ] `test_get_category_news_pagination`

---

### 📊 Phase 7 Success Metrics

- [ ] `GET /news/trending` → `view_count DESC` sıralı makale listesi
- [ ] `GET /news/category/sports?subcategory=football` → football haberleri
- [ ] `NewsFetcherAgent` "şu an ne trending?" sorusunda `FetchTrendingTool`'u kullanıyor
- [ ] Cache hit sonrası `article_cache.view_count` artıyor
- [ ] Phase 7 testleri geçiyor

---

## 🎯 Phase 8 Overview

### Scope

**Dahil:**
- E2E test senaryoları
- Rate limiter middleware
- Security hardening
- API dokümantasyonu
- Docker clean build testi
- Performance kontrol

### Definition of Done

- [ ] E2E test senaryoları %100 geçiyor
- [ ] Test coverage >= %80
- [ ] Rate limiter aktif
- [ ] Security checklist tamamlandı
- [ ] Docker clean build sorunsuz çalışıyor

---

## 📅 Week 9: Testing, Security Hardening & Dokümantasyon

---

### Task 9.1: Rate Limiter

**Tahmini Süre:** 1.5 saat

**Durum:** ⬜ BEKLEMEDE

**Yapılacaklar:**
- [ ] Test önce — `tests/test_e2e.py`'e rate limit testleri ekle:
  ```python
  async def test_rate_limit_returns_429_after_threshold(client):
      for _ in range(11):
          await client.post("/auth/login", json={"email": "rate@test.com", "password": "wrong"})
      response = await client.post("/auth/login", json={"email": "rate@test.com", "password": "wrong"})
      assert response.status_code == 429

  async def test_rate_limit_does_not_affect_non_auth_endpoints(client):
      for _ in range(15):
          response = await client.get("/health")
      assert response.status_code == 200
  ```
- [ ] `app/middleware/rate_limiter.py` oluştur:
  ```python
  from fastapi import Request, HTTPException
  from collections import defaultdict
  import time

  _request_counts: dict[str, list[float]] = defaultdict(list)
  WINDOW_SECONDS = 60
  MAX_REQUESTS = 10

  async def rate_limit_middleware(request: Request, call_next):
      if request.url.path.startswith("/auth"):
          client_ip = request.client.host
          now = time.time()
          window_start = now - WINDOW_SECONDS
          _request_counts[client_ip] = [t for t in _request_counts[client_ip] if t > window_start]
          if len(_request_counts[client_ip]) >= MAX_REQUESTS:
              raise HTTPException(status_code=429, detail="Çok fazla istek. Bir dakika bekleyin.")
          _request_counts[client_ip].append(now)
      return await call_next(request)
  ```
- [ ] `app/main.py`'ye middleware olarak ekle:
  ```python
  from app.middleware.rate_limiter import rate_limit_middleware
  app.middleware("http")(rate_limit_middleware)
  ```

---

### Task 9.2: Security Hardening

**Tahmini Süre:** 2 saat

**Durum:** ⬜ BEKLEMEDE

**Yapılacaklar:**
- [ ] Test önce — `tests/test_e2e.py`'e güvenlik testleri ekle:
  ```python
  async def test_hashed_password_not_in_user_response(client, auth_headers):
      response = await client.get("/users/me", headers=auth_headers)
      assert "hashed_password" not in response.json()
      assert "hashed_password" not in str(response.json())

  async def test_token_hash_not_in_any_response(client, auth_headers):
      response = await client.get("/users/me", headers=auth_headers)
      assert "token_hash" not in str(response.json())

  async def test_cors_disallows_unknown_origins(client):
      response = await client.get("/health", headers={"Origin": "https://evil-site.com"})
      assert response.headers.get("access-control-allow-origin") != "https://evil-site.com"

  async def test_sql_injection_attempt_returns_safe_response(client, auth_headers):
      response = await client.get("/news/feed?category=' OR '1'='1", headers=auth_headers)
      assert response.status_code in (200, 422)
      assert "error" not in str(response.json()).lower() or response.status_code == 422
  ```
- [ ] Response şemalarından `hashed_password`, `token_hash` alanlarının dışlandığını doğrula (zaten `model_config` ile yapılmış olmalı)
- [ ] CORS middleware'in `settings.ALLOWED_ORIGINS` ile kısıtlandığını doğrula
- [ ] SQL injection koruması: tüm sorgularda ORM parametrik yapılar kullanılıyor, raw SQL yok
- [ ] `.env` dosyasının `.gitignore`'da olduğunu doğrula
- [ ] `JWT_SECRET` minimum 32 karakter kısıtlaması ekle (`config.py`'de validator)

---

### Task 9.3: E2E Test Senaryoları

**Tahmini Süre:** 3 saat

**Durum:** ⬜ BEKLEMEDE

**Yapılacaklar:**
- [ ] `tests/test_e2e.py` oluştur:
  - [ ] **Senaryo 1: Tam Chat Akışı (News Crew)**
    1. Kullanıcı kayıt olur
    2. Giriş yapar, token alır
    3. Yeni konuşma oluşturur
    4. Haber sorusu sorar → `NewsFetcherAgent` Tavily'i kullanır (mock)
    5. `NewsAnalystAgent` yanıtı üretir, `messages`'a kaydedilir
    6. `agent_tool_calls`'a kayıt düşer
    7. Takip sorusu sorar → geçmiş context'e dahil edilir
    8. Konuşmayı arşivler

  - [ ] **Senaryo 2: Fact Check Akışı (Fact Check Crew)**
    1. Giriş yapmadan fact check isteği atar
    2. `FactCheckerAgent` araştırır, `VerdictAgent` karar verir (mock)
    3. `user_id = NULL` ile kaydediliyor
    4. Giriş yapar, aynı claim'i tekrar fact check eder
    5. Bu sefer `user_id` dolu kaydediliyor

  - [ ] **Senaryo 3: Article Cache Akışı**
    1. `GET /news/feed?category=technology` → NewsAPI çağrılır, cache'e yazılır
    2. Aynı istek tekrarlanır → cache hit, NewsAPI çağrılmaz
    3. Cache expire olur (mock ile) → yeniden NewsAPI çağrılır

  - [ ] **Senaryo 4: Auth Güvenlik Akışı**
    1. 5 hatalı giriş → hesap kilitlenir
    2. Doğru şifre ile giriş denenir → 423
    3. 15 dakika sonra (mock ile) kilit kalkar
    4. Token refresh → eski token revoke edilir
    5. Eski token ile refresh denenir → 401

---

### Task 9.4: Test Coverage & Eksik Testler

**Tahmini Süre:** 2 saat

**Durum:** ⬜ BEKLEMEDE

**Yapılacaklar:**
- [ ] `pytest --cov=app --cov-report=term-missing tests/` çalıştır
- [ ] Coverage raporunu incele, eksik branch'leri tespit et
- [ ] Kritik eksik testleri yaz:
  - [ ] Her servis fonksiyonunun hata yolu (exception path) testleri
  - [ ] Her router endpoint için 422 validation hata testleri
  - [ ] Access token süresi dolma senaryosu
  - [ ] Refresh token expire senaryosu
  - [ ] `FactCheck` confidence_score 0-1 dışında → DB constraint hatası
  - [ ] `NewsAnalystAgent` timeout durumu
- [ ] `coverage >= %80` hedefine ulaş
- [ ] `pytest.ini`'ye coverage minimum eşiği ekle:
  ```ini
  [pytest]
  asyncio_mode = auto
  testpaths = tests
  addopts = --cov=app --cov-fail-under=80
  ```

---

### Task 9.5: API Dokümantasyonu

**Tahmini Süre:** 2 saat

**Durum:** ⬜ BEKLEMEDE

**Yapılacaklar:**
- [ ] `app/main.py`'deki FastAPI instance'ına metadata ekle:
  ```python
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
      ]
  )
  ```
- [ ] Her router ve endpoint'e `summary`, `description`, `response_model`, `status_code` parametreleri ekle
- [ ] Her Pydantic şemasına `json_schema_extra` ile örnek veriler ekle:
  ```python
  class RegisterRequest(BaseModel):
      ...
      model_config = ConfigDict(json_schema_extra={
          "example": {"email": "user@example.com", "password": "securepass123", "display_name": "John Doe"}
      })
  ```
- [ ] `GET http://localhost:8001/docs` açılıyor, tüm 25+ endpoint görünüyor mu doğrula

---

### Task 9.6: Final Review & Docker Clean Build

**Tahmini Süre:** 1.5 saat

**Durum:** ⬜ BEKLEMEDE

**Yapılacaklar:**
- [ ] `docker compose down -v` → `docker compose up -d --build` → sıfırdan clean build testi
- [ ] `alembic upgrade head` sorunsuz çalışıyor mu doğrula
- [ ] `pytest --cov=app tests/` → tüm testler geçiyor, coverage >= %80
- [ ] `GET /health` → `{"status": "ok", "database": "connected"}`
- [ ] Tüm `.env.example` anahtarlarının dokümante edildiğini doğrula
- [ ] `console.log` / `print` debug çıktılarını temizle
- [ ] `README.md`'ye backend kurulum adımları güncel mi kontrol et
- [ ] `requirements.txt`'deki tüm bağımlılıkların stabil versiyonlarda olduğunu doğrula

---

### 📊 Phase 8 Success Metrics

- [ ] E2E test senaryoları 4/4 geçiyor
- [ ] `pytest --cov=app tests/` → coverage >= %80
- [ ] Rate limiter: auth endpoint'lerine 11. istekte 429
- [ ] `hashed_password` ve `token_hash` hiçbir API response'unda görünmüyor
- [ ] `docker compose down -v && docker compose up -d --build` sorunsuz çalışıyor
- [ ] `GET http://localhost:8001/docs` → tüm endpoint'ler görünüyor

---

## 📅 Genel Proje Takvimi

| Phase | İçerik | Süre | Durum |
|-------|--------|------|-------|
| **Phase 1** | Infrastructure & Database | 1 hafta | ⬜ Beklemede |
| **Phase 2** | Authentication & User Management | 1.5 hafta | ⬜ Beklemede |
| **Phase 3** | CrewAI Core (News Crew + Fact Check Crew altyapısı) | 2 hafta | ⬜ Beklemede |
| **Phase 4** | News Feed & Cache System | 1 hafta | ⬜ Beklemede |
| **Phase 5** | Fact Check Engine (Fact Check Crew endpoint entegrasyonu) | 1 hafta | ⬜ Beklemede |
| **Phase 6** | User Features | 1 hafta | ⬜ Beklemede |
| **Phase 7** | Trending & Category Pages | 1 hafta | ⬜ Beklemede |
| **Phase 8** | Testing, Security & Polish | 1 hafta | ⬜ Beklemede |
| **TOPLAM** | | **~9.5 hafta** | |

---

## 🔗 Bağımlılık Haritası

```
Phase 1 (altyapı)
    └── Phase 2 (auth)
            └── Phase 3 (CrewAI core — News Crew + Fact Check Crew altyapısı)
                    ├── Phase 4 (news feed + FetchNewsTool/FetchTrendingTool)  → Phase 7 (trending)
                    ├── Phase 5 (fact check endpoint — Fact Check Crew tam entegrasyon)
                    └── Phase 6 (user features — preferences → agent davranışı)
                                    └── Phase 8 (testing & polish)
```

Phase 4, 5, 6 birbirinden bağımsız olduğundan paralel geliştirilebilir.

---

> *Proje boyunca her phase tamamlandığında `docker compose down -v && docker compose up -d --build` ile clean build testi yapılması önerilir.*
