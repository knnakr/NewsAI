from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
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

    GROQ_MODEL_DEFAULT: str = "groq/meta-llama/llama-4-scout-17b-16e-instruct"
    GROQ_MODEL_REASONING: str = "groq/meta-llama/llama-4-scout-17b-16e-instruct"
    ENABLE_LANGGRAPH: bool = False
    LANGGRAPH_RECURSION_LIMIT: int = 25
    LANGSMITH_TRACING: bool = False
    LANGSMITH_API_KEY: str | None = None
    LANGSMITH_PROJECT: str = "newsai-langgraph"
    LANGSMITH_ENDPOINT: str = "https://api.smith.langchain.com"

    ARTICLE_CACHE_TTL_HOURS: int = 6

    @field_validator("JWT_SECRET")
    @classmethod
    def validate_jwt_secret_min_length(cls, value: str) -> str:
        if len(value) < 32:
            raise ValueError("JWT_SECRET must be at least 32 characters long")
        return value


settings = Settings()
