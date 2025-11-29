#!/bin/bash
# TalkyBoi launcher script
# Automatically detects its location and activates the virtual environment

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
source venv/bin/activate
python main.py "$@"
