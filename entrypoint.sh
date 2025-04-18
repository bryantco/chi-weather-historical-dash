#!/bin/bash

# Setup Superset
superset db upgrade
superset init

# Start the app
superset run -p 8088 -h 0.0.0.0
