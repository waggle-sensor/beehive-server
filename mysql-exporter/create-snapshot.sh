#!/bin/sh

mysqldump -h 127.0.0.1 -P 3306 -u waggle --password=waggle waggle > $(date +'waggle-%Y%m%d%H%M%S.sql')
