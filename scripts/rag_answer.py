import os
import re
from dotenv import load_dotenv

import chromadb
from sentence_transformers import SentenceTransformer


CHROMA_DIR = "data/index/chroma"
COLLECTION_NAME = "routepilot_kb"


def normalize(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9àâçéèêëîïôûùüÿñæœ\s\-]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def keyword_bonus(question, title, category, tags):
    q = normalize(question)
    t = normalize(title)
    c = normalize(category or "")
    g = normalize(tags or "")

    bonus = 0

    # Intention: export/pdf/csv
    if ("export" in q) or ("pdf" in q) or ("csv" in q):
        if ("export" in t) or ("pdf" in t) or ("csv" in t):
            bonus += 6
        if "workstation" in c or "mobile" in c:
            bonus += 2
        # pénalité si on tombe sur impression/étiquettes
        if ("impression" in t) or ("étiquette" in t) or ("etiquette" in t):
            bonus -= 3

    # Intention: impression / étiquettes
    if ("impression" in q) or ("étiquette" in q) or ("etiquette" in q):
        if ("impression" in t) or ("étiquette" in t) or ("etiquette" in t):
            bonus += 6

    # Intention: MFA / SSO
    if ("mfa" in q) or ("sso" in q):
        if ("mfa" in t) or ("sso" in t):
            bonus += 4

    # Bonus overlap mots (très simple)
    q_words = set(q.split())
    t_words = set(t.split())
    bonus += min(4, len(q_words.intersection(t_words)))

    # Bonus tags
    for w in ["pdf", "csv", "export", "mfa", "login", "vpn", "proxy"]:
        if w in q and w in g:
            bonus += 1

    return bonus


def extract_resolution_steps(text):
    if not text:
        return ""

    t = text.replace("\r\n", "\n").replace("\r", "\n")

    m = re.search(
        r"Resolution steps\s*(.*?)(?:\n\s*(Verification|Escalation|References)\b|$)",
        t,
        re.DOTALL | re.IGNORECASE,
    )
    if m:
        steps = m.group(1).strip()
        steps = re.sub(r"\n{3,}", "\n\n", steps).strip()
        return steps

    return t[:600].strip()


def choose_best(question, docs, metas):
    best_i = 0
    best_score = -10**9

    for i, (doc, meta) in enumerate(zip(docs, metas)):
        title = meta.get("title", "")
        category = meta.get("category", "")
        tags = meta.get("tags", "")

        score = keyword_bonus(question, title, category, tags)

        # petit bonus si le chunk contient vraiment le mot clé
        q = normalize(question)
        d = normalize(doc)
        if "export" in q and "export" in d:
            score += 2
        if "pdf" in q and "pdf" in d:
            score += 2
        if "mfa" in q and "mfa" in d:
            score += 2

        if score > best_score:
            best_score = score
            best_i = i

    return best_i


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

        best_i = choose_best(question, docs, metas)

        best_doc = docs[best_i]
        best_meta = metas[best_i]

        kb_id = best_meta.get("kb_id", "")
        title = best_meta.get("title", "")
        url = best_meta.get("url", "")

        steps = extract_resolution_steps(best_doc)

        print("\n==============================")
        print("Réponse recommandée (KB)")
        print("==============================")
        print(f"Page principale: {kb_id} | {title}")
        if url:
            print(f"Source: {url}\n")

        print("Actions (extrait):")
        print(steps)

        print("\n------------------------------")
        print("Sources (Top 3)")
        print("------------------------------")

        # on affiche toujours les 3 meilleurs "sémantiques", mais ça peut être différent de la page principale
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
