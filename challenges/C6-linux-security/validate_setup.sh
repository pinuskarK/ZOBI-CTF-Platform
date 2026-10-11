#!/usr/bin/env bash
# Read-only C6 setup checks. Run inside the authorised C6 guest.
# Does not exploit the challenge or print the flag.
set -u
failures=0

check_file() {
  local path="$1"
  if [ -f "$path" ]; then
    printf '[PASS] File exists: %s\n' "$path"
  else
    printf '[FAIL] Missing file: %s\n' "$path"
    failures=$((failures + 1))
  fi
}

printf '=== ZOBI C6 environment ===\n'
date -Is
hostname
ip -brief address 2>&1 || true
ip route 2>&1 || true

printf '\n=== Challenge account and script ===\n'
if id researcher >/dev/null 2>&1; then
  printf '[PASS] researcher account exists\n'
else
  printf '[FAIL] researcher account missing\n'
  failures=$((failures + 1))
fi
check_file /opt/zobi-c6/backup.sh
check_file /root/cure.txt

if [ -e /opt/zobi-c6/backup.sh ]; then
  stat -c 'owner=%U group=%G mode=%a path=%n' /opt/zobi-c6/backup.sh
  if [ -O /opt/zobi-c6/backup.sh ] && [ -w /opt/zobi-c6/backup.sh ]; then
    printf '[FAIL] Current administrator can write the script; inspect ownership and mode before release.\n'
    failures=$((failures + 1))
  fi
fi

printf '\n=== Sudo policy review ===\n'
if id researcher >/dev/null 2>&1; then
  sudo -l -U researcher 2>&1 || true
fi

printf '\nFailures: %s\n' "$failures"
printf 'This validator does not prove exploitability, CTFd flag validation, network isolation, or recovery.\n'
exit "$failures"
