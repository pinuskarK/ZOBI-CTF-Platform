# Member 4 — Stage Integration Guide

This guide describes how stage artefacts are laid out in this branch, how the services fit together, and what Member 4 must verify before the demonstration. C5's PCAP and build materials are now integrated; live CTFd validation and the C5-to-C6 handoff remain pending.

## 1. Current repository artefacts

### C1 — Steganography

**Repository path:** `challenges/C1-steganography/mystery_photo.jpg`

The participant receives the mystery photograph and uses Steghide to recover the embedded note. In the lab run recorded by the team, the extraction uses a blank passphrase. The recovered note is a narrative clue for the next stage.

Member 4 checks:
- The image exists in the checked-out branch and downloads without corruption.
- Steghide can read the image and recover the expected text artefact.
- CTFd's challenge attachment is the same file as the repository version.
- The participant submission is accepted and the expected score is recorded.

Do not put the live flag or full solution in participant-facing challenge text.

### C2 — Cryptography

**Repository path:** `challenges/C2-cryptography/lab_assistant_msg.txt`

The message is encoded with a Caesar shift. Decoding it reveals the research-portal clue for C3. The recovered message is an input artefact, not a replacement for the CTFd challenge description.

Member 4 checks:
- The artefact is present in the branch and attached to CTFd.
- The intended Caesar-shift method reproduces the same decoded clue.
- Any username/password needed for the intentionally vulnerable lab portal is provided only through the approved challenge path, not in public documentation.
- The C2 answer is accepted and scoring is recorded.

### C3 — Web security

**Repository path:** `challenges/C3-web-security/`

Included files:
- `app.py` — Flask challenge application.
- `init_db.py` — challenge database initialization.
- `requirements.txt` — Python dependencies.
- `Dockerfile` — container build.
- `compose.yaml` — service configuration.
- `.gitignore` — local-file exclusions.

The project notes identify the service as **The Abandoned Lab / Research Portal**, using Flask and SQLite in Docker, container name `zobi-c3-web-security`, Docker network `zobi_challenges`, and host port `5003`.

First follow docs/platform/C3-Abandoned-Lab.md. The current Compose file requires local C3_FLAG and FLASK_SECRET_KEY values; copy .env.example to .env and replace the placeholders. The default host binding is loopback. If participants must reach C3 from another machine, set C3_BIND_ADDRESS to the authorised lab interface address and enforce a matching firewall rule.

From the challenge directory on the authorised lab host:

```bash
cd ~/ZOBI-CTF-Platform/challenges/C3-web-security
sudo docker compose up -d --build
sudo docker compose ps
curl -i http://127.0.0.1:5003/health
```

If the health endpoint is unavailable, inspect service logs before changing configuration:

```bash
sudo docker compose logs --tail=100
```

Run commands only on the project lab host. Do not expose the deliberately vulnerable service to the public Internet.

Member 4 checks:
- Container is running and the health endpoint responds.
- CTFd challenge link/description points to the correct lab endpoint.
- Intended challenge path works and the CTFd answer is accepted.
- A dummy incorrect answer is rejected.
- Port binding and firewall behaviour match the approved lab boundary.

### C4 — Digital forensics

**Repository directory:** `challenges/C4-digital-forensics/`

Included evidence artefacts:
- `access.log`
- `deleted_message.txt`
- `network.log`
- `system.log`
- `usb_history.txt`

The challenge asks the participant to correlate workstation access, system activity, network transfer records, and USB history. The deleted message gives the investigation context; the network log records the suspicious outbound connection and transfer event. The logs should be analysed together rather than relying on a single line.

Member 4 checks:
- All five files are present and included in the CTFd attachment.
- File names and content are consistent with the source branch.
- The expected conclusion can be reproduced from the evidence set.
- CTFd accepts the intended answer.
- Screenshots used in the final demonstration do not reveal the final answer before the participant solves it.

### C5 — Network analysis

**Status: artefacts integrated; live acceptance pending.**

The intended role of C5 is to analyse a network capture and reveal only the connection details needed to proceed to C6. The PCAP, generator, organiser transmission source and expected-answer file are available under challenges/C5-networking/. The artefact is present, but that does not prove the CTFd attachment, correct/incorrect flag handling or C5-to-C6 handoff passed.

Before integration can be accepted:
- Review the integrated PCAP artefact and confirm its hash against the source of truth.
- Verify the intended solve path from a clean copy.
- Ensure the clue exposes only the required next-stage details.
- Attach the final artefact to CTFd and confirm scoring.
- Test the participant handoff to C6 without using administrator-only shortcuts.

### C6 — Linux/system security

**Deployment details from the current lab notes:** Ubuntu Server guest `10.10.20.50`, on the isolated libvirt network `10.10.20.0/24`. The intended challenge investigates an allowed backup script and a PATH lookup weakness. The VM is separate from the participant-facing CTFd service.

The integrated repository also contains `challenges/C6-linux-security/backup.sh`, `researcher-sudoers.example`, and `validate_setup.sh` as lab-only rebuild templates. Compare them with the actual guest before claiming they match the live VM. The validator checks configuration and file permissions; it does not exploit the guest or reveal the flag.

A host-to-guest SSH route was previously used from Windows through the central host:

```powershell
ssh -J pinuskar@192.168.8.188 researcher@10.10.20.50
```

This is an administrator/tester connection route, not proof that the C5-to-C6 participant flow works. Do not commit passwords or private keys.

Member 4 checks:
- The VM and isolated network are running.
- The intended task is solvable with the intended user permissions.
- The challenge result is accepted by CTFd.
- The final handoff from C5 is tested after C5's live attachment and handoff tests pass.
- VM reset/recovery returns the environment to the documented baseline.

## 2. Central services and network

Current lab endpoints recorded in the project notes:

| Service | Lab endpoint | Purpose |
|---|---|---|
| CTFd participant portal | `http://192.168.8.188:8081/` | Challenge listing, submissions and score |
| C3 web challenge | `http://192.168.8.188:5003/` | Stage 3 web application |
| Flag validation API | `http://127.0.0.1:8080/` on the host | API health/validation service |
| C6 guest | `10.10.20.50` | Isolated Linux challenge |

These are lab values, not public deployment URLs. Confirm the current bindings before a demo. The CTFd deployment notes describe its Nginx port as 8081 and application port as 8001. The Docker CTFd internal network uses separate internal services for its database and cache; those should not be exposed directly to participants.

## 3. Quick integration checks

From the repository root:

```bash
python3 scripts/testing/smoke_test.py
```

For a local CTFd endpoint:

```bash
ZOBI_CTFD_URL=http://127.0.0.1:8081 python3 scripts/testing/smoke_test.py
```

The smoke test checks HTTP reachability only. It does not prove challenge correctness, flag progression, reset behaviour, isolation, or C5-to-C6 dependency.

## 4. Demonstration acceptance checklist

- [ ] Show CTFd participant portal and all currently completed challenges.
- [ ] Demonstrate C1 with the mystery photograph and extracted clue.
- [ ] Demonstrate C2 decoding and the resulting clue.
- [ ] Demonstrate C3 container health and the intended vulnerable web challenge.
- [ ] Demonstrate C4 analysis using all five evidence files.
- [ ] Show the integrated PCAP and its intended analysis path, but distinguish repository checks from live CTFd acceptance.
- [ ] Demonstrate C6 separately as a completed challenge, while explaining that its participant handoff depends on C5.
- [ ] Show accepted and rejected submissions using safe test values.
- [ ] Show service/network isolation and the real recovery procedure.
- [ ] After C5's live acceptance tests pass, run the full C1-to-C6 sequence from a clean participant account.

## 5. Evidence log format

For each run, save a timestamped screenshot or text log and record:

| Field | What to record |
|---|---|
| Test ID | For example INT-04 for C3 |
| Date/time | Actual local timestamp |
| Git commit | Commit hash of the tested version |
| Environment | Host/VM and relevant service version |
| Action | Exact participant or operator action |
| Expected result | Defined before the test |
| Actual result | What really happened |
| Status | PASS / FAIL / BLOCKED / NOT RUN |
| Evidence path | Relative path under the team's approved evidence folder |
| Defect/fix | Issue ID and fixing commit if applicable |

Do not mark the whole platform as end-to-end complete while C5 artefacts are integrated; live acceptance remains pending.
