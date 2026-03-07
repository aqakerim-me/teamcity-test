#!/usr/bin/env bash
set -euo pipefail

COMPOSE_FILE="${1:-infra/docker_compose/docker-compose.yml}"
TC_URL="http://localhost:8111"
TIMEOUT=900
SLEEP_SECONDS=10
SETUP_DONE=0

echo "Starting TeamCity infrastructure from: $COMPOSE_FILE"
docker compose -f "$COMPOSE_FILE" up -d

echo "Waiting for TeamCity to be fully ready..."
elapsed=0

while true; do
  http_code="$(curl -sS -L -o /tmp/tc_root.html -w "%{http_code}" "$TC_URL/" || true)"
  body="$(cat /tmp/tc_root.html 2>/dev/null || true)"
  is_maintenance=1
  if ! grep -qiE "maintenance-welcome|first_start_screen|teamcity maintenance|saveRedirectedFromAndGoToMaintenance" <<< "$body"; then
    is_maintenance=0
  fi

  if [[ "$is_maintenance" -eq 1 && "$SETUP_DONE" -eq 0 ]]; then
    echo "Detected TeamCity first-start/maintenance stage. Running initial setup..."

    curl -sS -L -o /tmp/tc_agreement.html "$TC_URL/showAgreement.html" || true
    if grep -qiE "showAgreement|accept" /tmp/tc_agreement.html; then
      curl -sS -L -X POST "$TC_URL/showAgreement.html" \
        -d "accept=true" > /dev/null || true
    fi

    curl -sS -L -X POST "$TC_URL/setupAdmin.html" \
      -d "userName=admin&password=admin&retypedPassword=admin&submitCreate=1" > /dev/null || true

    SETUP_DONE=1
    echo "Initial setup request sent, waiting for TeamCity to restart..."
    sleep 20
  fi

  if [[ "$http_code" =~ ^(200|302|401)$ ]] && [[ "$is_maintenance" -eq 0 ]]; then
    echo "TeamCity is ready at $TC_URL (HTTP $http_code)"
    break
  fi

  if [[ "$elapsed" -ge "$TIMEOUT" ]]; then
    echo "TeamCity did not become ready within ${TIMEOUT}s"
    echo "Last HTTP code: $http_code"
    echo "Last response head:"
    head -n 40 /tmp/tc_root.html || true
    docker compose -f "$COMPOSE_FILE" logs --tail=200 || true
    exit 1
  fi

  echo "  ... still waiting (${elapsed}s), code=${http_code}"
  sleep "$SLEEP_SECONDS"
  elapsed=$((elapsed + SLEEP_SECONDS))
done
