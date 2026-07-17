import os
import uuid
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import get_current_user, CurrentUser
from app.config import get_settings
from app.models.models import Document
from app.schemas.course import DocumentOut
from app.services.pdf_extractor import extract_text_from_pdf, chunk_text
from app.services.vector_store import index_document

router = APIRouter(prefix="/documents", tags=["documents"])
settings = get_settings()


@router.post("", response_model=DocumentOut)
async def upload_document(
    file: UploadFile = File(...),
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    MAX_SIZE = 30 * 1024 * 1024  # 30MB

    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    doc_id = uuid.uuid4()
    storage_path = os.path.join(settings.UPLOAD_DIR, f"{doc_id}.pdf")

    contents = await file.read()

    if len(contents) == 0:
        raise HTTPException(status_code=400, detail="This file is empty.")
    if len(contents) > MAX_SIZE:
        raise HTTPException(status_code=413, detail="This PDF is larger than 30MB. Please upload a smaller file.")

    with open(storage_path, "wb") as f:
        f.write(contents)

    document = Document(
        id=doc_id,
        user_id=current_user.id,
        filename=file.filename,
        storage_path=storage_path,
        status="processing",
    )
    db.add(document)
    db.commit()
    db.refresh(document)

    try:
        text, page_count = extract_text_from_pdf(storage_path)
        document.extracted_text = text
        document.page_count = page_count
        document.status = "ready"
        db.commit()
        db.refresh(document)

        # Index chunks in Chroma for RAG (chatbot + quiz context retrieval)
        chunks = chunk_text(text)
        index_document(str(document.id), chunks)
    except Exception as e:
        document.status = "failed"
        db.commit()
        raise HTTPException(status_code=422, detail=f"Failed to process PDF: {e}")

    return document


@router.get("", response_model=list[DocumentOut])
def list_documents(
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return (
        db.query(Document)
        .filter(Document.user_id == current_user.id)
        .order_by(Document.created_at.desc())
        .all()
    )


@router.get("/{document_id}", response_model=DocumentOut)
def get_document(
    document_id: str,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    doc = (
        db.query(Document)
        .filter(Document.id == document_id, Document.user_id == current_user.id)
        .first()
    )
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc
