import chromadb

_client = chromadb.PersistentClient(path="./chroma_data")


def _collection_name(document_id: str) -> str:
    # Chroma collection names must be alphanumeric + limited symbols
    return f"doc_{document_id.replace('-', '')}"


def index_document(document_id: str, chunks: list[str]) -> None:
    """Stores text chunks for a document in its own Chroma collection."""
    collection = _client.get_or_create_collection(name=_collection_name(document_id))
    ids = [f"{document_id}_{i}" for i in range(len(chunks))]
    # Chroma's default embedding function (all-MiniLM-L6-v2) runs automatically
    # when documents are added without explicit embeddings.
    collection.add(documents=chunks, ids=ids)


def query_document(document_id: str, question: str, n_results: int = 5) -> list[str]:
    """Returns the most relevant chunks for a question — used for RAG in chat + quiz gen."""
    collection = _client.get_or_create_collection(name=_collection_name(document_id))
    if collection.count() == 0:
        return []
    results = collection.query(query_texts=[question], n_results=min(n_results, collection.count()))
    return results["documents"][0] if results["documents"] else []
