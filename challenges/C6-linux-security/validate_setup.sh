#!/usr/bin/env bash
# Read-only C6 setup validator. Run as root inside the dedicated guest.
set -u

SCRIPT="/opt/zobi-c6/backup.sh"
SUDOERS="/etc/sudoers.d/zobi-c6-researcher"
FLAG="/root/cure.txt"
USER_NAME="researcher"
failures=0

check() {
    local label="$1"
    shift
    if "$@"; then
        printf '[PASS] %s\n' "$label"
    else
        printf '[FAIL] %s\n' "$label"
        failures=$((failures + 1))
    fi
}

check "researcher account exists" id "$USER_NAME"
check "backup script exists" test -f "$SCRIPT"
check "backup script is owned by root" test "$(stat -c '%U:%G' "$SCRIPT" 2>/dev/null)" = "root:root"
check "backup script is not group/world writable" bash -c '[[ -f "$1" && ! -w "$1" ]]' _ "$SCRIPT"
check "sudoers policy installed" test -f "$SUDOERS"
check "sudoers policy passes syntax validation" visudo -cf "$SUDOERS"
check "flag file exists" test -f "$FLAG"
check "flag file is root-owned" test "$(stat -c '%U:%G' "$FLAG" 2>/dev/null)" = "root:root"
check "flag file has mode 0600" bash -c '[[ -f "$1" && "$(stat -c %a "$1")" == "600" ]]' _ "$FLAG"

if [[ -f "$SCRIPT" ]]; then
    if grep -Eq '^[[:space:]]*tar[[:space:]]' "$SCRIPT"; then
        printf '[PASS] backup script contains the documented command-name lookup\n'
    else
        printf '[FAIL] backup script does not match the intended PATH-lookup teaching pattern\n'
        failures=$((failures + 1))
    fi
fi

printf '\nChecks failed: %s\n' "$failures"
printf 'This script does not attempt privilege escalation or read the flag contents.\n'
exit "$failures"
