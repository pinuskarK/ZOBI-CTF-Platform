# Member 4 — Integration, Testing, Validation & Risk Register

**Owner:** Siriwardhana G.K.KG (Member 4)  
**Student ID in report:** IT24103096  
**Project:** ZOBI — Zombie Outbreak Breach Investigation  
**Module:** IE3132 Penetration Testing  
**Branch:** `member-4-integration-testing-docs`

> This document follows the final report's Member 4 scope: test strategy and acceptance criteria, technical/security/implementation/deployment risk analysis, mitigation recommendations, challenge review, validation documentation, and integration of all members' work. It distinguishes checks observed in the implementation session from planned tests that still require execution.

## 1. Responsibilities from the final report

Member 4's documented responsibilities are:

1. Develop the testing strategy and validation criteria for the CTF Box.
2. Participate in risk analysis for technical, security, implementation, and deployment risks.
3. Recommend mitigations to improve reliability and security.
4. Review Member 2 and Member 3 challenge designs for consistent flow, difficulty progression, technical requirements, and compliance with the CTF Box requirements.
5. Prepare testing, validation, and risk-analysis documentation.
6. Integrate the report contributions from all four members.

## 2. System under test

ZOBI contains six sequential challenges across six domains:

| Stage | Challenge | Domain | Main validation goal |
|---|---|---|---|
| C1 | The Photograph | Steganography | Extract hidden content, recover the stage flag, and obtain the C2 clue |
| C2 | Lab Assistant's Message | Cryptography | Decode the Caesar-cipher message, validate the flag, and obtain the C3 clue |
| C3 | The Abandoned Lab | Web Security | Demonstrate the intentionally vulnerable SQL-injection login in the lab, access the research files, and recover the flag/clue for C4 |
| C4 | What happened here? | Digital Forensics | Examine the supplied evidence, identify relevant artefacts, recover the flag/clue for C5 |
| C5 | The Last Transmission | Networking / Packet Analysis | Inspect the supplied PCAP, recover the expected flag/clue for C6 |
| C6 | The CURE research Server | Linux/System Security | Access the isolated VM, complete the intended Linux-security task, and recover the final flag |

The intended dependency chain is C1 → C2 → C3 → C4 → C5 → C6. Test both that each successful submission unlocks the next stage and that users cannot bypass dependencies where sequential access is required.

## 3. Test strategy and acceptance criteria

### T1 — Platform availability and service health

**Procedure**
- Open CTFd at the configured participant URL.
- Check that the participant can log in and see the expected challenge list.
- Check the Docker service, challenge services, flag API, and C6 VM status on the host.
- Check required ports and URLs from the participant side.

**Pass criteria**
- The platform loads without service errors.
- Each required challenge resource is reachable from the intended network.
- A failed or stopped service is detected and recorded rather than silently treated as a successful challenge.

### T2 — Challenge artifact and clue validation

For each challenge, confirm that the attachment exists, downloads successfully, matches the intended challenge, and contains the evidence described in the report. Confirm that each recovered clue points to the correct next stage.

**Pass criteria**
- C1 image and hidden content are usable.
- C2 text file decodes to readable instructions and the intended stage flag.
- C3 portal behaves as designed in the isolated lab and contains the expected research evidence.
- C4 evidence archive/logs are present and support the intended investigation.
- C5 PCAP opens in a packet-analysis tool and contains the intended traffic/evidence.
- C6 VM boots, provides the intended account and vulnerable configuration, and contains the intended flag file.

### T3 — Flag validation negative and positive tests

For each stage:
1. Submit the verified correct flag.
2. Confirm the platform accepts it and marks the stage complete.
3. Submit a deliberately incorrect value.
4. Confirm it is rejected and does not grant completion.
5. Repeat after a reset where supported.

**Pass criteria**
- Correct flags are accepted.
- Incorrect flags are rejected.
- A challenge is not marked complete merely because a request was submitted.
- Flag comparison is not unintentionally altered by whitespace or casing rules unless those rules are documented.

### T4 — Dependency and progression tests

- Complete C1 and confirm C2 becomes available.
- Repeat through C6 in order.
- Attempt to access a later stage before its prerequisite is completed.
- Confirm the observed behavior matches the intended CTFd dependency configuration.

**Pass criteria**
- The expected next challenge becomes available after successful completion.
- Restricted stages remain restricted when prerequisites are not met.
- Hints, URLs, credentials, files, and stage names agree across challenge pages and report documentation.

### T5 — Network isolation and access-control tests

- From the Ubuntu host, confirm the C6 VM's address and intended SSH port are reachable.
- Confirm VNC listens only on host loopback and use SSH port forwarding for remote graphical access.
- Inspect libvirt and Docker network definitions and the host firewall.
- From each relevant network, test only the ports that are supposed to be accessible and record both allowed and blocked paths.
- Confirm database services, if present, are not exposed publicly.

**Pass criteria**
- Required routes work.
- Unnecessary inbound access is denied.
- Intentionally vulnerable challenges remain isolated from unrelated services and the host management plane.
- The evidence includes the commands/results and the source/destination network for each test.

### T6 — Permissions and challenge safety

- Review C6 account privileges and the intended vulnerable script/configuration.
- Confirm privilege escalation, if intended by the challenge, is limited to the lab VM.
- Confirm participants do not receive unintended access to the host or unrelated challenge resources.
- Check file ownership and permissions on challenge files and flag locations.

**Pass criteria**
- The challenge is solvable using the documented path.
- Permissions are neither so restrictive that the intended task is impossible nor so broad that the challenge exposes unrelated systems.
- Host and guest privilege boundaries are documented.

### T7 — Reset and recovery

- Capture a known-good initial state.
- Complete or alter a challenge in the approved test environment.
- Run the documented reset/recovery procedure.
- Repeat the original test after reset.

**Pass criteria**
- The challenge returns to its intended initial state.
- Attachments, service health, flags, permissions, and dependencies remain correct.
- The recovery procedure is documented and reproducible.

### T8 — Resource and reliability checks

- Record CPU, RAM, disk, and service usage during normal operation.
- Observe logs during service startup, challenge submission, and failure.
- Conduct a small controlled multi-user smoke test if the platform is expected to support concurrent participants.
- Do not claim the planned 10–20 participant capacity or the 50+ scalability path has been demonstrated without measured load-test evidence.

**Pass criteria**
- No unexpected service crashes occur in the tested workload.
- Resource limits and capacity assumptions are documented.
- Logs provide enough information to diagnose a failure without exposing secrets or flags unnecessarily.

## 4. Test evidence actually observed so far

These are evidence-backed checks from the implementation session. They are not a substitute for the complete test plan above.

| ID | Test performed | Observed result | Status |
|---|---|---|---|
| E1 | Check Docker version on Ubuntu host | Docker 29.1.3 reported | Passed |
| E2 | Docker smoke test | `hello-world` completed successfully | Passed |
| E3 | Open CTFd | `http://192.168.8.188:8081/` was reported accessible during setup | Basic availability observed; full participant workflow not yet evidenced |
| E4 | Check Flask flag API health endpoint | API returned `{"service":"ZOBI CTF Flag Validation API","status":"running"}` | Passed |
| E5 | Submit a test value to the Flask API | Response indicated `Correct flag! True` | Passed for that test value only |
| E6 | Check flag API systemd service | `zobi-flag-api.service` observed enabled and active | Passed at time checked |
| E7 | Check C6 VM state | `zobi-c6-cure` was running under libvirt | Passed at time checked |
| E8 | Check host-to-guest connectivity | Host ping to `10.10.20.50` received 4/4 replies | Passed |
| E9 | Check C6 SSH port from host | `nc -zv -w 3 10.10.20.50 22` succeeded | Passed |
| E10 | Check VNC listener | QEMU listened on `127.0.0.1:5900` | Passed at time checked |
| E11 | Use TigerVNC via SSH tunnel | User reported logging into the C6 VM through TigerVNC | Basic console access observed |
| E12 | Inspect C6 challenge script | `/opt/zobi-c6/backup.sh` exists and calls `tar` by command name | File inspection completed; intended escalation path not fully validated |
| E13 | Search for C6 flag filename | `/root/cure.txt` found by `find` | File exists; its contents and CTFd submission are not evidenced here |
| E14 | Inspect C5 PCAP artifact | `last_transmission.pcap` was identified as an 8,538-byte PCAP with 74 packets | File format/artifact checked; full solve and flag submission need verification |
| E15 | Verify all six challenge flags and progression in CTFd | No complete end-to-end result recorded | Not yet verified |

**Important:** do not convert a proposed test into a “passed” result in the report. Add date, tester, exact command or action, expected result, actual result, screenshot/log evidence, and pass/fail status when each outstanding test is performed.

## 5. Risk register and mitigation recommendations

Use the following register to track the risks identified in the final report.

| ID | Risk | Likelihood / impact | Recommended mitigation | Verification evidence |
|---|---|---|---|---|
| R1 | Challenge service failure | Medium / High | Add service-health checks, restart policy where suitable, and a pre-demo checklist | Service status and restart/recovery result |
| R2 | Incorrect flag validation | Medium / High | Test known-correct and known-incorrect flags for every stage; verify CTFd and API behavior separately | Positive and negative submission results |
| R3 | Network connectivity failure | Medium / High | Document required routes and ports; test from the participant side and host side | Connectivity matrix and command output |
| R4 | Dependency or artifact missing | Medium / High | Check every attachment, package, URL, account, and service before demo; keep a dependency inventory | Artifact checklist and successful download/open |
| R5 | Insufficient environment isolation | Low–Medium / Critical | Use separate Docker/libvirt networks, restrict inbound traffic, keep VNC on loopback, and avoid exposing vulnerable services publicly | Firewall rules, network inspection, allowed/blocked connection results |
| R6 | Improper permissions / unintended privilege | Medium / High | Audit user and sudo permissions, file ownership, and challenge-only escalation; avoid broad guest privileges unless explicitly required for the challenge | `sudo -l`, file permissions, documented intended path |
| R7 | Challenge state corruption | Medium / High | Provide a known-good snapshot/backup and a tested reset/recovery procedure | Before/after state comparison |
| R8 | Insufficient CPU, RAM, disk, or network capacity | Medium / Medium–High | Monitor resource usage, set reasonable limits, and measure a controlled concurrent workload | Resource snapshots and load-test results |
| R9 | Inadequate logging or diagnostic evidence | Medium / Medium | Centralize relevant service logs, preserve timestamps, and avoid logging secrets | Example logs for startup, submission, and failure |
| R10 | Report/design differs from deployed configuration | Medium / High | Keep IPs, host OS versions, ports, challenge names, dependencies, and diagrams synchronized with the running system | Configuration inventory reviewed against report |
| R11 | Backup or recovery failure | Medium / High | Define backup contents, schedule, retention, and restore procedure; test an actual restore | Restore log and successful post-restore smoke test |
| R12 | Demo or deployment setup failure | Medium / High | Rehearse the full C1→C6 path, confirm services/attachments and VNC/SSH access, and keep a recovery checklist | Dated rehearsal checklist and evidence |

Likelihood and impact values are preliminary qualitative ratings for prioritization, not measured probabilities. Review them against the group's final risk-scoring method if one is defined elsewhere in the report.

## 6. Challenge integration review checklist

For each challenge submitted by Members 2 and 3, verify:

- [ ] Challenge title, domain, difficulty, and stage number match the report.
- [ ] Scenario and evidence fit the ZOBI research-facility storyline.
- [ ] Attachment path/name matches the instructions shown to participants.
- [ ] Intended flag exists and exactly matches the value configured in CTFd.
- [ ] The clue gives the right information for the next stage without revealing an unrelated answer.
- [ ] Required tools, accounts, URLs, packages, and services are available.
- [ ] The intended solve path works from a clean/reset state.
- [ ] Hints are useful and do not contradict the challenge.
- [ ] Dependency/unlock behavior matches C1 → C2 → C3 → C4 → C5 → C6.
- [ ] Reset/recovery instructions are available.
- [ ] Risky services remain confined to the intended lab environment.

## 7. Current integration findings and follow-up items

1. **Platform smoke tests have evidence** for Docker, the Flask API, the C6 VM, host-to-guest connectivity, and VNC console access.
2. **Full end-to-end challenge testing remains outstanding** until all six correct/incorrect flag submissions, attachment checks, and dependency unlocks have been recorded.
3. The implementation host was observed as Ubuntu Server 26.04.1 LTS, while the design report specifies Ubuntu Server 20.04. Document the actual version consistently.
4. The C6 guest has address `10.10.20.50` on the isolated `zobi_c6_isolated` network. Direct Windows SSH timed out, while host-to-guest SSH worked. Keep the intended isolation and VNC-over-SSH arrangement documented.
5. C6 `/root/cure.txt` was found by filename search, but the actual content and successful CTFd submission have not been included in the recorded test evidence.
6. Verify that C4 is present and correctly linked; the previous platform progress note specifically reported C1, C2, C3, C5, and C6 as added, so C4 should not be assumed complete without checking.
7. The report proposes logging, backups, reset/recovery, firewall rules, PostgreSQL, nginx, and resource/scalability planning. Mark these as implemented only after checking the actual configuration and collecting evidence.

## 8. Final test summary template

Complete this table after the rehearsal. Leave the result as **Pending** until the test is actually run.

| Test area | Result | Evidence / date |
|---|---|---|
| C1 attachment, extraction, correct/incorrect flag | Pending | Add screenshot/log |
| C2 decoding, correct/incorrect flag | Pending | Add screenshot/log |
| C3 intended SQL-injection path, research files, flag | Pending | Add screenshot/log |
| C4 evidence analysis and flag | Pending | Add screenshot/log |
| C5 PCAP analysis and flag | Pending | Add screenshot/log |
| C6 intended task and flag submission | Pending | Add screenshot/log |
| C1→C6 dependency progression | Pending | Add full walkthrough evidence |
| Service restart and failure recovery | Pending | Add command output |
| Reset/restore | Pending | Add before/after evidence |
| Network isolation and port exposure | Pending | Add configuration and connection tests |
| Backup/restore and logging | Pending | Add evidence |
| Resource / concurrent-user test | Pending | Add measurements |

**Completion rule:** the platform is ready for final demonstration only after the critical end-to-end path, flag validation, service availability, and isolation checks have been run and their results recorded.
