#!/bin/bash
set -e

# Setup Superset
superset db upgrade
superset init

echo "Importing dashboards"
superset import-dashboards --path /app/dashboards

# Start the app
superset run -p 8088 -h 0.0.0.0
