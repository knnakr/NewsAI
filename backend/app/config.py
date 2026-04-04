from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    
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


settings = Settings()
