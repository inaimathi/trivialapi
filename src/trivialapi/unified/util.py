import requests


def req(logger, token, method, path, params=None):
    if method is None:
        method = "GET"
    if params is not None:
        param_str = "&".join([f"{k}={v}" for k, v in params.items()])
        param_str = "?" + param_str
    else:
        param_str = ""
    url = f"https://api.unified.to/{path}{param_str}"
    resp = requests.request(
        url=url,
        method=method,
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {token}",
        },
    )
    if resp.status_code == 200:
        try:
            return resp.json()
        except requests.exceptions.JSONDecodeError:
            if not path.endswith("logs"):
                logger.error(f"non-JSON value returned from {path}")
            return resp.content.decode("utf-8")
    logger.error(f"unified request failed {path}")
    return None
