#!/bin/bash
set -x

# Check if the config.yaml file exists and copy it
if [ -f /opt/app-root/config/config.yaml ]; then
  cp /opt/app-root/config/config.yaml /opt/app-root/src/config.yaml
fi

# Start the Streamlit app
${POETRY_HOME}/bin/poetry run streamlit run streamlit/intro.py