#!/usr/bin/env bash
set -euo pipefail

COMPOSE_FILE="${1:-infra/docker_compose/docker-compose.yml}"
TC_URL="http://localhost:8111"
TIMEOUT=600

echo "▶ Starting TeamCity infrastructure from: $COMPOSE_FILE"
docker compose -f "$COMPOSE_FILE" up -d

echo "⏳ Waiting for TeamCity to respond..."
elapsed=0
until curl -s -o /dev/null -w "%{http_code}" "$TC_URL/" | grep -qE "^(200|302|401|404|503)"; do
    if [ "$elapsed" -ge "$TIMEOUT" ]; then
        echo "❌ TeamCity did not start within ${TIMEOUT}s"
        docker compose -f "$COMPOSE_FILE" logs --tail=50
        exit 1
    fi
    echo "  ... waiting (${elapsed}s)"
    sleep 10
    elapsed=$((elapsed + 10))
done

echo "✅ TeamCity responded — checking if setup is needed..."

# Complete setup wizard if needed
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$TC_URL/showAgreement.html")
if [ "$HTTP_CODE" = "200" ]; then
    echo "📋 Accepting license agreement..."
    curl -s -X POST "$TC_URL/showAgreement.html" \
        -d "accept=true" > /dev/null

    echo "🔧 Completing setup..."
    curl -s -X POST "$TC_URL/setupAdmin.html" \
        -d "userName=admin&password=admin&retypedPassword=admin&submitCreate=1" > /dev/null

    echo "⏳ Waiting for setup to complete..."
    sleep 30
fi

echo "✅ TeamCity is ready at $TC_URL"