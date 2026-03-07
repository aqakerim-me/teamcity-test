#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
DEFAULT_COMPOSE_FILE="$SCRIPT_DIR/../infra/docker_compose/docker-compose.yml"
DEFAULT_RUNTIME_ENV_FILE="${TEAMCITY_RUNTIME_ENV_FILE:-${TEAMCITY_RUNTIME_PARENT:-${RUNNER_TEMP:-$PROJECT_ROOT/.tmp}}/teamcity-runtime.env}"
TC_URL="http://localhost:8111"
TIMEOUT=600
SEEDED_STATE="${TEAMCITY_SEEDED_STATE:-0}"
LAST_FAILED_PHASE="transport"
SERVER_CONTAINER_NAME="teamcity-server"
CRASH_LOOP_THRESHOLD=3

if [ "$#" -gt 0 ]; then
    COMPOSE_FILES=("$@")
else
    COMPOSE_FILES=("$DEFAULT_COMPOSE_FILE")
fi

export TEAMCITY_RUNTIME_ENV_FILE="$DEFAULT_RUNTIME_ENV_FILE"
echo "Resolved TeamCity runtime env file: $TEAMCITY_RUNTIME_ENV_FILE"
bash "$SCRIPT_DIR/restore_teamcity_seed.sh"

if [ -f "$TEAMCITY_RUNTIME_ENV_FILE" ]; then
    # shellcheck disable=SC1090
    . "$TEAMCITY_RUNTIME_ENV_FILE"
fi
SEEDED_STATE="${TEAMCITY_SEEDED_STATE:-1}"

COMPOSE_CMD=(docker compose)
for compose_file in "${COMPOSE_FILES[@]}"; do
    COMPOSE_CMD+=(-f "$compose_file")
done

echo "Starting TeamCity infrastructure from: ${COMPOSE_FILES[*]}"
"${COMPOSE_CMD[@]}" up -d

print_timeout_and_logs() {
    echo "Timed out waiting for TeamCity readiness (last failed phase: ${LAST_FAILED_PHASE})"
    docker inspect "$SERVER_CONTAINER_NAME" 2>/dev/null || true
    "${COMPOSE_CMD[@]}" logs --tail=100
    exit 1
}

is_real_login_page() {
    local body="$1"
    [[ "$body" == *"Log in to TeamCity"* ]] && [[ "$body" != *"TeamCity is starting"* ]]
}

check_for_crash_loop() {
    local inspect_output state restart_count
    inspect_output="$(docker inspect -f '{{.State.Status}} {{.RestartCount}}' "$SERVER_CONTAINER_NAME" 2>/dev/null || true)"
    if [ -z "$inspect_output" ]; then
        return 1
    fi

    state="${inspect_output%% *}"
    restart_count="${inspect_output##* }"

    if [ "$state" = "restarting" ] || { [ "$restart_count" -ge "$CRASH_LOOP_THRESHOLD" ] 2>/dev/null; }; then
        echo "TeamCity server container is crash-looping (state=$state, restarts=$restart_count)"
        echo "Recent teamcity-server logs:"
        "${COMPOSE_CMD[@]}" logs --tail=200 "$SERVER_CONTAINER_NAME" || true
        exit 1
    fi

    return 1
}

echo "Waiting for TeamCity to respond..."
elapsed=0
until curl -s -o /dev/null -w "%{http_code}" "$TC_URL/" | grep -qE "^[1-5][0-9][0-9]$"; do
    LAST_FAILED_PHASE="transport"
    check_for_crash_loop || true
    if [ "$elapsed" -ge "$TIMEOUT" ]; then
        print_timeout_and_logs
    fi
    echo "  ... waiting (${elapsed}s)"
    sleep 10
    elapsed=$((elapsed + 10))
done

echo "TeamCity transport is reachable; waiting for application readiness..."

elapsed=0
while true; do
    check_for_crash_loop || true
    AUTH_CODE=$(curl -s -u "admin:admin" -o /dev/null -w "%{http_code}" "$TC_URL/app/rest/server")
    LOGIN_BODY=$(curl -s "$TC_URL/login.html")
    ROOT_BODY=$(curl -s "$TC_URL/")

    if [ "$AUTH_CODE" = "200" ]; then
        if is_real_login_page "$LOGIN_BODY"; then
            echo "Detected configured TeamCity state; application is ready."
            break
        fi
        LAST_FAILED_PHASE="ui"
    else
        LAST_FAILED_PHASE="api"
    fi

    if [ "$elapsed" -ge "$TIMEOUT" ]; then
        print_timeout_and_logs
    fi

    if [[ "$ROOT_BODY" == *"Page: maintenance-welcome"* ]] || [[ "$ROOT_BODY" == *"Stage: LICENSE_AGREEMENT_SCREEN"* ]] || [[ "$ROOT_BODY" == *"TeamCity Maintenance"* ]]; then
        LAST_FAILED_PHASE="maintenance"
        echo "  ... TeamCity is still transitioning through maintenance/license startup (${elapsed}s)"
    fi

    if [ "$LAST_FAILED_PHASE" = "api" ]; then
        echo "  ... waiting for authenticated REST readiness (${elapsed}s)"
    elif [ "$LAST_FAILED_PHASE" = "ui" ]; then
        echo "  ... waiting for login page readiness (${elapsed}s)"
    fi
    sleep 10
    elapsed=$((elapsed + 10))
done

echo "TeamCity is ready at $TC_URL"
