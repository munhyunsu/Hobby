#!/bin/bash

# A POSIX variable
OPTIND=1         # Reset in case getopts has been used previously in the shell.

while getopts ":h?p:a:i:s:d:" opt; do
    case "$opt" in
    h)  echo "Print help"
        echo "-p private_key_path -a account -i remote_ipaddress -s src_path -d dst_path"
        ;;
    p)  PKEY=$OPTARG
        ;;
    a)  ACCOUNT=$OPTARG
        ;;
    i)  RIP=$OPTARG
        ;;
    s)  SPATH=$OPTARG
        ;;
    d)  DPATH=$OPTARG
        ;;
    esac
done

shift $((OPTIND-1))

echo "scp -i ${PKEY} ${ACCOUNT}@${RIP}:${SPATH} ${DPATH}"
scp -i ${PKEY} ${ACCOUNT}@${RIP}:${SPATH} ${DPATH}

