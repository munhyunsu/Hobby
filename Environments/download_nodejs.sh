#!/bin/bash

wget https://nodejs.org/dist/v20.17.0/node-v20.17.0-linux-x64.tar.xz -O nodejs.tar.xz
mkdir -p nodejs
tar -xvf node-v20.17.0-linux-x64.tar.xz -C nodejs --strip-components 1
rm nodejs.tar.xz

