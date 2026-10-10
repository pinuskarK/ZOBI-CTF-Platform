# Member 4 — Integration, Testing & Documentation

This folder contains the integration evidence and repeatable test plan for the ZOBI CTF Play Box.

## Assignment 02 responsibilities

Member 4 is responsible for demonstrating and documenting:

- The complete C1 → C6 pathway, including dependencies and flag progression.
- Test cases, observed results, defects found/fixed, and checks for unintended shortcuts.
- Reset/recovery behaviour and risk-register outcomes.
- Changes from the Assignment 01 design, with a justification for each change.

## Current implementation context

The repository describes six stages:

| Stage | Domain | Known access/dependency |
|---|---|---|
| C1 | Steganography | File-based challenge |
| C2 | Cryptography | File-based challenge |
| C3 | Web security | Web challenge at `http://192.168.8.188:5003` in the current lab setup |
| C4 | Digital forensics | File-based challenge |
| C5 | Networking | Should provide the intended connection details for C6 |
| C6 | Linux/system security | SSH target documented in the lab notes as `10.10.20.50` |

These addresses are environment-specific. Confirm them on the actual running box before recording the demonstration. Do not commit real credentials or live flags.

## Run the lightweight checks

From the repository root:

```bash
python3 scripts/testing/smoke_test.py
```

Optional environment variables:

- `ZOBI_FLAG_API_URL`: flag API base URL (default `http://127.0.0.1:8080`)
- `ZOBI_C3_URL`: C3 URL (default `http://192.168.8.188:5003`)
- `ZOBI_CTFD_URL`: CTFd base URL; omitted unless supplied
- `ZOBI_C6_HOST`: C6 SSH host; default `10.10.20.50`
- `ZOBI_C6_PORT`: SSH port; default `22`

The smoke test only checks service reachability. It does not submit flags, exploit challenges, authenticate to SSH, or prove the full flag chain. Complete the manual acceptance checklist below on the real box and record actual evidence.

## Evidence to collect

Save timestamped screenshots or logs for:

1. Each challenge opening and intended solve path.
2. The flag validator accepting the correct flag and rejecting an incorrect one.
3. The C5 → C6 dependency, proving C6 details are obtained through the intended path.
4. Each reset/recovery operation and a post-reset retest.
5. Failed/unavailable service tests, defects, fixes, and retest results.
6. Repository commits identifying Member 4's contribution.

Do not label a test PASS until it has been run against the actual deployment.
