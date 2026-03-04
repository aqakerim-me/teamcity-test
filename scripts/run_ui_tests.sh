#!/usr/bin/env bash
# Runs the UI test suite across chromium, firefox, and webkit (matching pytest.ini).
# Bearer token is expected in TC_ADMIN_BEARERTOKEN env var.

set -euo pipefail

: "${TC_ADMIN_BEARERTOKEN:?TC_ADMIN_BEARERTOKEN env var must be set}"

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