# Konversa

```
  _  __                                   
 | |/ /                                   
 | ' / ___  _ ____   _____ _ __ ___  __ _ 
 |  < / _ \| '_ \ \ / / _ \ '__/ __|/ _` |
 | . \ (_) | | | \ V /  __/ |  \__ \ (_| |
 |_|\_\___/|_| |_|\_/ \___|_|  |___/\__,_|
```

**Konversa** is a case study for property graph-based conversational agent.

## Requirements

### Infrastructure

1. [Redis](https://redis.io).
2. [FalkorDB](https://www.falkordb.com). FalkorDB is RedisGraph fork.

For those two requirements, see [this article](https://zimeracorp.com/posts/18/) on how to install Redis and FalkorDB.

### Python

We use [Python 3.12](https://www.python.org) and [Mamba](https://github.com/mamba-org/mamba) as our environment and package manager. We simply use **pip** for our package manager. See [requirements.txt](requirements.txt) file for complete packages list. Note that, basically we just installed these pre-requisites:

1. [FalkorDB Python client](https://github.com/falkorDB/falkordb-py).
2. [falkordb-bulk-loader](https://pypi.org/project/falkordb-bulk-loader/).
3. [aiogram](https://aiogram.dev/).
4. [RDFlib](https://rdflib.dev/).
5. [Mako](https://www.makotemplates.org/).

Here's how to install them:

```
$ pip install FalkorDB
$ pip install falkordb-builk-loader
$ pip install aiogram
$ pip install rdflib
$ pip install Mako
```

## License

This work is [CC-BY-SA 4.0 Licensed](https://creativecommons.org/licenses/by-sa/4.0/).
