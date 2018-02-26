#!/bin/sh

# will be done on beehive
cat recent.csv |
../bin/filter-view view.json |
../bin/filter-sensors climate.json > plenario.csv

# may be done on beehive or at endpoint
./prepare-for-plenario view.json < plenario.csv
