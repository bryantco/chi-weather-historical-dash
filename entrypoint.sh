#!/bin/bash

# Setup Superset
superset db upgrade
superset init

# Import dashboards (assumes YAML is in /app/dashboards)
superset import-dashboards --path /app/dashboards
superset import-charts --path /app/charts

# Start the app
superset run -p 8088 -h 0.0.0.0
