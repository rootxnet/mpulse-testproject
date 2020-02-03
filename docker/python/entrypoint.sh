#!/usr/bin/env bash

echo "Welcome to ${PROJECT_NAME} - backend"
echo "Starting main application..."
source ${PROJECT_VENDOR_DIR}/bin/activate
python -Wd ${PROJECT_DIR}/manage.py runserver 0.0.0.0:8000