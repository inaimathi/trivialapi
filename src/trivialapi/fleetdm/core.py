import requests
import yaml


class FleetDM:
    def __init__(self, url, verify=None):
        self.url = url
        self.verify = verify

        self.email = None
        self.password = None
        self.token = None

    def login(self, email, password):
        resp = self.post("fleet/login", data={"email": email, "password": password})
        if resp.status_code == 200:
            self.email = email
            self.password = password
            self.token = resp.json()["token"]
            return True
        return False

    def relogin(self):
        return self.login(self.email, self.password)

    def logout(self):
        return self.post("fleet/logout")

    def _headers(self):
        if self.token is not None:
            return {"Authorization": f"Bearer {self.token}"}

    def _raw_get(self, endpoint, version):
        return requests.get(
            f"{self.url}/api/{version}/{endpoint}",
            headers=self._headers(),
            verify=self.verify,
        )

    def get(self, endpoint, version="v1"):
        resp = self._raw_get(endpoint, version)
        if resp.status_code == 401 and self.email:
            self.relogin()
            resp = self._raw_get(endpoint, version)

        if resp.status_code == 401:
            raise PermissionError()

        if 200 <= resp.status_code <= 299:
            return resp

        raise Exception(resp.status_code, resp.content)

    def _raw_post(self, endpoint, data, version):
        return requests.post(
            f"{self.url}/api/{version}/{endpoint}",
            headers=self._headers(),
            json=data,
            verify=self.verify,
        )

    def post(self, endpoint, data=None, version="v1"):
        resp = self._raw_post(endpoint, data, version)
        if resp.status_code == 401 and self.email:
            self.relogin()
            resp = self._raw_post(endpoint, data, version)

        if resp.status_code == 401:
            raise PermissionError()

        if 200 <= resp.status_code <= 299:
            return resp

        raise Exception(resp.status_code, resp.content)

    def standard_query_library(self):
        resp = requests.get(
            "https://raw.githubusercontent.com/fleetdm/fleet/main/docs/01-Using-Fleet/standard-query-library/standard-query-library.yml"
        )
        if resp.status_code == 200:
            return [
                yaml.safe_load(s)["spec"]
                for s in resp.content.decode("utf-8").split("---\n")
                if s
            ]

    def add_query(self, query, name, description, platform, interval=None):
        if interval is None:
            interval = 60 * 60
        return self.post(
            "fleet/queries",
            data={
                "query": query,
                "name": name,
                "description": description,
                "interval": interval,
                "platform": platform,
            },
        )

    def queries(self):
        return self.get("fleet/queries").json()["queries"]

    def query_report(self, query):
        return self.get(f"fleet/queries/{query['id']}/report").json()["results"]

    def hosts(self):
        return self.get("fleet/hosts").json()["hosts"]

    def host_livequery(self, host, query_string):
        return self.post(
            f"fleet/hosts/{host['id']}/query", data={"query": query_string}
        )

    def host_encrypted(self, host):
        if host["platform_like"] == "windows":
            query = "SELECT 1 FROM bitlocker_info WHERE drive_letter='C:' AND protection_status=1;"
        elif host["platform_like"] == "darwin":
            query = """SELECT 1 FROM disk_encryption WHERE user_uuid IS NOT "" AND filevault_status = 'on' LIMIT 1;"""
        elif host["platform_like"] == "debian":
            query = "SELECT 1 FROM disk_encryption WHERE encrypted=1 AND name LIKE '/dev/dm-1';"
        return self.host_livequery(host, query)

    def enroll_secret(self):
        return self.get("fleet/spec/enroll_secret").json()["spec"]["secrets"][0][
            "secret"
        ]

    def build_commands(self):
        url = self.url
        secret = self.enroll_secret()
        return [
            f"fleetctl package --type={tp} --enable-scripts --fleet-desktop --fleet-url={url} --enroll-secret={secret}"
            for tp in ["pkg", "msi", "deb", "rpm"]
        ]

    def add_user(self, email, password):
        return self.post(
            "fleet/users/admin",
            data={
                "email": email,
                "name": email.split("@")[0],
                "password": password,
                "api_only": True,
                "global_role": "admin",
                "admin_forced_password_reset": False,
            },
        ).json()

    def add_initial_user(self, email, password, org_name, fleet_url=None):
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            with p.firefox.launch() as browser:
                try:
                    page = browser.new_page()
                    page.goto(self.url)
                    print("Filling out user...")
                    page.query_selector("#name").fill(email.split("@")[0])
                    page.query_selector("#email").fill(email)
                    page.query_selector("#password").fill(password)
                    page.query_selector("#password_confirmation").fill(password)
                    page.query_selector('button[type="submit"]').click()

                    print("Filling out org...")
                    page.query_selector("#org_name").fill(org_name)
                    page.query_selector('button[type="submit"]').click()

                    if fleet_url is not None:
                        print(f"Using specified URL {fleet_url}...")
                        page.query_selector("#server_url").fill(fleet_url)
                    else:
                        print("Accepting default URL...")
                    page.query_selector('button[type="submit"]').click()

                    print("Confirming...")
                    page.query_selector('button[type="submit"]').click()

                    return True
                except Exception as e:
                    print(f"FAILED {e}")
                    return False

    def users(self):
        return self.get("fleet/users").json()["users"]
