import base64

from . import util


def get(clientId, clientSecret):
    token = base64.b64encode(f"{clientId}:{clientSecret}".encode("utf-8")).decode(
        "utf-8"
    )
    return util.apiPost("v2/account/oauth/token", f"Basic {token}")
