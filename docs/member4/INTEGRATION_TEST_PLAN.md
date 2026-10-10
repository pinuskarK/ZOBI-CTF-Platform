# ZOBI CTF — Integration and Acceptance Test Plan

**Owner:** Member 4 — Integration, Testing & Documentation  
**Environment:** Actual running ZOBI lab box  
**Execution status:** Not yet executed by this document; fill in the evidence/results during testing.

## 1. End-to-end stage flow

The expected learner journey is C1 → C2 → C3 → C4 → C5 → C6. Confirm the actual CTFd configuration and challenge descriptions match this sequence.

| Test ID | Test / expected result | Evidence to capture | Result |
|---|---|---|---|
| E2E-01 | CTFd opens and all six stages are visible to the intended user | Browser screenshot and URL | NOT RUN |
| E2E-02 | C1 opens and the intended steganography path reveals the next required clue/flag | Challenge screen and solve output | NOT RUN |
| E2E-03 | C2 opens and the intended cryptographic solution works with the supplied artefacts | Challenge screen and solver output | NOT RUN |
| E2E-04 | C3 web service is reachable and its intended vulnerability/solution works only as designed | Browser/dev-tools evidence | NOT RUN |
| E2E-05 | C4 evidence artefact can be analysed using the intended forensic workflow | Commands and output | NOT RUN |
| E2E-06 | C5 can be solved and yields only the intended C6 connection information | Challenge output; redact credentials | NOT RUN |
| E2E-07 | C6 is reachable using the details obtained through C5, not by skipping the earlier stage | SSH connection evidence; redact secrets | NOT RUN |
| E2E-08 | Flag submissions are accepted/rejected correctly and progress is recorded by CTFd/validator | Sanitised request/response screenshots | NOT RUN |

## 2. Negative and unintended-shortcut checks

| Test ID | Check | Expected result | Result |
|---|---|---|---|
| NEG-01 | Submit a clearly incorrect dummy flag | Rejected; no progress granted | NOT RUN |
| NEG-02 | Attempt C6 using no C5 clue | No unintended shortcut; access remains controlled by the intended challenge design | NOT RUN |
| NEG-03 | Inspect challenge files and public web responses for later-stage flags | Later-stage flags are not exposed early | NOT RUN |
| NEG-04 | Access service ports from outside the intended lab/network boundary | Only explicitly required ports are reachable | NOT RUN |
| NEG-05 | Restart the flag API and check health again | Service recovers and validation remains available | NOT RUN |
| NEG-06 | Repeat an already accepted submission | Behaviour is consistent with the documented scoring configuration | NOT RUN |

Perform tests only against the group's authorised lab environment.

## 3. Reset and recovery checks

| Test ID | Action | Expected result | Result |
|---|---|---|---|
| REC-01 | Record initial state, then reset C1 | Challenge returns to documented initial state | NOT RUN |
| REC-02 | Reset/restart each containerised stage (C1–C3) using its approved procedure | Service returns healthy; challenge artefacts are restored | NOT RUN |
| REC-03 | Restore/revert VM-backed stages (C4–C6) using the documented snapshot/reset procedure | VM state and challenge artefacts return to baseline | NOT RUN |
| REC-04 | Restart central flag API and CTFd dependencies | Services become available and validation still works | NOT RUN |
| REC-05 | Run the end-to-end smoke test after reset | No new failures; expected stage sequence remains intact | NOT RUN |

Record the exact reset command or snapshot name used for each stage. Do not invent a reset procedure where one has not been implemented.

## 4. Defect log

For every issue, record: ID, date/time, stage, expected behaviour, actual behaviour, severity, root cause, fix/commit, retest evidence, and final status.

| Defect ID | Description | Severity | Fix/commit | Retest result |
|---|---|---|---|---|
| D-001 | To be completed during live testing | — | — | NOT RUN |

## 5. Change log from Assignment 01

Compare the approved Assignment 01 design with the actual deployed box. Add one row for every difference; do not claim a change unless verified.

| Area | Approved design | Actual implementation | Justification / impact | Evidence |
|---|---|---|---|---|
| Deployment | Hybrid Docker + KVM/QEMU design | Verify on the running server | Record practical constraints and any change | Pending |
| CTFd / flag validation | Central challenge progression and validation | Verify configured integration | Record how progression and validation are enforced | Pending |
| Network / ports | Restricted access and isolated stages | Verify actual bindings and firewall | Record security or operational reason for each deviation | Pending |
| Reset / recovery | Repeatable reset of stages/box | Verify actual reset scripts or VM snapshots | Record recovery reliability and limitations | Pending |

## 6. Risk-register outcome review

Reconcile this table with the group's Assignment 01 risk register. These are review prompts, not claims that a risk has already been mitigated.

| Risk | Verification / evidence required | Outcome |
|---|---|---|
| Later-stage flag exposed early | Inspect files, web responses, logs and challenge configuration | PENDING |
| C6 bypasses C5 dependency | Attempt the intended and shortcut paths from a clean state | PENDING |
| Flag validator accepts invalid input | Submit an incorrect dummy flag | PENDING |
| Challenge state cannot be restored | Execute stage and whole-box reset/recovery tests | PENDING |
| Challenge service exposed outside intended boundary | Check host bindings and firewall from an authorised test point | PENDING |
| Secrets leaked in repository/logs | Review tracked files and sanitised logs; rotate any exposed real credentials | PENDING |

## 7. Final acceptance criteria

- [ ] All six stages are reachable and solvable using the intended path.
- [ ] Challenge dependencies and flag progression match the CTFd configuration.
- [ ] Correct and incorrect flag submissions behave as expected.
- [ ] Unintended shortcuts have been checked and documented.
- [ ] Stage and whole-box recovery procedures have been run and retested.
- [ ] Defects, fixes, and actual results have evidence.
- [ ] Assignment 01 design changes are justified with evidence.
- [ ] Screenshots/logs contain no live flags, passwords, tokens, or other secrets.
- [ ] All results in this document reflect tests actually performed on the running box.
