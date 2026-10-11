# Member 4 — Final Integration, Acceptance, Evidence and Handover Runbook

**Project:** ZOBI — Zombie Outbreak Breach Investigation  
**Module:** IE3132 Penetration Testing — Assignment 02  
**Branch:** `member-4-integration-testing-docs`  
**Scope:** integrate Members 1–3, test all six stages, track risks/defects, validate dependencies, reset/recovery, and prepare the evidence pack.

## 1. Rule for completion claims

A repository file, a challenge author's statement, or a health endpoint is not a substitute for an observed end-to-end result. For every acceptance test, record the date/time, exact environment, expected result, actual result, pass/fail, evidence location, and tester. Use **NOT RUN**, **PASS**, **FAIL**, or **BLOCKED**. Never change a pending result to PASS without performing the test.

## 2. System and branch inventory

Observed in prior setup notes:
- Ubuntu host: `ZOBI-Central-server`, `192.168.8.188`, Ubuntu Server 26.04.1 LTS.
- CTFd participant portal: `http://192.168.8.188:8081/`.
- C3: Flask/SQLite application intended on host port 5003.
- C6: `zobi-c6-cure`, guest `10.10.20.50/24`, isolated libvirt network `zobi_c6_isolated`.
- Intended stage order: C1 → C2 → C3 → C4 → C5 → C6.
- The original design report described Ubuntu Server 20.04, whereas the running host was observed as 26.04.1 LTS. Treat this as a design deviation and document compatibility impact.

## 3. Stage integration matrix

| Stage | Domain | Required evidence before marking PASS |
|---|---|---|
| C1 — The Photograph | Steganography | Downloaded source attachment matches expected image; intended extraction succeeds; correct flag accepted, wrong flag rejected |
| C2 — Lab Assistant's Message | Cryptography | Attachment decodes to the intended clue; decoded flag matches CTFd configuration; correct/wrong submissions tested |
| C3 — The Abandoned Lab | Web security | Container healthy; intended SQLi path works only in the lab; flag matches CTFd; correct/wrong submissions and reset tested |
| C4 — What happened here? | Digital forensics | All advertised evidence files exist; finding is supported by at least two artefacts; flag and clue validated |
| C5 — The Last Transmission | Network analysis | PCAP opens; intended stream is evidence-supported; source and attached PCAP checksums match; CTFd flag and C6 handoff tested |
| C6 — The CURE Research Server | Linux/system security | Guest boots on isolated network; intended account and script configuration confirmed; intended path and flag validated inside guest; recovery tested |

## 4. Required end-to-end acceptance sequence

1. Create or reset a designated test participant; record the starting state.
2. Confirm CTFd shows all six expected challenge entries and attachments.
3. Attempt a later stage before completing its prerequisite and record the observed access-control behaviour.
4. For each stage C1 through C6, solve the intended path, submit the verified correct flag, then submit a deliberately incorrect value using a safe test attempt. Record both outcomes.
5. Confirm each accepted flag unlocks the intended next stage and does not accidentally unlock unrelated stages.
6. Validate that clues, URLs, credentials, filenames and challenge titles agree between source files, CTFd and the report.
7. Confirm C3 is not exposed beyond the approved lab boundary; confirm C6 remains on its isolated libvirt network and VNC uses host loopback/SSH forwarding.
8. Perform the approved reset/recovery procedure.
9. Re-run health, artifact, flag, dependency and representative solve tests after recovery.
10. Attach sanitised screenshots/logs and record defects that remain unresolved.

## 5. Test evidence register

Use `docs/member4/TEST_RESULTS.md` as the stage register and add evidence references rather than replacing results with assumptions. At minimum, record:

| Test ID | Expected result | Result until executed |
|---|---|---|
| INT-01 | CTFd portal and all challenge entries available | NOT RUN / update with evidence |
| INT-02 | All attachments download and match source artefacts | NOT RUN / update with evidence |
| INT-03 | C1 and C2 correct/wrong flag behaviour works | NOT RUN / update with evidence |
| INT-04 | C3 intended SQLi path, flag validation and reset work | NOT RUN / update with evidence |
| INT-05 | C4 answer is supported by supplied logs | NOT RUN / update with evidence |
| INT-06 | C5 PCAP solve and C6 connection handoff work | NOT RUN / update with evidence |
| INT-07 | C6 intended path and CTFd final submission work | NOT RUN / update with evidence |
| INT-08 | Prerequisite enforcement prevents stage bypass | NOT RUN / update with evidence |
| INT-09 | Host firewall and Docker/libvirt boundaries behave as intended | NOT RUN / update with evidence |
| INT-10 | Reset/recovery and post-reset smoke tests pass | NOT RUN / update with evidence |
| INT-11 | Logs contain useful events without secret leakage | NOT RUN / update with evidence |
| INT-12 | CPU, RAM and disk usage recorded under representative load | NOT RUN / update with evidence |

## 6. Risk register — minimum required coverage

Keep `docs/member4/RISK-REGISTER.md` and `docs/MEMBER4_INTEGRATION_TESTING_RISK_REGISTER.md` consistent. Assess likelihood and impact using the team's chosen scale; assign an owner and a retest/evidence reference.

| Risk | Potential impact | Required mitigation / evidence |
|---|---|---|
| Vulnerable C3 exposed outside the lab | Unauthorised exploitation | Loopback or approved lab-interface binding, host firewall, source/destination tests |
| C6 guest reaches host or unrelated network | Host/lab compromise | Inspect libvirt XML, routes and firewall; test allowed/blocked paths |
| CTFd flags differ from challenge flags | Progression fails or wrong solutions accepted | Compare authoritative flag configuration; correct and incorrect submission evidence |
| Challenge dependencies misconfigured | Participants bypass intended learning path | Fresh-account prerequisite tests |
| Reset damages CTFd scores or data | Loss of submissions/users | Approved backup/snapshot and tested recovery procedure |
| Secret/flag committed to public Git history | Challenge answers disclosed | Remove from current files, rotate secret/flag, review history and access settings |
| Documentation differs from running environment | Failed deployment or inaccurate demonstration | Re-run inventory and update version/port/topology tables |
| Logs expose credentials or flags | Information disclosure | Redact secrets and verify sample logs |
| Resource exhaustion during demo | Service instability | Capture CPU/RAM/disk, test expected concurrency and document limits |

## 7. Reset and recovery controls

Before changing anything, identify the exact Compose project, volumes, database, VM disk and snapshot names. Preserve logs and configuration. Do not run destructive volume removal or reset CTFd scores without explicit team approval.

After recovery, confirm:
- CTFd is accessible and its challenge entries/attachments remain present.
- C3 health endpoint responds and its database is in the intended state.
- C6 boots and remains on `zobi_c6_isolated`.
- Challenge flags and prerequisites still match the source of truth.
- A new smoke test and a representative solve succeed.

Record the actual operation and output in `docs/member4/RESET-RECOVERY.md`. This runbook is not evidence that recovery has already been tested.

## 8. Repository and security review

- The Member 1 branch has a C3 setup pattern that requires private environment values and defaults to loopback binding. Keep the Member 4 branch consistent with that approach; do not commit live flags or session secrets in Compose files.
- The public repository must not contain production credentials, private keys, admin tokens, or live challenge secrets that are meant to remain undisclosed. Review existing Git history as well as the current tree; deleting a secret in a later commit does not remove it from history.
- The C6 VM disk, live credentials and final flag should remain outside the source repository. Commit only reviewed templates and sanitised documentation.
- A successful custom Flask flag API test does not prove CTFd is integrated with that API. Verify and document the actual CTFd validation path.
- The current host version is Ubuntu Server 26.04.1 LTS in prior evidence; do not claim the running host is 20.04.

## 9. Final Member 4 deliverables checklist

- [ ] Six-stage acceptance register completed with evidence.
- [ ] CTFd flag values and challenge prerequisites checked against source-of-truth values.
- [ ] C5-to-C6 handoff demonstrated using a clean participant.
- [ ] Correct/incorrect submissions tested for every stage.
- [ ] Defects have impact, owner, fix, and retest evidence.
- [ ] Risk register includes isolation, secrets, validation, reset and resource risks.
- [ ] Reset/recovery performed and post-reset validation recorded.
- [ ] Runtime CPU/RAM/disk measurements included.
- [ ] Differences from Assignment 01 are explained and justified.
- [ ] Contribution evidence and final repository links are ready.
- [ ] Live demonstration remains unscripted and each member explains their own work in their own words.

## 10. Current completion statement

This branch contains integration guides, stage artefacts, test helpers and risk/recovery documentation. Some stages have been reported complete by the team, but the branch alone does not prove the current CTFd deployment, all flags, dependencies, network isolation, or reset/recovery pass end-to-end. Keep any unexecuted test marked NOT RUN/PENDING and attach evidence after execution.
