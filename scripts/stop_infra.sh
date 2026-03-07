#!/usr/bin/env bash
# Tears down the TeamCity containers and removes the disposable runtime by
# default. Pass --preserve-volumes only when you intentionally want to keep
# Docker volumes around for debugging.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
DEFAULT_COMPOSE_FILE="$SCRIPT_DIR/../infra/docker_compose/docker-compose.yml"
RUNTIME_ENV_FILE="${TEAMCITY_RUNTIME_ENV_FILE:-${TEAMCITY_RUNTIME_PARENT:-${RUNNER_TEMP:-$PROJECT_ROOT/.tmp}}/teamcity-runtime.env}"
PRESERVE_VOLUMES=0
COMPOSE_FILES=()

if [ -n "$RUNTIME_ENV_FILE" ] && [ -f "$RUNTIME_ENV_FILE" ]; then
    # shellcheck disable=SC1090
    . "$RUNTIME_ENV_FILE"
fi

for arg in "$@"; do
    case "$arg" in
        --preserve-volumes)
            PRESERVE_VOLUMES=1
            ;;
        --help|-h)
            echo "Usage: $0 [--preserve-volumes] [compose-file ...]"
            exit 0
            ;;
        *)
            COMPOSE_FILES+=("$arg")
            ;;
    esac
done

if [ "${#COMPOSE_FILES[@]}" -eq 0 ]; then
    COMPOSE_FILES=("$DEFAULT_COMPOSE_FILE")
fi

COMPOSE_CMD=(docker compose)
for compose_file in "${COMPOSE_FILES[@]}"; do
    COMPOSE_CMD+=(-f "$compose_file")
done

echo "Stopping TeamCity infrastructure..."
if [ "$PRESERVE_VOLUMES" = "1" ]; then
    "${COMPOSE_CMD[@]}" down --remove-orphans
else
    "${COMPOSE_CMD[@]}" down -v --remove-orphans
fi

if [ -n "${TEAMCITY_RUNTIME_DIR:-}" ] && [ -d "$TEAMCITY_RUNTIME_DIR" ]; then
    rm -rf "$TEAMCITY_RUNTIME_DIR"
fi

if [ -n "$RUNTIME_ENV_FILE" ] && [ -f "$RUNTIME_ENV_FILE" ]; then
    rm -f "$RUNTIME_ENV_FILE"
fi

if [ "$PRESERVE_VOLUMES" = "1" ]; then
    echo "Infrastructure stopped; TeamCity volumes preserved"
else
    echo "Infrastructure stopped and volumes removed"
fi
