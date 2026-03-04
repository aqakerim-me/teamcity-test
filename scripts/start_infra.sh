#!/usr/bin/env bash
# Starts the TeamCity server + agent and waits until the server is responsive.

set -euo pipefail

COMPOSE_FILE="${1:-infra/docker_compose/docker-compose.yml}"
TC_URL="http://localhost:8111"
TIMEOUT=180   # seconds to wait for TC server

echo "▶ Starting TeamCity infrastructure from: $COMPOSE_FILE"
docker compose -f "$COMPOSE_FILE" up -d

echo "⏳ Waiting for TeamCity server at $TC_URL (timeout: ${TIMEOUT}s)..."
elapsed=0
until curl -sf "$TC_URL" -o /dev/null; do
  if [ "$elapsed" -ge "$TIMEOUT" ]; then
    echo "❌ Timed out waiting for TeamCity server after ${TIMEOUT}s"
    docker compose -f "$COMPOSE_FILE" logs teamcity-server
    exit 1
  fi
  sleep 5
  elapsed=$((elapsed + 5))
  echo "   ... still waiting (${elapsed}s)"
done

echo "✅ TeamCity server is up after ${elapsed}s"