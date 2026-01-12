# scripts/confluence_sync_kb.py
"""
Sync KB locale -> Confluence (v2 API)

- Lit les fichiers .md dans ./kb
- Convertit Markdown -> HTML (storage)
- Crée la page si elle n'existe pas, sinon la met à jour

API Confluence v2 utilisée :
- GET /wiki/api/v2/pages?space-id=...&title=...   (trouver une page)  (params: space-id, title, cursor, limit)
- POST /wiki/api/v2/pages                         (créer)
- GET /wiki/api/v2/pages/{id}                     (récupérer version.number)
- PUT /wiki/api/v2/pages/{id}                     (mettre à jour avec version.number+1)

Docs Atlassian:
- Pages v2: création / update / params title & space-id :contentReference[oaicite:2]{index=2}
- Auth basic (email + API token) :contentReference[oaicite:3]{index=3}
"""

import os
import json
import re
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
from markdown import markdown


def load_config():
    load_dotenv()

    base_url = os.getenv("CONF_BASE_URL", "").rstrip("/")
    email = os.getenv("CONF_EMAIL", "")
    token = os.getenv("CONF_API_TOKEN", "")
    space_id = os.getenv("CONF_SPACE_ID", "")
    parent_id = os.getenv("CONF_PARENT_PAGE_ID", "")

    if not base_url or not email or not token or not space_id:
        print(" Config manquante. Vérifiez votre .env (CONF_BASE_URL, CONF_EMAIL, CONF_API_TOKEN, CONF_SPACE_ID).")
        return None

    return {
        "base_url": base_url,
        "email": email,
        "token": token,
        "space_id": space_id,
        "parent_id": parent_id,
    }


def get_headers():
    return {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }


def read_markdown_file(path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    # Nettoyage simple (Windows / BOM)
    text = text.lstrip("\ufeff")              # retire BOM si présent
    text = text.replace("\r\n", "\n")         # CRLF -> LF
    text = text.replace("\r", "\n")           # sécurité

    return text


def split_front_matter(text):
    """
    Accepte:
    - CRLF / LF
    - éventuelles lignes vides avant le front-matter
    """
    text = text.lstrip()  # enlève lignes vides au début

    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.DOTALL)
    if not m:
        return "", text
    return m.group(1), m.group(2)


def get_front_value(front, key):
    # ex: id: KB-001
    m = re.search(rf"^{key}:\s*(.+)$", front, re.MULTILINE)
    if not m:
        return ""
    return m.group(1).strip().strip('"').strip("'")


def md_to_storage_html(md_body):
    # conversion simple Markdown -> HTML (Confluence "storage")
    # Pour un POC/portfolio, c'est suffisant.
    return markdown(md_body, extensions=["fenced_code", "tables"])


def build_page_html(kb_id, title, category, tags, body_html):
    tags_str = ", ".join([t.strip() for t in tags.split(",") if t.strip()]) if tags else ""
    meta_html = f"""
    <p><strong>ID:</strong> {kb_id}<br/>
    <strong>Category:</strong> {category}<br/>
    <strong>Tags:</strong> {tags_str}</p>
    <hr/>
    """
    return meta_html + body_html


def find_page_by_title(cfg, title):
    """
    GET /wiki/api/v2/pages?space-id=...&title=...&limit=1
    """
    url = cfg["base_url"] + "/api/v2/pages"
    params = {
        "space-id": cfg["space_id"],
        "title": title,
        "limit": 1,
    }

    r = requests.get(url, headers=get_headers(), params=params,
                     auth=HTTPBasicAuth(cfg["email"], cfg["token"]))
    if r.status_code != 200:
        print(" Erreur find_page_by_title:", r.status_code, r.text[:200])
        return None

    data = r.json()
    results = data.get("results", [])
    if not results:
        return None
    return results[0]  # contient id, title, version, etc.


def get_page_by_id(cfg, page_id):
    url = cfg["base_url"] + f"/api/v2/pages/{page_id}"
    r = requests.get(url, headers=get_headers(),
                     auth=HTTPBasicAuth(cfg["email"], cfg["token"]))
    if r.status_code != 200:
        print(" Erreur get_page_by_id:", r.status_code, r.text[:200])
        return None
    return r.json()


def create_page(cfg, title, html_value):
    """
    POST /wiki/api/v2/pages
    Body: spaceId (required), status, title, parentId (optional), body{representation,value}
    """
    url = cfg["base_url"] + "/api/v2/pages"

    payload = {
        "spaceId": str(cfg["space_id"]),
        "status": "current",
        "title": title,
        "body": {
            "representation": "storage",
            "value": html_value
        }
    }

    if cfg["parent_id"]:
        payload["parentId"] = str(cfg["parent_id"])

    r = requests.post(url, headers=get_headers(), data=json.dumps(payload),
                      auth=HTTPBasicAuth(cfg["email"], cfg["token"]))
    return r


def update_page(cfg, page_id, title, html_value, current_version_number):
    """
    PUT /wiki/api/v2/pages/{id}
    Body requiert: id, status, title, body, version{number,message}
    """
    url = cfg["base_url"] + f"/api/v2/pages/{page_id}"

    payload = {
        "id": str(page_id),
        "status": "current",
        "title": title,
        "body": {
            "representation": "storage",
            "value": html_value
        },
        "version": {
            "number": int(current_version_number) + 1,
            "message": "KB sync (local -> Confluence)"
        }
    }

    r = requests.put(url, headers=get_headers(), data=json.dumps(payload),
                     auth=HTTPBasicAuth(cfg["email"], cfg["token"]))
    return r


def list_local_md_files(kb_root="kb"):
    files = []
    for root, _, filenames in os.walk(kb_root):
        for name in filenames:
            if name.lower().endswith(".md"):
                files.append(os.path.join(root, name))
    # tri simple pour avoir un ordre stable
    files.sort()
    return files


def main():
    cfg = load_config()
    if cfg is None:
        return

    files = list_local_md_files("kb")
    if not files:
        print(" Aucun fichier .md trouvé dans ./kb")
        return

    print(f" {len(files)} fichier(s) Markdown trouvé(s). Début sync...\n")

    for path in files:
        text = read_markdown_file(path)
        front, md_body = split_front_matter(text)

        kb_id = get_front_value(front, "id") or "UNKNOWN"
        title = get_front_value(front, "title") or os.path.basename(path)
        category = get_front_value(front, "category")
        tags = get_front_value(front, "tags")

        body_html = md_to_storage_html(md_body)
        html_value = build_page_html(kb_id, title, category, tags, body_html)

        file_title = os.path.basename(path)

        existing = find_page_by_title(cfg, title)

        # Fallback : si une page a déjà été créée avec le nom du fichier,
        # on la retrouve et on la renomme lors du UPDATE (pas de doublons)
        if existing is None and title != file_title:
            existing = find_page_by_title(cfg, file_title)
            if existing:
                print(f"ℹ Found existing page by filename, will rename -> {title}")


        if existing is None:
            # Create
            resp = create_page(cfg, title, html_value)
            if resp.status_code in (200, 201):
                print(f" CREATED  | {kb_id} | {title}")
            else:
                print(f" CREATE FAILED | {kb_id} | {title} | {resp.status_code} | {resp.text[:200]}")
        else:
            # Update
            page_id = existing.get("id")
            page_data = get_page_by_id(cfg, page_id)
            if not page_data:
                print(f" UPDATE SKIPPED | {kb_id} | {title} (cannot read page by id)")
                continue

            version = page_data.get("version", {})
            current_version_number = version.get("number", 1)

            resp = update_page(cfg, page_id, title, html_value, current_version_number)
            if resp.status_code == 200:
                print(f"  UPDATED  | {kb_id} | {title} (v{current_version_number} -> v{current_version_number + 1})")
            else:
                print(f" UPDATE FAILED | {kb_id} | {title} | {resp.status_code} | {resp.text[:200]}")

    print("\n Sync terminé.")


if __name__ == "__main__":
    main()
