#!/bin/sh

./list-datasets | ./filter-last-day | ./export-decoded-datasets-csv
sleep 5
./compress-datasets
sleep 5
./build-index
