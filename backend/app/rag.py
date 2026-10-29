import re, uuid
from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer
from .config import settings
_client = None
_model = None
def get_vector_store():
    global _client
    if _client is None:
        path = Path(settings.chroma_path)
        if not path.is_absolute(): path = Path(__file__).resolve().parents[1] / path
        path.mkdir(parents=True, exist_ok=True)
        _client = chromadb.PersistentClient(path=str(path))
    return _client
def get_embedding_model():
    global _model
    if _model is None: _model = SentenceTransformer(settings.embedding_model)
    return _model
def chunk_text(text: str, size: int = 900, overlap: int = 150):
    text = re.sub(r"\s+", " ", text).strip()
    chunks, start = [], 0
    while start < len(text):
        end = min(len(text), start + size)
        chunks.append(text[start:end])
        if end == len(text): break
        start = max(start + 1, end - overlap)
    return chunks
def add_document(owner_id: int, document_id: int, filename: str, content: str):
    chunks = chunk_text(content)
    if not chunks: return 0
    embeddings = get_embedding_model().encode(chunks, normalize_embeddings=True).tolist()
    collection = get_vector_store().get_or_create_collection("supportiq_kb")
    ids = [f"u{owner_id}_d{document_id}_{i}_{uuid.uuid4().hex[:8]}" for i in range(len(chunks))]
    collection.add(ids=ids, documents=chunks, embeddings=embeddings,
      metadatas=[{"owner_id": owner_id, "document_id": document_id, "filename": filename, "chunk": i} for i in range(len(chunks))])
    return len(chunks)
def retrieve(owner_id: int, query: str, limit: int = 5):
    collection = get_vector_store().get_or_create_collection("supportiq_kb")
    if collection.count() == 0: return []
    emb = get_embedding_model().encode([query], normalize_embeddings=True).tolist()
    result = collection.query(query_embeddings=emb, n_results=min(limit, collection.count()),
      where={"owner_id": owner_id}, include=["documents", "metadatas", "distances"])
    rows = []
    for doc, meta, distance in zip((result.get("documents") or [[]])[0], (result.get("metadatas") or [[]])[0], (result.get("distances") or [[]])[0]):
        if meta and int(meta.get("owner_id", -1)) == owner_id:
            rows.append({"text": doc, "filename": meta.get("filename", "unknown"), "distance": float(distance)})
    return rows
