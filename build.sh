#!/usr/bin/env bash
# exit on error
set -o errexit

# Limpar cache do pip
pip cache purge || true

pip install --upgrade pip
pip install -r requirements.txt
