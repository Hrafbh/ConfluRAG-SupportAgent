import os
import re
import json
import streamlit as st
from dotenv import load_dotenv

import chromadb
from sentence_transformers import SentenceTransformer

CHROMA_DIR = "data/index/chroma"
COLLECTION_NAME = "routepilot_kb"
ROUTING_PATH = "config/intent_routing.json"
UNKNOWN_THRESHOLD = 1.20


def normalize(s):
    s = (s or "").lower()
    s = re.sub(r"[^a-z0-9àâçéèêëîïôûùüÿñæœ\s\-]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def load_routing():
    if not os.path.exists(ROUTING_PATH):
        return {}
    with open(ROUTING_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def detect_intent(question, routing):
    q = normalize(question)
    best_intent = None
    best_score = 0
    for name, cfg in routing.items():
        score = 0
        for kw in cfg.get("keywords", []):
            if normalize(kw) in q:
                score += 1
        if score > best_score:
            best_score = score
            best_intent = name

    category = routing.get(best_intent, {}).get("category") if best_intent else None
    return best_intent, best_score, category


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
        return m.group(1).strip()
    return t[:700].strip()


def keyword_bonus(question, meta, doc):
    q = normalize(question)
    title = normalize(meta.get("title", ""))
    tags = normalize(meta.get("tags", ""))

    bonus = 0
    q_words = set(q.split())
    t_words = set(title.split())
    bonus += min(4, len(q_words.intersection(t_words)))

    for w in ["pdf", "csv", "export", "mfa", "login", "vpn", "proxy", "incident", "runbook"]:
        if w in q and w in tags:
            bonus += 1
        if w in q and w in normalize(doc):
            bonus += 1
    return bonus


def rerank(question, docs, metas, dists):
    scored = []
    for i in range(len(docs)):
        dist = dists[i] if dists and i < len(dists) else 0.0
        score = (-dist) + keyword_bonus(question, metas[i], docs[i])
        scored.append((score, i))
    scored.sort(reverse=True, key=lambda x: x[0])
    return [i for _, i in scored]


def dedup_by_page_id(indices, metas):
    seen = set()
    out = []
    for i in indices:
        pid = metas[i].get("page_id", "")
        if pid in seen:
            continue
        seen.add(pid)
        out.append(i)
    return out


@st.cache_resource
def load_models():
    load_dotenv()
    os.environ["ANONYMIZED_TELEMETRY"] = "False"
    model_name = os.getenv("RAG_EMBED_MODEL", "all-MiniLM-L6-v2")
    model = SentenceTransformer(model_name)
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = client.get_collection(name=COLLECTION_NAME)
    return model_name, model, collection


def main():
    st.set_page_config(page_title="RoutePilot Support Agent (RAG)", layout="wide")
    st.title("RoutePilot Support Agent — RAG Demo")

    if not os.path.exists(CHROMA_DIR):
        st.error("Index introuvable. Lancez d'abord: python scripts/rag_build_index.py")
        return

    routing = load_routing()
    model_name, model, collection = load_models()

    st.sidebar.subheader("Settings")
    use_routing = st.sidebar.checkbox("Use routing (intent → category)", value=True)
    k = st.sidebar.slider("Top-K retrieval", 3, 12, 6)
    threshold = st.sidebar.slider("Unknown threshold (distance)", 0.5, 2.0, float(UNKNOWN_THRESHOLD), 0.05)

    st.sidebar.caption(f"Embedding model: {model_name}")

    q = st.text_input("Question", value="Que faire si l’export PDF échoue ?")
    go = st.button("Rechercher")

    if not go:
        return

    intent = score = category = None
    if use_routing and routing:
        intent, score, category = detect_intent(q, routing)

    q_vec = model.encode([q])[0].tolist()

    # Query with optional category filter
    try:
        if category:
            res = collection.query(
                query_embeddings=[q_vec],
                n_results=k,
                where={"category": category},
                include=["documents", "metadatas", "distances"],
            )
        else:
            res = collection.query(
                query_embeddings=[q_vec],
                n_results=k,
                include=["documents", "metadatas", "distances"],
            )
    except Exception:
        res = collection.query(
            query_embeddings=[q_vec],
            n_results=k,
            include=["documents", "metadatas", "distances"],
        )

    docs = res.get("documents", [[]])[0]
    metas = res.get("metadatas", [[]])[0]
    dists = res.get("distances", [[]])[0]

    if not docs:
        st.warning("Aucun résultat.")
        return

    order = rerank(q, docs, metas, dists)
    order = dedup_by_page_id(order, metas)

    best_i = order[0]
    best_meta = metas[best_i]
    best_doc = docs[best_i]
    best_dist = dists[best_i] if dists and best_i < len(dists) else None

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Answer (KB steps)")
        if intent:
            st.caption(f"Intent: {intent} (score={score}) | Category filter: {category}")

        if best_dist is not None and best_dist > threshold:
            st.error("Je ne trouve pas de réponse fiable dans la KB (fallback).")
            st.write("Actions recommandées : clarifier le contexte + ouvrir un ticket + escalade si impact.")
        else:
            st.markdown(f"**{best_meta.get('kb_id','')} — {best_meta.get('title','')}**")
            if best_meta.get("url"):
                st.write(best_meta["url"])
            st.write(extract_resolution_steps(best_doc))

    with col2:
        st.subheader("Top sources")
        for rank, i in enumerate(order[:5], start=1):
            m = metas[i]
            st.markdown(f"**[{rank}] {m.get('kb_id','')} — {m.get('title','')}**")
            st.caption(f"distance={dists[i]:.4f}" if dists and i < len(dists) else "")
            if m.get("url"):
                st.write(m["url"])
            st.write(docs[i][:350].replace("\n", " ") + ("..." if len(docs[i]) > 350 else ""))


if __name__ == "__main__":
    main()
