# ZOBI — Zombie Outbreak Breach Investigation

ZOBI is the team's six-stage cybersecurity CTF environment for IE3132 Assignment 02. CTFd provides the participant portal; file-based challenges are delivered as attachments, C3 is a Dockerised Flask/SQLite web-security lab, and C6 is a dedicated KVM/QEMU guest.

## Current platform facts

- Central host observed during setup: Ubuntu Server 26.04.1 LTS, 192.168.8.188.
- CTFd participant URL observed during setup: http://192.168.8.188:8081/.
- Custom Flask flag API: systemd service zobi-flag-api.service. A successful API test does not prove CTFd is integrated with it.
- C3: challenges/C3-web-security/; host port 5003; Flask, SQLite and Docker.
- C6: zobi-c6-cure; guest 10.10.20.50/24; isolated libvirt network zobi_c6_isolated.
- Intended stage order: C1 → C2 → C3 → C4 → C5 → C6.

The actual running host version differs from the Ubuntu 20.04 version in the original design report. Keep documentation aligned with the measured environment.

## Repository map

- challenges/ — platform-owned challenge source (C3); the Member 4 branch contains the integrated team artefacts.
- docs/MEMBER1_PLATFORM_ARCHITECTURE_IMPLEMENTATION.md — implementation evidence and limits.
- docs/MEMBER1_ASSIGNMENT2_COMPLIANCE_CHECKLIST.md — assignment requirements and outstanding evidence.
- docs/platform/ — CTFd, network and challenge deployment documentation.
- infrastructure/ — network and infrastructure notes.
- scripts/setup/ — platform setup helpers.
- scripts/testing/ — non-destructive checks and C3 unit tests.

## C3 local setup

Run on the authorised lab host:

    cd challenges/C3-web-security
    cp .env.example .env
    nano .env

Set a private C3_FLAG that exactly matches the CTFd configuration, a long random FLASK_SECRET_KEY, and a private C3_DEMO_PASSWORD used to seed the lab account. Do not commit .env. The default host binding is loopback. To allow authorised participants from the LAN, set C3_BIND_ADDRESS to the lab host's intended LAN address and enforce the matching firewall rule.

From the repository root, run the approved network setup helper and inspect the result:

    bash scripts/setup/create-challenge-network.sh
    sudo docker network inspect zobi_challenges

The helper creates an internal bridge on a clean setup and stops if an existing network is not internal. Do not delete an active network to make the check pass; plan and verify a safe migration.
    docker compose up -d --build
    docker compose ps
    curl -i http://127.0.0.1:5003/health

Do not expose the deliberately vulnerable C3 service to the public Internet. Inspect the network and firewall rather than assuming that a named bridge provides complete isolation.

## C3 automated tests

From challenges/C3-web-security:

    python3 -m venv .venv
    . .venv/bin/activate
    pip install -r requirements.txt
    python -m unittest discover -s tests -v

These tests use a temporary database. They do not prove the live Docker service, CTFd flag configuration, firewall isolation or end-to-end progression.

## Platform inventory

Run on the Ubuntu host to collect evidence:

    hostnamectl
    lsb_release -a
    docker --version
    sudo docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Ports}}\t{{.Status}}'
    sudo docker network ls
    sudo systemctl status zobi-flag-api.service --no-pager
    sudo virsh list --all
    sudo virsh net-info zobi_c6_isolated
    sudo ss -ltnp
    free -h
    df -h /

Run the read-only platform check:

    bash scripts/testing/member1-platform-check.sh

## C6

The C6 source templates are in challenges/C6-linux-security/ (backup script, sudoers example, and read-only setup validator). Review the lab-only warning before use, and compare the templates with the actual VM. See docs/platform/C6-CURE-Research-Server.md. The VM disk, live flag and credentials are intentionally not stored in this repository.

## Assignment completion status

This repository documents the platform and provides repeatable checks. Do not claim final acceptance until the live team environment demonstrates all six intended paths, correct and incorrect flags, progression rules, isolation, reset/recovery, logs, and measured resource use. Keep evidence and secrets out of public logs.
