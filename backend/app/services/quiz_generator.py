import uuid
from sqlalchemy.orm import Session
from app.services.groq_client import chat_completion_json
from app.models.models import Quiz, Lesson

SYSTEM_PROMPT = """You are an expert exam writer. Generate rigorous but fair quiz
questions strictly from the given lesson content. Respond with valid JSON only."""


def _build_prompt(chapter_title: str, lessons_text: str, count: int) -> str:
    return f"""Generate {count} multiple-choice questions for this chapter: "{chapter_title}"

Return ONLY JSON matching exactly this shape:
{{
  "questions": [
    {{
      "question": "string",
      "options": ["string", "string", "string", "string"],
      "correct_answer": "must exactly match one of the 4 options",
      "explanation": "string, 1-2 sentences on why the answer is correct"
    }}
  ]
}}

Base every question strictly on the content below.

CHAPTER CONTENT:
\"\"\"
{lessons_text[:12000]}
\"\"\"
"""


def generate_quiz_for_chapter(db: Session, chapter_id: str, chapter_title: str, count: int = 10) -> list[Quiz]:
    lessons = db.query(Lesson).filter(Lesson.chapter_id == chapter_id).all()
    lessons_text = "\n\n".join(f"{l.title}\n{l.content}\n{l.summary or ''}" for l in lessons)

    if not lessons_text.strip():
        raise ValueError("This chapter has no lesson content to generate a quiz from.")

    data = chat_completion_json(SYSTEM_PROMPT, _build_prompt(chapter_title, lessons_text, count))

    created = []
    for q in data.get("questions", []):
        quiz = Quiz(
            id=uuid.uuid4(),
            chapter_id=chapter_id,
            question=q.get("question", ""),
            options=q.get("options", []),
            correct_answer=q.get("correct_answer", ""),
            explanation=q.get("explanation", ""),
        )
        db.add(quiz)
        created.append(quiz)

    db.commit()
    for quiz in created:
        db.refresh(quiz)
    return created
