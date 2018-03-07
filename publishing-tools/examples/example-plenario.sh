#!/bin/sh

# will be done on beehive
../bin/filter-view plenario < recent.csv | ../bin/filter-sensors climate.csv > plenario.csv

# may be done on beehive or by consumer
../bin/prepare-for-plenario plenario < plenario.csv
