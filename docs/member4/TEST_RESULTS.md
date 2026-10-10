# ZOBI CTF — Test Results Register

**Owner:** Member 4 — Integration, Testing & Documentation  
**Current scope:** C1, C2, C3, C4 and C6 are reported complete by the project owner. C5 remains unfinished.  
**Important:** “Reported complete” means the team says the stage implementation is done; attach screenshots/logs from the current deployment before presenting the work as independently re-tested.

## 1. Stage-by-stage status

| Stage | Domain and intended activity | Implementation / intended solve path | Current status | Evidence to attach |
|---|---|---|---|---|
| C1 | Steganography | Player downloads the mystery photograph and uses Steghide to extract the embedded note. The note provides the clue for the next stage. | COMPLETE — per project owner | CTFd challenge page, downloaded image, extraction terminal output, accepted submission/score screenshot |
| C2 | Cryptography | Player reads the recovered message artefact and decodes the Caesar-shifted text. The decoded clue points to the web challenge in C3. | COMPLETE — per project owner | CTFd attachment, decoded output with secrets redacted, accepted submission screenshot |
| C3 | Web security | Flask-based “Abandoned Lab / Research Portal” challenge packaged as a Docker service. The intended exercise demonstrates SQL injection against the challenge login and retrieval of the challenge result. Lab port previously used: 5003. | COMPLETE — per project owner | Container status, health response, intended solve-path screenshot, CTFd accepted submission, isolation/binding check |
| C4 | Digital forensics | Player inspects the supplied forensic evidence bundle and correlates logs to identify the intended finding. The evidence archive was prepared as C4_evidence.zip with five evidence files. | COMPLETE — per project owner | CTFd attachment, archive listing, analysis commands/output, accepted submission screenshot |
| C5 | Network analysis | Player analyses the supplied network capture to identify the required clue and intended C6 connection information. | NOT FINISHED — BLOCKED | Complete the PCAP artefact, validate intended solve path, then test the handoff to C6 |
| C6 | Linux/system security | Isolated Ubuntu Server VM challenge. The intended exercise involves reviewing the allowed backup script and demonstrating the configured PATH lookup weakness in the authorised lab. Lab notes identify guest IP 10.10.20.50 on an isolated 10.10.20.0/24 network. | COMPLETE — per project owner | VM/network state, intended task output, accepted submission and completion evidence |

## 2. Platform and integration observations

| Test ID | Check | Current result | Evidence / next action |
|---|---|---|---|
| M4-01 | CTFd portal availability | CTFd has been hosted on the lab server at port 8081. | Capture current participant and admin portal screenshots |
| M4-02 | C1 intended extraction path | Reported complete | Attach current run evidence |
| M4-03 | C2 decode path | Reported complete | Confirm artefact is attached to CTFd and record current submission result |
| M4-04 | C3 web service | Flask challenge and health endpoint have been tested in the lab | Attach service and participant evidence |
| M4-05 | C4 forensic artefact | Archive was prepared and ZIP contents checked | Confirm current CTFd attachment and participant solve |
| M4-06 | C5 PCAP and handoff | Not finished | Do not claim end-to-end completion until C5 is complete |
| M4-07 | C6 intended path | Reported complete | Attach current VM and participant-path evidence |
| M4-08 | Full C1-to-C6 clean-account run | BLOCKED by unfinished C5 | Re-run after C5 is complete; prove dependencies and progression |
| M4-09 | Correct and incorrect answer handling | Needs consolidated evidence across all stages | Record accepted and rejected submissions without exposing live flags |
| M4-10 | Reset/recovery | Requires execution evidence for each implemented reset method | Record exact approved procedure and post-reset retest |

## 3. Defect and blocker log

| ID | Description | Priority | State | Resolution / retest |
|---|---|---|---|---|
| B-001 | C5 network-analysis challenge is not finished, so the C5-to-C6 dependency and full end-to-end flow cannot yet be accepted. | High | OPEN | Finish the PCAP challenge, validate its clue, then run the full clean-account sequence |
| D-001 | No consolidated evidence register for a clean participant run across all six stages. | High | OPEN | Capture timestamped evidence after C5 is complete |
| D-002 | Reset/recovery claims need test logs for the actual deployed procedures. | Medium | OPEN | Execute each approved recovery operation and record the post-reset state |

## 4. Live execution record

Fill this table with actual run data. Never invent a PASS or backdate evidence.

| Date/time | Stage/test | Tester/account (no password) | Actual result | Evidence path | Defect ID |
|---|---|---|---|---|---|
| Pending | C1 | — | Reported complete; evidence to attach | — | — |
| Pending | C2 | — | Reported complete; evidence to attach | — | — |
| Pending | C3 | — | Reported complete; evidence to attach | — | — |
| Pending | C4 | — | Reported complete; evidence to attach | — | — |
| Pending | C5 | — | NOT FINISHED | — | B-001 |
| Pending | C6 | — | Reported complete; evidence to attach | — | — |
| Pending | End-to-end C1→C6 | — | BLOCKED until C5 is complete | — | B-001 |

## 5. Evidence hygiene

- Use a clean participant account for end-to-end acceptance.
- Keep passwords, tokens, private keys and live flags out of screenshots and public-facing documentation.
- Save timestamped evidence under the agreed evidence directory.
- Record the relevant commit hash for each implementation fix.
- Do not mark the overall platform “fully integrated” until C5 and the C1-to-C6 flow have been tested.
