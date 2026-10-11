# ZOBI Challenge Network

## Intended network policy

| Property | Value |
|---|---|
| Name | zobi_challenges |
| Driver | bridge |
| Internal flag for a clean deployment | true |
| Subnet | 172.20.0.0/24 |
| Gateway | 172.20.0.1 |

The dedicated challenge network is intended to keep challenge containers separate from CTFd networks and restrict ordinary container egress. This setting alone does not prove complete isolation: published host ports, host routing, firewall policy and other network attachments must also be inspected.

## Networks

CTFd uses separate networks for participant-facing access and internal services. Challenge containers should not be attached to the CTFd database/cache network.

- CTFd participant-facing network: ctfd_default
- CTFd internal services network: ctfd_internal
- Challenge network: zobi_challenges

## Create or inspect

From the repository root on the authorised Ubuntu host:

    bash scripts/setup/create-challenge-network.sh
    sudo docker network inspect zobi_challenges

For a new network, the script creates an internal bridge on 172.20.0.0/24. If a network with the same name already exists but is not internal, the script stops and reports the mismatch rather than deleting a network that may have running containers attached. Plan any migration separately and preserve the current deployment first.

## Validation

- Inspect the network's Internal value, subnet and connected containers.
- Confirm C3 is attached only to the intended challenge network.
- Confirm C3's published host binding is restricted to the approved lab interface.
- Test participant-to-C3 reachability and attempt out-of-scope routes from an authorised test point.
- Confirm the CTFd database and cache are not reachable from the challenge container.
- Record actual firewall rules and allowed/blocked results.

Do not claim isolation based only on the network name or the existence of a Docker bridge.
