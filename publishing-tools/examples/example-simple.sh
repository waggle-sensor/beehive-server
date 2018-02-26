#!/bin/sh

cat recent.csv |
../bin/filter-view view.json |
../bin/filter-sensors climate.json
