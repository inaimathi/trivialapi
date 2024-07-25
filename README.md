# TrivialAPI
_(A set of `requests`-based, trivial API bindings for things I use)_

## FleetDM

- Partial implementation of the [FleetDM API](https://fleetdm.com/docs/rest-api/rest-api)

#### Basic usage
```
(env-whatever) $ pip install trivialapi
Collecting trivialapi
...snip...
(env-whatever) $ python
Python 3.10.12 (main, Mar 22 2024, 16:50:05) [GCC 11.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from src.trivialapi.fleetdm import core
>>> core.FleetDM("https://your-server.url")
<src.trivialapi.fleetdm.core.FleetDM object at 0x7afe7e9ffaa0>
>>> fleet = _
>>> fleet.login("you@your.email", "your-password")
True
>>> fleet.hosts()
[...your hosts show up here...]
>>> fleet.host_livequery(host, "SELECT 1 FROM disk_encryption WHERE encrypted=1 AND name LIKE '/dev/dm-1';")
{'host_id': 1, 'rows': None, 'query': "SELECT 1 FROM disk_encryption WHERE encrypted=1 AND name LIKE '/dev/dm-1';", 'status': 'offline'}
>>> qs = fleet.standard_query_library()
>>> len(qs)
91
>>> qs[0]
{'name': 'Get OpenSSL versions', 'platform': ['linux'], 'description': 'Retrieves the OpenSSL version.', 'query': "SELECT name AS name, version AS version, 'deb_packages' AS source FROM deb_packages WHERE name LIKE 'openssl%' UNION SELECT name AS name, version AS version, 'apt_sources' AS source FROM apt_sources WHERE name LIKE 'openssl%' UNION SELECT name AS name, version AS version, 'rpm_packages' AS source FROM rpm_packages WHERE name LIKE 'openssl%';", 'purpose': 'Informational', 'tags': 'inventory', 'contributors': 'zwass'}
>>> enc_qs = [q for q in qs if "Full disk encryption" in q["name"]]
>>> q = enc_qs[0]
>>> fleet.add_query(q["query"], q["name"], q["description"], ",".join(q["platform"]))
<Response [200]>
```

## TODA

- A basic port of [this](https://github.com/TODAQmicro/payment-node) that doesn't suck too much.

#### Basic usage

```
(env-whatever) $ pip install trivialapi
Collecting trivialapi
...snip...
(env-whatever) $ python
Python 3.10.12 (main, Mar 22 2024, 16:50:05) [GCC 11.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from src.trivialapi.toda import core
<module 'src.trivialapi.toda.core'>
>>> tw = core.Twin.from_file("~/path/to/your/twin.json")
<src.trivialapi.toda.core.Twin object at 0x74622b7ed150>
>>> tw.hostname
'41a9cbc977c39bd3eb5a52a5924f8ef5.micro-staging.biz.todaq.net'
>>> tw.key
'redacted'
>>> tw.mint(1000, minting_info="Precision 0 minting test")
{'result': 'success', 'files': ['419bfe67b7fafe0842813f13044d637775349d2b4df347639eccc6ec82093a8ecb'], 'root': '41a2099e84dd4690ea55774506d58ee6cf6ac9fe0c9806239ef6e251a6bc597641'}
>>> tw.balance()
[{'balance': 1000, 'quantity': 1000, 'files': ['419bfe67b7fafe0842813f13044d637775349d2b4df347639eccc6ec82093a8ecb'], 'fileValue': {'419bfe67b7fafe0842813f13044d637775349d2b4df347639eccc6ec82093a8ecb': 1000}, 'poptop': '419ccac82bcf1216a70929664cdeaa97bcc01deb87d190a0c7ce90e62d7b89a6bf', 'displayPrecision': 0, 'type': '41a2099e84dd4690ea55774506d58ee6cf6ac9fe0c9806239ef6e251a6bc597641'}]
```



