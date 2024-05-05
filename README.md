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

1. [FalkorDB Python client](https://github.com/falkorDB/falkordb-py): `pip install FalkorDB`
2. [falkordb-bulk-loader](https://pypi.org/project/falkordb-bulk-loader/): `pip install falkordb-build-loader`
3. [aiogram](https://aiogram.dev/): `pip install aiogram`
4. [RDFlib](https://rdflib.dev/): `pip install rdflib`
5. [SPARQLWrapper](https://github.com/RDFLib/sparqlwrapper): `pip install sparqlwrapper`
6. [Mako](https://www.makotemplates.org/): `pip install Mako`
7. [NLTK](https://nltk.org): `pip install nltk`
8. NLTK Data:

```python
>>> import nltk
>>> nltk.download('punkt')
```

9. [spaCy](https://spacy.io)
10. spaCy data:

```bash
python -m spacy download en_core_web_sm
```

Here's how to install them:

## TELEGRAM_API_TOKEN

To use this bot, A token from Telegram is needed. See [Bots: An introduction for developers](https://core.telegram.org/bots) on how to get the token. The token should be put inside an environment variable named `TELEGRAM_API_TOKEN` prior running this bot, in Linux you may use this:

```bash
export TELEGRAM_API_TOKEN='yourToken' # if you use bash

# or:

set -x TELEGRAM_API_TOKEN yourToken  # if you use Fish
```

## Run

```bash
python src/konversa_bot.py
```

## License

This work is [CC-BY-SA 4.0 Licensed](https://creativecommons.org/licenses/by-sa/4.0/).
