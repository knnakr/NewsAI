from datetime import datetime
import uuid

from pydantic import BaseModel, ConfigDict, Field


class FactCheckRequest(BaseModel):
	claim: str = Field(min_length=1, max_length=4000)


class FactCheckResponse(BaseModel):
	id: uuid.UUID
	user_id: uuid.UUID | None
	claim: str
	verdict: str
	explanation: str
	confidence_score: float
	sources: list[dict]
	created_at: datetime

	model_config = ConfigDict(from_attributes=True)
