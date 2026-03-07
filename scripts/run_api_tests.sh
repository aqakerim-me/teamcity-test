#!/usr/bin/env bash
# Runs the API test suite using the admin bearer token from resources/config.properties.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/../resources/config.properties"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "Config file not found: $CONFIG_FILE" >&2
    exit 1
fi

if ! grep -Eq '^admin\.bearerToken=.+$' "$CONFIG_FILE"; then
    echo "resources/config.properties must contain a non-empty admin.bearerToken before running API tests." >&2
    exit 1
fi

REPORT_DIR="reports/api"
mkdir -p "$REPORT_DIR"

echo "▶ Running API tests..."
pytest src/tests/api/ \
  -m "api" \
  --tb=short \
  --junitxml="$REPORT_DIR/results.xml" \
  --html="$REPORT_DIR/report.html" \
  --self-contained-html \
  -v

echo "✅ API tests complete. Reports in $REPORT_DIR/"
