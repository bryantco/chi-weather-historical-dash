#!/bin/bash
set -e

superset db upgrade
superset init

superset fab create-admin \
              --username admin \
              --firstname Superset \
              --lastname Admin \
              --email admin@superset.com \
              --password admin

gunicorn -b 0.0.0.0:${PORT:-8088} --workers 4 --timeout 120 "superset.app:create_app()"