#!/bin/bash

if [ "$1" == "u" ] ; then
    # HelloWorld
    tar -cvzf ./HelloWorld.tar.gz --exclude=SDK_Makefile ./HelloWorld/
elif [ "$1" == "g" ] ; then
    # HelloWorld
    rm -v ./HelloWorld.tar.gz
else
    echo "u or g needed for setting"
fi
