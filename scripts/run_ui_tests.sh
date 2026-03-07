#!/usr/bin/env bash
# Runs the UI test suite across chromium, firefox, and webkit (matching pytest.ini)
# using the admin bearer token from resources/config.properties.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/../resources/config.properties"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "Config file not found: $CONFIG_FILE" >&2
    exit 1
fi

if ! grep -Eq '^admin\.bearerToken=.+$' "$CONFIG_FILE"; then
    echo "resources/config.properties must contain a non-empty admin.bearerToken before running UI tests." >&2
    exit 1
fi

REPORT_DIR="reports/ui"
mkdir -p "$REPORT_DIR"

echo "▶ Running UI tests (chromium + firefox + webkit)..."

# pytest.ini already sets --browser chromium --browser firefox --browser webkit
# so we just invoke normally — no need to pass browser flags here.
pytest src/tests/ui/ \
  -m "ui" \
  --tb=short \
  --junitxml="$REPORT_DIR/results.xml" \
  --html="$REPORT_DIR/report.html" \
  --self-contained-html \
  -v

echo "✅ UI tests complete. Reports in $REPORT_DIR/"
