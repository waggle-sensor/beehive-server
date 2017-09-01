# Data Exporting Tools

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
