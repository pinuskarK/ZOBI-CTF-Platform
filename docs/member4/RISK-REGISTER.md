# ZOBI CTF — Integration Risk Register

**Owner:** Member 4 — Integration, Testing & Documentation  
**Purpose:** Track operational risks found while integrating and testing the six-stage CTF. Reconcile with the team's Assignment 01 risk register.

Initial ratings are review estimates, not claims that a risk has occurred.

| ID | Risk | Likelihood | Impact | Mitigation / control | Verification evidence | Status |
|---|---|---|---|---|---|---|
| R-01 | Later-stage flag exposed before that stage | Medium | High | Keep flags out of public artefacts and descriptions; inspect tracked files and web responses | Repository review and participant-access tests | OPEN — verify |
| R-02 | C6 reachable without completing C5 | Medium | High | Keep C6 details in intended C5 artefact and enforce CTFd progression where supported | Clean-account shortcut test and configuration screenshot | OPEN — verify |
| R-03 | Incorrect flags accepted or valid flags rejected due to case/prefix mismatch | Medium | Medium | Maintain source-of-truth flag list and compare CTFd configuration with challenge artefacts | Positive and negative submission evidence | OPEN — verify |
| R-04 | Challenge service reachable outside authorised lab boundary | Medium | High | Restrict firewall/bindings; use controlled VPN or lab network; avoid public exposure of vulnerable services | Binding/firewall review from authorised test point | OPEN — verify |
| R-05 | CTFd or challenge data lost during reset | Medium | High | Back up data and document approved reset/snapshot procedure | Recovery record and post-reset checks | OPEN — verify |
| R-06 | Live credentials or flags committed or logged | Medium | High | Keep secrets out of source control; redact evidence; rotate exposed real credentials | Tracked-file and evidence review | OPEN — verify |
| R-07 | Challenge service fails after restart or reboot | Medium | Medium | Verify restart policy and health checks; document manual recovery | Restart/reboot test with timestamps | OPEN — verify |
| R-08 | Report differs from actual OS, VM size, address, or port | Medium | Medium | Compare report with live host/VM configuration and document justified deviations | Sanitised configuration evidence and change log | OPEN — reconcile |
| R-09 | Custom C6 completion page assumed to be stock CTFd functionality | Medium | Medium | Treat as a separate feature requiring implementation and testing | Completion-page implementation and final submission evidence | OPEN — verify |

## Review log

| Date | Reviewer | Change / decision | Evidence |
|---|---|---|---|
| Pending | — | — | — |

Close a risk only after mitigation is implemented and evidence supports the outcome.
