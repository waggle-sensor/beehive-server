<!--
waggle_topic=Waggle/Beehive/Operations
waggle_topic=Waggle/Data
-->

# Exporting Data

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

The you could grep the tree using something like:

```
grep -h -r 'failures,nc' mydatasets
```

### Working Remote

You can access the Cassandra database remotely opening an SSH tunnel in the
background.

```
ssh beehive1 -L 9042:localhost:9042
```

This allows you to remotely run exporting commands for testing, backups, etc.
