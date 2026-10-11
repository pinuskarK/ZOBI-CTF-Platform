#!/usr/bin/env bash
set -euo pipefail

NETWORK_NAME="zobi_challenges"
SUBNET="172.20.0.0/24"
GATEWAY="172.20.0.1"

if docker network inspect "$NETWORK_NAME" >/dev/null 2>&1; then
    internal="$(docker network inspect "$NETWORK_NAME" --format '{{.Internal}}')"
    docker network inspect "$NETWORK_NAME" \
        --format 'Name={{.Name}} Internal={{.Internal}} Subnet={{(index .IPAM.Config 0).Subnet}}'
    if [[ "$internal" != "true" ]]; then
        echo "ERROR: $NETWORK_NAME exists but is not an internal network." >&2
        echo "Do not delete or recreate it automatically while containers may be attached." >&2
        echo "Plan a maintenance window, preserve configuration/data, and migrate to an approved internal network." >&2
        exit 2
    fi
    echo "The existing challenge network is marked internal."
    exit 0
fi

docker network create \
    --driver bridge \
    --internal \
    --subnet "$SUBNET" \
    --gateway "$GATEWAY" \
    "$NETWORK_NAME"

echo "Internal challenge network created."
docker network inspect "$NETWORK_NAME" \
    --format 'Name={{.Name}} Internal={{.Internal}} Subnet={{(index .IPAM.Config 0).Subnet}}'
