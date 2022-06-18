#!/bin/sh
cd ..
APP_ENV=dev uvicorn app.main:app --log-config app/logging.yaml --host 127.0.0.1 --port 8080 --workers 1
