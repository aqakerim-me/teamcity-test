#!/usr/bin/env bash
set -euo pipefail

TEAMCITY_SERVER_IMAGE="${TEAMCITY_SERVER_IMAGE:-jetbrains/teamcity-server:2025.11.2}"
TEAMCITY_AGENT_IMAGE="${TEAMCITY_AGENT_IMAGE:-jetbrains/teamcity-agent:2025.11.2}"
TEAMCITY_IMAGE_CACHE_DIR="${TEAMCITY_IMAGE_CACHE_DIR:-${RUNNER_TEMP:-${TMPDIR:-/tmp}}/docker-cache/teamcity}"
SERVER_ARCHIVE="${TEAMCITY_IMAGE_CACHE_DIR}/teamcity-server.tar"
AGENT_ARCHIVE="${TEAMCITY_IMAGE_CACHE_DIR}/teamcity-agent.tar"

mkdir -p "$TEAMCITY_IMAGE_CACHE_DIR"

ensure_image() {
    local image_ref="$1"
    local archive_path="$2"
    local label="$3"

    if [ -f "$archive_path" ]; then
        echo "Loading ${label} image from cache: $archive_path"
        docker load -i "$archive_path"
        return
    fi

    echo "Cache miss for ${label} image; pulling $image_ref"
    docker pull "$image_ref"
    echo "Saving ${label} image to cache archive: $archive_path"
    docker image save -o "$archive_path" "$image_ref"
}

echo "Using TeamCity image cache directory: $TEAMCITY_IMAGE_CACHE_DIR"
ensure_image "$TEAMCITY_SERVER_IMAGE" "$SERVER_ARCHIVE" "server"
ensure_image "$TEAMCITY_AGENT_IMAGE" "$AGENT_ARCHIVE" "agent"

echo "Available TeamCity images:"
docker image ls | grep teamcity || true
