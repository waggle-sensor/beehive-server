# Data Exporting Tools

```
                Filter nodes and dates                     +----> Stdout
                        v                                  |
[List Dataset] -> grep, awk, etc -> [Export Datasets] -----+
     ^                                  ^                  |
 Emits list of (Node ID, Date)       Exports datasets for  +----> Dataset Tree on Disk
 partition keys.                     partition keys.                  
```

## Installing dependencies

```sh
# Expects Python 3, so you may need pip3 install ...
pip install -r requirements.txt
```

## Usage

### Listing Datasets

```
Sean@mcswl072 ~/t/b/data-exporter> ./list-datasets | tail
001e0610f725 2017-12-09
001e0610ba16 2017-08-30
001e0610f6dd 2018-04-27
001e0610ee41 2018-04-23
001e06109416 2018-04-04
001e0610c2d7 2018-04-01
```


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

## build-index

This provides an easy way to get a quick overview of what datasets you've
pulled. Running the command

```sh
./build-index
```

will populate the `static` directory with a statically generated set of pages.
Open `static/index.html` to view the datasets.

## Remote backup

You can do pulls over the network using ssh forwarding

```
ssh -C -L 9042:localhost:9042 beehive1
```

Then, just run `export` or `exportall`.
