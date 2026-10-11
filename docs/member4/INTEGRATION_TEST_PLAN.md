# ZOBI CTF — Integration and Acceptance Test Plan

**Owner:** Member 4 — Integration, Testing & Documentation  
**Current status:** C1, C2, C3, C4 and C6 are reported complete by the project owner. C5 artefacts are integrated; live acceptance remains pending. Therefore the complete C1-to-C6 acceptance run remains pending until C5's live attachment, flag validation, and C5-to-C6 handoff are tested.

## 1. Six-stage integration overview

| Stage | Domain | Intended learner task | Current status |
|---|---|---|---|
| C1 | Steganography | Extract the hidden note from the supplied photograph with Steghide | Reported complete |
| C2 | Cryptography | Decode the Caesar-shifted message and follow the resulting clue | Reported complete |
| C3 | Web security | Use the intended SQL-injection path against the Flask Research Portal challenge | Reported complete |
| C4 | Digital forensics | Analyse the supplied evidence archive and correlate the relevant logs | Reported complete |
| C5 | Network analysis | Analyse the integrated PCAP and identify the clue needed to continue to C6 | Artefact integrated; live acceptance pending |
| C6 | Linux/system security | Reach the isolated Ubuntu VM through the intended clue and complete the Linux privilege-escalation exercise | Reported complete; dependency handoff awaits C5 |

The status labels above reflect the project owner's update. Attach live evidence before claiming each stage has been independently acceptance-tested.

## 2. Acceptance tests

| Test ID | Procedure | Expected result | Current result |
|---|---|---|---|
| INT-01 | Open CTFd as a participant | Portal loads and participant can sign in | Capture current evidence |
| INT-02 | Open C1 and follow intended steganography path | Hidden note is recovered and correct answer is accepted | Reported complete; attach evidence |
| INT-03 | Open C2 and decode supplied artefact | Decoded clue is meaningful and correct answer is accepted | Reported complete; attach evidence |
| INT-04 | Open C3 and use intended SQLi path | Challenge behaves as designed and correct answer is accepted | Reported complete; attach evidence |
| INT-05 | Download and analyse C4 evidence bundle | Intended forensic finding is reproducible and correct answer is accepted | Reported complete; attach evidence |
| INT-06 | Open C5 and analyse its PCAP | Player obtains the intended clue without later-stage flags being exposed prematurely | PENDING — live C5 acceptance not recorded |
| INT-07 | Use clue from C5 to access C6 | Participant reaches the isolated VM through the intended path | PENDING — live C5-to-C6 handoff not recorded |
| INT-08 | Complete C6 task and submit answer | Validator accepts intended answer and records progress | C6 reported complete; end-to-end handoff pending |
| INT-09 | Submit an incorrect dummy answer at each applicable stage | Incorrect answer is rejected and does not grant progress | Capture evidence |
| INT-10 | Run C1 through C6 using a clean participant account | All stages work in sequence and completion state is recorded | PENDING — live C5 acceptance not recorded |
| INT-11 | Restart/recover each implemented service or VM using its approved procedure | Service returns to a healthy, known state without unintended loss of scores/data | Evidence pending |
| INT-12 | Inspect files, web responses, CTFd settings and network exposure for shortcuts | No unintended early access to later-stage flags or services | Evidence pending |

## 3. C5 completion gate

Do not close the following items until C5 live acceptance is complete:

- [ ] Final PCAP artefact is in the agreed repository/location and attached to CTFd.
- [ ] Intended network-analysis solve path is repeatable on a clean copy.
- [ ] Resulting clue gives only the intended C6 connection information.
- [ ] No C6 flag or unrelated secret is exposed in the PCAP description, download path, repository metadata, or public response.
- [ ] A participant can follow C5 to C6 using the actual configured environment.
- [ ] CTFd records the expected score/progression for C5.
- [ ] Evidence is saved with secrets redacted.

## 4. Negative and unintended-shortcut checks

| Test ID | Check | Expected result | Status |
|---|---|---|---|
| NEG-01 | Submit an incorrect dummy flag | Rejected; no points or progress granted | Evidence pending |
| NEG-02 | Try to obtain C6 details without solving C5 | No unintended shortcut; access follows intended design | Pending live C5 acceptance |
| NEG-03 | Inspect challenge files and web responses for later-stage flags | Later-stage flags are not exposed early | Evidence pending |
| NEG-04 | Check service bindings/firewall from an authorised test point | Only explicitly required ports are reachable | Evidence pending |
| NEG-05 | Restart Flag API and check its health endpoint | Service recovers and remains available | Evidence pending |
| NEG-06 | Repeat an accepted submission | Scoring behaviour matches documented CTFd settings | Evidence pending |

Only perform these checks against the authorised project lab.

## 5. Reset and recovery acceptance

| Test ID | Action | Expected result | Status |
|---|---|---|---|
| REC-01 | Record initial state and execute documented C1 reset method | C1 returns to its documented baseline | Not recorded |
| REC-02 | Restart/recover C2 and C3 services/artefacts using actual procedures | Challenge content and service are available after recovery | Not recorded |
| REC-03 | Restore C4/C5 artefacts from approved source | Correct files are present and listings/checksums match | C5 artefact present; restore and checksum evidence pending |
| REC-04 | Restore/revert C6 using actual approved VM procedure | VM returns to baseline and intended task remains solvable | Not recorded |
| REC-05 | Restart central CTFd and Flag API dependencies | Portal and validation become available without unintended data loss | Not recorded |
| REC-06 | Run full acceptance plan after recovery | All six stages work in sequence | Pending live C5 acceptance |

Record the exact command, snapshot name, operator, time, pre-state, post-state and evidence. Do not invent a reset command or claim a snapshot exists unless verified.

## 6. Defect and deviation log

| ID | Description | Priority | State | Action |
|---|---|---|---|---|
| B-001 | C5 artefacts are integrated; live acceptance remains pending; C5-to-C6 handoff and full sequential test cannot be completed | High | Open | Run INT-06 and INT-07 with the integrated artefact, then run INT-10 after all live stage tests pass |
| D-001 | Consolidated clean-account end-to-end evidence not yet recorded | High | Open | Record a full run after C5 completion |
| D-002 | Reset/recovery behaviour needs execution evidence | Medium | Open | Run REC-01 to REC-06 where applicable |

## 7. Design changes from Assignment 01

Compare the approved design and actual deployed box. For each difference, record the original requirement, actual setting, reason, impact, and evidence. Verify live OS versions, VM resources, IPs, ports, firewall rules, isolation, scoring/dependencies and reset mechanisms before finalising the comparison. Do not treat planned features as implemented features.

## 8. Final acceptance criteria

- [ ] C1, C2, C3, C4 and C6 evidence is attached to the results register.
- [ ] C5 PCAP solve path, CTFd answer, and C5-to-C6 handoff are verified in the live environment.
- [ ] C5-to-C6 dependency is demonstrated without shortcuts.
- [ ] Correct and incorrect answer handling is tested.
- [ ] Reset/recovery procedures are executed and recorded.
- [ ] Risk register and design deviations are updated from evidence.
- [ ] Full clean-account C1-to-C6 run is successful.
- [ ] Evidence contains no passwords, tokens or live flags.
