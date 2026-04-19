"""
Tests for database models and schema integrity.
"""
import pytest
import uuid
from sqlalchemy import text
import asyncio


async def test_all_11_tables_exist(db):
    """Verify all 11 expected tables exist in database."""
    expected_tables = [
        "users", 
        "refresh_tokens", 
        "password_reset_tokens",
        "email_verification_tokens", 
        "user_preferences",
        "conversations", 
        "messages", 
        "agent_tool_calls",
        "fact_checks", 
        "saved_articles", 
        "article_cache"
    ]
    result = await db.execute(
        text("SELECT tablename FROM pg_tables WHERE schemaname='public'")
    )
    existing = {row[0] for row in result.fetchall()}
    for table in expected_tables:
        assert table in existing, f"Tablo eksik: {table}"


async def test_user_preferences_trigger_creates_row_on_user_insert(db):
    """Verify user_preferences row is automatically created when user is inserted."""
    await db.execute(text(
        "INSERT INTO users (id, email, display_name, hashed_password, role, auth_provider, failed_login_count) "
        "VALUES (gen_random_uuid(), 'trigger@test.com', 'Test User', 'hashed', 'user', 'email', 0)"
    ))
    await db.commit()
    
    result = await db.execute(
        text("SELECT COUNT(*) FROM user_preferences WHERE user_id = "
             "(SELECT id FROM users WHERE email = 'trigger@test.com')")
    )
    count = result.scalar()
    assert count == 1, "Trigger user_preferences satırı oluşturmadı"


async def test_user_preferences_trigger_sets_default_orchestrator(db):
    """Verify triggered user_preferences row defaults orchestrator to crewai."""
    await db.execute(text(
        "INSERT INTO users (id, email, display_name, hashed_password, role, auth_provider, failed_login_count) "
        "VALUES (gen_random_uuid(), 'orchestrator@test.com', 'Orchestrator User', 'hashed', 'user', 'email', 0)"
    ))
    await db.commit()

    result = await db.execute(
        text(
            "SELECT orchestrator FROM user_preferences WHERE user_id = "
            "(SELECT id FROM users WHERE email = 'orchestrator@test.com')"
        )
    )
    orchestrator = result.scalar()
    assert orchestrator == "crewai"


async def test_agent_tool_enum_values(db):
    """Verify agent_tool ENUM contains expected values."""
    expected_values = {
        "web_search", 
        "fetch_news_by_category", 
        "fetch_trending", 
        "fact_check_search", 
        "summarize_article"
    }
    result = await db.execute(
        text("SELECT unnest(enum_range(NULL::agent_tool))::text")
    )
    actual_values = {row[0] for row in result.fetchall()}
    assert actual_values == expected_values, f"Expected {expected_values}, got {actual_values}"


async def test_fact_verdict_enum_values(db):
    """Verify fact_verdict ENUM contains expected values."""
    expected_values = {"TRUE", "FALSE", "UNVERIFIED"}
    result = await db.execute(
        text("SELECT unnest(enum_range(NULL::fact_verdict))::text")
    )
    actual_values = {row[0] for row in result.fetchall()}
    assert actual_values == expected_values, f"Expected {expected_values}, got {actual_values}"


async def test_user_orchestrator_enum_values(db):
    """Verify user_orchestrator ENUM contains expected values."""
    expected_values = {"crewai", "langgraph"}
    result = await db.execute(
        text("SELECT unnest(enum_range(NULL::user_orchestrator))::text")
    )
    actual_values = {row[0] for row in result.fetchall()}
    assert actual_values == expected_values, f"Expected {expected_values}, got {actual_values}"


async def test_updated_at_trigger_fires_on_conversation_update(db):
    """Verify updated_at column changes when conversation is updated."""
    import asyncio
    
    # Create user first
    user_id = uuid.uuid4()
    await db.execute(text(
        "INSERT INTO users (id, email, display_name, hashed_password, role, auth_provider, failed_login_count) "
        "VALUES (:user_id, 'update@test.com', 'Update User', 'hashed', 'user', 'email', 0)"
    ), {"user_id": user_id})
    await db.commit()
    
    # Create conversation
    conv_id = uuid.uuid4()
    await db.execute(text(
        "INSERT INTO conversations (id, user_id, is_archived, is_deleted) "
        "VALUES (:conv_id, :user_id, false, false)"
    ), {"conv_id": conv_id, "user_id": user_id})
    await db.commit()
    
    # Get initial updated_at
    result1 = await db.execute(
        text("SELECT updated_at FROM conversations WHERE id = :conv_id"),
        {"conv_id": conv_id}
    )
    updated_at_1 = result1.scalar()
    
    # Wait a moment
    await asyncio.sleep(0.1)
    
    # Update conversation
    await db.execute(text(
        "UPDATE conversations SET title = 'Updated' WHERE id = :conv_id"
    ), {"conv_id": conv_id})
    await db.commit()
    
    # Get updated updated_at
    result2 = await db.execute(
        text("SELECT updated_at FROM conversations WHERE id = :conv_id"),
        {"conv_id": conv_id}
    )
    updated_at_2 = result2.scalar()
    
    # Verify they're different (trigger fired)
    assert updated_at_2 > updated_at_1, "Trigger did not update updated_at column"


async def test_unique_constraint_on_saved_articles(db):
    """Verify unique constraint on (user_id, article_url) in saved_articles."""
    from sqlalchemy.exc import IntegrityError
    
    # Create user first
    await db.execute(text(
        "INSERT INTO users (id, email, display_name, hashed_password, role, auth_provider, failed_login_count) "
        "VALUES (gen_random_uuid(), 'unique@test.com', 'Unique User', 'hashed', 'user', 'email', 0)"
    ))
    await db.commit()
    
    # Get user id
    user_result = await db.execute(
        text("SELECT id FROM users WHERE email = 'unique@test.com'")
    )
    user_id = user_result.scalar()
    
    # Insert first article
    await db.execute(text(
        f"INSERT INTO saved_articles (id, user_id, title, article_url, source_name, category) "
        f"VALUES (gen_random_uuid(), '{user_id}', 'Test Article', 'http://test.com/1', 'Test Source', 'technology')"
    ))
    await db.commit()
    
    # Try to insert duplicate
    with pytest.raises(IntegrityError):
        await db.execute(text(
            f"INSERT INTO saved_articles (id, user_id, title, article_url, source_name, category) "
            f"VALUES (gen_random_uuid(), '{user_id}', 'Another Title', 'http://test.com/1', 'Test Source', 'technology')"
        ))
        await db.commit()
