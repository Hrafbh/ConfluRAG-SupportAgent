# scripts/confluence_sync_kb.py
"""
Sync KB locale -> Confluence (v2 API)

"""

import os
import json
import re
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
from markdown import markdown


# ----------------------------
# Config
# ----------------------------

CATEGORY_PARENTS_PATH = "config/category_parents.json"


def load_config():
    load_dotenv()

    base_url = os.getenv("CONF_BASE_URL", "").rstrip("/")
    email = os.getenv("CONF_EMAIL", "")
    token = os.getenv("CONF_API_TOKEN", "")
    space_id = os.getenv("CONF_SPACE_ID", "")

    # Page racine "Index" (RoutePilot Knowledge Base)
    root_page_id = os.getenv("CONF_ROOT_PAGE_ID", "").strip()

    if not base_url or not email or not token or not space_id:
        print(" Config manquante. Vérifiez votre .env (CONF_BASE_URL, CONF_EMAIL, CONF_API_TOKEN, CONF_SPACE_ID).")
        return None

    if not root_page_id:
        print(" CONF_ROOT_PAGE_ID non défini. Les pages seront créées à la racine du space si category non trouvée.")

    return {
        "base_url": base_url,
        "email": email,
        "token": token,
        "space_id": str(space_id),
        "root_page_id": root_page_id,
    }


def load_category_parents(path=CATEGORY_PARENTS_PATH):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        # sécuriser en string
        return {str(k): str(v) for k, v in data.items()}
    except FileNotFoundError:
        print(f" Fichier introuvable: {path} (les pages iront sous CONF_ROOT_PAGE_ID si défini).")
        return {}
    except json.JSONDecodeError:
        print(f" JSON invalide dans {path}")
        return {}


def get_headers():
    return {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }


# ----------------------------
# Markdown parsing
# ----------------------------

def read_markdown_file(path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    # Nettoyage Windows / BOM
    text = text.lstrip("\ufeff")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return text


def split_front_matter(text):
    """
    Front matter:
    ---
    key: value
    ---
    body...
    """
    text = text.lstrip()  # enlève lignes vides au début
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.DOTALL)
    if not m:
        return "", text
    return m.group(1), m.group(2)


def get_front_value(front, key):
    """
    Récupère une ligne du front-matter:
    key: value
    key: "value"
    """
    m = re.search(rf"^\s*{re.escape(key)}\s*:\s*(.+?)\s*$", front, re.MULTILINE)
    if not m:
        return ""
    v = m.group(1).strip()
    # enlever quotes simples/doubles si value simple
    if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
        v = v[1:-1].strip()
    return v


def parse_tags(raw_tags):
    """
    Supporte:
    tags: ["a", "b"]   (JSON list sur une ligne)
    tags: a, b, c      (texte)
    """
    if not raw_tags:
        return []

    raw = raw_tags.strip()

    # cas JSON list
    if raw.startswith("[") and raw.endswith("]"):
        try:
            arr = json.loads(raw)
            return [str(x).strip() for x in arr if str(x).strip()]
        except Exception:
            pass

    # fallback: split simple
    return [t.strip() for t in raw.split(",") if t.strip()]


def md_to_storage_html(md_body):
    return markdown(md_body, extensions=["fenced_code", "tables"])


def build_page_html(kb_id, category, tags_list, body_html):
    tags_str = ", ".join(tags_list) if tags_list else ""
    meta_html = f"""
    <p><strong>ID:</strong> {kb_id}<br/>
    <strong>Category:</strong> {category}<br/>
    <strong>Tags:</strong> {tags_str}</p>
    <hr/>
    """
    return meta_html + body_html


# ----------------------------
# Confluence API helpers
# ----------------------------

def find_page_by_title(cfg, title):
    url = cfg["base_url"] + "/api/v2/pages"
    params = {"space-id": cfg["space_id"], "title": title, "limit": 1}

    r = requests.get(url, headers=get_headers(), params=params,
                     auth=HTTPBasicAuth(cfg["email"], cfg["token"]))
    if r.status_code != 200:
        print(" Erreur find_page_by_title:", r.status_code, r.text[:200])
        return None

    data = r.json()
    results = data.get("results", [])
    return results[0] if results else None


def get_page_by_id(cfg, page_id):
    url = cfg["base_url"] + f"/api/v2/pages/{page_id}"
    r = requests.get(url, headers=get_headers(),
                     auth=HTTPBasicAuth(cfg["email"], cfg["token"]))
    if r.status_code != 200:
        print(" Erreur get_page_by_id:", r.status_code, r.text[:200])
        return None
    return r.json()


def create_page(cfg, title, html_value, parent_id=""):
    """
    POST /api/v2/pages
    parentId optionnel (pour ranger sous une catégorie)
    """
    url = cfg["base_url"] + "/api/v2/pages"

    payload = {
        "spaceId": str(cfg["space_id"]),
        "status": "current",
        "title": title,
        "body": {"representation": "storage", "value": html_value},
    }

    if parent_id:
        payload["parentId"] = str(parent_id)

    r = requests.post(url, headers=get_headers(), data=json.dumps(payload),
                      auth=HTTPBasicAuth(cfg["email"], cfg["token"]))
    return r


def update_page(cfg, page_id, title, html_value, current_version_number):
    """
    PUT /api/v2/pages/{id}
    (ne déplace pas la page, met juste à jour title/body/version)
    """
    url = cfg["base_url"] + f"/api/v2/pages/{page_id}"

    payload = {
        "id": str(page_id),
        "status": "current",
        "title": title,
        "body": {"representation": "storage", "value": html_value},
        "version": {
            "number": int(current_version_number) + 1,
            "message": "KB sync (local -> Confluence)",
        },
    }

    r = requests.put(url, headers=get_headers(), data=json.dumps(payload),
                     auth=HTTPBasicAuth(cfg["email"], cfg["token"]))
    return r


# ----------------------------
# Local files
# ----------------------------

def list_local_md_files(kb_root="kb"):
    files = []
    for root, _, filenames in os.walk(kb_root):
        for name in filenames:
            if name.lower().endswith(".md"):
                files.append(os.path.join(root, name))
    files.sort()
    return files


# ----------------------------
# Main
# ----------------------------

def main():
    cfg = load_config()
    if cfg is None:
        return

    category_parents = load_category_parents()
    root_parent_id = cfg.get("root_page_id", "")

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
        tags_raw = get_front_value(front, "tags")
        tags_list = parse_tags(tags_raw)

        body_html = md_to_storage_html(md_body)
        html_value = build_page_html(kb_id, category, tags_list, body_html)

        # parent cible (Choix B)
        target_parent_id = category_parents.get(category, "") or root_parent_id

        file_title = os.path.basename(path)
        existing = find_page_by_title(cfg, title)

        # Fallback: si déjà créée avec le nom du fichier
        if existing is None and title != file_title:
            existing = find_page_by_title(cfg, file_title)
            if existing:
                print(f" Found existing page by filename, will rename -> {title}")

        if existing is None:
            resp = create_page(cfg, title, html_value, parent_id=target_parent_id)
            if resp.status_code in (200, 201):
                where = f"(parent={category})" if category else "(no category)"
                print(f" CREATED  | {kb_id} | {title} {where}")
            else:
                print(f" CREATE FAILED | {kb_id} | {title} | {resp.status_code} | {resp.text[:200]}")
        else:
            page_id = existing.get("id")
            page_data = get_page_by_id(cfg, page_id)
            if not page_data:
                print(f" UPDATE SKIPPED | {kb_id} | {title} (cannot read page by id)")
                continue

            version = page_data.get("version", {})
            current_version_number = version.get("number", 1)

            resp = update_page(cfg, page_id, title, html_value, current_version_number)
            if resp.status_code == 200:
                print(f" UPDATED  | {kb_id} | {title} (v{current_version_number} -> v{current_version_number + 1})")
            else:
                print(f" UPDATE FAILED | {kb_id} | {title} | {resp.status_code} | {resp.text[:200]}")

    print("\n Sync terminé.")


if __name__ == "__main__":
    main()
