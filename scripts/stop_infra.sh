#!/usr/bin/env bash
# Tears down the TeamCity containers and removes volumes.

set -euo pipefail

COMPOSE_FILE="${1:-infra/docker_compose/docker-compose.yml}"

echo "▶ Stopping TeamCity infrastructure..."
docker compose -f "$COMPOSE_FILE" down -v --remove-orphans
echo "✅ Infrastructure stopped and volumes removed"