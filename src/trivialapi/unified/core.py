import logging

import requests


def getLogger(name, level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger


logger = getLogger("trivialapi::unified", level=logging.DEBUG)


def _request(token):
    def req(path, method=None, params=None):
        if method is None:
            method = "GET"
        if params is not None and not method == "POST":
            json_body = None
            param_str = "&".join([f"{k}={v}" for k, v in params.items()])
            param_str = "?" + param_str
        else:
            json_body = params
            param_str = ""
        url = f"https://api.unified.to/{path}{param_str}"
        resp = requests.request(
            url=url,
            method=method,
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {token}",
            },
            json=json_body,
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

    return req


def _paginated(req):
    def pgreq(path, params=None):
        paging = {"limit": 100, "offset": 0}
        page = []
        while True:
            page = req(path, params={**(params or {}), **paging})
            for item in page:
                yield item
            if not len(page) == paging["limit"]:
                return
            paging["offset"] += paging["limit"]

    return pgreq


class Connection:
    def __init__(self, req, connection_id):
        self.req = req
        self.connection_id = connection_id

    def info(self):
        return self.req(f"unified/connection/{self.connection_id}")

    def delete(self):
        return self.req(f"unified/connection/{self.connection_id}", method="DELETE")


class Messaging:
    def __init__(self, req, connection_id):
        self.req = req
        self.pgreq = _paginated(req)
        self.connection_id = connection_id

    def channels(self):
        return self.req(f"messaging/{self.connection_id}/channel")

    def all_channels(self):
        return self.pgreq(f"messaging/{self.connection_id}/channel")

    def messages(self, channel_id):
        return self.req(
            f"messaging/{self.connection_id}/message", params={"channel_id": channel_id}
        )

    def all_messages(self, channel_id):
        return self.pgreq(
            f"messaging/{self.connection_id}/message",
            params={"channel_id": channel_id},
        )

    def send(self, channel_id, subject, message, message_html=None):
        return self.req(
            f"messaging/{self.connection_id}/message",
            method="POST",
            params={
                "channel_id": channel_id,
                "subject": subject,
                "message": message,
                "message_html": message_html,
            },
        )
        return None


class Task:
    def __init__(self, req, connection_id):
        self.req = req
        self.pgreq = _paginated(req)
        self.connection_id = connection_id

    def projects(self):
        return self.req(f"task/{self.connection_id}/project")

    def all_projects(self):
        return self.pgreq(f"task/{self.connection_id}/project")

    def tasks(self):
        return self.req(f"task/{self.connection_id}/task")

    def all_tasks(self):
        return self.pgreq(f"task/{self.connection_id}/task")


class HRIS:
    def __init__(self, req, connection_id):
        self.req = req
        self.pgreq = _paginated(req)
        self.connection_id = connection_id

    def employees(self):
        return self.req(f"hris/{self.connection_id}/employee")

    def all_employees(self):
        return self.pgreq(f"hris/{self.connection_id}/employee")


class KMS:
    def __init__(self, req, connection_id):
        self.req = req
        self.pgreq = _paginated(req)

    def spaces(self):
        return self.req(f"kms/{self.connection_id}/space")

    def all_spaces(self):
        return self.pgreq(f"kms/{self.connection_id}/space")

    def pages(self):
        return self.req(f"kms/{self.connection_id}/page")

    def all_pages(self):
        return self.pgreq(f"kms/{self.connection_id}/page")


class Unified:
    def __init__(self, token):
        self.token = token
        self.req = _request(token)

    def connection(self, connection_id):
        return Connection(self.req, connection_id)

    def messaging(self, connection_id):
        return Messaging(self.req, connection_id)

    def task(self, connection_id):
        return Task(self.req, connection_id)

    def hris(self, connection_id):
        return HRIS(self.req, connection_id)

    def kms(self, connection_id):
        return KMS(self.req, connection_id)

    def passthrough(self, connection_id, path, method="GET", params=None):
        return self.req(f"passthrough/{connection_id}/{path}", method, params)
