#!/bin/sh
exec uvicorn --host 0.0.0.0 --port 5000 main:app