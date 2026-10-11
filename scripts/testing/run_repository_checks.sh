#!/usr/bin/env bash
# Run repository-only checks. Live network tests are opt-in and require the lab host.
set -u
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"
failures=0

run() {
  local label="$1"; shift
  printf '\n===== %s =====\n' "$label"
  if "$@"; then
    printf '[PASS] %s\n' "$label"
  else
    printf '[FAIL] %s\n' "$label"
    failures=$((failures + 1))
  fi
}

run 'Repository artefacts' python3 scripts/testing/check_artifacts.py

if python3 -c 'import flask, gunicorn' >/dev/null 2>&1; then
  run 'C3 application unit tests' bash -c 'cd challenges/C3-web-security && PYTHONPATH=. python3 -m unittest discover -s tests -v'
else
  printf '[SKIP] C3 unit tests: install challenges/C3-web-security/requirements.txt first.\n'
fi

if python3 -c 'import scapy' >/dev/null 2>&1; then
  run 'C5 PCAP integrity' python3 scripts/testing/validate_c5_pcap.py
else
  printf '[SKIP] C5 PCAP validation: Scapy is not installed in this Python environment.\n'
fi

if [[ "${ZOBI_RUN_LIVE_SMOKE:-0}" == "1" ]]; then
  run 'Live HTTP smoke test' python3 scripts/testing/smoke_test.py
else
  printf '\n[SKIP] Live HTTP smoke test. Set ZOBI_RUN_LIVE_SMOKE=1 on the authorised lab host.\n'
fi

printf '\nRepository check failures: %s\n' "$failures"
printf 'A successful run does not prove CTFd flags, stage dependencies, isolation, or reset/recovery.\n'
exit "$failures"
