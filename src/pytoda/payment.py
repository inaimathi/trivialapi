from . import util


def valid(accessToken, hash, nonce, timestamp):
    return util.apiPost(
        f"v2/payment/{hash}/validate", {"nonce": nonce, "timestamp": timestamp}
    )
