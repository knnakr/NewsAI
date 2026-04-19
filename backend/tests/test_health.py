"""
Tests for health check endpoint.
"""
import pytest

from app.main import app


async def test_docs_endpoint_returns_swagger_ui(client):
    response = await client.get("/docs")

    assert response.status_code == 200
    assert "swagger" in response.text.lower()


async def test_openapi_metadata_matches_roadmap(client):
    openapi_schema = app.openapi()

    assert openapi_schema["info"]["title"] == "News AI API"
    assert openapi_schema["info"]["version"] == "1.0.0"
    assert openapi_schema["info"]["description"] == (
        "AI-powered news platform with CrewAI agents (News Crew + Fact Check Crew)"
    )

    tags = {tag["name"]: tag["description"] for tag in openapi_schema["tags"]}
    assert tags == {
        "auth": "Kayıt, giriş, token yönetimi",
        "users": "Kullanıcı profili ve tercihler",
        "conversations": "Chat konuşmaları ve News Crew",
        "fact-check": "Fact Check Crew",
        "news": "Haber feed, trending, kategori, kayıt",
    }


async def test_openapi_operations_include_summary_description_and_responses(client):
    openapi_schema = app.openapi()
    missing = []

    for path, methods in openapi_schema["paths"].items():
        if path in {"/openapi.json", "/docs", "/redoc"}:
            continue
        for method, operation in methods.items():
            if method.lower() not in {"get", "post", "put", "patch", "delete"}:
                continue
            if not operation.get("summary") or not operation.get("description"):
                missing.append(f"{method.upper()} {path}")
            if not operation.get("responses"):
                missing.append(f"{method.upper()} {path} missing responses")

    assert missing == [], f"OpenAPI metadata missing: {missing}"


async def test_openapi_schemas_include_examples(client):
    openapi_schema = app.openapi()
    schemas = openapi_schema["components"]["schemas"]

    expected_examples = {
        "RegisterRequest": {
            "email": "user@example.com",
            "password": "securepass123",
            "display_name": "John Doe",
        },
        "LoginRequest": {
            "email": "user@example.com",
            "password": "securepass123",
        },
        "TokenResponse": {
            "access_token": "eyJhbGciOi...",
            "token_type": "bearer",
            "expires_in": 900,
        },
        "UserResponse": {
            "id": "11111111-1111-1111-1111-111111111111",
            "email": "user@example.com",
            "display_name": "John Doe",
            "role": "user",
            "created_at": "2026-04-05T12:00:00Z",
        },
        "UpdateUserRequest": {"display_name": "Updated Name"},
        "UserPreferencesResponse": {
            "language": "Turkish",
            "ai_tone": "neutral",
            "orchestrator": "crewai",
            "news_categories": ["world", "technology"],
            "email_digest": False,
        },
        "UpdatePreferencesRequest": {
            "language": "English",
            "ai_tone": "formal",
            "orchestrator": "langgraph",
            "news_categories": ["technology"],
            "email_digest": True,
        },
        "ConversationCreate": {"title": "Morning news"},
        "ConversationUpdate": {"title": "Updated title"},
        "ConversationResponse": {
            "id": "22222222-2222-2222-2222-222222222222",
            "title": "Morning news",
            "created_at": "2026-04-05T12:00:00Z",
            "updated_at": "2026-04-05T12:00:00Z",
        },
        "MessageCreate": {"content": "What is trending today?"},
        "MessageResponse": {
            "id": "33333333-3333-3333-3333-333333333333",
            "role": "assistant",
            "content": "Here is the latest update.",
            "sources": [{"url": "https://example.com"}],
            "created_at": "2026-04-05T12:00:00Z",
        },
        "ConversationDetailResponse": {
            "id": "22222222-2222-2222-2222-222222222222",
            "title": "Morning news",
            "created_at": "2026-04-05T12:00:00Z",
            "updated_at": "2026-04-05T12:00:00Z",
            "messages": [],
        },
        "ArticleResponse": {
            "title": "Example article",
            "url": "https://example.com/article",
            "source_name": "Example Source",
            "published_at": "2026-04-05T12:00:00Z",
            "ai_summary": "Short summary.",
            "category": "technology",
        },
        "SaveArticleRequest": {
            "title": "Example article",
            "url": "https://example.com/article",
            "source_name": "Example Source",
            "published_at": "2026-04-05T12:00:00Z",
            "category": "technology",
        },
        "SavedArticleResponse": {
            "id": "44444444-4444-4444-4444-444444444444",
            "title": "Example article",
            "url": "https://example.com/article",
            "source_name": "Example Source",
            "published_at": "2026-04-05T12:00:00Z",
            "ai_summary": "Short summary.",
            "category": "technology",
            "saved_at": "2026-04-05T12:00:00Z",
        },
        "FactCheckRequest": {"claim": "The earth is flat"},
        "FactCheckResponse": {
            "id": "55555555-5555-5555-5555-555555555555",
            "claim": "The earth is flat",
            "verdict": "FALSE",
            "explanation": "The claim is false.",
            "confidence_score": 0.98,
            "sources": [{"url": "https://example.com/fact-check"}],
            "created_at": "2026-04-05T12:00:00Z",
        },
    }

    for schema_name, expected_example in expected_examples.items():
        assert schemas[schema_name]["example"] == expected_example


async def test_health_endpoint_returns_200(client):
    """Health endpoint should return 200 status code."""
    response = await client.get("/health")
    assert response.status_code == 200


async def test_health_endpoint_returns_correct_schema(client):
    """Health endpoint response should contain required fields."""
    response = await client.get("/health")
    data = response.json()
    assert "status" in data
    assert "database" in data


async def test_health_endpoint_db_connected(client):
    """Health endpoint should report database as connected."""
    response = await client.get("/health")
    assert response.json()["database"] == "connected"


async def test_health_endpoint_returns_ok_status(client):
    """Health endpoint should return ok status."""
    response = await client.get("/health")
    assert response.json()["status"] == "ok"
