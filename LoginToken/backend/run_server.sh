#!/bin/bash

cd "$(dirname "$0")"
source venv/bin/activate
fastapi dev app/main.py --app app --host 127.0.0.1 --port 8000

