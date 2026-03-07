#!/usr/bin/env bash
set -euo pipefail

COMPOSE_FILE="${1:-infra/docker_compose/docker-compose.yml}"
TC_URL="http://localhost:8111"
TIMEOUT=300

echo "⬇️ Pulling images..."
docker compose -f "$COMPOSE_FILE" pull

echo "▶ Starting TeamCity infrastructure..."
docker compose -f "$COMPOSE_FILE" up -d

echo "⏳ Waiting for TeamCity to respond..."
elapsed=0
until curl -s -o /dev/null -w "%{http_code}" "$TC_URL/" | grep -qE "^(200|302|401|503)"; do
    if [ "$elapsed" -ge "$TIMEOUT" ]; then
        echo "❌ TeamCity did not respond within ${TIMEOUT}s"
        docker compose -f "$COMPOSE_FILE" logs teamcity-server --tail=30
        exit 1
    fi
    echo "  ... waiting (${elapsed}s)"
    sleep 10
    elapsed=$((elapsed + 10))
done

echo "✅ TeamCity responded — confirming first start..."

# Confirm first start via the maintenance REST endpoint
curl -s -X POST "$TC_URL/app/rest/server/startup" \
    -H "Content-Type: application/json" \
    -d '{}' > /dev/null || true

sleep 3

# Also try the maintenance confirm endpoint
curl -s -X POST "$TC_URL/mnt/first-start-accept" \
    -H "Content-Type: application/json" > /dev/null || true

sleep 5

echo "⏳ Waiting for super user token..."
elapsed=0
SUPER_TOKEN=""
until [ -n "$SUPER_TOKEN" ]; do
    if [ "$elapsed" -ge "$TIMEOUT" ]; then
        echo "❌ Super user token did not appear within ${TIMEOUT}s"
        docker exec teamcity-server cat /opt/teamcity/logs/teamcity-server.log 2>/dev/null | grep -i "super user" | tail -5 || true
        docker compose -f "$COMPOSE_FILE" logs teamcity-server --tail=30
        exit 1
    fi
    SUPER_TOKEN=$(
        { docker logs teamcity-server 2>&1; \
          docker exec teamcity-server cat /opt/teamcity/logs/teamcity-server.log 2>/dev/null || true; } \
        | grep -o 'Super user authentication token: [0-9]*' \
        | grep -o '[0-9]*' \
        | tail -1 || true
    )
    if [ -z "$SUPER_TOKEN" ]; then
        echo "  ... waiting for token (${elapsed}s)"
        sleep 10
        elapsed=$((elapsed + 10))
    fi
done

echo "✅ Got super user token"

# Create admin user
echo "👤 Creating admin user..."
curl -s -X POST "$TC_URL/app/rest/users" \
    -H "Authorization: Bearer $SUPER_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"username":"admin","password":"admin","roles":{"role":[{"roleId":"SYSTEM_ADMIN","scope":"g"}]}}'

sleep 5

# Wait for REST API with admin credentials
echo "⏳ Waiting for REST API to be ready..."
elapsed=0
until curl -s -o /dev/null -w "%{http_code}" \
    -u admin:admin "$TC_URL/app/rest/server" | grep -qE "^200$"; do
    if [ "$elapsed" -ge 180 ]; then
        echo "❌ REST API not ready after setup"
        docker compose -f "$COMPOSE_FILE" logs teamcity-server --tail=30
        exit 1
    fi
    echo "  ... REST not ready yet (${elapsed}s)"
    sleep 10
    elapsed=$((elapsed + 10))
done

echo "✅ TeamCity is fully ready at $TC_URL"