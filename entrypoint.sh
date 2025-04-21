#!/bin/bash
set -e

# Setup Superset
superset db upgrade
superset init

superset fab create-admin \
              --username admin \
              --firstname Superset \
              --lastname Admin \
              --email admin@superset.com \
              --password admin

# Start the app
superset run -p 8088 -h 0.0.0.0
