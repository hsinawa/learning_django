#!/bin/bash
# start.sh

# Export PORT if not set (default to 8080)
PORT=${PORT:-8080}

# Start Gunicorn
exec gunicorn --bind 0.0.0.0:$PORT your_project.wsgi:application