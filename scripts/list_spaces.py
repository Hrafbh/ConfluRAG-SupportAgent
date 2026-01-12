import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()

base_url = os.getenv("CONF_BASE_URL", "").rstrip("/")   # ex: https://YOUR_SITE.atlassian.net/wiki
email = os.getenv("CONF_EMAIL", "")
token = os.getenv("CONF_API_TOKEN", "")

url = base_url + "/api/v2/spaces"
params = {"limit": 100}

r = requests.get(url, params=params, headers={"Accept": "application/json"},
                 auth=HTTPBasicAuth(email, token))

print("HTTP:", r.status_code)
if r.status_code != 200:
    print(r.text)
else:
    data = r.json()
    for s in data.get("results", []):
        print("-", s.get("id"), "|", s.get("key"), "|", s.get("name"))
