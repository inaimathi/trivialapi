from . import util


def create(accessToken, dq):
    return util.apiPost("v2/twin", accessToken, {"dq": dq})


def get(accessToken, twinId):
    return util.apiGet(f"v2/twin/{twinId}", accessToken)


def getTwins(accessToken):
    return util.apiGet("v2/twins", accessToken)
