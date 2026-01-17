# scripts/rag_build_index.py
"""
Build un index Chroma (vector store) à partir de data/confluence/pages.json

- Convertit HTML (storage Confluence) -> texte
- Chunking simple (taille fixe + overlap)
- Embeddings via sentence-transformers
- Stockage persistant dans: data/index/chroma

Usage:
  python scripts/rag_build_index.py
"""

import os
import json
import re
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from tqdm import tqdm

import os
os.environ["ANONYMIZED_TELEMETRY"] = "False"

import chromadb
from sentence_transformers import SentenceTransformer


PAGES_JSON_PATH = "data/confluence/pages_full.json"
CHROMA_DIR = "data/index/chroma"
COLLECTION_NAME = "routepilot_kb"

CHUNK_SIZE = 550
CHUNK_OVERLAP = 120


def html_to_text(html):
    if not html:
        return ""
    soup = BeautifulSoup(html, "lxml")
    text = soup.get_text("\n")
    # nettoyage simple
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def make_chunks(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    if not text:
        return []

    chunks = []
    start = 0
    n = len(text)

    while start < n:
        end = min(start + chunk_size, n)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        if end == n:
            break
        start = end - overlap  # overlap

    return chunks


def safe_get(d, *keys, default=None):
    cur = d
    for k in keys:
        if not isinstance(cur, dict) or k not in cur:
            return default
        cur = cur[k]
    return cur


def build_full_url(base_url, webui):
    # base_url doit être "https://xxx.atlassian.net/wiki"
    if not webui:
        return ""
    if webui.startswith("http"):
        return webui
    return base_url.rstrip("/") + webui

def extract_category(text):
    m = re.search(r"Category:\s*([^\n]+)", text, re.IGNORECASE)
    return m.group(1).strip() if m else ""

def extract_tags(text):
    m = re.search(r"Tags:\s*(\[[^\]]*\])", text, re.IGNORECASE)
    return m.group(1).strip() if m else ""



def main():
    load_dotenv()
    base_url = os.getenv("CONF_BASE_URL", "").rstrip("/")

    if not os.path.exists(PAGES_JSON_PATH):
        print(f" Fichier introuvable: {PAGES_JSON_PATH}")
        print("Lancez d'abord: python scripts/confluence_pull_space.py")
        return

    with open(PAGES_JSON_PATH, "r", encoding="utf-8") as f:
        pages = json.load(f)

    if not pages:
        print(" pages.json est vide.")
        return

    os.makedirs(CHROMA_DIR, exist_ok=True)

    # Chroma persistent
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = client.get_or_create_collection(name=COLLECTION_NAME)

    # Embeddings (local)
    model_name = os.getenv("RAG_EMBED_MODEL", "all-MiniLM-L6-v2")
    model = SentenceTransformer(model_name)

    print(f" Pages à indexer: {len(pages)}")
    print(f" Embedding model: {model_name}")
    print(f" Chroma dir: {CHROMA_DIR}\n")

    total_added = 0

    for page in tqdm(pages, desc="Indexing pages"):
        page_id = str(page.get("id", ""))
        title = page.get("title", "")
        # v2 pages list: body may exist depending on body-format
        storage_html = safe_get(page, "body", "storage", "value", default="")

        # fallback : si body absent, on indexe quand même le peu qu'on a
        if not storage_html:
            storage_html = safe_get(page, "body", "value", default="")

        text = html_to_text(storage_html)


        # Si votre sync a mis un bloc meta HTML ("ID: KB-xxx"), on peut tenter de le détecter
        kb_id = ""
        m = re.search(r"\bKB-\d{3}\b", text)
        if m:
            kb_id = m.group(0)

        # URL (si présente)
        webui = safe_get(page, "_links", "webui", default="")
        url = build_full_url(base_url, webui)

        # Chunking
        chunks = make_chunks(text)
        if not chunks:
            continue

        # Embeddings
        vectors = model.encode(chunks, show_progress_bar=False)

        # IDs uniques par chunk
        ids = []
        metadatas = []
        documents = []

        category = extract_category(text)
        tags = extract_tags(text)

        for i, chunk in enumerate(chunks):
            chunk_id = f"{page_id}__chunk_{i}"
            ids.append(chunk_id)
            documents.append(chunk)
            metadatas.append({
                "page_id": page_id,
                "kb_id": kb_id,
                "title": title,
                "url": url,
                "category": category,
                "tags": tags,
                "chunk_index": i,
            })


        # Supprime uniquement les chunks de cette page (propre, sans warnings)
        try:
            collection.delete(where={"page_id": page_id})
        except Exception:
            pass

        collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=[v.tolist() for v in vectors],
        )

        total_added += len(ids)

    print(f"\n Index terminé. Chunks ajoutés: {total_added}")
    print("Prochaine étape: python scripts/rag_ask.py")


if __name__ == "__main__":
    main()
