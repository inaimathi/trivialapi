# TODA Micro

- A basic port of [this](https://github.com/TODAQmicro/payment-node) that doesn't suck too much.

## Basic usage

```
>>> from src.pytoda import core
<module 'src.pytoda.core'>
>>> tw = core.Twin.from_file("~/path/to/your/twin.json")
<src.pytoda.core.Twin object at 0x74622b7ed150>
>>> tw.hostname
'41a9cbc977c39bd3eb5a52a5924f8ef5.micro-staging.biz.todaq.net'
>>> tw.key
'redacted'
>>> tw.mint(1000, minting_info="Precision 0 minting test")
{'result': 'success', 'files': ['419bfe67b7fafe0842813f13044d637775349d2b4df347639eccc6ec82093a8ecb'], 'root': '41a2099e84dd4690ea55774506d58ee6cf6ac9fe0c9806239ef6e251a6bc597641'}
>>> tw.balance()
[{'balance': 1000, 'quantity': 1000, 'files': ['419bfe67b7fafe0842813f13044d637775349d2b4df347639eccc6ec82093a8ecb'], 'fileValue': {'419bfe67b7fafe0842813f13044d637775349d2b4df347639eccc6ec82093a8ecb': 1000}, 'poptop': '419ccac82bcf1216a70929664cdeaa97bcc01deb87d190a0c7ce90e62d7b89a6bf', 'displayPrecision': 0, 'type': '41a2099e84dd4690ea55774506d58ee6cf6ac9fe0c9806239ef6e251a6bc597641'}]
```



