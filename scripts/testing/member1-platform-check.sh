#!/usr/bin/env bash
# Read-only Member 1 platform inventory. Run on the Ubuntu ZOBI host.
set -u

section() { printf '\n===== %s =====\n' "$1"; }
run_check() {
  local label="$1"; shift
  printf '\n--- %s ---\n' "$label"
  "$@" 2>&1 || printf '[WARN] command returned non-zero: %s\n' "$label"
}

section "Host"
run_check "hostname" hostnamectl
run_check "OS release" lsb_release -a
run_check "disk" df -h /
run_check "memory" free -h

section "Docker"
run_check "Docker version" docker --version
run_check "Docker service" systemctl is-active docker
run_check "running containers" sudo docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Ports}}\t{{.Status}}'
run_check "Docker networks" sudo docker network ls

section "Flag API"
run_check "flag API service" sudo systemctl status zobi-flag-api.service --no-pager

section "C6 virtual machine"
run_check "VM list" sudo virsh list --all
run_check "C6 network" sudo virsh net-info zobi_c6_isolated
run_check "C6 guest interface" sudo virsh domiflist zobi-c6-cure

section "Listening TCP ports"
run_check "listeners" sudo ss -ltnp

printf '\nInventory finished. Review warnings and save a sanitised copy as evidence.\n'
printf 'This script is observational only; it does not test flag correctness, firewall policy, reset, or end-to-end challenge completion.\n'
