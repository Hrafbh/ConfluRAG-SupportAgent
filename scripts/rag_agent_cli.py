import os
import json
import re
from dotenv import load_dotenv

import chromadb
from sentence_transformers import SentenceTransformer


CHROMA_DIR = "data/index/chroma"
COLLECTION_NAME = "routepilot_kb"
ROUTING_PATH = "config/intent_routing.json"

# seuil simple (à ajuster): plus grand = plus permissif
# (Chroma renvoie souvent des distances L2 : plus petit = plus proche)
UNKNOWN_THRESHOLD = 1.20


def normalize(s):
    s = (s or "").lower()
    s = re.sub(r"[^a-z0-9àâçéèêëîïôûùüÿñæœ\s\-]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def load_routing():
    try:
        with open(ROUTING_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def detect_intent(question, routing):
    q = normalize(question)
    best = None
    best_score = 0

    for intent_name, cfg in routing.items():
        kws = cfg.get("keywords", [])
        score = 0
        for kw in kws:
            kw_n = normalize(kw)
            if kw_n and kw_n in q:
                score += 1
        if score > best_score:
            best_score = score
            best = intent_name

    return best, best_score


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

    # fallback : extrait utile
    return t[:600].strip()


def keyword_bonus(question, meta, doc):
    q = normalize(question)
    title = normalize(meta.get("title", ""))
    tags = normalize(meta.get("tags", ""))
    category = normalize(meta.get("category", ""))

    bonus = 0
    # overlap titre
    q_words = set(q.split())
    t_words = set(title.split())
    bonus += min(4, len(q_words.intersection(t_words)))

    # bonus tags
    for w in ["pdf", "csv", "export", "mfa", "login", "vpn", "proxy", "incident", "runbook"]:
        if w in q and w in tags:
            bonus += 1

    # petit bonus si doc contient le mot clé principal
    for w in ["export", "pdf", "csv", "mfa", "vpn", "incident", "runbook"]:
        if w in q and w in normalize(doc):
            bonus += 1

    # bonus category si question mentionne
    if "incident" in q and "incidents" in category:
        bonus += 2

    return bonus


def choose_best(question, docs, metas, distances):
    best_i = 0
    best_score = -10**9

    for i in range(len(docs)):
        dist = distances[i] if distances and i < len(distances) else 0.0
        score = -dist  # plus dist est petit, plus score est grand
        score += keyword_bonus(question, metas[i], docs[i])
        if score > best_score:
            best_score = score
            best_i = i

    return best_i


def query_kb(collection, q_vec, category=None, n=6):
    # tentative avec filtre category
    if category:
        try:
            return collection.query(
                query_embeddings=[q_vec],
                n_results=n,
                where={"category": category},
                include=["documents", "metadatas", "distances"]
            )
        except Exception:
            pass

    # fallback sans filtre
    return collection.query(
        query_embeddings=[q_vec],
        n_results=n,
        include=["documents", "metadatas", "distances"]
    )


def main():
    load_dotenv()

    if not os.path.exists(CHROMA_DIR):
        print(" Index introuvable. Lancez d'abord: python scripts/rag_build_index.py")
        return

    routing = load_routing()

    model_name = os.getenv("RAG_EMBED_MODEL", "all-MiniLM-L6-v2")
    model = SentenceTransformer(model_name)

    client = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = client.get_collection(name=COLLECTION_NAME)

    print(" Agent Support prêt (RAG + routing). Tapez votre question (ou 'exit').\n")

    while True:
        question = input("Question> ").strip()
        if question.lower() in ("exit", "quit"):
            break
        if not question:
            continue

        intent, intent_score = detect_intent(question, routing)
        category = routing.get(intent, {}).get("category") if intent else None

        q_vec = model.encode([question])[0].tolist()
        res = query_kb(collection, q_vec, category=category, n=6)

        docs = res.get("documents", [[]])[0]
        metas = res.get("metadatas", [[]])[0]
        dists = res.get("distances", [[]])[0]

        if not docs:
            print("\n Je ne trouve rien dans la KB.\n")
            continue

        best_i = choose_best(question, docs, metas, dists)

        best_doc = docs[best_i]
        best_meta = metas[best_i]
        best_dist = dists[best_i] if dists and best_i < len(dists) else None

        # Fallback "je ne sais pas" si trop loin
        if best_dist is not None and best_dist > UNKNOWN_THRESHOLD:
            print("\n==============================")
            print("Réponse agent")
            print("==============================")
            print("Je ne trouve pas de réponse fiable dans la KB pour le moment.")
            print(" Actions recommandées :")
            print("- clarifier le contexte (module, tenant, message d’erreur, heure)")
            print("- ouvrir un ticket et escalader L2 si impact bloquant\n")
            print("Sources (retrieval, à vérifier):")
            for i in range(min(3, len(metas))):
                m = metas[i]
                print(f"- {m.get('kb_id','')} | {m.get('title','')}")
                if m.get("url"):
                    print(f"  {m.get('url')}")
            print("\n")
            continue

        kb_id = best_meta.get("kb_id", "")
        title = best_meta.get("title", "")
        url = best_meta.get("url", "")
        cat = best_meta.get("category", "")

        steps = extract_resolution_steps(best_doc)

        print("\n==============================")
        print("Réponse agent")
        print("==============================")
        if intent:
            print(f"Intention détectée: {intent} (score={intent_score}) | Catégorie: {category or 'N/A'}")
        print(f"Page principale: {kb_id} | {title}")
        if url:
            print(f"Source: {url}")
        if cat:
            print(f"Category(meta): {cat}")

        print("\nÉtapes (extrait KB):")
        print(steps)

        print("\nEscalade (si non résolu / impact large):")
        print("- collecter: tenant, utilisateur, module, heure, screenshots, message exact")
        print("- si multi-users / multi-tenants: escalader immédiatement (runbook/incident)")

        print("\n------------------------------")
        print("Sources (Top 3)")
        print("------------------------------")
        for i in range(min(3, len(metas))):
            m = metas[i]
            print(f"- {m.get('kb_id','')} | {m.get('title','')}")
            if m.get("url"):
                print(f"  {m.get('url')}")

        print("\n")


if __name__ == "__main__":
    main()
