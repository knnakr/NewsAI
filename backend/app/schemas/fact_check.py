from datetime import datetime
import uuid

from pydantic import BaseModel, ConfigDict, Field


class FactCheckRequest(BaseModel):
	claim: str = Field(min_length=1, max_length=4000)

	model_config = ConfigDict(
		json_schema_extra={"example": {"claim": "The earth is flat"}}
	)


class FactCheckResponse(BaseModel):
	id: uuid.UUID
	user_id: uuid.UUID | None
	claim: str
	verdict: str
	explanation: str
	confidence_score: float
	sources: list[dict]
	created_at: datetime

	model_config = ConfigDict(
		from_attributes=True,
		json_schema_extra={
			"example": {
				"id": "55555555-5555-5555-5555-555555555555",
				"user_id": None,
				"claim": "The earth is flat",
				"verdict": "FALSE",
				"explanation": "The claim is false.",
				"confidence_score": 0.98,
				"sources": [{"url": "https://example.com/fact-check"}],
				"created_at": "2026-04-05T12:00:00Z",
			}
		},
	)
