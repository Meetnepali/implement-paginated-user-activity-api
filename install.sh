#!/bin/bash
set -e
apt-get update
apt-get install -y python3 python3-pip gcc
pip3 install fastapi uvicorn pydantic passlib[bcrypt] pyjwt