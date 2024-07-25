from . import util


def create(accessToken, twinId, cost, descriptor, dq):
    return util.apiPost(
        "v2/commodity",
        accessToken,
        {"cost": cost, "descriptor": descriptor, "dq": dq, "twin_id": twinId},
    )
