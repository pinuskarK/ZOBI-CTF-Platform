#!/usr/bin/env bash
# Read-only inventory checks for the authorised ZOBI Ubuntu host.
# This script does not change services, firewall rules, VM state, or data.
set -u

section() { printf '\n===== %s =====\n' "$1"; }
run_check() {
  local label="$1"; shift
  printf '\n--- %s ---\n' "$label"
  if command -v "$1" >/dev/null 2>&1; then
    "$@"
  else
    printf 'SKIP: command not installed: %s\n' "$1"
  fi
}

section "Timestamp and host"
date -Is
hostnamectl 2>&1 || true
lsb_release -a 2>&1 || true

section "Docker"
docker --version 2>&1 || true
if command -v systemctl >/dev/null 2>&1; then
  systemctl is-active docker 2>&1 || true
fi
if command -v docker >/dev/null 2>&1; then
  docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Ports}}\t{{.Status}}' 2>&1 || true
  docker network ls 2>&1 || true
fi

section "Flag API"
if command -v systemctl >/dev/null 2>&1; then
  systemctl is-active zobi-flag-api.service 2>&1 || true
  systemctl --no-pager --lines=15 status zobi-flag-api.service 2>&1 || true
fi

section "KVM/libvirt"
if command -v virsh >/dev/null 2>&1; then
  virsh list --all 2>&1 || true
  virsh net-info zobi_c6_isolated 2>&1 || true
fi

section "Listening sockets"
ss -ltn 2>&1 || true

section "Resources"
free -h 2>&1 || true
df -h / 2>&1 || true

printf '\nScope: inventory only. This does not prove flags, stage dependencies, firewall isolation, reset/recovery, or load capacity.\n'
