#!/bin/bash
export HOME=/app/tmp
source /app/venv/bin/activate
exec gunicorn -b :80 --access-logfile - --error-logfile - run:app