from os import environ as ENV

import requests

STAGING_DQ = "410ddbac7c8a259da8dfcc5f55bcb28b77d29be9c540a2c23444b416d584801c30"
BASE_URL = ENV.get("API_BASE_URL", "https://pay.stage.m.todaq.net").rstrip("/")


def url(path, base=None):
    if path.startswith("http"):
        return path

    if base is None:
        base = BASE_URL

    return f"{base.rstrip('/')}/{path.lstrip('/')}"


def headers(accessToken):
    hdrs = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    if accessToken is None:
        return hdrs
    elif accessToken.startswith("Basic") or accessToken.startswith("Bearer"):
        auth = accessToken
    else:
        auth = f"Bearer {accessToken}"

    hdrs["Authorization"] = auth
    return hdrs


def apiGet(path, accessToken):
    resp = requests.get(url(path), headers=headers(accessToken))
    if 299 >= resp.status_code >= 200:
        return resp.json(), None
    return None, resp


def apiPost(path, accessToken, data=None):
    resp = requests.post(url(path), headers=headers(accessToken), json=data)
    if 299 >= resp.status_code >= 200:
        return resp.json(), None
    return None, resp
