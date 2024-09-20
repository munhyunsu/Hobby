#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd ${SCRIPT_DIR}
sqlite3 rawdata/app.db ".header on" ".mode csv" ".once data/flock.csv" "SELECT latitude, longitude FROM message ORDER BY created_at ASC;" ".exit"
vi +':e ++ff=dos' +':w ++ff=unix' +':q' "data/flock.csv"
