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
127.0.0.1:6379> GRAPH.QUERY reserve_meeting "CREATE (:Step {order: 0, req: '', tpl:'reserve_meeting_begin'})-[:next]->(:Step {order: 1, req:'title', tpl:'reserve_meeting_1'})-[:next]->(:Step {order: 2, req:'date', tpl:'reserve_meeting_2'})-[:next]->(:Step {order: 3, req:'time', tpl:'reserve_meeting_3'})-[:next]->(:Step {order: 4, req:'agenda', tpl:'reserve_meeting_4'})-[:next]->(:Step {order: 5, req:'attendees', tpl:'reserve_meeting_5'})-[:next]->(:Step {order: 6, req:'place', tpl:'reserve_meeting_6'})-[:next]->(:Step {order: 7, req: 'title,date,time,agenda,attendees,place', tpl:'reserve_meeting_end'})"
1) 1) "Labels added: 1"
   2) "Nodes created: 8"
   3) "Properties set: 24"
   4) "Relationships created: 7"
   5) "Cached execution: 0"
   6) "Query internal execution time: 2.679637 milliseconds"
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
127.0.0.1:6379> GRAPH.QUERY reserve_meeting "MATCH (n) RETURN n.order as Order, n.req as Postcondition, n.tpl as Template"
1) 1) "Order"
   2) "Postcondition"
   3) "Template"
2) 1) 1) (integer) 0
      2) ""
      3) "reserve_meeting_begin"
   2) 1) (integer) 1
      2) "title"
      3) "reserve_meeting_1"
   3) 1) (integer) 2
      2) "date"
      3) "reserve_meeting_2"
   4) 1) (integer) 3
      2) "time"
      3) "reserve_meeting_3"
   5) 1) (integer) 4
      2) "agenda"
      3) "reserve_meeting_4"
   6) 1) (integer) 5
      2) "attendees"
      3) "reserve_meeting_5"
   7) 1) (integer) 6
      2) "place"
      3) "reserve_meeting_6"
   8) 1) (integer) 7
      2) "title,date,time,agenda,attendees,place"
      3) "reserve_meeting_end"
3) 1) "Cached execution: 0"
   2) "Query internal execution time: 1.091951 milliseconds"
127.0.0.1:6379>
```

### Redis client: redis.py

```
$ pip install redis
```

We can use `redis-py`:

```python
Python 3.12.3 | packaged by conda-forge | (main, Apr 15 2024, 18:38:13) [GCC 12.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import redis
>>> r = redis.Redis()
>>> reply = r.graph('reserve_meeting').query("MATCH (n) RETURN n.order as Order, n.req as Postcondition, n.tpl as Template")
>>> reply.result_set
[[0, '', 'reserve_meeting_begin'], [1, 'title', 'reserve_meeting_1'], [2, 'date', 'reserve_meeting_2'], [3, 'time', 'reserve_meeting_3'], [4, 'agenda', 'reserve_meeting_4'], [5, 'attendees', 'reserve_meeting_5'], [6, 'place', 'reserve_meeting_6'], [7, 'title,date,time,agenda,attendees,place', 'reserve_meeting_end']]
>>> reply = r.graph('reserve_meeting').query("MATCH (n) RETURN n.order, n.req, n.tpl")
>>> reply.result_set
[[0, '', 'reserve_meeting_begin'], [1, 'title', 'reserve_meeting_1'], [2, 'date', 'reserve_meeting_2'], [3, 'time', 'reserve_meeting_3'], [4, 'agenda', 'reserve_meeting_4'], [5, 'attendees', 'reserve_meeting_5'], [6, 'place', 'reserve_meeting_6'], [7, 'title,date,time,agenda,attendees,place', 'reserve_meeting_end']]
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
