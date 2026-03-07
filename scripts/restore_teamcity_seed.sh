#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SEED_ARCHIVE="${1:-$PROJECT_ROOT/infra/teamcity_seed/teamcity-server-seed.tar.gz}"
RUNTIME_PARENT="${TEAMCITY_RUNTIME_PARENT:-${RUNNER_TEMP:-$PROJECT_ROOT/.tmp}}"
RUNTIME_ENV_FILE="${TEAMCITY_RUNTIME_ENV_FILE:-$RUNTIME_PARENT/teamcity-runtime.env}"

mkdir -p "$RUNTIME_PARENT"

if [ ! -f "$SEED_ARCHIVE" ]; then
    echo "TeamCity seed archive not found: $SEED_ARCHIVE"
    exit 1
fi

if [ -f "$RUNTIME_ENV_FILE" ]; then
    # shellcheck disable=SC1090
    . "$RUNTIME_ENV_FILE"
    if [ -n "${TEAMCITY_RUNTIME_DIR:-}" ] && [ -d "$TEAMCITY_RUNTIME_DIR" ]; then
        docker compose \
            -f "$PROJECT_ROOT/infra/docker_compose/docker-compose.yml" \
            down -v --remove-orphans >/dev/null 2>&1 || true
        rm -rf "$TEAMCITY_RUNTIME_DIR"
    fi
fi

TEAMCITY_RUNTIME_DIR="$(mktemp -d "$RUNTIME_PARENT/teamcity-seed.XXXXXX")"
TEAMCITY_SERVER_DATADIR="$TEAMCITY_RUNTIME_DIR/datadir"
TEAMCITY_SERVER_LOGS="$TEAMCITY_RUNTIME_DIR/logs"

mkdir -p "$TEAMCITY_SERVER_DATADIR" "$TEAMCITY_SERVER_LOGS"
tar -xzf "$SEED_ARCHIVE" -C "$TEAMCITY_SERVER_DATADIR"

{
    printf 'export TEAMCITY_SEEDED_STATE=%q\n' "1"
    printf 'export TEAMCITY_RUNTIME_DIR=%q\n' "$TEAMCITY_RUNTIME_DIR"
    printf 'export TEAMCITY_RUNTIME_ENV_FILE=%q\n' "$RUNTIME_ENV_FILE"
    printf 'export TEAMCITY_SERVER_DATADIR=%q\n' "$TEAMCITY_SERVER_DATADIR"
    printf 'export TEAMCITY_SERVER_LOGS=%q\n' "$TEAMCITY_SERVER_LOGS"
} > "$RUNTIME_ENV_FILE"

if [ -n "${GITHUB_ENV:-}" ]; then
    {
        printf 'TEAMCITY_SEEDED_STATE=%s\n' "1"
        printf 'TEAMCITY_RUNTIME_DIR=%s\n' "$TEAMCITY_RUNTIME_DIR"
        printf 'TEAMCITY_RUNTIME_ENV_FILE=%s\n' "$RUNTIME_ENV_FILE"
        printf 'TEAMCITY_SERVER_DATADIR=%s\n' "$TEAMCITY_SERVER_DATADIR"
        printf 'TEAMCITY_SERVER_LOGS=%s\n' "$TEAMCITY_SERVER_LOGS"
    } >> "$GITHUB_ENV"
fi

echo "Restored TeamCity seed to $TEAMCITY_SERVER_DATADIR"
echo "Runtime env file: $RUNTIME_ENV_FILE"
