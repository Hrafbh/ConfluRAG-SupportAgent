import os
import json
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
from tqdm import tqdm

def load_config():
    load_dotenv()
    base_url = os.getenv("CONF_BASE_URL", "").rstrip("/")
    email = os.getenv("CONF_EMAIL", "")
    token = os.getenv("CONF_API_TOKEN", "")
    space_id = os.getenv("CONF_SPACE_ID", "")
    if not base_url or not email or not token or not space_id:
        print(" Config manquante (.env).")
        return None
    return {"base_url": base_url, "email": email, "token": token, "space_id": space_id}

def headers():
    return {"Accept": "application/json"}

def get_pages_list(cfg):
    url = cfg["base_url"] + "/api/v2/pages"
    params = {"space-id": cfg["space_id"], "limit": 50}
    pages = []
    cursor = None

    while True:
        if cursor:
            params["cursor"] = cursor

        r = requests.get(url, params=params, headers=headers(),
                         auth=HTTPBasicAuth(cfg["email"], cfg["token"]))
        if r.status_code != 200:
            print(" Erreur list pages:", r.status_code, r.text[:200])
            break

        data = r.json()
        pages.extend(data.get("results", []))

        next_link = (data.get("_links") or {}).get("next")
        if not next_link or "cursor=" not in next_link:
            break
        cursor = next_link.split("cursor=")[-1]

    return pages

def get_page_full(cfg, page_id):
    url = cfg["base_url"] + f"/api/v2/pages/{page_id}"
    params = {"body-format": "storage"}
    r = requests.get(url, params=params, headers=headers(),
                     auth=HTTPBasicAuth(cfg["email"], cfg["token"]))
    if r.status_code != 200:
        return None
    return r.json()

def main():
    cfg = load_config()
    if cfg is None:
        return

    os.makedirs("data/confluence", exist_ok=True)

    pages = get_pages_list(cfg)
    if not pages:
        print(" Aucun résultat.")
        return

    full_pages = []
    for p in tqdm(pages, desc="Pull full pages"):
        pid = p.get("id")
        if not pid:
            continue
        full = get_page_full(cfg, pid)
        if full:
            full_pages.append(full)

    out_path = "data/confluence/pages_full.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(full_pages, f, ensure_ascii=False, indent=2)

    print(f" {len(full_pages)} pages sauvegardées dans {out_path}")

if __name__ == "__main__":
    main()
