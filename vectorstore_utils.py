import chromadb
from chromadb.config import Settings

CHROMA_DIR = "chroma_db"

def store_embeddings(session_id, chunks, embeddings):
    client = chromadb.Client(Settings(persist_directory=CHROMA_DIR))
    collection = client.get_or_create_collection(session_id)
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    collection.add(documents=chunks, embeddings=embeddings.tolist(), ids=ids)
    return collection

def query_chromadb(session_id, q_embedding, top_k=3):
    client = chromadb.Client(Settings(persist_directory=CHROMA_DIR))
    collection = client.get_or_create_collection(session_id)
    results = collection.query(query_embeddings=q_embedding.tolist(), n_results=top_k)
    return results["documents"][0] if results["documents"] else []

def cleanup_collection(session_id):
    client = chromadb.Client(Settings(persist_directory=CHROMA_DIR))
    try:
        client.delete_collection(session_id)
    except Exception:
        pass 