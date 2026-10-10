# ZOBI CTF — Design Changes and Deployment Deviations

**Owner:** Member 4 — Integration, Testing & Documentation  
**Baseline:** Approved Assignment 01 architecture/report  
**Status:** Working comparison based on current project notes. Confirm every implementation detail against the live box and the approved Assignment 01 document before final submission.

## 1. Stage integration status

| Stage | Planned domain / intended design | Current implementation notes | Status / impact |
|---|---|---|---|
| C1 | Steganography challenge | Mystery photograph contains an embedded note; intended path uses Steghide extraction. | Reported complete; capture final participant evidence |
| C2 | Cryptography challenge | Recovered message is decoded with a Caesar shift and provides the next clue. | Reported complete; capture final participant evidence |
| C3 | Web security challenge | Flask-based Research Portal / Abandoned Lab challenge runs as a Docker service; lab port previously used is 5003. | Reported complete; retain service health, intended solve, and CTFd submission evidence |
| C4 | Digital forensics challenge | Forensic evidence bundle prepared as C4_evidence.zip with five evidence files. | Reported complete; confirm attached artefact and intended solve in CTFd |
| C5 | Network analysis challenge | PCAP must yield the intended clue and connection information for C6. | Not finished; blocks validation of C5-to-C6 dependency and full six-stage acceptance |
| C6 | Linux/system security challenge | Isolated Ubuntu Server VM; lab notes identify guest IP 10.10.20.50 on 10.10.20.0/24 and an intended PATH lookup weakness in the allowed backup-script path. | Reported complete; participant access via C5 remains unverified until C5 is finished |

## 2. Deployment and architecture comparison

| Area | Baseline / expectation | Current implementation notes | Reason / impact | Verification status |
|---|---|---|---|---|
| Challenge delivery | Six ordered stages across multiple cybersecurity domains | CTFd is hosted on the central server; challenge artefacts and services are configured separately | Centralises participant access while supporting file-based, containerised and VM challenges | Partial — C5 unfinished |
| CTFd network port | Participant portal exposed through selected host port | Lab URL has been used on port 8081 | Avoids conflict with existing host services | Verify current listener and firewall |
| Flag API | Central API validates submitted flags | Flask API has been run as a systemd service on the central server; port 8080 was used in lab tests | Provides a separate validation service for the project | Verify current health and CTFd integration; do not assume every stage uses it unless configured |
| C3 implementation | Isolated web-security challenge | Flask challenge deployed as a Docker service on host port 5003 | Supports repeatable delivery of intentionally vulnerable login challenge | Reported complete; participant and isolation evidence should be retained |
| C6 virtual machine | Assignment 01 baseline needs to be compared with actual VM OS/resources/network | Lab notes record Ubuntu Server 26.04.1, guest IP 10.10.20.50 and isolated libvirt network 10.10.20.0/24; earlier design notes may specify different OS/resources | A deviation can affect fidelity and must be justified or the VM should be adjusted to the approved design | Verify live OS, RAM, disk, network and approved baseline |
| C5-to-C6 handoff | C5 should provide the connection details required for C6 | C5 is not finished, so the intended participant handoff has not been acceptance-tested | Full end-to-end sequence cannot be claimed yet | Blocked by C5 |
| Reset/recovery | Stages should be recoverable to a known baseline | Actual reset scripts/snapshot procedures must be confirmed on the deployed host | Prevents accidental loss of scores or challenge state during recovery | Pending execution evidence |
| Final completion state | Final answer should lead to a clear completion indication | Completion/results page should be treated as a separate feature unless confirmed implemented | Avoids claiming UI functionality that is not deployed | Verify implementation and final submission behaviour |

## 3. Required design-deviation record

For every difference from Assignment 01, record:

1. The exact original requirement or configuration.
2. The actual live setting or behaviour.
3. Why the difference was made.
4. Security, usability, marking or operational impact.
5. Who approved the change.
6. Evidence path and related commit.

## 4. Finalisation steps

- [ ] Compare each row with the approved Assignment 01 report.
- [ ] Verify implementation details on the live host.
- [ ] Finish C5 and validate the C5-to-C6 handoff.
- [ ] Capture evidence for C1, C2, C3, C4 and C6 as reported complete.
- [ ] Record the reason and evidence for each accepted deviation.
- [ ] Obtain team approval for deviations affecting isolation, usability or assignment compliance.
- [ ] Update the final report to match the final tested deployment.
