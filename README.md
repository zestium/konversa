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

9. [spaCy](https://spacy.io): `pip install spacy`
10. spaCy data:

```bash
python -m spacy download en_core_web_sm
```

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

## Infrastructure Preparation

### Redis

Get [Redis Stack](https://redis.io/downloads/).

See [conf/](conf/) and make some changes, suitable to your server.

Run Redis Server:

```bash
$ redis-server <PATH/redis.conf> 
```

PATH can be everywhere.

### Redis Client: redis-cli

**Note**: symbol ``>`` is redis-cli prompt.

```
127.0.0.1:6379> GRAPH.QUERY reserve_meeting "CREATE (:Begin {req_begin:'name', num_of_steps:5})-[:next]->(:First {req_first:'date', template_first:'reserve_meeting_first'})-[:next]->(:Second {req_second:'time', template_second:'reserve_meeting_second'})-[:next]->(:Third {req_third:'agenda', template_third:'reserve_meeting_third'})-[:next]->(:Fourth {req_fourth:'member', template_fourth:'reserve_meeting_fourth'})-[:next]->(:Fifth {req_fifth:'place', template_fifth:'reserve_meeting_fifth'})-[:next]->(:End {postcondition: 'name,date,time,agenda,member,place', template:'reserve_meeting_complete'})"
1) 1) "Labels added: 7"
   2) "Nodes created: 7"
   3) "Properties set: 14"
   4) "Relationships created: 6"
   5) "Cached execution: 0"
   6) "Query internal execution time: 71.751520 milliseconds"
127.0.0.1:6379> 
```

This way, there will be one key (reserve_meeting):

```
127.0.0.1:6379> info keyspace
# Keyspace
db0:keys=8,expires=0,avg_ttl=0
127.0.0.1:6379> 
```

Example of query:

```
127.0.0.1:6379> GRAPH.QUERY reserve_meeting "MATCH (b:Begin)-[:next]->(f:First) WHERE f.req_first = 'date' RETURN b.num_of_steps, f.req_first"
1) 1) "b.num_of_steps"
   2) "f.req_first"
2) 1) 1) (integer) 5
      2) "date"
3) 1) "Cached execution: 0"
   2) "Query internal execution time: 94.713853 milliseconds"
127.0.0.1:6379> 
```

### Redis client: redis.py

```
$ pip install redis
```

We can use `redis-py`:

```python
>>> import redis
>>> r = redis.Redis()
>>> reply = r.graph("reserve_meeting").query("MATCH (b:Begin)-[:next]->(f:First) WHERE f.req_first = 'date' RETURN b.num_of_steps, f.req_first")
>>> reply.result_set
[[5, 'date']]
>>> 
```

### Save Database

From redis-cli:

```
> SAVE
```

**Note**: case insensitive.

## License

This work is [CC-BY-SA 4.0 Licensed](https://creativecommons.org/licenses/by-sa/4.0/).
