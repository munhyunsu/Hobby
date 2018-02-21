#!/bin/bash

#echo $( cd "$( dirname ${BASH_SOURCE[0]} )" && pwd )
echo ${BASH_SOURCE[0]}
echo $(pwd)
cd $(dirname ${BASH_SOURCE[0]})
echo $(pwd)
