# Data Exporting Tools

## Installing dependencies

```sh
# Expects Python 3, so you may need pip3 install ...
pip install -r requirements.txt
```

## export / exportall

On Beehive, these can do a direct bulk pull from the Cassandra database. You
simply provide:

```sh
./export node1 node2 ... noden
```

or

```sh
./exportall
```

This will dump all datasets using the prefix `data/nodeid/date.csv`.

## buildindex

This provides an easy way to get a quick overview of what datasets you've
pulled. Running the command

```sh
./buildindex
```

will populate the `static` directory with a statically generated set of pages.
Open `static/index.html` to view the datasets.

## Remote backup

You can do pulls over the network using ssh forwarding

```
ssh -C -L 9042:localhost:9042 beehive1
```

Then, just run `export` or `exportall`.
