#!/bin/bash

cd "$(dirname "$0")"
flutter --device-id web-server run --web-hostname 127.0.0.1 --web-port 8080 --dart-define-from-file config.json
