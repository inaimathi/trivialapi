import json
import os

from . import commodity, payment, token, twin, util


class TODA:
    def __init__(self, id, created_at, updated_at, secrets):
        self.id = id
        self.created_at = created_at
        self.updated_at = updated_at
        self.secrets = secrets
        client = [s for s in secrets if "client_id" in s and "client_secret" in s][0]
        self.client_id = client["client_id"]
        self.client_secret = client["client_secret"]
        self.bump()

    def bump(self):
        self.token = token.get(self.client_id, self.client_secret)[0]["access_token"]

    def publicSecret(self):
        try:
            return [s for s in self.secrets if "public_secret" in s][0]["public_secret"]
        except IndexError:
            return None

    @classmethod
    def fresh(cls):
        dct, error = util.apiPost("v2/account", None)
        if error is None:
            with open(f"toda-account-{dct['id']}.json", "w") as f:
                f.write(json.dumps(dct))
            return cls.from_dict(dct)

    @classmethod
    def from_dict(cls, dct):
        res = cls(**dct)
        return res

    @classmethod
    def from_file(cls, path):
        with open(os.path.expanduser(path), "r") as f:
            return cls.from_dict(json.loads(f.read()))

    def createTwin(self, dq=None):
        if dq is None:
            dq = util.PROD_DQ
        res = twin.create(self.token, dq)[0]
        if res is not None:
            with open(f"twin-{res['id']}.json", "w") as f:
                f.write(json.dumps(res))
            return Twin.from_dict(res)

    def validPayment(self, payment_dict):
        self.bump()
        return payment.valid(
            self.token,
            payment_dict["hash"],
            payment_dict["nonce"],
            payment_dict["timestamp"],
        )

    # def getTwin(self):
    #     pass


class Twin:
    def __init__(self, id, hostname, key, balances):
        self.id = id
        self.hostname = hostname
        self.key = key
        self.balances = balances
        pass

    @classmethod
    def from_dict(cls, dct):
        res = cls(**dct)
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
        )[0]

    def createCommodity(self, toda, value, metadata=None, dq=None):
        if metadata is None:
            metadata = ""
        if dq is None:
            dq = util.PROD_DQ
        toda.bump()
        return commodity.create(toda.token, self.id, value, metadata, dq)

    def transfer(self, root, amount, destination_hostname):
        return util.apiPost(
            f"https://{self.hostname}/dq/{root}/transfer?apiKey={self.key}",
            None,
            {"amount": amount, "destination": destination_hostname},
        )[0]

    def transfer_file(self, filehash, destination_hostname, metadata=None):
        dat = {"destination": destination_hostname}
        if metadata is not None:
            dat["metadata"] = metadata
        url = f"https://{self.hostname}/files/{filehash}/transfer?apiKey={self.key}"
        return util.apiPost(url, None, dat)

    def balance(self):
        return util.apiGet(f"https://{self.hostname}/dq?apiKey={self.key}", None)[0]

    def binder(self):
        return util.apiGet(f"https://{self.hostname}/binder?apiKey={self.key}", None)[0]
