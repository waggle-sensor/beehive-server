#!/bin/sh

rm -rf /tmp/recent
./list-datasets | ./filter-last-day | ./export-recent-datasets --since 1800 /tmp/recent
