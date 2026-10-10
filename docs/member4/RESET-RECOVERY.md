# ZOBI CTF — Reset and Recovery Runbook

**Owner:** Member 4 — Integration, Testing & Documentation  
**Status:** Runbook template; verify procedures on the actual deployment before claiming they were tested.

## Safety rules

1. Confirm the target is the authorised ZOBI lab host.
2. Record current service state and preserve relevant logs before changes.
3. Do not delete volumes, databases, VM disks, or participant scores as a first troubleshooting step.
4. Do not reset CTFd or its database without team approval; this may erase users, submissions, and scores.
5. Record operator, timestamp, action, outcome, and evidence for every recovery operation.

## Recovery decision table

| Symptom | First checks | Safe next action | Validation |
|---|---|---|---|
| CTFd portal unavailable | Check host, Compose service status, and recent logs | Restart only the identified failed service using the approved Compose configuration | Open participant portal and admin page; inspect logs |
| C3 unavailable | Check container status, port 5003 binding, and /health endpoint | Restart C3 using its existing Compose file; do not remove its data volume | Request /health and run intended challenge test |
| Flag API unavailable | Check zobi-flag-api.service and system journal | Restart service if failed; inspect logs if it fails again | Call health endpoint and test with a dummy incorrect flag |
| C6 VM unavailable | Check libvirt VM state, isolated network, and host-to-guest connectivity | Start existing VM or restore an approved snapshot; do not recreate it without backup | Confirm connectivity and recheck intended permissions |
| Challenge artefact missing | Check repository version and backup/evidence copies | Restore only the missing artefact from a verified source | Compare file listing/checksum and repeat challenge test |
| Suspected compromise or secret exposure | Preserve logs and restrict access as approved | Notify project lead; rotate exposed credentials and rebuild from known-good baseline if needed | Confirm restrictions and validate rebuilt service |

## Reset execution record

Fill this table only after performing the operation.

| Date/time | Component | Approved command/snapshot | Pre-reset state | Post-reset validation | Result | Evidence |
|---|---|---|---|---|---|---|
| Pending | — | — | — | — | NOT RUN | — |

## Full-box recovery checklist

- [ ] Confirm approved backup/snapshot and recovery owner.
- [ ] Preserve logs and configuration before changing state.
- [ ] Recover CTFd and dependencies without unintentionally deleting scoring data.
- [ ] Recover C3 and confirm its health endpoint.
- [ ] Recover C6 and confirm its isolated network and SSH path.
- [ ] Confirm challenge files and flags match the authorised source of truth.
- [ ] Run smoke tests and manual C1-to-C6 acceptance flow.
- [ ] Record failures, fixes, and evidence.

**Important:** This document does not claim automated reset scripts or VM snapshots exist. Confirm mechanisms on the actual host before relying on them.
