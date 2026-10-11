# Member 4 — Integration, Testing, Validation and Risk Register

**Owner:** Member 4 — Integration, Testing & Documentation  
**Project:** ZOBI — Zombie Outbreak Breach Investigation  
**Module:** IE3132 Penetration Testing  
**Branch:** member-4-integration-testing-docs

This document consolidates Member 4's test strategy, current implementation evidence, risk register, and final acceptance gate. It separates repository artefact presence and previously observed setup checks from tests that still require execution on the live CTFd environment.

## 1. Member 4 responsibilities

1. Define the test strategy and acceptance criteria for the CTF platform.
2. Review stage integration, difficulty progression, challenge clues, and dependency rules.
3. Track defects, mitigations, retests, reset/recovery and design deviations.
4. Verify correct/incorrect answer handling and record evidence.
5. Maintain the final integration and risk documentation for the team.

## 2. Intended challenge chain

| Stage | Challenge | Domain | Acceptance focus |
|---|---|---|---|
| C1 | The Photograph | Steganography | Extract the hidden message and follow the intended clue. |
| C2 | Lab Assistant's Message | Cryptography | Decode the message and follow the intended clue to C3. |
| C3 | The Abandoned Lab | Web Security | Demonstrate the intentional SQL injection in the isolated lab and recover the configured result. |
| C4 | What happened here? | Digital Forensics | Correlate supplied logs and recover the intended result. |
| C5 | The Last Transmission | Network analysis | Analyse the integrated PCAP and recover the intended result and next-stage clue. |
| C6 | The CURE Research Server | Linux/System Security | Complete the intended task inside the isolated VM. |

Expected progression is C1 → C2 → C3 → C4 → C5 → C6. A repository directory or challenge listing alone does not prove that CTFd prerequisites are configured or enforced.

## 3. Current repository status

- C1 image, C2 message, C3 application source, C4 evidence files, and C5 PCAP/build materials are present in this branch.
- C6 is a VM-based challenge. The VM disk and live environment state are managed outside the repository.
- Member 4's stage guide, test plan, test-results register, recovery runbook, risk register, design comparison, artifact checker, HTTP smoke test, PCAP validator and combined check runner are committed.
- The C5 repository artefacts are integrated; live CTFd attachment, answer validation and C5-to-C6 handoff remain pending evidence.
- The owner reports C1, C2, C3, C4 and C6 as implemented. Independently captured acceptance evidence should be attached before presenting each as fully retested.

## 4. Previously observed platform checks

| Check | Recorded observation | Scope / limitation |
|---|---|---|
| Docker | Docker 29.1.3 reported; hello-world completed | Runtime smoke test only. |
| CTFd | Participant URL at port 8081 was reported accessible during setup | Does not prove every challenge or progression rule works. |
| Custom Flask flag API | Health endpoint returned service/status JSON; a test POST was accepted | Does not prove CTFd is integrated with the API or that all CTFd flags work. |
| API service | zobi-flag-api.service was observed enabled/active | State may have changed; recheck before demo. |
| C6 VM | zobi-c6-cure was running | Does not prove the intended challenge path or final submission. |
| C6 network | Guest 10.10.20.50/24 was attached to zobi_c6_isolated via virbr-c6 | Complete isolation still requires an allowed/blocked connection matrix. |
| C6 SSH | Host-to-guest TCP 22 was reachable | Does not prove participant-to-guest access is correctly restricted. |
| C6 VNC | Listener observed at host loopback 127.0.0.1:5900 and used through SSH forwarding | Recheck current listener and keep it off the LAN. |
| C5 PCAP | Source artefact is integrated into this branch | Manual Wireshark solve and CTFd submission remain pending. |

## 5. Acceptance test plan

| ID | Test | Expected result | Current status |
|---|---|---|---|
| INT-01 | Open CTFd as a clean participant | Portal loads and intended challenge list is visible | Recheck live |
| INT-02 | Download and solve C1 | Intended extraction works and configured answer is accepted | Evidence pending |
| INT-03 | Decode and solve C2 | Message produces the intended clue and configured answer is accepted | Evidence pending |
| INT-04 | Solve C3 in the lab | Intended SQL injection works only in the lab; correct answer accepted | Source tests added; live acceptance pending |
| INT-05 | Analyse C4 evidence | Supplied evidence supports the intended conclusion | Evidence pending |
| INT-06 | Analyse C5 PCAP in Wireshark | Intended stream and next-stage clue are recovered | Artefact integrated; manual test pending |
| INT-07 | Follow C5 clue to C6 | Clean participant can reach the intended guest path only | Pending |
| INT-08 | Complete C6 and submit result | Intended task works and CTFd records completion | Evidence pending |
| INT-09 | Submit incorrect answers | Incorrect answers are rejected without awarding completion | Pending across all stages |
| INT-10 | Test stage dependencies | Only intended next stage is unlocked; premature access is blocked | Pending |
| INT-11 | Run reset/recovery | Documented baseline is restored and smoke tests pass | Pending |
| INT-12 | Verify network isolation | Required paths work; unnecessary paths are blocked | Pending |
| INT-13 | Capture resource usage and logs | CPU/RAM/disk and diagnostic evidence are recorded without secrets | Pending |

## 6. Risk register

| ID | Risk | Priority | Mitigation | Evidence to close |
|---|---|---|---|---|
| R-01 | Later-stage answer exposed early | High | Keep organiser files separate from participant attachments; inspect repository and responses | Clean-account shortcut test and access review |
| R-02 | C6 reachable without intended C5 step | High | Verify CTFd prerequisites and network access using a clean participant | C5-to-C6 walkthrough and denied-shortcut evidence |
| R-03 | Correct/incorrect answer handling is inconsistent | High | Test both outcomes at every stage and compare with configured values | Submission screenshots/logs for each stage |
| R-04 | Vulnerable service is exposed beyond the lab | Critical | Restrict bindings/firewall and inspect Docker/libvirt networks | Sanitised firewall and allowed/blocked connection matrix |
| R-05 | Reset destroys scores or challenge state | High | Preserve backups; use approved reset or VM snapshot procedures | Recorded restore and post-restore test |
| R-06 | Lab secrets or flags are accidentally exposed | High | Keep organiser files restricted, redact evidence, rotate exposed lab secrets | Repository and evidence review |
| R-07 | Service fails after restart/reboot | Medium | Use health checks and a documented recovery procedure | Restart/reboot test and healthy response |
| R-08 | Report differs from live configuration | Medium | Reconcile OS, ports, IPs, resource allocation and dependencies with the running host | Dated configuration inventory and change record |
| R-09 | Resource capacity is assumed rather than measured | Medium | Capture CPU/RAM/disk and run a controlled workload if required | Dated measurements and workload notes |
| R-10 | Full progression is claimed without evidence | High | Keep final acceptance pending until a clean C1-to-C6 run is captured | Full walkthrough and test log |

Likelihood/impact are qualitative priorities for review, not measured probabilities.

## 7. Design differences to reconcile

- The original design report specified Ubuntu Server 20.04; the host observed during setup reported Ubuntu Server 26.04.1 LTS. Record the actual version and explain the compatibility/reproducibility impact.
- The CTFd portal was observed on host port 8081, while the application and reverse-proxy services use separate internal ports. Confirm live bindings and firewall policy.
- The custom Flask flag API has been tested separately. Do not claim CTFd uses it for all submissions unless the actual integration is inspected and demonstrated.
- The C6 VM's actual OS release, CPU/RAM/disk allocation, permissions and reset method must be confirmed on the guest.
- Record each accepted deviation with the original requirement, actual state, reason, impact, approver and evidence.

## 8. Evidence rules

For each test, record the test ID, date/time, tester, branch commit, environment, exact action/command, expected result, actual result, PASS/FAIL/BLOCKED/NOT RUN, evidence path, and related defect/fix. Redact passwords, tokens and live answers from screenshots and logs.

Run repository-only checks from the repository root:

    bash scripts/testing/run_repository_checks.sh

Run the live HTTP smoke test only on the authorised lab host:

    ZOBI_RUN_LIVE_SMOKE=1 bash scripts/testing/run_repository_checks.sh

The combined runner checks repository files, C3 unit tests and C5 PCAP structure when dependencies are available. Its live smoke test checks HTTP reachability only. It does not submit flags, test CTFd progression, verify isolation or execute reset/recovery.

## 9. Final acceptance gate

- [ ] C1–C6 attachments match the approved source artefacts.
- [ ] Every stage's intended solve path is reproducible.
- [ ] Correct answers are accepted and incorrect answers rejected at all stages.
- [ ] C1 → C2 → C3 → C4 → C5 → C6 progression is demonstrated with a clean account.
- [ ] C5-to-C6 handoff is tested without administrator-only shortcuts.
- [ ] Vulnerable services and the C6 VM remain within the approved lab boundary.
- [ ] Reset/recovery is executed and a post-reset smoke test passes.
- [ ] Logs and CPU/RAM/disk evidence are captured.
- [ ] All design differences from Assignment 01 are explained.
- [ ] The final video shows the real environment and each member's own work.

**Completion rule:** do not mark the overall platform fully integrated until the live tests above have actual results and saved evidence.