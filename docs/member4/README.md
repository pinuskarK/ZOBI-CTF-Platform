# Member 4 — Integration, Testing & Documentation

This folder contains the integration plan, test results register, reset/recovery runbook, risk register, and design-change comparison for the ZOBI CTF Play Box.

## Current status

- **Reported complete:** C1 Steganography, C2 Cryptography, C3 Web Security, C4 Digital Forensics, and C6 Linux/System Security.
- **Not finished:** C5 Network Analysis.
- **Overall end-to-end acceptance:** Pending C5. Do not describe the full C1-to-C6 sequence as complete until a clean participant account has followed the intended path through all six stages.

The stage statuses above reflect the current project update. The documents distinguish implementation status from independently captured acceptance evidence.

## Member 4 responsibilities

1. Integrate the six challenge stages and confirm dependencies and flag progression.
2. Maintain test cases, actual results, defects, fixes and retest evidence.
3. Test reset/recovery behaviour and update the risk register with evidence-based outcomes.
4. Compare the approved Assignment 01 design with the deployed implementation and justify deviations.
5. Keep setup, execution and recovery documentation aligned with the actual lab.

## Documents in this folder

| File | Purpose |
|---|---|
| INTEGRATION_TEST_PLAN.md | End-to-end acceptance plan, negative tests, C5 completion gate and reset checks |
| TEST_RESULTS.md | Stage-by-stage implementation status, known observations, evidence checklist and blocker log |
| RESET-RECOVERY.md | Safe recovery procedures and execution record |
| RISK-REGISTER.md | Integration/security/recovery risks and required verification |
| DESIGN-CHANGES.md | Comparison of intended architecture and implementation details |

## Stage summary

| Stage | Domain | Intended path | Status |
|---|---|---|---|
| C1 | Steganography | Extract a hidden note from the mystery photograph using Steghide | Reported complete |
| C2 | Cryptography | Decode the Caesar-shifted message and follow its clue | Reported complete |
| C3 | Web security | Solve the intentionally vulnerable Flask Research Portal challenge | Reported complete |
| C4 | Digital forensics | Analyse the provided forensic evidence archive | Reported complete |
| C5 | Network analysis | Analyse the PCAP to find the intended clue for C6 | Not finished |
| C6 | Linux/system security | Complete the Linux challenge on the isolated Ubuntu VM through the intended path | Reported complete; C5 handoff pending |

## Run the non-destructive HTTP smoke test

From the repository root, run:

    python3 scripts/testing/smoke_test.py

Defaults:
- Flag API: http://127.0.0.1:8080/
- C3 health endpoint: http://192.168.8.188:5003/health

Optional environment variables:
- ZOBI_FLAG_API_URL — Flag API base URL
- ZOBI_C3_URL — C3 base URL
- ZOBI_CTFD_URL — if set, also check CTFd
- ZOBI_HTTP_TIMEOUT — request timeout in seconds

Example:

    ZOBI_CTFD_URL=http://127.0.0.1:8081 python3 scripts/testing/smoke_test.py

This script checks HTTP reachability only. It does not submit flags, exploit challenges, log into SSH, validate reset procedures, or prove the full flag chain.

## Evidence required before final acceptance

- Screenshots of each stage and its intended solve path.
- Accepted and rejected answer behaviour, with secrets redacted.
- CTFd scoring/progression evidence.
- PCAP solve evidence and C5-to-C6 handoff after C5 is finished.
- Reset/recovery commands or snapshot names and post-recovery retest results.
- Defect descriptions, fixes, commit references and retest evidence.
- Sanitised live configuration showing ports, isolation and VM settings.
- One complete clean-account C1-to-C6 run.

Never put real credentials, tokens or live flags in public-facing docs or screenshots. Do not mark a test PASS until it has actually been executed and its evidence saved.


## Actual integrated artefacts and test code

This branch now includes the completed-stage artefacts needed for integration review:

- C1: `challenges/C1-steganography/mystery_photo.jpg`
- C2: `challenges/C2-cryptography/lab_assistant_msg.txt`
- C3: Flask application, database initializer, Dockerfile, Compose file and requirements under `challenges/C3-web-security/`
- C4: `access.log`, `deleted_message.txt`, `network.log`, `system.log` and `usb_history.txt` under `challenges/C4-digital-forensics/`

C5's unfinished PCAP has intentionally not been included as a completed stage. C6 remains a VM-based challenge; the VM itself and secrets are not stored in this repository.

Additional Member 4 files:
- `docs/member4/STAGE-INTEGRATION-GUIDE.md` — exact stage artefacts, current lab endpoints, C3 commands, expected integration behaviour and demonstration checklist.
- `scripts/testing/check_artifacts.py` — verifies that all expected completed-stage files and Member 4 documents exist.
- `scripts/testing/smoke_test.py` — checks HTTP service reachability only.

Run the repository integrity test from the repository root:

```bash
python3 scripts/testing/check_artifacts.py
```

Then run the service smoke test:

```bash
python3 scripts/testing/smoke_test.py
```

A passing artifact check does not mean the runtime challenges or full C1-to-C6 sequence have passed acceptance testing. C5 must be finished before the full flow can be verified.
