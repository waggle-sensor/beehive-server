# Data Exporting Tools

## Installing dependencies

```sh
# Expects Python 3, so you may need pip3 install ...
pip install -r requirements.txt
```

## list-datasets and export-datasets

These tools are used together to perform bulk pulls from the Cassandra database.
They will dump all pulled datasets to `data/nodeid/date.csv`. Let's look a few
use cases:

This first example pulls all the datasets.

```sh
./list-datasets | ./export-datasets
```

This second example pulls all the datasets from node 001e0610ba3f.

```sh
./list-datasets | awk '/001e0610ba3f/' | ./export-datasets
```

This last example pulls all the datasets after September 1, 2017.

```sh
./list-datasets | awk '$3 >= "2017-09-01"' | ./export-datasets
```

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
