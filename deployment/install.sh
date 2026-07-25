#!/usr/bin/env bash
set -euo pipefail

APP_DIR="/opt/ha-mikroservice"
SERVICE_FILE="/etc/systemd/system/ha-mikroservice.service"

sudo mkdir -p "$APP_DIR"
sudo cp -r . "$APP_DIR"
sudo python3 -m venv "$APP_DIR/.venv"
sudo "$APP_DIR/.venv/bin/pip" install --upgrade pip
sudo "$APP_DIR/.venv/bin/pip" install -r "$APP_DIR/requirements.txt"

sudo cp deployment/ha-mikroservice.service "$SERVICE_FILE"
sudo systemctl daemon-reload
sudo systemctl enable ha-mikroservice.service
sudo systemctl restart ha-mikroservice.service
