#!/usr/bin/env bash
# Installs Python dependencies and Playwright browsers.

set -euo pipefail

echo "▶ Installing Python dependencies..."
pip install -r requirements.txt

echo "▶ Installing Playwright browsers (chromium, firefox, webkit)..."
playwright install --with-deps chromium firefox webkit

echo "✅ Dependencies ready"