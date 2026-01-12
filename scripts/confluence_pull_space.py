# scripts/confluence_pull_space.py
"""
Pull Confluence Space -> JSON local

- Récupère les pages d'un space via GET /wiki/api/v2/pages?space-id=...
- Gère la pagination via cursor/_links.next (v2)
- Sauvegarde data/confluence/pages.json

Docs: GET /pages accepte space-id, cursor, limit et renvoie _links.next :contentReference[oaicite:6]{index=6}
"""

import os
import json
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv


def load_config():
    load_dotenv()
    base_url = os.getenv("CONF_BASE_URL", "").rstrip("/")
    email = os.getenv("CONF_EMAIL", "")
    token = os.getenv("CONF_API_TOKEN", "")
    space_id = os.getenv("CONF_SPACE_ID", "")

    if not base_url or not email or not token or not space_id:
        print(" Config manquante. Vérifiez votre .env.")
        return None

    return {"base_url": base_url, "email": email, "token": token, "space_id": space_id}


def headers():
    return {"Accept": "application/json"}


def main():
    cfg = load_config()
    if cfg is None:
        return

    os.makedirs("data/confluence", exist_ok=True)

    url = cfg["base_url"] + "/api/v2/pages"
    params = {
        "space-id": cfg["space_id"],
        "limit": 50,
        "body-format": "storage"
    }

    all_pages = []
    cursor = None

    while True:
        if cursor:
            params["cursor"] = cursor

        r = requests.get(
            url, headers=headers(), params=params,
            auth=HTTPBasicAuth(cfg["email"], cfg["token"])
        )

        if r.status_code != 200:
            print(" Erreur API:", r.status_code, r.text[:200])
            break

        data = r.json()
        results = data.get("results", [])
        all_pages.extend(results)

        next_link = (data.get("_links") or {}).get("next")
        if not next_link:
            break

        # next ressemble souvent à une URL relative contenant cursor=...
        # Exemple: "/wiki/api/v2/pages?cursor=XXXX"
        if "cursor=" in next_link:
            cursor = next_link.split("cursor=")[-1]
        else:
            cursor = None
            break

    out_path = "data/confluence/pages.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_pages, f, ensure_ascii=False, indent=2)

    print(f" {len(all_pages)} page(s) sauvegardée(s) dans {out_path}")


if __name__ == "__main__":
    main()
