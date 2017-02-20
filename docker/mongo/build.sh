#!/usr/bin/env bash

if (( $EUID != 0 )); then
    sudo /usr/src/app/build.sh
    exit
fi

mongod --fork --logpath /var/log/mongodb.log --dbpath /data/db --smallfiles

mongod --shutdown
mongod