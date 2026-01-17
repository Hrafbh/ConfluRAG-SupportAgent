import os
import re
from dotenv import load_dotenv

import chromadb
from sentence_transformers import SentenceTransformer


CHROMA_DIR = "data/index/chroma"
COLLECTION_NAME = "routepilot_kb"


def extract_resolution_steps(text):
    """
    Essaie d'extraire la partie "Resolution steps" jusqu'à Verification/Escalation/References.
    Si on ne trouve pas, on retourne un extrait utile.
    """
    if not text:
        return ""

    # Normaliser un peu
    t = text.replace("\r\n", "\n").replace("\r", "\n")

    m = re.search(
        r"Resolution steps\s*(.*?)(?:\n\s*(Verification|Escalation|References)\b|$)",
        t,
        re.DOTALL | re.IGNORECASE,
    )
    if m:
        steps = m.group(1).strip()
        # Nettoyage simple
        steps = re.sub(r"\n{3,}", "\n\n", steps).strip()
        return steps

    # fallback : retourner le début
    return t[:600].strip()


def main():
    load_dotenv()

    if not os.path.exists(CHROMA_DIR):
        print(" Index introuvable. Lancez d'abord: python scripts/rag_build_index.py")
        return

    model_name = os.getenv("RAG_EMBED_MODEL", "all-MiniLM-L6-v2")
    model = SentenceTransformer(model_name)

    client = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = client.get_collection(name=COLLECTION_NAME)

    print(" Agent RAG prêt. Tapez votre question (ou 'exit').\n")

    while True:
        question = input("Question> ").strip()
        if question.lower() in ("exit", "quit"):
            break
        if not question:
            continue

        q_vec = model.encode([question])[0].tolist()

        res = collection.query(
            query_embeddings=[q_vec],
            n_results=5
        )

        docs = res.get("documents", [[]])[0]
        metas = res.get("metadatas", [[]])[0]

        if not docs:
            print("\n Je ne trouve pas de réponse dans la KB.\n")
            continue

        # On prend le meilleur match comme "page principale"
        best_doc = docs[0]
        best_meta = metas[0]

        kb_id = best_meta.get("kb_id", "")
        title = best_meta.get("title", "")
        url = best_meta.get("url", "")

        steps = extract_resolution_steps(best_doc)

        print("\n==============================")
        print("Réponse recommandée (KB)")
        print("==============================")
        if kb_id or title:
            print(f"Page principale: {kb_id} | {title}")
        if url:
            print(f"Source: {url}\n")

        print("Actions (extrait):")
        print(steps)

        print("\n------------------------------")
        print("Sources (Top 3)")
        print("------------------------------")
        for i in range(min(3, len(metas))):
            m = metas[i]
            k = m.get("kb_id", "")
            t = m.get("title", "")
            u = m.get("url", "")
            print(f"- {k} | {t}")
            if u:
                print(f"  {u}")

        print("\n")


if __name__ == "__main__":
    main()
