#!/bin/bash
set -x
docker exec -ti beehive-nginx nginx -s reload