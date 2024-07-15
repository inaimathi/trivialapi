import json
import os

from . import util


class TODA:
    def __init__(self):
        pass

    @classmethod
    def from_file(cls, path):
        pass

    def createTwin(self):
        pass

    def getTwin(self):
        pass


class Twin:
    def __init__(self, id, hostname, key, balances):
        self.id = id
        self.hostname = hostname
        self.key = key
        self.balances = balances
        pass

    @classmethod
    def from_dict(cls, dct):
        res = Twin(**dct)
        return res

    @classmethod
    def from_file(cls, path):
        with open(os.path.expanduser(path), "r") as f:
            return cls.from_dict(json.loads(f.read()))

    def mint(self, quantity, display_precision=0, minting_info=None):
        return util.apiPost(
            f"https://{self.hostname}/dq?apiKey={self.key}",
            None,
            {
                "quantity": quantity,
                "displayPrecision": display_precision,
                "mintingInfo": minting_info,
            },
        )

    def transfer(self, root, amount, destination_hostname):
        return util.apiPost(
            f"https://{self.hostname}/dq/{root}/transfer?apiKey={self.key}",
            None,
            {"amount": amount, "destination": destination_hostname},
        )

    def balance(self):
        return util.apiGet(f"https://{self.hostname}/dq?apiKey={self.key}", None)
