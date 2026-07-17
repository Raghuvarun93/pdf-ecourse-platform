from app.services.groq_client import chat_completion
from app.services.vector_store import query_document

SYSTEM_PROMPT = """You are an AI learning companion helping a student understand a
document they uploaded. Answer ONLY using the provided context from the document.
If the context doesn't contain the answer, say so honestly rather than guessing.
You can also explain concepts more simply, summarize, suggest what to study next,
or offer to generate a quiz — but always ground your answers in the given context."""


def answer_question(document_id: str, question: str, chat_history: list[dict] | None = None) -> str:
    """
    RAG pipeline: retrieve top-5 relevant chunks from the document's vector store,
    then ask Groq to answer using only that context.
    """
    relevant_chunks = query_document(document_id, question, n_results=5)
    context = "\n\n---\n\n".join(relevant_chunks) if relevant_chunks else "(no matching content found)"

    history_text = ""
    if chat_history:
        history_text = "\n".join(
            f"{'Student' if m['role'] == 'user' else 'Tutor'}: {m['content']}"
            for m in chat_history[-6:]  # last few turns for context continuity
        )

    # Build the user prompt without backslashes in f-string
    conversation_section = f"RECENT CONVERSATION:\n{history_text}\n\n" if history_text else ""
    
    user_prompt = f"""CONTEXT FROM DOCUMENT:
---
{context}
---

{conversation_section}STUDENT'S QUESTION: {question}

Answer clearly and helpfully, grounded in the context above."""

    return chat_completion(SYSTEM_PROMPT, user_prompt, temperature=0.5)
