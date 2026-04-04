"""
Tests for authentication and security utilities.
"""
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

import pytest
from fastapi import HTTPException, Response
from pydantic import ValidationError
from sqlalchemy import select, text
from app.models.user import PasswordResetToken, User
from app.routers.auth import (
    ForgotPasswordRequest,
    ResetPasswordRequest,
    post_forgot_password,
    post_login,
    post_refresh,
    post_reset_password,
)
from app.utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
    hash_token,
)
from app.schemas.user import RegisterRequest, LoginRequest
from app.services.auth_service import register_user, login_user, refresh_tokens, logout_user


# ============================================================================
# Security Utility Tests
# ============================================================================

def test_hash_password_returns_different_from_plain():
    """Verify password is hashed, not stored as plain text."""
    hashed = hash_password("mysecret")
    assert hashed != "mysecret"


def test_verify_password_correct():
    """Verify correct password validates against hash."""
    hashed = hash_password("mysecret")
    assert verify_password("mysecret", hashed) is True


def test_verify_password_wrong():
    """Verify wrong password fails validation."""
    hashed = hash_password("mysecret")
    assert verify_password("wrong", hashed) is False


def test_create_access_token_returns_string():
    """Verify access token creation returns JWT string."""
    token = create_access_token("user-id-123")
    assert isinstance(token, str)
    assert len(token) > 0


def test_decode_access_token_returns_user_id():
    """Verify token decoding extracts user_id from payload."""
    token = create_access_token("user-id-123")
    payload = decode_access_token(token)
    assert payload["sub"] == "user-id-123"


def test_decode_invalid_token_raises():
    """Verify invalid token raises exception."""
    with pytest.raises(Exception):
        decode_access_token("invalid.token.here")


def test_hash_token_is_deterministic():
    """Verify token hash is consistent for same input."""
    assert hash_token("abc") == hash_token("abc")


def test_hash_token_different_inputs():
    """Verify different inputs produce different hashes."""
    assert hash_token("abc") != hash_token("xyz")


# ============================================================================
# Schema Validation Tests
# ============================================================================

def test_register_request_rejects_short_password():
    """Verify RegisterRequest rejects passwords shorter than 8 characters."""
    with pytest.raises(ValidationError):
        RegisterRequest(email="a@b.com", password="short", display_name="Test")


def test_register_request_rejects_invalid_email():
    """Verify RegisterRequest rejects invalid email addresses."""
    with pytest.raises(ValidationError):
        RegisterRequest(email="not-an-email", password="validpass123", display_name="Test")


def test_register_request_rejects_short_display_name():
    """Verify RegisterRequest rejects display names shorter than 2 characters."""
    with pytest.raises(ValidationError):
        RegisterRequest(email="a@b.com", password="validpass123", display_name="T")


def test_register_request_valid():
    """Verify RegisterRequest accepts valid input."""
    req = RegisterRequest(email="a@b.com", password="validpass123", display_name="Test User")
    assert req.email == "a@b.com"
    assert req.password == "validpass123"
    assert req.display_name == "Test User"


def test_login_request_requires_email_and_password():
    """Verify LoginRequest requires both email and password."""
    with pytest.raises(ValidationError):
        LoginRequest(email="a@b.com")
    
    with pytest.raises(ValidationError):
        LoginRequest(password="password123")


# ============================================================================
# Auth Service Tests
# ============================================================================

@pytest.mark.asyncio
async def test_register_creates_user_in_db(db):
    """Verify register_user creates a user and stores hashed password."""
    user = await register_user("test@example.com", "password123", "Test User", db)
    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.hashed_password != "password123"


@pytest.mark.asyncio
async def test_register_creates_user_preferences(db):
    """Verify user_preferences row is auto-created on registration."""
    await register_user("pref@example.com", "password123", "Pref User", db)
    result = await db.execute(
        text(
            "SELECT COUNT(*) FROM user_preferences WHERE user_id = "
            "(SELECT id FROM users WHERE email = 'pref@example.com')"
        )
    )
    assert result.scalar() == 1


@pytest.mark.asyncio
async def test_register_duplicate_email_raises_409(db):
    """Verify duplicate registration fails with HTTP 409."""
    await register_user("dup@example.com", "password123", "User", db)
    with pytest.raises(HTTPException) as exc:
        await register_user("dup@example.com", "password123", "User2", db)
    assert exc.value.status_code == 409


@pytest.mark.asyncio
async def test_login_valid_credentials_returns_tokens(db):
    """Verify successful login returns access and refresh tokens."""
    await register_user("login@example.com", "password123", "Login User", db)
    access_token, refresh_token = await login_user("login@example.com", "password123", db)
    assert isinstance(access_token, str)
    assert isinstance(refresh_token, str)


@pytest.mark.asyncio
async def test_login_wrong_password_returns_401(db):
    """Verify login fails with 401 for wrong password."""
    await register_user("fail@example.com", "password123", "Fail User", db)
    with pytest.raises(HTTPException) as exc:
        await login_user("fail@example.com", "wrongpassword", db)
    assert exc.value.status_code == 401


@pytest.mark.asyncio
async def test_brute_force_locks_account_after_5_attempts(db):
    """Verify account is temporarily locked after 5 failed attempts."""
    await register_user("brute@example.com", "password123", "Brute User", db)
    for _ in range(5):
        try:
            await login_user("brute@example.com", "wrong", db)
        except HTTPException:
            pass

    with pytest.raises(HTTPException) as exc:
        await login_user("brute@example.com", "password123", db)
    assert exc.value.status_code == 423


@pytest.mark.asyncio
async def test_refresh_tokens_rotates_refresh_token(db):
    """Verify refresh endpoint rotates token and returns new pair."""
    await register_user("refresh@example.com", "password123", "Refresh User", db)
    _, old_refresh = await login_user("refresh@example.com", "password123", db)
    new_access, new_refresh = await refresh_tokens(old_refresh, db)
    assert new_refresh != old_refresh
    assert isinstance(new_access, str)


@pytest.mark.asyncio
async def test_refresh_with_revoked_token_raises_401(db):
    """Verify revoked refresh token cannot be used again."""
    await register_user("revoke@example.com", "password123", "Revoke User", db)
    _, refresh = await login_user("revoke@example.com", "password123", db)
    await logout_user(refresh, db)
    with pytest.raises(HTTPException) as exc:
        await refresh_tokens(refresh, db)
    assert exc.value.status_code == 401


# ============================================================================
# Auth Router Tests
# ============================================================================

@pytest.mark.asyncio
async def test_post_register_returns_201(client):
    response = await client.post(
        "/auth/register",
        json={
            "email": "new@example.com",
            "password": "password123",
            "display_name": "New User",
        },
    )
    assert response.status_code == 201
    assert "id" in response.json()
    assert "hashed_password" not in response.json()


@pytest.mark.asyncio
async def test_post_register_invalid_body_returns_422(client):
    response = await client.post("/auth/register", json={"email": "bad"})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_post_login_returns_access_token(client):
    await client.post(
        "/auth/register",
        json={
            "email": "login2@example.com",
            "password": "password123",
            "display_name": "Login",
        },
    )
    response = await client.post(
        "/auth/login",
        json={"email": "login2@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_post_login_sets_refresh_cookie(client):
    await client.post(
        "/auth/register",
        json={
            "email": "cookie@example.com",
            "password": "password123",
            "display_name": "Cookie",
        },
    )
    response = await client.post(
        "/auth/login",
        json={"email": "cookie@example.com", "password": "password123"},
    )
    assert "refresh_token" in response.cookies


@pytest.mark.asyncio
async def test_post_refresh_rotates_token(client):
    await client.post(
        "/auth/register",
        json={
            "email": "rot@example.com",
            "password": "password123",
            "display_name": "Rot",
        },
    )
    login_resp = await client.post(
        "/auth/login",
        json={"email": "rot@example.com", "password": "password123"},
    )
    old_cookie = login_resp.cookies.get("refresh_token")
    client.cookies.set("refresh_token", old_cookie)
    refresh_resp = await client.post("/auth/refresh")
    assert refresh_resp.status_code == 200
    assert refresh_resp.cookies.get("refresh_token") != old_cookie


@pytest.mark.asyncio
async def test_post_logout_revokes_refresh_token(client):
    await client.post(
        "/auth/register",
        json={
            "email": "logout@example.com",
            "password": "password123",
            "display_name": "Logout",
        },
    )
    login_resp = await client.post(
        "/auth/login",
        json={"email": "logout@example.com", "password": "password123"},
    )
    cookie_value = login_resp.cookies.get("refresh_token")
    client.cookies.set("refresh_token", cookie_value)
    await client.post("/auth/logout")
    refresh_resp = await client.post("/auth/refresh")
    assert refresh_resp.status_code == 401


@pytest.mark.asyncio
async def test_register_duplicate_email_returns_409(client):
    await client.post(
        "/auth/register",
        json={
            "email": "dup2@example.com",
            "password": "password123",
            "display_name": "Dup",
        },
    )
    response = await client.post(
        "/auth/register",
        json={
            "email": "dup2@example.com",
            "password": "password123",
            "display_name": "Dup2",
        },
    )
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_post_refresh_without_cookie_returns_401(client):
    response = await client.post("/auth/refresh")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_post_logout_without_cookie_returns_200(client):
    response = await client.post("/auth/logout")
    assert response.status_code == 200
    assert response.json()["detail"] == "Cikis yapildi"


@pytest.mark.asyncio
async def test_post_forgot_password_unknown_email_returns_generic_success(client):
    response = await client.post("/auth/forgot-password", json={"email": "unknown@example.com"})
    assert response.status_code == 200
    assert "detail" in response.json()


@pytest.mark.asyncio
async def test_post_forgot_password_existing_email_creates_reset_token(client, db):
    email = "forgot@example.com"
    await register_user(email, "password123", "Forgot User", db)

    response = await client.post("/auth/forgot-password", json={"email": email})
    assert response.status_code == 200

    user_result = await db.execute(select(User).where(User.email == email))
    user = user_result.scalar_one()
    token_result = await db.execute(
        select(PasswordResetToken).where(PasswordResetToken.user_id == user.id)
    )
    assert token_result.scalar_one_or_none() is not None


@pytest.mark.asyncio
async def test_post_reset_password_invalid_token_returns_400(client):
    response = await client.post(
        "/auth/reset-password",
        json={"token": "invalid-token", "password": "newpassword123"},
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_post_reset_password_expired_token_returns_400(client, db):
    user = await register_user("expired-reset@example.com", "password123", "Expired Reset", db)
    expired_plain = "expired-reset-token"
    db.add(
        PasswordResetToken(
            user_id=user.id,
            token_hash=hash_token(expired_plain),
            expires_at=datetime.now(timezone.utc) - timedelta(minutes=1),
        )
    )
    await db.commit()

    response = await client.post(
        "/auth/reset-password",
        json={"token": expired_plain, "password": "newpassword123"},
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_post_reset_password_valid_token_updates_password_and_marks_used(client, db):
    user = await register_user("reset@example.com", "password123", "Reset User", db)
    reset_plain = "valid-reset-token"
    token_hash_value = hash_token(reset_plain)

    db.add(
        PasswordResetToken(
            user_id=user.id,
            token_hash=token_hash_value,
            expires_at=datetime.now(timezone.utc) + timedelta(minutes=30),
        )
    )
    await db.commit()

    response = await client.post(
        "/auth/reset-password",
        json={"token": reset_plain, "password": "newpassword123"},
    )
    assert response.status_code == 200

    user_result = await db.execute(select(User).where(User.id == user.id))
    updated_user = user_result.scalar_one()
    assert verify_password("newpassword123", updated_user.hashed_password)

    token_result = await db.execute(
        select(PasswordResetToken).where(PasswordResetToken.token_hash == token_hash_value)
    )
    used_token = token_result.scalar_one()
    assert used_token.used_at is not None


@pytest.mark.asyncio
async def test_post_login_unit_sets_cookie_and_returns_token(monkeypatch):
    async def fake_login_user(email: str, password: str, db):
        return "access-token", "refresh-token"

    monkeypatch.setattr("app.routers.auth.login_user", fake_login_user)
    response = Response()
    payload = LoginRequest(email="unit-login@example.com", password="password123")

    result = await post_login(payload, response, db=None)

    assert result.access_token == "access-token"
    assert "refresh_token=refresh-token" in response.headers.get("set-cookie", "")


@pytest.mark.asyncio
async def test_post_refresh_unit_sets_cookie_and_returns_token(monkeypatch):
    async def fake_refresh_tokens(old_token: str, db):
        return "new-access-token", "new-refresh-token"

    monkeypatch.setattr("app.routers.auth.refresh_tokens", fake_refresh_tokens)
    response = Response()

    result = await post_refresh(response, refresh_token="old-refresh-token", db=None)

    assert result.access_token == "new-access-token"
    assert "refresh_token=new-refresh-token" in response.headers.get("set-cookie", "")


@pytest.mark.asyncio
async def test_post_forgot_password_unit_user_exists_creates_token(monkeypatch):
    fake_user = SimpleNamespace(id="user-id")
    execute_result = SimpleNamespace(scalar_one_or_none=lambda: fake_user)

    class FakeDB:
        def __init__(self):
            self.added = []
            self.committed = False

        async def execute(self, *_args, **_kwargs):
            return execute_result

        def add(self, obj):
            self.added.append(obj)

        async def commit(self):
            self.committed = True

    db = FakeDB()
    payload = ForgotPasswordRequest(email="exists@example.com")

    result = await post_forgot_password(payload, db=db)

    assert result["detail"]
    assert len(db.added) == 1
    assert db.committed is True


@pytest.mark.asyncio
async def test_post_reset_password_unit_success_updates_user_and_marks_token(monkeypatch):
    now = datetime.now(timezone.utc)
    token_obj = SimpleNamespace(user_id="user-id", used_at=None)
    user_obj = SimpleNamespace(hashed_password="old-hash")

    first_result = SimpleNamespace(scalar_one_or_none=lambda: token_obj)
    second_result = SimpleNamespace(scalar_one_or_none=lambda: user_obj)

    class FakeDB:
        def __init__(self):
            self._calls = 0
            self.committed = False

        async def execute(self, *_args, **_kwargs):
            self._calls += 1
            if self._calls == 1:
                return first_result
            return second_result

        async def commit(self):
            self.committed = True

    monkeypatch.setattr("app.routers.auth.datetime", SimpleNamespace(now=lambda *_args, **_kwargs: now))
    db = FakeDB()
    payload = ResetPasswordRequest(token="unit-token", password="newpassword123")

    result = await post_reset_password(payload, db=db)

    assert result["detail"] == "Sifre basariyla guncellendi"
    assert verify_password("newpassword123", user_obj.hashed_password)
    assert token_obj.used_at == now
    assert db.committed is True


# ============================================================================
# User Router Tests
# ============================================================================

@pytest.fixture
async def auth_headers(client) -> dict[str, str]:
    await client.post(
        "/auth/register",
        json={
            "email": "me@example.com",
            "password": "password123",
            "display_name": "Me User",
        },
    )
    login_resp = await client.post(
        "/auth/login",
        json={"email": "me@example.com", "password": "password123"},
    )
    token = login_resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_get_me_returns_current_user(client, auth_headers):
    response = await client.get("/users/me", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["email"] == "me@example.com"


@pytest.mark.asyncio
async def test_get_me_without_token_returns_401(client):
    response = await client.get("/users/me")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_me_with_invalid_token_returns_401(client):
    response = await client.get("/users/me", headers={"Authorization": "Bearer invalid.token.here"})
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_me_response_excludes_hashed_password(client, auth_headers):
    response = await client.get("/users/me", headers=auth_headers)
    assert "hashed_password" not in response.json()


@pytest.mark.asyncio
async def test_patch_me_updates_display_name(client, auth_headers):
    response = await client.patch("/users/me", json={"display_name": "Updated Name"}, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["display_name"] == "Updated Name"


@pytest.mark.asyncio
async def test_get_preferences_returns_defaults(client, auth_headers):
    response = await client.get("/users/me/preferences", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["language"] == "Turkish"
    assert data["ai_tone"] == "neutral"


@pytest.mark.asyncio
async def test_patch_preferences_updates_language(client, auth_headers):
    response = await client.patch("/users/me/preferences", json={"language": "English"}, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["language"] == "English"


@pytest.mark.asyncio
async def test_patch_preferences_invalid_ai_tone_returns_422(client, auth_headers):
    response = await client.patch("/users/me/preferences", json={"ai_tone": "aggressive"}, headers=auth_headers)
    assert response.status_code == 422


# ============================================================================
# Global Exception Handler Tests (Task 3.2)
# ============================================================================

@pytest.mark.asyncio
async def test_not_found_route_returns_404(client):
    response = await client.get("/nonexistent-route-xyz")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_validation_error_returns_422_with_detail(client):
    response = await client.post("/auth/register", json={"email": "bad-email"})
    assert response.status_code == 422
    assert "detail" in response.json()


@pytest.mark.asyncio
async def test_http_exception_returns_json_with_detail(client):
    response = await client.get("/users/me")
    assert response.status_code in (401, 403)
    assert "detail" in response.json()
