#!/bin/sh
set -e
python init_db.py

gunicorn event_book.main:app -b :8080 --worker-class aiohttp.GunicornWebWorker --reload --access-logfile -