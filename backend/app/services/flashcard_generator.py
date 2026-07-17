import uuid
from sqlalchemy.orm import Session
from app.services.groq_client import chat_completion_json
from app.models.models import Flashcard, Lesson

SYSTEM_PROMPT = """You are an expert at creating concise study flashcards.
Generate front/back flashcard pairs strictly from the given lesson content.
Respond with valid JSON only."""


def _build_prompt(chapter_title: str, lessons_text: str, count: int) -> str:
    return f"""Generate {count} flashcards for this chapter: "{chapter_title}"

Return ONLY JSON matching exactly this shape:
{{
  "flashcards": [
    {{ "front": "a concise question or term", "back": "a concise, clear answer/definition" }}
  ]
}}

Base every flashcard strictly on the content below. Keep both front and back short (1-2 sentences).

CHAPTER CONTENT:
\"\"\"
{lessons_text[:12000]}
\"\"\"
"""


def generate_flashcards_for_chapter(db: Session, chapter_id: str, chapter_title: str, count: int = 10) -> list[Flashcard]:
    lessons = db.query(Lesson).filter(Lesson.chapter_id == chapter_id).all()
    lessons_text = "\n\n".join(f"{l.title}\n{l.content}\n{l.summary or ''}" for l in lessons)

    if not lessons_text.strip():
        raise ValueError("This chapter has no lesson content to generate flashcards from.")

    data = chat_completion_json(SYSTEM_PROMPT, _build_prompt(chapter_title, lessons_text, count))

    created = []
    for c in data.get("flashcards", []):
        card = Flashcard(
            id=uuid.uuid4(),
            chapter_id=chapter_id,
            front=c.get("front", ""),
            back=c.get("back", ""),
        )
        db.add(card)
        created.append(card)

    db.commit()
    for card in created:
        db.refresh(card)
    return created
