# Data Exporting Tools

```
                                                             +----> Stdout
                                                             |
list-datasets ---> grep, awk, etc ---> export-datasets ------+
    ^                                        ^               |
 Emits list of (Node ID, Date)       Exports datasets for    +----> Dataset Tree on Disk
 partition keys.                     partition keys.                  
```

## Installing dependencies

```sh
# Expects Python 3, so you may need pip3 install ...
pip install -r requirements.txt
```

## Example Usage

### Export Datasets from 2018-05-10

The following would export all datasets from 2018-05-10 to `mydatasets` as a
`mydatasets/nodeid/date.csv` tree.

```
./list-datasets | grep 2018-05-10 | ./export-datasets mydatasets
```
