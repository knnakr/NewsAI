import uuid
import asyncio
import json

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.crew.utils import clear_tool_call_context
from app.models.conversation import Conversation, Message
from app.models.user import User, UserPreferences
from app.schemas.conversation import (
	ConversationCreate,
	ConversationDetailResponse,
	ConversationResponse,
	ConversationUpdate,
	MessageCreate,
	MessageResponse,
)
from app.services.crew_service import run_chat_crew

router = APIRouter(prefix="/conversations", tags=["conversations"])


def _format_sse(data: dict) -> str:
	return f"data: {json.dumps(data, ensure_ascii=False)}\n\n"


def _extract_step_token(payload) -> str | None:
	for attribute in ("output", "result", "text"):
		value = getattr(payload, attribute, None)
		if isinstance(value, str) and value.strip():
			return value
	return None


async def _get_user_conversation_or_raise(
	conversation_id: uuid.UUID,
	current_user_id: uuid.UUID,
	db: AsyncSession,
) -> Conversation:
	result = await db.execute(select(Conversation).where(Conversation.id == conversation_id))
	conversation = result.scalar_one_or_none()
	if conversation is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Konuşma bulunamadı")
	if conversation.user_id != current_user_id:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Bu konuşmaya erişim yetkiniz yok")
	if conversation.is_deleted:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Konuşma bulunamadı")
	return conversation


@router.get(
	"",
	response_model=list[ConversationResponse],
	status_code=status.HTTP_200_OK,
	summary="List conversations",
	description="Giriş yapmış kullanıcının aktif konuşmalarını listeler.",
)
async def list_conversations(
	current_user: User = Depends(get_current_user),
	db: AsyncSession = Depends(get_db),
):
	result = await db.execute(
		select(Conversation)
		.where(Conversation.user_id == current_user.id, Conversation.is_deleted.is_(False))
		.order_by(Conversation.updated_at.desc())
	)
	return list(result.scalars().all())


@router.post(
	"",
	response_model=ConversationResponse,
	status_code=status.HTTP_201_CREATED,
	summary="Create conversation",
	description="Yeni bir konuşma oluşturur.",
)
async def create_conversation(
	payload: ConversationCreate | None = None,
	current_user: User = Depends(get_current_user),
	db: AsyncSession = Depends(get_db),
):
	conversation = Conversation(user_id=current_user.id, title=payload.title if payload else None)
	db.add(conversation)
	await db.commit()
	await db.refresh(conversation)
	return conversation


@router.get(
	"/{conversation_id}",
	response_model=ConversationDetailResponse,
	status_code=status.HTTP_200_OK,
	summary="Get conversation",
	description="Bir konuşmayı ve tüm mesajlarını döndürür.",
)
async def get_conversation(
	conversation_id: uuid.UUID,
	current_user: User = Depends(get_current_user),
	db: AsyncSession = Depends(get_db),
):
	conversation = await _get_user_conversation_or_raise(conversation_id, current_user.id, db)
	messages_result = await db.execute(
		select(Message)
		.where(Message.conversation_id == conversation.id)
		.order_by(Message.created_at.asc())
	)
	messages = list(messages_result.scalars().all())
	return ConversationDetailResponse(
		id=conversation.id,
		title=conversation.title,
		created_at=conversation.created_at,
		updated_at=conversation.updated_at,
		messages=messages,
	)


@router.patch(
	"/{conversation_id}",
	response_model=ConversationResponse,
	status_code=status.HTTP_200_OK,
	summary="Update conversation",
	description="Konuşma başlığını günceller.",
)
async def update_conversation(
	conversation_id: uuid.UUID,
	payload: ConversationUpdate,
	current_user: User = Depends(get_current_user),
	db: AsyncSession = Depends(get_db),
):
	conversation = await _get_user_conversation_or_raise(conversation_id, current_user.id, db)
	conversation.title = payload.title
	await db.commit()
	await db.refresh(conversation)
	return conversation


@router.delete(
	"/{conversation_id}",
	status_code=status.HTTP_200_OK,
	summary="Delete conversation",
	description="Konuşmayı soft delete ile siler.",
)
async def delete_conversation(
	conversation_id: uuid.UUID,
	current_user: User = Depends(get_current_user),
	db: AsyncSession = Depends(get_db),
):
	conversation = await _get_user_conversation_or_raise(conversation_id, current_user.id, db)
	conversation.is_deleted = True
	await db.commit()
	return {"detail": "Konuşma silindi"}


@router.post(
	"/{conversation_id}/archive",
	response_model=ConversationResponse,
	status_code=status.HTTP_200_OK,
	summary="Archive conversation",
	description="Konuşmayı arşivlenmiş olarak işaretler.",
)
async def archive_conversation(
	conversation_id: uuid.UUID,
	current_user: User = Depends(get_current_user),
	db: AsyncSession = Depends(get_db),
):
	conversation = await _get_user_conversation_or_raise(conversation_id, current_user.id, db)
	conversation.is_archived = True
	await db.commit()
	await db.refresh(conversation)
	return conversation


@router.post(
	"/{conversation_id}/messages",
	response_model=MessageResponse,
	status_code=status.HTTP_200_OK,
	summary="Send message",
	description="Kullanıcı mesajını kaydeder, News Crew'u çalıştırır ve asistandan yanıt döndürür.",
)
async def send_message(
	conversation_id: uuid.UUID,
	message_body: MessageCreate,
	current_user: User = Depends(get_current_user),
	db: AsyncSession = Depends(get_db),
):
	conversation = await _get_user_conversation_or_raise(conversation_id, current_user.id, db)

	user_message = Message(
		conversation_id=conversation.id,
		role="user",
		content=message_body.content,
	)
	db.add(user_message)
	await db.flush()

	history_result = await db.execute(
		select(Message)
		.where(Message.conversation_id == conversation.id)
		.order_by(Message.created_at.desc())
		.limit(20)
	)
	history_messages = list(history_result.scalars().all())
	history_messages.reverse()
	conversation_history = [{"role": m.role, "content": m.content} for m in history_messages]

	prefs = await db.get(UserPreferences, current_user.id)
	user_preferences = {
		"language": prefs.language if prefs else "Turkish",
		"ai_tone": prefs.ai_tone if prefs else "neutral",
	}

	try:
		assistant_text, sources = await run_chat_crew(
			user_message=message_body.content,
			conversation_history=conversation_history,
			user_preferences=user_preferences,
			db=db,
			message_id=user_message.id,
		)
	except Exception as exc:
		error_text = str(exc).lower()
		if "rate_limit_exceeded" in error_text or "ratelimiterror" in error_text:
			raise HTTPException(
				status_code=status.HTTP_429_TOO_MANY_REQUESTS,
				detail="AI servisinde yoğunluk var. Lütfen birkaç saniye sonra tekrar deneyin.",
			) from exc
		raise HTTPException(
			status_code=status.HTTP_502_BAD_GATEWAY,
			detail=f"AI servis hatası: {exc}",
		) from exc

	assistant_message = Message(
		conversation_id=conversation.id,
		role="assistant",
		content=assistant_text,
		sources=sources,
	)
	db.add(assistant_message)

	if conversation.title is None:
		conversation.title = message_body.content[:80].strip()

	await db.commit()
	await db.refresh(assistant_message)
	return assistant_message


@router.post(
	"/{conversation_id}/messages/stream",
	status_code=status.HTTP_200_OK,
	summary="Send streaming message",
	description="Kullanıcı mesajını kaydeder ve CrewAI ara çıktıları ile SSE stream döndürür.",
)
async def send_message_stream(
	conversation_id: uuid.UUID,
	message_body: MessageCreate,
	current_user: User = Depends(get_current_user),
	db: AsyncSession = Depends(get_db),
):
	conversation = await _get_user_conversation_or_raise(conversation_id, current_user.id, db)

	user_message = Message(
		conversation_id=conversation.id,
		role="user",
		content=message_body.content,
	)
	db.add(user_message)
	await db.flush()

	history_result = await db.execute(
		select(Message)
		.where(Message.conversation_id == conversation.id)
		.order_by(Message.created_at.desc())
		.limit(20)
	)
	history_messages = list(history_result.scalars().all())
	history_messages.reverse()
	conversation_history = [{"role": m.role, "content": m.content} for m in history_messages]

	prefs = await db.get(UserPreferences, current_user.id)
	user_preferences = {
		"language": prefs.language if prefs else "Turkish",
		"ai_tone": prefs.ai_tone if prefs else "neutral",
	}

	event_queue: asyncio.Queue[dict] = asyncio.Queue()
	result_holder: dict[str, object] = {}

	def step_callback(payload) -> None:
		token = _extract_step_token(payload)
		if token:
			event_queue.put_nowait({"event": "token", "token": token})

	async def run_crew() -> None:
		try:
			assistant_text, sources = await run_chat_crew(
				user_message=message_body.content,
				conversation_history=conversation_history,
				user_preferences=user_preferences,
				db=db,
				message_id=user_message.id,
				step_callback=step_callback,
				stream_queue=event_queue,
			)
			result_holder["assistant_text"] = assistant_text
			result_holder["sources"] = sources
			event_queue.put_nowait({"event": "crew_completed"})
		except Exception as exc:  # pragma: no cover - streaming error path is defensive
			result_holder["error"] = exc
			event_queue.put_nowait({"event": "crew_failed", "detail": str(exc)})

	task = asyncio.create_task(run_crew())

	async def event_stream():
		try:
			while True:
				event = await event_queue.get()
				if event["event"] == "crew_completed":
					break
				if event["event"] == "crew_failed":
					yield _format_sse({"event": "error", "detail": event["detail"]})
					return
				yield _format_sse(event)

			await task
			if result_holder.get("error") is not None:
				yield _format_sse({"event": "error", "detail": str(result_holder["error"])})
				return

			assistant_message = Message(
				conversation_id=conversation.id,
				role="assistant",
				content=str(result_holder["assistant_text"]),
				sources=result_holder.get("sources"),
			)
			db.add(assistant_message)

			if conversation.title is None:
				conversation.title = message_body.content[:80].strip()

			await db.commit()
			await db.refresh(assistant_message)

			yield _format_sse(
				{
					"event": "final",
					"role": assistant_message.role,
					"content": assistant_message.content,
					"sources": assistant_message.sources,
				}
			)
			yield "data: [DONE]\n\n"
		finally:
			clear_tool_call_context()

	return StreamingResponse(event_stream(), media_type="text/event-stream")
