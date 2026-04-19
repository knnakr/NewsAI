"""
Pytest configuration and shared fixtures for backend tests.
"""
import pytest
import asyncio
import os
from urllib.parse import urlparse, urlunparse
from httpx import AsyncClient, ASGITransport
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.main import app
from app.database import get_db
from app.models import Base


def _get_test_database_url() -> str:
    """
    Get test database URL from environment.
    Uses DATABASE_URL from .env and replaces database name with newsai_test.
    """
    database_url = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://newsai:newsai@localhost:5433/newsai"
    )
    
    # Parse URL and replace database name
    parsed = urlparse(database_url)
    test_path = "/newsai_test"
    
    # Reconstruct URL with test database
    test_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        test_path,
        "",
        "",
        ""
    ))
    
    return test_url


TEST_DATABASE_URL = _get_test_database_url()


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


async def _create_triggers(conn):
    """Create database triggers for test database."""
    # User preferences trigger
    await conn.exec_driver_sql("""
    CREATE OR REPLACE FUNCTION create_user_preferences()
    RETURNS TRIGGER AS $$
    BEGIN
        INSERT INTO user_preferences (
            user_id,
            language,
            ai_tone,
            orchestrator,
            news_categories,
            email_digest
        ) VALUES (
            NEW.id,
            'Turkish',
            'neutral',
            'crewai',
            '["world", "technology", "sports"]'::jsonb,
            FALSE
        );
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """)
    
    await conn.exec_driver_sql("""
    DROP TRIGGER IF EXISTS user_preferences_on_insert ON users;
    """)
    
    await conn.exec_driver_sql("""
    CREATE TRIGGER user_preferences_on_insert
    AFTER INSERT ON users
    FOR EACH ROW
    EXECUTE FUNCTION create_user_preferences();
    """)
    
    # Conversation timestamp trigger
    await conn.exec_driver_sql("""
    CREATE OR REPLACE FUNCTION update_conversation_timestamp()
    RETURNS TRIGGER AS $$
    BEGIN
        NEW.updated_at = NOW();
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """)
    
    await conn.exec_driver_sql("""
    DROP TRIGGER IF EXISTS conversation_updated_at_on_update ON conversations;
    """)
    
    await conn.exec_driver_sql("""
    CREATE TRIGGER conversation_updated_at_on_update
    BEFORE UPDATE ON conversations
    FOR EACH ROW
    EXECUTE FUNCTION update_conversation_timestamp();
    """)


@pytest.fixture(scope="function")
async def db():
    """
    Create isolated test database.
    Creates all tables before test, drops all after.
    """
    engine = create_async_engine(TEST_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        # Create triggers after tables are created
        await _create_triggers(conn)
    
    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    async with session_factory() as session:
        yield session
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture(scope="function")
async def client(db):
    """
    Create FastAPI test client with overridden database dependency.
    """
    app.dependency_overrides[get_db] = lambda: db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
