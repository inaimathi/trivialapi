from . import util


def valid(accessToken, hash, nonce, timestamp):
    return util.apiPost(
        f"v2/payment/{hash}/validate",
        accessToken,
        {"nonce": nonce, "timestamp": timestamp},
    )
