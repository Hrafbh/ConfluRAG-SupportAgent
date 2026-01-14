# scripts/rag_ask.py
"""
Interroger l'index (Chroma) et afficher les meilleurs passages + citations.

Usage:
  python scripts/rag_ask.py
"""

import os
from dotenv import load_dotenv

import chromadb
from sentence_transformers import SentenceTransformer


CHROMA_DIR = "data/index/chroma"
COLLECTION_NAME = "routepilot_kb"


def main():
    load_dotenv()

    if not os.path.exists(CHROMA_DIR):
        print(" Index introuvable. Lancez d'abord: python scripts/rag_build_index.py")
        return

    model_name = os.getenv("RAG_EMBED_MODEL", "all-MiniLM-L6-v2")
    model = SentenceTransformer(model_name)

    client = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = client.get_collection(name=COLLECTION_NAME)

    print(" RAG CLI prêt. Tapez votre question (ou 'exit').\n")

    while True:
        q = input("Question> ").strip()
        if q.lower() in ("exit", "quit"):
            break
        if not q:
            continue

        q_vec = model.encode([q])[0].tolist()

        res = collection.query(
            query_embeddings=[q_vec],
            n_results=5
        )

        docs = res.get("documents", [[]])[0]
        metas = res.get("metadatas", [[]])[0]

        print("\n--- TOP MATCHES ---")
        for i, (doc, meta) in enumerate(zip(docs, metas), start=1):
            title = meta.get("title", "")
            url = meta.get("url", "")
            kb_id = meta.get("kb_id", "")
            page_id = meta.get("page_id", "")
            chunk_index = meta.get("chunk_index", "")

            print(f"\n[{i}] {kb_id} | {title} | page_id={page_id} | chunk={chunk_index}")
            if url:
                print(f"    Source: {url}")
            print("    Extrait:")
            print("    " + doc[:400].replace("\n", " ") + ("..." if len(doc) > 400 else ""))

        print("\n")


if __name__ == "__main__":
    main()
