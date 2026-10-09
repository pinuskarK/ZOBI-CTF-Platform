#!/usr/bin/env bash
set -euo pipefail

NETWORK_NAME="zobi_challenges"
SUBNET="172.20.0.0/24"
GATEWAY="172.20.0.1"

if docker network inspect "$NETWORK_NAME" >/dev/null 2>&1; then
    echo "Network '$NETWORK_NAME' already exists."
    docker network inspect "$NETWORK_NAME" \
        --format 'Name={{.Name}} Internal={{.Internal}} Subnet={{(index .IPAM.Config 0).Subnet}}'
    exit 0
fi

docker network create \
    --driver bridge \
    --subnet "$SUBNET" \
    --gateway "$GATEWAY" \
    "$NETWORK_NAME"

echo "Challenge network created successfully."
docker network inspect "$NETWORK_NAME" \
    --format 'Name={{.Name}} Internal={{.Internal}} Subnet={{(index .IPAM.Config 0).Subnet}}'
