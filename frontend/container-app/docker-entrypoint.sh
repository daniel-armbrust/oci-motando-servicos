#!/bin/sh
exec gunicorn --access-logfile - --error-logfile - -b 127.0.0.1:5000 wsgi:app