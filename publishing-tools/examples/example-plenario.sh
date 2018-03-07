#!/bin/sh

# will be done on beehive
../bin/filter-view plenario < recent.csv | ../bin/filter-sensors climate.csv > plenario.csv

# may be done on beehive or at endpoint
../bin/prepare-for-plenario plenario < plenario.csv
