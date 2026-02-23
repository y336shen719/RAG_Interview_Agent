import sys
from pathlib import Path
from rag_core import answer_query

OUTPUT_FILE = Path("rag_answer.txt")

def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/rag_answer.py \"your question\"")
        sys.exit(1)

    query = sys.argv[1]

    # Call core RAG engine
    answer, debug = answer_query(query)

    # Print to logs
    print("\n" + "=" * 80)
    print("Query:")
    print(query)
    print("\nAnswer:")
    print(answer)
    print("=" * 80)

    OUTPUT_FILE.write_text(
        f"Query:\n{query}\n\nAnswer:\n{answer}\n",
        encoding="utf-8"
    )

    print(f"\nSaved answer to {OUTPUT_FILE.resolve()}")

if __name__ == "__main__":
    main()
