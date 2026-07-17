import fitz  # PyMuPDF


def extract_text_from_pdf(file_path: str) -> tuple[str, int]:
    """
    Extracts all text from a PDF. Returns (full_text, page_count).
    Falls back to pdfplumber if PyMuPDF finds no extractable text
    (e.g. some scanned/odd-encoded PDFs parse better with it).
    """
    text_parts = []
    page_count = 0

    try:
        doc = fitz.open(file_path)
        page_count = doc.page_count
        for page in doc:
            text_parts.append(page.get_text())
        doc.close()
        full_text = "\n\n".join(text_parts).strip()

        if full_text:
            return full_text, page_count
    except Exception:
        pass  # fall through to pdfplumber

    # Fallback: pdfplumber (slower, sometimes catches text PyMuPDF misses)
    import pdfplumber

    text_parts = []
    with pdfplumber.open(file_path) as pdf:
        page_count = len(pdf.pages)
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            text_parts.append(page_text)

    full_text = "\n\n".join(text_parts).strip()

    if not full_text:
        raise ValueError(
            "Could not extract any text from this PDF. It may be a scanned "
            "image-only document — OCR support isn't included in this build."
        )

    return full_text, page_count


def chunk_text(text: str, chunk_size: int = 1200, overlap: int = 150) -> list[str]:
    """Simple sliding-window chunker for the vector store (RAG)."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return [c.strip() for c in chunks if c.strip()]
