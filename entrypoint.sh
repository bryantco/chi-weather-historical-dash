#!/bin/bash
set -e

superset db upgrade
superset init

superset fab list-users | grep -q admin || \
superset fab create-admin \
              --username admin \
              --firstname Superset \
              --lastname Admin \
              --email admin@superset.com \
              --password "${SUPERSET_ADMIN_PASSWORD:?SUPERSET_ADMIN_PASSWORD must be set}"

gunicorn -b 0.0.0.0:${PORT:-8088} --workers 2 --timeout 120 "superset.app:create_app()"