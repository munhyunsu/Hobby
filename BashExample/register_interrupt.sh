#!/bin/bash

trap ctrl_c INT

function ctrl_c() {
    echo "Pressed CTRL + C"
    exit 0
}

while :
do
    sleep 1
done
