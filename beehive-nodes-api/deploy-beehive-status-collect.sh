#!/bin/bash


if [ ! -x "$(command -v pidof)" ] ; then
  echo "not linux"
  exit 1
fi


if [ $(pidof systemd)_ != "1_" ] ; then
  echo "systemd not found"
  exit 1
fi

cp beehive-status-collect.service /etc/systemd/system/
systemctl enable beehive-status-collect.service
systemctl start beehive-status-collect.service

