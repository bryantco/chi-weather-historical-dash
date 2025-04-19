#!/bin/bash
set -e

# Setup Superset
superset db upgrade
superset init

superset fab create-admin \
    --username admin \
    --password admin || true

echo "📦 Importing databases..."
superset import-datasources --path /app/databases || echo "No databases found."

echo "📦 Importing datasets..."
superset import-datasources --path /app/datasets || echo "No datasets found."

echo "📦 Importing charts..."
superset import-charts --path /app/charts || echo "No charts found."

echo "📦 Importing dashboards..."
superset import-dashboards --username admin --path /app/dashboards || echo "No dashboards found."

# Start the app
superset run -p 8088 -h 0.0.0.0
