#!/bin/bash

cd /root/my-app
npm run build

serve -s /var/www/myweb/ -l 3001

