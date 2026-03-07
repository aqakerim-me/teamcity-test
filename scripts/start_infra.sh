#!/usr/bin/env bash
set -euo pipefail

COMPOSE_FILE="${1:-infra/docker_compose/docker-compose.yml}"
TC_URL="http://localhost:8111"
TIMEOUT=300
COOKIES=/tmp/tc_cookies.txt

echo "⬇️ Pulling images..."
docker compose -f "$COMPOSE_FILE" pull

echo "▶ Starting TeamCity infrastructure..."
docker compose -f "$COMPOSE_FILE" up -d

echo "⏳ Waiting for TeamCity to respond..."
elapsed=0
until curl -s -o /dev/null -w "%{http_code}" "$TC_URL/" | grep -qE "^(200|302|401|503)"; do
    if [ "$elapsed" -ge "$TIMEOUT" ]; then
        echo "❌ TeamCity did not respond within ${TIMEOUT}s"
        docker compose -f "$COMPOSE_FILE" logs --tail=50
        exit 1
    fi
    echo "  ... waiting (${elapsed}s)"
    sleep 10
    elapsed=$((elapsed + 10))
done

echo "✅ TeamCity responded — running first-time setup..."

# Step 1: Accept license agreement (maintain cookies throughout)
echo "📋 Accepting license agreement..."
curl -s -X POST "$TC_URL/showAgreement.html" \
    -c "$COOKIES" -b "$COOKIES" \
    -d "accept=true" > /dev/null

sleep 3

# Step 2: Create admin user
echo "👤 Creating admin user..."
curl -s -X POST "$TC_URL/setupAdmin.html" \
    -c "$COOKIES" -b "$COOKIES" \
    -d "userName=admin&password=admin&retypedPassword=admin&submitCreate=1" > /dev/null

sleep 5

# Step 3: Wait until REST API accepts requests
echo "⏳ Waiting for REST API to be ready..."
elapsed=0
until curl -s -o /dev/null -w "%{http_code}" \
    -u admin:admin "$TC_URL/app/rest/server" | grep -qE "^200$"; do
    if [ "$elapsed" -ge 120 ]; then
        echo "❌ REST API not ready after setup"
        exit 1
    fi
    echo "  ... REST not ready yet (${elapsed}s)"
    sleep 5
    elapsed=$((elapsed + 5))
done

echo "✅ TeamCity is fully ready at $TC_URL"