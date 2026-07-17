from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import get_current_user, CurrentUser
from app.models.models import ChatHistory
from app.schemas.misc import ChatMessageIn, ChatMessageOut
from app.services.chatbot import answer_question
from app.services.groq_client import GroqServiceError

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatMessageOut)
def chat(
    body: ChatMessageIn,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Pull recent history for this course to give the model conversational context
    recent = (
        db.query(ChatHistory)
        .filter(ChatHistory.user_id == current_user.id, ChatHistory.course_id == body.course_id)
        .order_by(ChatHistory.created_at.desc())
        .limit(6)
        .all()
    )
    history = []
    for h in reversed(recent):
        history.append({"role": "user", "content": h.question})
        history.append({"role": "assistant", "content": h.answer})

    answer = None
    try:
        answer = answer_question(body.document_id, body.question, history)
    except GroqServiceError as e:
        raise HTTPException(status_code=429 if e.is_rate_limit else 502, detail=e.message)

    record = ChatHistory(
        user_id=current_user.id,
        course_id=body.course_id,
        question=body.question,
        answer=answer,
    )
    db.add(record)
    db.commit()

    return ChatMessageOut(question=body.question, answer=answer)


@router.get("/{course_id}/history", response_model=list[ChatMessageOut])
def get_chat_history(
    course_id: str,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    records = (
        db.query(ChatHistory)
        .filter(ChatHistory.user_id == current_user.id, ChatHistory.course_id == course_id)
        .order_by(ChatHistory.created_at.asc())
        .all()
    )
    return [ChatMessageOut(question=r.question, answer=r.answer) for r in records]
