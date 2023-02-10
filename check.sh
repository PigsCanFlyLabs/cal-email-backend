#!/bin/bash
set -ex

# Configure us to use the integrated settings
export DJANGO_SETTINGS_MODULE="backend.pcf_web.src.config.settings"
export DJANGO_CONFIGURATION="unit_test"
export MEDIA_URL="/media-faaarts/"

nosetests -vs --traverse-namespace backend
flake8 backend --max-line-length=100  --exclude "*/web/*"
mypy backend --exclude "*/web/*"
