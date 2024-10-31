#!/bin/bash
set -x

# Check if the config.yaml file exists and copy it
if [ -f /opt/app-root/config/config.yaml ]; then
  cp /opt/app-root/config/config.yaml /opt/app-root/src/config.yaml
fi

# Start the agent server
${POETRY_HOME}/bin/poetry run python react_agent/api.py