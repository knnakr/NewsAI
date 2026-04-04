import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, Enum as SAEnum, ForeignKey, Numeric, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.models.user import Base

if TYPE_CHECKING:
	from app.models.user import User


class FactCheck(Base):
	__tablename__ = "fact_checks"
	__table_args__ = (
		CheckConstraint("confidence_score BETWEEN 0.0 AND 1.0", name="ck_fact_checks_confidence_score"),
	)

	id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
	user_id: Mapped[uuid.UUID | None] = mapped_column(
		UUID(as_uuid=True),
		ForeignKey("users.id", ondelete="SET NULL"),
		nullable=True,
		index=True,
	)
	claim: Mapped[str] = mapped_column(Text, nullable=False)
	verdict: Mapped[str] = mapped_column(
		SAEnum("TRUE", "FALSE", "UNVERIFIED", name="fact_verdict"),
		nullable=False,
	)
	explanation: Mapped[str] = mapped_column(Text, nullable=False)
	confidence_score: Mapped[float] = mapped_column(Numeric(3, 2), nullable=False)
	sources: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
	created_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		nullable=False,
		server_default=func.now(),
	)

	user: Mapped["User | None"] = relationship(back_populates="fact_checks")
