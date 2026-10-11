# Member 4 — End-to-End Challenge Build, Solve, Installation and Final Validation Guide

**Project:** ZOBI — Zombie Outbreak Breach Investigation  
**Module:** IE3132 Penetration Testing — Assignment 02  
**Owner:** Member 4, Integration, Testing & Documentation  
**Branch:** `member-4-integration-testing-docs`

## 1. Purpose and evidence rules

This guide complements `MEMBER4_INTEGRATION_TESTING_RISK_REGISTER.md`. It gives the integration team a reproducible plan to install CTFd, place challenge artefacts, test each stage's intended path, validate flags and dependencies, and capture final evidence.

The Assignment 02 brief requires a live, unscripted demonstration of the actual box; at least six working stages across four or more domains; difficulty progression of C1–C2 Easy, C3–C4 Moderate, C5 Moderate–Hard, C6 Hard; working flag validation; isolation; reset/recovery; and at least one self-developed solver/exploit script per member. A document cannot replace a live run. Mark a test passed only after running it and saving evidence.

## 2. Current platform topology

| Component | Observed configuration |
|---|---|
| Central host | Ubuntu Server 26.04.1 LTS, hostname `ZOBI-Central-server` |
| Host LAN IP | `192.168.8.188` |
| CTFd participant URL | `http://192.168.8.188:8081/` |
| Custom flag API | Flask application; systemd unit `zobi-flag-api.service` |
| Docker | Docker 29.1.3 |
| C3 web challenge | `http://192.168.8.188:5003` was referenced by the C2 clue |
| C6 guest | `zobi-c6-cure`, guest address `10.10.20.50/24` |
| C6 isolated network | `zobi_c6_isolated`, bridge `virbr-c6`, host gateway `10.10.20.1` |
| VNC | Bound to host loopback `127.0.0.1:5900`; remote access should use an SSH tunnel |

These are observed settings from the implementation sessions, not a claim that every service is currently up. Check status immediately before testing.

## 3. Installation and startup instructions

### 3.1 Requirements

Use a dedicated Ubuntu host/VM for the lab. Do not run intentionally vulnerable challenges on a public production server. Before deploying, confirm:

- Ubuntu and a supported Docker Engine / Docker Compose plugin are installed.
- The host has enough RAM, CPU and disk for CTFd, challenge containers and the C6 VM.
- Host firewall rules expose only required participant-facing ports.
- The vulnerable C3 service and C6 VM are separated from host management services and unrelated networks.
- You have a copy of the source repository, challenge files and a known-good backup.

### 3.2 Inspect the repository before starting

On the Ubuntu host:

```bash
git clone https://github.com/pinuskarK/ZOBI-CTF-Platform.git
cd ZOBI-CTF-Platform
git branch -a
find . -maxdepth 3 -type f -print | sort
```

For the branch-specific implementation files, check out the appropriate branch only in a separate working copy if you do not want to disturb an existing checkout:

```bash
git switch member-4-integration-testing-docs
```

Inspect for a committed Compose file before running a deployment command:

```bash
find . -iname 'compose.yml' -o -iname 'compose.yaml' -o -iname 'docker-compose.yml'
```

**Repository finding:** the inspected root README documents the architecture and folder names, but this review has not verified a complete, self-contained CTFd Compose deployment file plus all challenge assets in the repository. Do not tell a lecturer the repository is one-command deployable until a clean deployment test proves it.

### 3.3 Start the existing CTFd installation

The running CTFd instance was previously reported accessible at `http://192.168.8.188:8081/`. On the server, inspect the existing project before changing it:

```bash
cd ~/ctfd
sudo docker compose ps
sudo docker compose config --services
```

If this directory is not the actual Compose project, locate the compose file rather than creating or overwriting one blindly:

```bash
find ~ -maxdepth 4 \( -iname 'compose.yml' -o -iname 'compose.yaml' -o -iname 'docker-compose.yml' \) -print
```

From the directory that contains the verified Compose file:

```bash
sudo docker compose up -d
sudo docker compose ps
sudo docker compose logs --tail=100
```

Open `http://192.168.8.188:8081/` from an authorized client on the same LAN. Complete the CTFd initial setup if it has not already been completed. Create the administrator account securely, then configure the event name and participant settings.

**Important:** do not replace the existing deployment's Compose file, database, or upload directory without first taking a backup. The exact Compose project and its environment variables must be checked from the running server; this repository audit has not verified those secrets or deployment files.

### 3.4 Add challenge entries in CTFd

For each stage:

1. Open the CTFd admin panel and create a challenge with the report's title, category, difficulty/points, description and hints.
2. Choose the appropriate challenge type (normally standard flag submission for these stages).
3. Configure the exact flag value from the challenge owner's source artefact/VM. Never invent a flag based on a guessed solution.
4. Upload the required attachment (image, text, evidence archive or PCAP) where appropriate.
5. Configure the dependency on the previous stage if the design requires sequential unlocks.
6. Save, open the participant view, download the attachment and test both a correct and deliberately incorrect flag.
7. Capture a screenshot of the challenge settings and participant view without exposing administrative credentials.

CTFd may validate flags internally. The custom Flask API's successful test POST does not prove CTFd invokes that API. Confirm the actual configured validation path before describing it as integrated.

### 3.5 Start and verify the custom flag API

```bash
sudo systemctl status zobi-flag-api.service --no-pager
sudo journalctl -u zobi-flag-api.service -n 80 --no-pager
```

The API health endpoint was previously observed to return:

```json
{"service":"ZOBI CTF Flag Validation API","status":"running"}
```

Test using the documented API endpoint and a disposable test value only. Keep any real flags, API secrets and administrator credentials out of screenshots and repository history. Verify API and CTFd flag validation separately.

## 4. Stage-by-stage construction and intended solve path

The following is the intended integration path based on the Assignment 01 report and the challenge artefacts discussed during implementation. The precise build commands, exact flag strings and some challenge internals must be confirmed from the source code and live challenge; this guide does not treat unverified assumptions as completed tests.

### C1 — The Photograph (Steganography, Easy)

**Build / configuration**
- The participant receives the challenge photograph, previously identified as `mystery_photo.jpg`.
- The image was observed to contain an embedded `hidden_message.txt` according to `steghide info`.
- The hidden payload was reported as compressed and encrypted. The extraction passphrase and final flag must be confirmed from the authored challenge files; do not guess them.
- Upload the intended image to the CTFd challenge and confirm the download matches the source artefact.

**Intended solve path**
1. Download the image from CTFd.
2. Inspect file type and metadata; identify that steganography may be present.
3. Use `steghide info mystery_photo.jpg` to check for embedded data.
4. Use the clue/passphrase supplied by the challenge to extract the payload with `steghide extract -sf mystery_photo.jpg`.
5. Read and decode the extracted message as instructed; submit the verified C1 flag and follow its clue to C2.

**Validation**
- The attachment downloads and opens.
- Extraction succeeds with the intended clue/passphrase.
- The recovered flag is accepted; a wrong flag is rejected.
- The stage unlocks C2 only as intended.
- Reset the test participant's progress and repeat.

### C2 — Lab Assistant's Message (Cryptography, Easy)

**Build / configuration**
- The challenge file is `lab_assistant_msg.txt`.
- The message observed in the implementation was Caesar-shifted by 3; the decoded text includes a clue to the Research Portal on port 5003.
- The observed ciphertext includes a candidate C2 flag rendered as Caesar text. Confirm the decoded flag against the actual CTFd configuration before calling it final.

**Intended solve path**
1. Download and inspect the text file.
2. Recognize a Caesar substitution from the shifted alphabet and repeated readable-message patterns.
3. Decode using a Caesar shift of 3 (or a small solver written by the challenge owner).
4. Read the recovered instructions and URL.
5. Submit the verified C2 flag and use the clue to reach C3.

**Validation**
- Decoding yields coherent instructions and the expected next-stage clue.
- The decoded flag exactly matches the flag configured in CTFd.
- Wrong flag rejected, correct flag accepted, expected next stage unlocked.

### C3 — The Abandoned Lab (Web Security / SQL Injection, Moderate)

**Build / configuration**
- The clue points to the Research Portal at `http://192.168.8.188:5003`.
- The portal is intended to run as a deliberately vulnerable web challenge in the lab, with its required database and test records.
- Keep the vulnerable application confined to its challenge network. Do not expose it to the public Internet.
- The exact application source, database schema, credentials, and flag location must be checked in the C3 source files and running service before being recorded as facts.

**Intended solve path**
1. Browse the portal and inspect the login form and response behavior.
2. Use a local, authorized lab test to determine whether input is unsafely incorporated into a database query.
3. Demonstrate the intended SQL-injection weakness using a payload approved by the challenge author, then inspect the research evidence exposed by the challenge.
4. Recover the actual C3 flag and next-stage clue from the lab evidence.
5. Submit the exact configured flag in CTFd.

**Validation**
- The intended vulnerable behavior can be reproduced on the isolated challenge only.
- The solution does not require access to the central host or another user's account.
- The correct flag is accepted, an incorrect one rejected, and C4 unlock behavior matches the design.
- Confirm the application can be reset to its original database state.

### C4 — What happened here? (Digital Forensics, Moderate)

**Build / configuration**
- The intended participant evidence is a supplied archive of recovered lab artefacts. Previously discussed artefact names include access, system, USB-history, deleted-message and network logs; confirm exact filenames from the actual archive.
- Ensure the archive is attached in CTFd and contains the files the challenge description names.
- Do not use a guessed suspicious IP or guessed flag as the expected answer; validate them against the actual evidence files.

**Intended solve path**
1. Download the evidence archive and extract it into a working directory.
2. Inventory the files and timestamps.
3. Search logs for the intrusion timeline, account/access anomalies, removable-media events, deleted-message clues and suspicious network activity.
4. Correlate at least two artefacts before selecting the intended answer.
5. Recover the verified C4 flag and the clue pointing to C5.

**Validation**
- Every named file exists and has relevant content.
- The answer can be supported by the supplied evidence rather than an undocumented assumption.
- Correct/incorrect flag tests work and C5 progression is correct.
- Re-upload/reset restores the same original evidence set.

### C5 — The Last Transmission (Networking / Packet Analysis, Moderate–Hard)

**Build / configuration**
- The PCAP artefact identified during implementation is `last_transmission.pcap`, reported as 8,538 bytes and 74 packets.
- Verify the current CTFd attachment by downloading it and comparing its hash with the source file.
- The PCAP has been opened/identified, but the complete solve and CTFd flag submission are not yet evidenced.

**Intended solve path**
1. Download the PCAP and open it in Wireshark.
2. Inspect packet counts and TCP conversations.
3. Use the C4 clue to focus on the relevant endpoint or conversation; confirm the IP from the actual C4 evidence rather than assuming it.
4. Follow the relevant TCP stream and inspect HTTP or other application payloads.
5. Search for the intended flag or reconstruct it from the evidence if the challenge requires that.
6. Submit the exact verified C5 flag and use the recovered clue for C6.

**Validation**
- The PCAP opens without corruption and includes the traffic described in the prompt.
- The clue leads to a specific, evidence-supported stream.
- The intended flag can be recovered without relying on a hidden answer stored outside the challenge.
- C6 unlocks as configured; incorrect flags do not advance progress.

### C6 — The CURE Research Server (Linux/System Security, Hard capstone)

**Build / configuration**
- KVM/QEMU VM name: `zobi-c6-cure`.
- Guest address observed: `10.10.20.50/24`.
- Isolated libvirt network: `zobi_c6_isolated`, bridge `virbr-c6`.
- The intended guest account is `researcher`.
- The implementation session identified `/opt/zobi-c6/backup.sh` and found `/root/cure.txt` by filename search. The actual contents of the flag file and the intended privilege-escalation path need a final live validation.
- Keep the challenge VM isolated; VNC should remain bound to host loopback and be reached via SSH forwarding.

**Intended solve path**
1. Obtain the VM access information from the previous stage and connect only to the designated lab VM.
2. Enumerate the account's permitted privileges and inspect the provided backup script.
3. Identify the documented weakness in the script and demonstrate the intended privilege escalation inside the disposable guest.
4. Read the designated challenge flag file after reaching the required privilege level.
5. Submit the exact configured C6 flag in CTFd.

**Validation**
- VM boots reliably and the intended account can log in.
- The intended path works only within the guest; no host escape is possible or necessary.
- The correct C6 flag is accepted and a wrong one rejected.
- Reverting the VM snapshot or running the documented reset restores the initial challenge state.

## 5. Full end-to-end test procedure

Use a new test account or reset a designated participant account. Record a screen capture or timestamped screenshots.

1. Open CTFd and confirm all six challenge entries and attachments are present.
2. Attempt to access C2 before solving C1; record whether the dependency blocks access.
3. Solve C1 using the intended extraction path; submit correct flag, then test a wrong flag.
4. Repeat the same correct/incorrect submission pattern for C2 through C6.
5. Confirm each completed stage unlocks only the expected next stage.
6. At C3, verify the web vulnerability is reachable only from the authorized lab network.
7. At C5, confirm the actual attached PCAP is the same validated source file.
8. At C6, confirm the guest IP, account permissions and intended solve path.
9. Reset/revert the environment to its baseline.
10. Repeat a short smoke test after reset and confirm the attachments, services and flags still work.

### Test result log template

| Test ID | Expected result | Actual result | Pass/Fail | Evidence path/date |
|---|---|---|---|---|
| INT-01 CTFd loads | Login page and challenges visible | Pending | Pending | Add evidence |
| INT-02 C1 attachment | Correct image downloads | Pending | Pending | Add evidence |
| INT-03 C1 correct/wrong flag | Correct accepted, wrong rejected | Pending | Pending | Add evidence |
| INT-04 C2 correct/wrong flag | Correct accepted, wrong rejected | Pending | Pending | Add evidence |
| INT-05 C3 intended path | Lab-only SQLi path works | Pending | Pending | Add evidence |
| INT-06 C4 evidence | Archive supports intended answer | Pending | Pending | Add evidence |
| INT-07 C5 PCAP | Opens and intended stream found | Pending | Pending | Add evidence |
| INT-08 C6 intended path | Guest-only task works | Pending | Pending | Add evidence |
| INT-09 stage dependencies | C1→C6 flow enforced | Pending | Pending | Add evidence |
| INT-10 reset/recovery | Baseline restored | Pending | Pending | Add evidence |
| INT-11 isolation | Only approved connections succeed | Pending | Pending | Add evidence |
| INT-12 resource check | CPU/RAM/disk captured | Pending | Pending | Add evidence |

## 6. Defect tracking and design changes

Use one row per actual issue. Do not invent a defect or mark it fixed without evidence.

| ID | Defect / design difference | Impact | Fix or justification | Retest evidence |
|---|---|---|---|---|
| D-01 | Host OS version differs: report proposed Ubuntu Server 20.04; implementation host reported 26.04.1 LTS | Reproducibility and compatibility assumptions differ | Document actual version and test dependencies on it; explain deviation in demo | Pending |
| D-02 | CTFd full flag-validation integration with custom Flask API is not yet evidenced | Architecture may be described inaccurately | Inspect configuration/code and demonstrate the actual flag validation path | Pending |
| D-03 | Complete C4 presence and all six stage dependencies need live verification | End-to-end progression may fail | Verify C4 entry, attachments, flags and prerequisites in CTFd | Pending |
| D-04 | Reset/restore and resource/load evidence are not recorded | Required recovery/capacity claims remain unproven | Run repeatable reset and record before/after state; capture resource usage | Pending |

## 7. What Member 4 should demonstrate in the video

Member 4 should speak naturally and demonstrate the real running platform, not read this document. A useful order is:

1. Introduce themselves and their student ID.
2. Show CTFd and explain the six-stage storyline and dependencies.
3. Show the test checklist and a real correct/incorrect flag result.
4. Demonstrate a short end-to-end path or representative transition between stages.
5. Show evidence of a defect discovered, its fix, and the retest result—or clearly explain an actual design deviation if no defect was fixed.
6. Demonstrate reset/recovery and a post-reset smoke test.
7. Show network/isolation evidence and discuss the risk register.
8. State honestly which tests passed, failed, or remain untested.

Assignment 02 specifies one live, unscripted video of at most 20 minutes for all four members and prohibits AI-generated scripts/explanations during the demonstration. Use this as a checklist for your own preparation; explain the work in your own words.

## 8. Final completion gate

The documents and repository structure are improved, but the implementation is only complete when the following have real evidence:

- [ ] All six stages work through the intended solve path.
- [ ] Correct flags pass and wrong flags fail at every stage.
- [ ] Dependencies are enforced and no trivial shortcut bypasses a stage.
- [ ] Each member's self-developed solver/exploit script is committed and demonstrated.
- [ ] CTFd can be deployed from the submitted repository on a clean environment.
- [ ] Isolation and required/blocked ports have been checked.
- [ ] Reset/recovery has been performed and validated.
- [ ] Resource usage has been recorded.
- [ ] Any differences from Assignment 01 have a technical justification.
- [ ] The final 20-minute video shows the actual running environment and each member's own contribution.

Until each box is checked using actual evidence, retain the corresponding Pending status in the test log.
