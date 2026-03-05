#!/usr/bin/env bash
set -euo pipefail

COMPOSE_FILE="${1:-infra/docker_compose/docker-compose.yml}"
TC_URL="http://localhost:8111"
TIMEOUT=300

echo "▶ Starting TeamCity infrastructure from: $COMPOSE_FILE"
docker compose -f "$COMPOSE_FILE" up -d

echo "⏳ Waiting for TeamCity to be ready..."
elapsed=0
until curl -s -o /dev/null -w "%{http_code}" "$TC_URL/login.html" | grep -qE "^(200|302)"; do
    if [ "$elapsed" -ge "$TIMEOUT" ]; then
        echo "❌ TeamCity did not start within ${TIMEOUT}s"
        docker compose -f "$COMPOSE_FILE" logs --tail=50
        exit 1
    fi
    echo "  ... waiting (${elapsed}s)"
    sleep 10
    elapsed=$((elapsed + 10))
done

echo "✅ TeamCity is ready at $TC_URL"