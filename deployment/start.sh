#!/usr/bin/env bash
set -euo pipefail

APP_DIR="/opt/ha-mikroservice"
cd "$APP_DIR"
exec "$APP_DIR/.venv/bin/python" -m fastapi run --host 0.0.0.0 --port 8000
