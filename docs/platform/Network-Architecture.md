# ZOBI CTF Network Architecture

## 1. Purpose

This document defines the network segmentation and isolation architecture
for the ZOBI Capture The Flag platform.

The design separates the CTFd platform infrastructure from the individual
challenge environments.

## 2. Central Server

Host operating system:

- Ubuntu Server 26.04.1 LTS
- Host IP: 192.168.8.188/24
- Docker Engine
- Docker Compose
- KVM/QEMU for virtual-machine challenges

## 3. CTFd Platform Networks

### CTFd Participant-Facing Network

- Network: ctfd_default
- Driver: Docker bridge
- Subnet: 172.19.0.0/16
- Gateway: 172.19.0.1

Services:

- CTFd
- CTFd nginx

### CTFd Internal Network

- Network: ctfd_internal
- Driver: Docker bridge
- Subnet: 172.18.0.0/16
- Gateway: 172.18.0.1
- Internal network: Enabled

Services:

- CTFd
- MariaDB
- Redis

The database and Redis services are not connected directly to the
participant-facing network.

## 4. Challenge Environment Segmentation

The challenge environments will remain logically separated from the
CTFd infrastructure.

### Dedicated Challenge Network

A dedicated Docker bridge network named `zobi_challenges` is used for
containerized challenge environments.

- Network: zobi_challenges
- Driver: bridge
- Subnet: 172.20.0.0/24
- Gateway: 172.20.0.1
- C3 service is defined to attach to this network; confirm current attachment with `docker network inspect zobi_challenges` before the demo.

The challenge network is intended to remain separate from the CTFd participant-facing
network (`ctfd_default`) and the CTFd internal network (`ctfd_internal`). Inspect the live network and container attachments before claiming the separation is enforced.

### File-Based Challenges

- C1 - Steganography
- C2 - Cryptography
- C4 - Digital Forensics
- C5 - Networking

These challenges use controlled challenge files and evidence rather than
being directly exposed as public network services.

### Container-Based Challenge

- C3 - Web Security

C3 is defined in `challenges/C3-web-security/` as a Flask/SQLite Docker service. The Compose configuration attaches it to `zobi_challenges`; its host binding defaults to loopback. For remote participant access, configure only the intended lab interface and a matching firewall rule. Verify the live network attachments and firewall before describing the isolation as tested.

### Virtual-Machine Challenge

- C6 - Linux/System Security

The Linux/system-security challenge will run in an isolated KVM/QEMU
virtual machine.

## 5. Isolation Principles

1. CTFd infrastructure must remain separate from challenge environments.
2. MariaDB and Redis must remain on the internal CTFd network.
3. Challenge services should expose only the ports required for the
   corresponding challenge.
4. Challenge environments must not expose unnecessary services to the
   host LAN.
5. Challenge environments must not provide uncontrolled access to the
   public Internet or institutional network.
6. Challenge environments must support reset and recovery.
7. Firewall rules should follow a default-deny approach for unnecessary
   inbound traffic.

## 6. Current Verified CTFd Topology

Participant
    |
    v
CTFd nginx
172.19.0.3
    |
    v
CTFd
172.19.0.2
    |
    v
CTFd internal network
172.18.0.0/16
    |              |
    v              v
MariaDB          Redis
172.18.0.3       172.18.0.2

## 7. Implementation Status

Completed:

- CTFd Docker deployment
- CTFd participant-facing network
- CTFd internal network
- Database isolation
- Redis isolation
- Network inspection and verification

Next:

- Verify the C3 container's actual network attachment and host binding
- Implement/verify challenge-environment isolation
- Configure required ports
- Configure firewall rules
- Implement reset/recovery
- Implement platform health/testing scripts
- Integrate completed challenges from other members
