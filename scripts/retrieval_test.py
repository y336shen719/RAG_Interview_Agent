import os
import sys
import json
import numpy as np
import faiss
from openai import OpenAI

# ----------------------------
# Configuration
# ----------------------------
CHUNK_FILE = "vector_store/chunks.json"
INDEX_FILE = "vector_store/faiss.index"
MODEL = "text-embedding-3-small"

# ----------------------------
# Initialize OpenAI client
# ----------------------------
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not set.")

client = OpenAI(api_key=api_key)

# ----------------------------
# Load chunks
# ----------------------------
def load_chunks():
    with open(CHUNK_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# ----------------------------
# Load FAISS index
# ----------------------------
def load_index():
    return faiss.read_index(INDEX_FILE)

# ----------------------------
# Generate query embedding
# ----------------------------
def embed_query(query):
    response = client.embeddings.create(
        model=MODEL,
        input=query
    )

    vector = np.array(response.data[0].embedding).astype("float32")
    vector = vector.reshape(1, -1)

    # Normalize for cosine similarity
    faiss.normalize_L2(vector)

    return vector

# ----------------------------
# Search
# ----------------------------
def search(query, top_k, index, chunks):
    query_vector = embed_query(query)

    scores, indices = index.search(query_vector, top_k)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        results.append({
            "rank": len(results) + 1,
            "score": float(score),
            "metadata": chunks[idx]["metadata"],
            "preview": chunks[idx]["content"][:500]
        })

    return results

# ----------------------------
# Main
# ----------------------------
def main():

    if len(sys.argv) < 3:
        print("Usage: python retrieval_test.py 'your query' top_k")
        sys.exit(1)

    query = sys.argv[1]
    top_k = int(sys.argv[2])

    print("Loading vector store...")
    chunks = load_chunks()
    index = load_index()

    print("\nQuery:", query)
    print("Top K:", top_k)

    results = search(query, top_k, index, chunks)

    print("\nResults:")
    print("=" * 80)

    for r in results:
        print(f"\nRank {r['rank']}")
        print(f"Score: {r['score']:.4f}")
        print("Metadata:", r["metadata"])
        print("Preview:")
        print(r["preview"])
        print("-" * 80)


if __name__ == "__main__":
    main()
