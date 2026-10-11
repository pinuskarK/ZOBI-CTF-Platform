# ZOBI Lab Firewall and Port Policy

This file records the intended exposure policy. It is not an applied firewall ruleset. Inspect the live host and obtain team approval before changing firewall settings; a mistaken SSH or default-policy change can lock out the administrator.

## Intended exposure matrix

| Service | Port | Intended reachability | Verification |
|---|---:|---|---|
| CTFd participant portal | TCP 8081 | Authorised participant LAN only | Test from an approved client and an out-of-scope network |
| C3 Research Portal | TCP 5003 | Only the intended lab interface / participant network | Check Docker port binding and host firewall |
| SSH to central host | TCP 22 | Administrator management network only | Test from authorised admin client |
| C6 guest SSH | TCP 22 on 10.10.20.50 | Host or approved jump path; not directly exposed to the participant LAN unless explicitly required | Compare host-to-guest and participant-to-guest tests |
| C6 VNC | TCP 5900 | Host loopback only, accessed via SSH forwarding | Confirm listener is 127.0.0.1:5900 |
| Flask flag API | TCP 8080, if configured | Localhost/trusted platform components only | Inspect systemd service and listener |
| PostgreSQL | TCP 5432, if configured | Localhost or trusted internal network only | Inspect listener and firewall; never expose publicly |

## Principles

1. Default-deny unnecessary inbound connections.
2. Expose only services required by the participant workflow.
3. Do not expose intentionally vulnerable C3 to the public Internet.
4. Keep CTFd database/cache ports internal.
5. Keep C6 VNC bound to loopback.
6. Keep the isolated libvirt network separate from the participant LAN.
7. Record allowed and blocked paths with source, destination, port, expected result, actual result and timestamp.
8. Do not claim isolation from a subnet name alone; inspect routes, Docker network attachments, libvirt network XML, listening sockets and firewall rules.

## Evidence commands

Run on the Ubuntu host:

    sudo ss -ltnp
    sudo ufw status verbose
    sudo nft list ruleset
    sudo docker network ls
    sudo docker network inspect zobi_challenges
    sudo virsh net-info zobi_c6_isolated
    sudo virsh net-dumpxml zobi_c6_isolated

Some systems use iptables rather than UFW/nftables directly. Inspect the actual active firewall backend. Redact public IPs or sensitive details before sharing logs.

## Change procedure

- Save the current firewall state before edits.
- Confirm local/console recovery access is available.
- Apply one approved change at a time.
- Test both allowed and denied paths from the correct source networks.
- Confirm SSH and CTFd remain reachable as intended.
- Record rollback instructions and attach sanitised output.
