#!/bin/bash
set -e
bash install.sh
uvicorn main:app --host 0.0.0.0 --port 8000