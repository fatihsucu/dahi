#!/usr/bin/env bash

if (( $EUID != 0 )); then
    sudo /usr/src/app/build.sh
    exit
fi
tail -f /dev/null