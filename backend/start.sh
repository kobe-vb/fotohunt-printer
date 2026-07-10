#!/bin/bash
cd /opt/scoutsbox/games/printer/backend
ip addr add 192.168.1.10/24 dev eth0
exec ./venv/bin/uvicorn main:app --host 127.0.0.1 --port 8003
