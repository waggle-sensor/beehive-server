#!/bin/sh

cat recent.csv |
../bin/filter-view metadata.json |
../bin/filter-sensors climate.json
