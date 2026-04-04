import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Enum as SAEnum, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func

if TYPE_CHECKING:
	from app.models.conversation import Conversation
	from app.models.fact_check import FactCheck
	from app.models.news import SavedArticle


class Base(DeclarativeBase):
	pass


class User(Base):
	__tablename__ = "users"

	id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
	email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
	hashed_password: Mapped[str | None] = mapped_column(String(255), nullable=True)
	display_name: Mapped[str] = mapped_column(String(100), nullable=False)
	role: Mapped[str] = mapped_column(
		SAEnum("user", "admin", name="user_role"),
		nullable=False,
		default="user",
	)
	auth_provider: Mapped[str] = mapped_column(
		SAEnum("email", "google", "github", name="auth_provider"),
		nullable=False,
		default="email",
	)
	email_verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
	failed_login_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
	locked_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
	created_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		nullable=False,
		server_default=func.now(),
	)
	updated_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		nullable=False,
		server_default=func.now(),
		onupdate=func.now(),
	)

	preferences: Mapped["UserPreferences"] = relationship(back_populates="user", uselist=False)
	conversations: Mapped[list["Conversation"]] = relationship(back_populates="user")
	refresh_tokens: Mapped[list["RefreshToken"]] = relationship(back_populates="user")
	password_reset_tokens: Mapped[list["PasswordResetToken"]] = relationship(back_populates="user")
	email_verification_tokens: Mapped[list["EmailVerificationToken"]] = relationship(back_populates="user")
	fact_checks: Mapped[list["FactCheck"]] = relationship(back_populates="user")
	saved_articles: Mapped[list["SavedArticle"]] = relationship(back_populates="user")


class UserPreferences(Base):
	__tablename__ = "user_preferences"

	user_id: Mapped[uuid.UUID] = mapped_column(
		UUID(as_uuid=True),
		ForeignKey("users.id", ondelete="CASCADE"),
		primary_key=True,
	)
	language: Mapped[str] = mapped_column(String(10), nullable=False, default="Turkish")
	ai_tone: Mapped[str] = mapped_column(
		SAEnum("neutral", "formal", "casual", name="ai_tone"),
		nullable=False,
		default="neutral",
	)
	news_categories: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
	email_digest: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
	updated_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		nullable=False,
		server_default=func.now(),
		onupdate=func.now(),
	)

	user: Mapped["User"] = relationship(back_populates="preferences")


class RefreshToken(Base):
	__tablename__ = "refresh_tokens"

	id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
	user_id: Mapped[uuid.UUID] = mapped_column(
		UUID(as_uuid=True),
		ForeignKey("users.id", ondelete="CASCADE"),
		nullable=False,
	)
	token_hash: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
	expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
	revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
	created_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		nullable=False,
		server_default=func.now(),
	)

	user: Mapped["User"] = relationship(back_populates="refresh_tokens")


class PasswordResetToken(Base):
	__tablename__ = "password_reset_tokens"

	id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
	user_id: Mapped[uuid.UUID] = mapped_column(
		UUID(as_uuid=True),
		ForeignKey("users.id", ondelete="CASCADE"),
		nullable=False,
	)
	token_hash: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
	expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
	used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
	created_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		nullable=False,
		server_default=func.now(),
	)

	user: Mapped["User"] = relationship(back_populates="password_reset_tokens")


class EmailVerificationToken(Base):
	__tablename__ = "email_verification_tokens"

	id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
	user_id: Mapped[uuid.UUID] = mapped_column(
		UUID(as_uuid=True),
		ForeignKey("users.id", ondelete="CASCADE"),
		nullable=False,
	)
	token_hash: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
	expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
	verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
	created_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		nullable=False,
		server_default=func.now(),
	)

	user: Mapped["User"] = relationship(back_populates="email_verification_tokens")
