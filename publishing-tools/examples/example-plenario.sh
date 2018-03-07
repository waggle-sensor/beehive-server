#!/bin/sh

# will be done on beehive
../bin/filter-view plenario < recent.csv |
../bin/filter-sensors climate.json | tee plenario.csv

# may be done on beehive or at endpoint
#./prepare-for-plenario view.json < plenario.csv
