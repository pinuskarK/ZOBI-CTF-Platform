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
  owner="$(stat -c '%U' /opt/zobi-c6/backup.sh)"
  mode="$(stat -c '%a' /opt/zobi-c6/backup.sh)"
  printf 'owner=%s mode=%s path=%s\n' "$owner" "$mode" /opt/zobi-c6/backup.sh
  if [ "$owner" != "root" ]; then
    printf '[FAIL] Challenge script is not owned by root.\n'
    failures=$((failures + 1))
  fi
  if find /opt/zobi-c6/backup.sh -maxdepth 0 -perm /022 -print -quit | grep -q .; then
    printf '[FAIL] Group/other write permission is enabled on the challenge script.\n'
    failures=$((failures + 1))
  else
    printf '[PASS] Challenge script is not group/other writable\n'
  fi
fi

printf '\n=== Sudo policy review ===\n'
if id researcher >/dev/null 2>&1; then
  sudo -l -U researcher 2>&1 || true
fi

printf '\nFailures: %s\n' "$failures"
printf 'This validator does not prove exploitability, CTFd flag validation, network isolation, or recovery.\n'
exit "$failures"
