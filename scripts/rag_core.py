import os
import json
import numpy as np
import faiss
from openai import OpenAI
from query_classifier import classify_query

# Configuration
CHUNK_FILE = "vector_store/chunks.json"
INDEX_FILE = "vector_store/faiss.index"

EMBED_MODEL = "text-embedding-3-small"
GEN_MODEL = "gpt-4o-mini"

TOP_K = 3
THRESHOLD = 0.4
CANDIDATE_K = 10
MAX_CONTEXT_CHARS = 6000

# OpenAI Client
def get_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set.")
    return OpenAI(api_key=api_key)

# Load Vector Store
def load_vector_store():
    with open(CHUNK_FILE, "r", encoding="utf-8") as f:
        chunks = json.load(f)
    index = faiss.read_index(INDEX_FILE)
    return chunks, index

# Embed Query
def embed_query(query: str, client):
    resp = client.embeddings.create(
        model=EMBED_MODEL,
        input=query
    )
    vec = np.array(resp.data[0].embedding, dtype="float32").reshape(1, -1)
    faiss.normalize_L2(vec)
    return vec

# Retrieval
def retrieve(query: str, client, index, chunks):
    category, confidence, method = classify_query(query)

    qvec = embed_query(query, client)
    scores, indices = index.search(qvec, CANDIDATE_K)

    results = []

    for score, idx in zip(scores[0], indices[0]):
        if idx == -1:
            continue

        chunk = chunks[idx]
        meta = chunk.get("metadata", {})
        src_type = meta.get("source_type")

        # Metadata routing
        if category and src_type != category:
            continue

        # Threshold filtering
        if float(score) < THRESHOLD:
            continue

        results.append({
            "score": float(score),
            "chunk_id": int(idx),
            "metadata": meta,
            "content": chunk.get("content", "")
        })

        if len(results) >= TOP_K:
            break

    return results

# Build Context
def build_context(results):
    parts = []
    total = 0

    for i, r in enumerate(results, start=1):
        meta = r["metadata"]
        src_type = meta.get("source_type", "unknown")
        file_name = meta.get("file_name", "unknown")
        tag = meta.get("section") or meta.get("question") or "unknown"

        header = f"[{i}] source_type={src_type} | file={file_name} | tag={tag} | score={r['score']:.4f}"
        body = r["content"].strip()

        block = header + "\n" + body

        if total + len(block) > MAX_CONTEXT_CHARS:
            break

        parts.append(block)
        total += len(block)

    return "\n\n---\n\n".join(parts)

# Generate Answer
def generate_answer(query: str, context: str, client):

    system = (
        "You are a professional interview and project assistant. "
        "Answer ONLY using the provided context. "
        "If insufficient information is available, say so clearly."
    )

    user = f"""
Question:
{query}

Context:
{context}

Provide a structured and professional answer.
"""

    resp = client.responses.create(
        model=GEN_MODEL,
        input=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=0.2,
    )

    return resp.output_text

# Public API
def answer_query(query: str):
    client = get_client()
    chunks, index = load_vector_store()

    retrieved = retrieve(query, client, index, chunks)

    if not retrieved:
        return "I do not have enough information in the current knowledge base to answer this question."

    context = build_context(retrieved)
    return generate_answer(query, context, client)
