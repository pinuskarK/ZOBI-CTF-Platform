# Member 1 — CTF Platform & Architecture Implementation Record

**Owner:** Pinuskar K (Member 1)  
**Project:** ZOBI — Zombie Outbreak Breach Investigation  
**Module:** IE3132 Penetration Testing  
**Scope:** Platform architecture, central host, Docker/KVM foundation, service access, flag API, network separation, and operational setup.

> This file records implementation evidence separately from design intentions. A feature described in the report is not labelled as tested unless there is evidence from the implementation session.

## 1. Responsibilities aligned with the report

The final report assigns Member 1 responsibility for:

- Designing the hybrid file-based, Docker, and KVM/QEMU platform for all six challenges.
- Producing the system architecture and CTF network diagrams.
- Defining the operating environment and per-challenge resource requirements.
- Planning phased deployment, isolation, and reset/recovery.
- Configuring firewall rules and port-forwarding strategy.
- Designing access control, logging, and backup strategy.
- Selecting technologies and planning resources/scalability.
- Integrating the challenge details supplied by Members 2 and 3 into one architecture.

## 2. Implemented platform foundation

### Central Ubuntu host

- Hostname: `ZOBI-Central-server`
- Host LAN address observed during testing: `192.168.8.188/24`
- Implemented OS reported by `lsb_release -a`: Ubuntu Server `26.04.1 LTS`.
- Docker version observed: `29.1.3`.
- Docker service was enabled with systemd.
- A Docker `hello-world` test completed successfully.
- Project workspace was created under `~/zobi-ctf/` with these directories: `docker/`, `flag-api/`, `challenges/`, `configs/`, `logs/`, `scripts/`, and `backups/`.

**Report alignment note:** the design report describes an Ubuntu Server 20.04 environment. The running implementation observed during setup is Ubuntu Server 26.04.1 LTS. Keep the report and implementation documentation consistent by recording this as an implementation-version difference, rather than claiming the running host is 20.04.

### CTFd platform

- CTFd was accessible at `http://192.168.8.188:8081/` during the setup session.
- Six challenge stages are represented in the platform:
  1. C1 — The Photograph (Steganography)
  2. C2 — Lab Assistant's Message (Cryptography)
  3. C3 — The Abandoned Lab (Web Security)
  4. C4 — What happened here? (Digital Forensics)
  5. C5 — The Last Transmission (Networking / Packet Analysis)
  6. C6 — The CURE research Server (Linux/System Security)
- The intended progression is C1 → C2 → C3 → C4 → C5 → C6.
- A prior project update reported C1, C2, C3, C5, and C6 added to CTFd. Verify C4 and all unlock/dependency rules in the live platform before claiming all six are fully validated.

### Flask Flag Validation API

- A Python virtual environment was created for the flag API and Flask was installed.
- The API was run, called from Windows PowerShell, and returned the service status JSON:
  `{"service":"ZOBI CTF Flag Validation API","status":"running"}`.
- A POST test with a test flag returned a response indicating the test flag was accepted (`Correct flag! True`).
- A systemd unit named `zobi-flag-api.service` was created and enabled; its status was observed as active during the session.

**Scope note:** the successful POST was a test of the custom Flask API. It does not by itself prove that every CTFd challenge flag, CTFd unlock rule, or end-to-end player workflow is correctly configured.

## 3. Virtualization and network separation

### C6 KVM/QEMU VM

- VM name: `zobi-c6-cure`
- VM was listed as running by `virsh`.
- Guest address observed inside the VM: `10.10.20.50/24`.
- Isolated libvirt network: `zobi_c6_isolated`.
- Bridge: `virbr-c6`; host-side gateway: `10.10.20.1/24`.
- The VM interface `vnet0` was attached to `virbr-c6`.
- The libvirt network was observed as active and persistent with autostart enabled.
- The VNC console was bound to host loopback `127.0.0.1:5900`, rather than being exposed on the LAN.
- Windows access used an SSH local-forwarding tunnel to the Ubuntu host, followed by TigerVNC Viewer at `127.0.0.1::5900`.
- Direct SSH from Windows to `10.10.20.50:22` timed out, as expected when the isolated guest network is not routed to the Windows LAN.
- From the Ubuntu host, `ping -c 4 10.10.20.50` received 4/4 replies and `nc -zv -w 3 10.10.20.50 22` reported that TCP port 22 was open.

**Security interpretation:** these checks demonstrate host-to-guest reachability and the local VNC tunnel setup. They do not constitute a full isolation audit or prove that every path from the guest to the host/other networks is blocked.

### Docker networks

The host showed Docker bridge interfaces including `docker0` (`172.17.0.1/16`) and project-created bridges in `172.18.0.0/16`, `172.19.0.0/16`, and `172.20.0.0/24`. These are observed interfaces; map each bridge to its container/service with `docker network ls` and `docker network inspect` before documenting a definitive challenge-to-network mapping.

## 4. Architecture and operational design to maintain

The design report specifies a hybrid platform:

- File-based challenges: C1, C2, C4, and C5.
- Docker-based web application: C3.
- KVM/QEMU VM: C6.
- Central participant interface and challenge/flag management through CTFd and the flag-validation service.
- Separate, controlled network segments for intentionally vulnerable challenge environments.
- Default-deny inbound firewall approach, only exposing required ports.
- PostgreSQL should remain bound to an appropriate trusted/local interface and should not be publicly exposed.
- Logging, backups, reset/recovery, resource limits, and a growth path from 10–20 participants toward 50+ are design requirements that need evidence and repeatable checks before being called fully implemented.

The report's proposed central services include Docker, KVM/QEMU, Flask Flag Validation API, PostgreSQL, and nginx. In the implementation record, only services directly confirmed in the session are marked as observed above. Do not infer that nginx, PostgreSQL, all firewall rules, central logging, scheduled backups, or a complete reset automation are deployed without checking the server.

## 5. Testing evidence and current status

| Check | Evidence observed | Status |
|---|---|---|
| Docker installation | `docker --version` returned Docker 29.1.3 | Passed |
| Docker runtime smoke test | `hello-world` completed successfully | Passed |
| CTFd availability | Browser access to `http://192.168.8.188:8081/` reported during setup | Basic access observed; full workflow still needs verification |
| Flask API health endpoint | Returned expected service/status JSON | Passed |
| Flask API test submission | Test POST returned `Correct flag! True` | Passed for the test value |
| systemd API service | `zobi-flag-api.service` observed active/enabled | Passed at time checked |
| C6 VM state | `zobi-c6-cure` listed running | Passed at time checked |
| Host-to-C6 reachability | 4/4 ICMP replies from `10.10.20.50` | Passed |
| Host-to-C6 SSH port | TCP 22 connection succeeded from host | Passed |
| VNC exposure | QEMU listening on `127.0.0.1:5900`; SSH tunnel + TigerVNC used | Local-console path observed |
| C6 intended flag retrieval | `/root/cure.txt` was found by filename search, but contents/end-to-end submission were not shown in the recorded output | Not yet verified |
| All six CTFd challenges and dependencies | Some challenges were reported added; complete dependency walkthrough not evidenced | Needs end-to-end test |
| Firewall/isolation audit | Isolated libvirt bridge observed; complete rules and reachability matrix not supplied | Needs verification |
| Reset/backup/restore | Design requirements documented; repeatable restore test not evidenced | Needs verification |
| Load/resource/scalability | No measured concurrent-user test evidence supplied | Planned/not yet verified |

## 6. Recommended repeatable checks before final demonstration

Run on the Ubuntu host:

```bash
hostnamectl
lsb_release -a
docker --version
sudo systemctl status docker --no-pager
sudo docker ps
sudo systemctl status zobi-flag-api.service --no-pager
sudo virsh list --all
sudo virsh net-info zobi_c6_isolated
sudo ss -ltnp
```

Check Docker network mappings:

```bash
sudo docker network ls
sudo docker network inspect bridge
```

From the host, check C6 reachability:

```bash
ping -c 4 10.10.20.50
nc -zv -w 3 10.10.20.50 22
```

Also test, in the CTFd browser, the full C1→C6 path with a correct flag and an incorrect flag at each stage, expected unlocks, attachments, and reset/recovery. Record actual results and screenshots; do not mark a test passed until it has been run.

## 7. Final implementation checklist

- [x] Ubuntu host reachable over SSH.
- [x] Docker installed and smoke-tested.
- [x] Project workspace directories created.
- [x] Flask flag API health and test POST checked.
- [x] Flag API systemd service enabled/active at time checked.
- [x] C6 KVM VM running and reachable from host.
- [x] VNC console accessible through an SSH tunnel.
- [ ] Verify all six challenges, attachments, flags, and unlock dependencies end to end.
- [ ] Verify incorrect flags are rejected and correct flags are accepted in the actual CTFd workflow.
- [ ] Confirm the exact firewall rules and network isolation with documented tests.
- [ ] Demonstrate a reset/recovery procedure and validate restored state.
- [ ] Confirm logging, backup scheduling/restoration, resource limits, and any nginx/PostgreSQL services before describing them as implemented.


## 8. Repository implementation updates — 2026-10-11

The C3 repository component now includes:

- A Flask application that intentionally retains the SQL injection weakness for the isolated teaching challenge.
- Required environment variables for the C3 flag and Flask session secret; neither has a hard-coded fallback in the application.
- A Compose configuration with a loopback-only default host binding, persistent SQLite volume, and HTTP health check.
- A safe environment template at `challenges/C3-web-security/.env.example`; the real `.env` file is excluded by the challenge directory's `.gitignore`.
- Unit tests at `challenges/C3-web-security/tests/test_app.py` for health, unauthenticated archive access, ordinary invalid login, intended SQLi behaviour, and logout.
- A full C3 setup, operation, recovery and evidence guide at `docs/platform/C3-Abandoned-Lab.md`.
- A root setup/inventory guide and read-only host inventory script at `scripts/testing/member1-platform-check.sh`.
- C6 VM notes at `docs/platform/C6-CURE-Research-Server.md`.

Run C3 unit tests from the C3 directory with Flask/Gunicorn dependencies installed:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python -m unittest discover -s tests -v
```

Run the read-only platform inventory from the repository root:

```bash
bash scripts/testing/member1-platform-check.sh
```

These source changes and test definitions have been committed to the Member 1 branch. They have not been executed on the live Ubuntu host in this review. Live CTFd submissions, firewall isolation, clean deployment, reset/recovery, logging and resource tests remain pending until the team runs them and records evidence.
