import os
import json
import numpy as np
import faiss
from openai import OpenAI
from pathlib import Path
from scripts.query_classifier import classify_query

# Configuration
PROJECT_ROOT = Path(__file__).resolve().parent.parent
VECTOR_STORE_DIR = PROJECT_ROOT / "vector_store"

CHUNK_FILE = VECTOR_STORE_DIR / "chunks.json"
INDEX_FILE = VECTOR_STORE_DIR / "faiss.index"

EMBED_MODEL = "text-embedding-3-small"
GEN_MODEL = "gpt-4o-mini"

TOP_K = 3
CANDIDATE_K = 10
THRESHOLD = 0.25
ROUTING_CONF_THRESHOLD = 0.7
MAX_CONTEXT_CHARS = 6000

# OpenAI Client
_client = None

def get_client():
    global _client
    if _client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set.")
        _client = OpenAI(api_key=api_key)
    return _client

# Load Vector Store
def load_vector_store():
    with open(CHUNK_FILE, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    index = faiss.read_index(str(INDEX_FILE))
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

    print("\nRouting decision:", category)
    print("Routing method:", method)
    print("Routing confidence:", round(float(confidence), 4))

    qvec = embed_query(query, client)
    scores, indices = index.search(qvec, CANDIDATE_K)

    results = []

    for score, idx in zip(scores[0], indices[0]):

        if idx == -1:
            continue

        if float(score) < THRESHOLD:
            continue

        chunk = chunks[idx]
        meta = chunk.get("metadata", {})
        src_type = meta.get("source_type")

        # Apply metadata routing only if high confidence
        if (
            confidence is not None
            and confidence >= ROUTING_CONF_THRESHOLD
            and category
            and src_type != category
        ):
            continue

        results.append({
            "score": float(score),
            "chunk_id": int(idx),
            "metadata": meta,
            "content": chunk.get("content", "")
        })

    # Sort explicitly by score (descending)
    results = sorted(results, key=lambda x: x["score"], reverse=True)

    return results[:TOP_K]

# Build Context
def build_context(results):

    parts = []
    total_chars = 0

    for i, r in enumerate(results, start=1):

        meta = r["metadata"]
        src_type = meta.get("source_type", "unknown")
        file_name = meta.get("file_name", "unknown")
        tag = meta.get("section") or meta.get("question") or "unknown"

        header = (
            f"[{i}] Source: {src_type} | "
            f"File: {file_name} | "
            f"Tag: {tag}"
        )

        body = r["content"].strip()
        block = header + "\n" + body

        if total_chars + len(block) > MAX_CONTEXT_CHARS:
            break

        parts.append(block)
        total_chars += len(block)

    return "\n\n---\n\n".join(parts)

# Generate Answer
def generate_answer(query: str, context: str, client):

    system_prompt = (
        "You are responding as the job candidate in a professional interview. "
        "Always answer in natural first-person language. "
        "Use only the information provided below. "
        "Do not fabricate details or use outside knowledge. "
        "If the information needed to answer the question is not available, "
        "do not mention missing context. "
        "Instead, explain honestly that this is an area I am currently developing "
        "and describe concrete steps I am taking or plan to take to strengthen this skill. "
        "Maintain clarity, confidence, and a structured professional tone. "
        "Do not mention the word 'context' or 'knowledge base'."
    )

    user_prompt = f"""
Question:
{query}

Information:
{context if context else "No relevant project or experience information found."}

Provide a structured and professional answer.
"""

    response = client.responses.create(
        model=GEN_MODEL,
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
    )

    return response.output_text

# Public API
def answer_query(query: str):

    client = get_client()
    chunks, index = load_vector_store()

    retrieved = retrieve(query, client, index, chunks)

    context = build_context(retrieved) if retrieved else ""

    return generate_answer(query, context, client)
