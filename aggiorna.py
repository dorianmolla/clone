import requests, os

APP_KEY = os.environ["DBX_KEY"]
APP_SECRET = os.environ["DBX_SECRET"]
REFRESH = os.environ["DBX_REFRESH"]
URL = os.environ["RENTRY_URL"]

tok = requests.post("https://api.dropbox.com/oauth2/token",
    data={"grant_type": "refresh_token", "refresh_token": REFRESH},
    auth=(APP_KEY, APP_SECRET), timeout=30).json()["access_token"]

r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
r.raise_for_status()

requests.post("https://content.dropboxapi.com/2/files/upload",
    headers={
        "Authorization": f"Bearer {tok}",
        "Dropbox-API-Arg": '{"path": "/file.txt", "mode": "overwrite"}',
        "Content-Type": "application/octet-stream",
    },
    data=r.content, timeout=30).raise_for_status()
