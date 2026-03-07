#!/usr/bin/env bash
# Runs the UI test suite on chromium only (stabilized CI mode).
# Bearer token is expected in TC_ADMIN_BEARERTOKEN env var.

set -euo pipefail

: "${TC_ADMIN_BEARERTOKEN:?TC_ADMIN_BEARERTOKEN env var must be set}"

REPORT_DIR="reports/ui"
mkdir -p "$REPORT_DIR"

echo "Running UI tests (chromium only)..."

# Override pytest.ini addopts browsers for CI stability.
pytest src/tests/ui/ \
  -m "my_ui" \
  -o addopts="--browser chromium" \
  --tb=short \
  --junitxml="$REPORT_DIR/results.xml" \
  --html="$REPORT_DIR/report.html" \
  --self-contained-html \
  -v

echo "UI tests complete. Reports in $REPORT_DIR/"
