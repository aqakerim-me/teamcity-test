#!/usr/bin/env bash
# Runs the API test suite. Bearer token is expected in TC_ADMIN_BEARERTOKEN env var.

set -euo pipefail

: "${TC_ADMIN_BEARERTOKEN:?TC_ADMIN_BEARERTOKEN env var must be set}"

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