![](https://static.pepy.tech/badge/cogdb) [![PyPI version](https://badge.fury.io/py/cogdb.svg)](https://badge.fury.io/py/cogdb) ![Python 3.8](https://img.shields.io/badge/python-3.8+-blue.svg)
 [![Build Status](https://travis-ci.org/arun1729/cog.svg?branch=master)](https://travis-ci.org/arun1729/cog) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![codecov](https://codecov.io/gh/arun1729/cog/branch/master/graph/badge.svg)](https://codecov.io/gh/arun1729/cog)

# CogDB - Micro Graph Database for Python Applications
# ![logo](cog-logo.png)
> Documents and examples at [cogdb.io](https://cogdb.io)

> New release!: 3.0.1
>
> - Ability to use lambda in graph queries.
> - Adjustable height and width for views.  

![ScreenShot](notes/ex2.png)

## Installing Cog
```
pip install cogdb
```
CogDB is a persistent graph database implemented purely in Python. Torque is CogDB's graph query language. CogDB is an ideal choice if you need a database that is very easy to use and that has no setup overhead. All you need to do is to import it into your Python application. CogDB can be used interactively in an IPython environment like Jupyter notebooks.

CogDB can load a graph stored as N-Triples, a serialization format for RDF. See [Wikipedia](https://en.wikipedia.org/wiki/N-Triples), [W3C](https://www.w3.org/TR/n-triples/) for details. 

In short, an N-Triple is sequence of subject, predicate and object in a single line that defines a connection between two vertices:

  ```vertex <predicate> vertex```

[Learn more about RDF triples](https://www.w3.org/TR/rdf-concepts/#:~:text=An%20RDF%20triple%20contains%20three,literal%20or%20a%20blank%20node)


### Creating a graph

```python
from cog.torque import Graph
g = Graph("people")
g.put("alice","follows","bob")
g.put("bob","follows","fred")
g.put("bob","status","cool_person")
g.put("charlie","follows","bob")
g.put("charlie","follows","dani")
g.put("dani","follows","bob")
g.put("dani","follows","greg")
g.put("dani","status","cool_person")
g.put("emily","follows","fred")
g.put("fred","follows","greg")
g.put("greg","status","cool_person")
g.put("bob","score","5")
g.put("greg","score","10")
g.put("alice","score","7")
g.put("dani","score","100")
```

### Torque query examples

#### Scan vertices
```python
g.scan(3)
```

> {'result': [{'id': 'bob'}, {'id': 'emily'}, {'id': 'charlie'}]}

#### Scan edges
```python
g.scan(3, 'e')
```
>{'result': [{'id': 'status'}, {'id': 'follows'}]}

#### Starting from a vertex, follow all outgoing edges and list all vertices
```python
g.v("bob").out().all()
```
> {'result': [{'id': '5'}, {'id': 'fred'}, {'id': 'cool_person'}]}

#### Everyone with status 'cool_person'
```python
g.v().has("status", 'cool_person').all()
```

> {'result': [{'id': 'bob'}, {'id': 'dani'}, {'id': 'greg'}]}

#### Include edges in the results
```python
g.v().has("follows", "fred").inc().all('e')
```
> {'result': [{'id': 'dani', 'edges': ['follows']}, {'id': 'charlie', 'edges': ['follows']}, {'id': 'alice', 'edges': ['follows']}]}

#### starting from a vertex, follow all outgoing edges and count vertices
```python
g.v("bob").out().count()
```
> '3'

#### See who is following who and create a view of that network
#### Note: `render()` is supported only in IPython environment like Jupyter notebook otherwise use view(..).url.
By tagging the vertices 'from' and 'to', the resulting graph can be visualized.
```python
g.v().tag("from").out("follows").tag("to").view("follows").render()

```

# ![ScreenShot](notes/ex1.png)

```python
g.v().tag("from").out("follows").tag("to").view("follows").url

```
> file:///Path/to/your/cog_home/views/follows.html

#### List all views 
```
g.lsv()
```
> ['follows']

#### Load existing visualization
```
g.getv('follows').render()
```

#### starting from a vertex, follow all out going edges and tag them

```python
g.v("bob").out().tag("from").out().tag("to").all()
```
> {'result': [{'from': 'fred', 'id': 'greg', 'to': 'greg'}]}
> 

#### starting from a vertex, follow all incoming edges and list all vertices
```python
g.v("bob").inc().all()
```
> {'result': [{'id': 'alice'}, {'id': 'charlie'}, {'id': 'dani'}]}

#### Using lambda to chose vertices while traversing the graph.

```python
g.v(func=lambda x: x.startswith("d")).all()
```
> {'result': [{'id': 'dani'}]}


```python
g.v().out("score", func=lambda x: int(x) > 5).inc().all()
```
> {'result': [{'id': 'alice'}, {'id': 'dani'}, {'id': 'greg'}]}

```python
g.v("emily").out("follows", func=lambda x: x.startswith("f")).all()
```
> {'result': [{'id': 'fred'}]}

## Loading data from a file

### Create a graph from CSV file

```python
from cog.torque import Graph
g = Graph("books")
g.load_csv('test/test-data/books.csv', "book_id")
```
#### Get the names of the books that have an average rating greater than 4.0
```python
g.v().out("average_rating", func=lambda x: float(x) > 4.0).inc().out("title").all()
```

#### Triples file
```python
from cog.torque import Graph
g = Graph(graph_name="people")
g.load_triples("/path/to/triples.nt", "people")
```

#### Edgelist file
```python
from cog.torque import Graph
g = Graph(graph_name="people")
g.load_edgelist("/path/to/edgelist", "people")
```

## Low level key-value store API:
Every record inserted into Cog's key-value store is directly persisted on to disk. It stores and retrieves data based 
on hash values of the keys, it can perform fast look ups (O(1) avg) and fast (O(1) avg) inserts.

```python

from cog.database import Cog

cogdb = Cog('path/to/dbdir')

# create a namespace
cogdb.create_or_load_namespace("my_namespace")

# create new table
cogdb.create_table("new_db", "my_namespace")

# put some data
cogdb.put(('key', 'val'))

# retrieve data 
cogdb.get('key')

# put some more data
cogdb.put(('key2', 'val2'))

# scan
scanner = cogdb.scanner()
for r in scanner:
 print
 r

# delete data
cogdb.delete('key1')

```

## Config

If no config is provided when creating a Cog instance, it will use the defaults:

```
COG_PATH_PREFIX = "/tmp"
COG_HOME = "cog-test"
```

### Example updating config

```python
from cog import config

config.COG_HOME = "app1_home"
data = ('user_data:id=1', '{"firstname":"Hari","lastname":"seldon"}')
cog = Cog(config)
cog.create_or_load_namespace("test")
cog.create_table("db_test", "test")
cog.put(data)
scanner = cog.scanner()
for r in scanner:
 print
 r

```

## Benchmark

# ![Put Perf](notes/bench.png)
