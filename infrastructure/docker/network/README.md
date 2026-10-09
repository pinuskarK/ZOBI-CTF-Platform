# ZOBI Challenge Network

## Network

The ZOBI challenge environment uses a dedicated Docker bridge network.

| Property | Value |
|---|---|
| Name | `zobi_challenges` |
| Driver | `bridge` |
| Subnet | `172.20.0.0/24` |
| Gateway | `172.20.0.1` |

## Purpose

This network separates containerized challenge environments from the
CTFd platform networks.

CTFd uses:

- `ctfd_default` — participant-facing network
- `ctfd_internal` — internal CTFd services

Challenge containers use:

- `zobi_challenges` — challenge environment network

## Creation

The network can be created with:

sudo docker network create \
  --driver bridge \
  --subnet 172.20.0.0/24 \
  --gateway 172.20.0.1 \
  zobi_challenges
