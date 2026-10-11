# Member 1 — Final Platform Runbook and Completion Record

**Project:** ZOBI — Zombie Outbreak Breach Investigation  
**Module:** IE3132 Penetration Testing — Assignment 02  
**Branch:** `member1-platform`  
**Scope:** central platform, CTFd, Docker/C3, custom flag API, KVM/QEMU/C6, network boundaries, operations and evidence.

## 1. Purpose and evidence rule

This is the consolidated runbook for Member 1's platform contribution. It separates (a) observed setup facts, (b) repository implementation, and (c) live tests that still need to be performed. Do not mark a test passed because a file or command exists; run it on the actual host and save sanitised evidence.

## 2. Observed environment

- Hostname recorded: `ZOBI-Central-server`
- Host LAN address recorded: `192.168.8.188/24`
- Host OS reported by `lsb_release -a`: Ubuntu Server 26.04.1 LTS. The original design described Ubuntu Server 20.04; this is an implementation deviation to disclose.
- Docker reported: 29.1.3.
- CTFd URL observed during setup: `http://192.168.8.188:8081/`.
- Custom Flask API service: `zobi-flag-api.service`; health endpoint and a disposable test POST were observed working.
- C6 VM: `zobi-c6-cure`, guest `10.10.20.50/24`, libvirt network `zobi_c6_isolated`, bridge `virbr-c6`, gateway `10.10.20.1`.
- C6 VNC was observed on host loopback `127.0.0.1:5900`; remote graphical access used SSH forwarding.

These are previously recorded observations. Check current state again before a demonstration.

## 3. Architecture as implemented / intended

- CTFd is the participant-facing challenge and submission platform.
- C1, C2, C4 and C5 are file/evidence-led challenges.
- C3 is a Flask application using SQLite, packaged as a Docker service on port 5003.
- C6 is a separate Ubuntu guest managed by KVM/QEMU.
- The custom Flask flag API is a separate service. Its health check and test POST do **not** prove that CTFd is configured to call it; inspect the real CTFd configuration before claiming integration.
- The intended progression is C1 → C2 → C3 → C4 → C5 → C6. All six dependency rules and the actual CTFd flags still require one clean end-to-end test.
- Do not claim nginx, PostgreSQL, central logging, scheduled backups, automatic reset, or complete firewall isolation unless current host evidence confirms each feature.

## 4. C3 service runbook

Source directory: `challenges/C3-web-security/`.

The application uses Flask, SQLite and Gunicorn. The intentional vulnerability is unsafe SQL string concatenation in the login path. The archive route is session-protected and displays the flag supplied through `C3_FLAG`. The service runs as a non-root container user in the repository Dockerfile; confirm the live image matches the repository.

On the authorised Ubuntu lab host, from the C3 directory:

```bash
cp .env.example .env
# Edit .env locally: set C3_FLAG to the value configured in CTFd,
# generate a private FLASK_SECRET_KEY, and choose the intended bind IP.
docker network inspect zobi_challenges
docker compose config
docker compose up -d --build
docker compose ps
docker compose logs --tail=100 c3-web-security
curl -fsS http://127.0.0.1:5003/health
```

If the network does not exist, create it only after confirming the subnet does not conflict with existing Docker/libvirt networks:

```bash
docker network create --driver bridge --subnet 172.20.0.0/24 --gateway 172.20.0.1 zobi_challenges
```

The Compose default should bind to loopback. If participants require LAN access, set `C3_BIND_ADDRESS` to the intended lab interface address and enforce the matching host firewall rule. Never expose the vulnerable challenge to the public Internet.

Local unit tests:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python -m unittest discover -s tests -v
```

Unit tests use a temporary test database. They do not prove the live container, CTFd flag, network isolation, or stage progression.

## 5. C6 VM and isolation runbook

Run on the Ubuntu host:

```bash
sudo virsh list --all
sudo virsh domiflist zobi-c6-cure
sudo virsh net-info zobi_c6_isolated
sudo virsh net-dumpxml zobi_c6_isolated
ping -c 4 10.10.20.50
nc -zv -w 3 10.10.20.50 22
sudo ss -ltnp
```

Use the existing approved SSH tunnel for the VNC console; do not expose port 5900 to the LAN. Inside the guest, verify the actual `researcher` account, `/opt/zobi-c6/backup.sh`, permissions, sudo policy and `/root/cure.txt`. The saved evidence identifies these paths, but the final intended escalation and flag submission must be re-run and recorded.

Do not run challenge escalation commands on the central host. Use a disposable/snapshotted guest and restore it after testing.

## 6. Current evidence versus open requirements

| Requirement | Recorded evidence | Final state |
|---|---|---|
| Docker installed | Version 29.1.3 observed | Previously observed; recheck live |
| Docker smoke test | hello-world succeeded | Previously passed |
| CTFd availability | Browser access at port 8081 reported | Basic access only; retest |
| Custom Flask API | Health JSON and disposable POST response observed | API-only test; CTFd integration unproven |
| C6 VM/network | VM running, isolated libvirt network, host-to-guest ping and TCP 22 observed | Partial; repeat current checks |
| All challenge flags/dependencies | Six stage names and intended sequence documented | Pending full end-to-end acceptance |
| Firewall/isolation | C6 network and loopback VNC observed | Pending allowed/blocked path matrix |
| Logs | API systemd journal available | Centralised challenge logging not established |
| Reset/restore | Design notes exist | No complete restore run evidenced |
| Resource usage | No final live measurements in the saved evidence | Pending |
| Clean deployment from repository | Existing CTFd installation works; full clean deployment not evidenced | Pending |

## 7. Evidence capture commands

Run on the Ubuntu host and save output to a private project evidence folder. Redact secrets, tokens, usernames where appropriate, and final flags.

```bash
date -Is
hostnamectl
lsb_release -a
docker --version
sudo systemctl is-active docker
sudo docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Ports}}\t{{.Status}}'
sudo docker network ls
sudo systemctl status zobi-flag-api.service --no-pager
sudo journalctl -u zobi-flag-api.service -n 80 --no-pager
sudo virsh list --all
sudo virsh net-info zobi_c6_isolated
sudo ss -ltnp
free -h
df -h /
```

For each test record timestamp, source machine, destination, expected result, actual result, pass/fail and evidence path. Do not publish secret environment files or actual CTF flags in screenshots.

## 8. Final acceptance checklist

- [ ] A second team member follows the setup notes without undocumented steps.
- [ ] CTFd contains all six challenges and the intended attachments.
- [ ] Correct and incorrect flags tested for C1–C6.
- [ ] C1→C6 prerequisites tested using a fresh participant account.
- [ ] C3 local unit tests pass and live C3 is only reachable from the approved lab network.
- [ ] C6 intended path and final flag are re-tested inside the guest.
- [ ] Docker/libvirt network mappings and firewall allow/deny matrix recorded.
- [ ] Service logs inspected without leaking secrets.
- [ ] Reset/recovery performed and post-reset smoke test passed.
- [ ] CPU, memory and disk measurements captured under representative load.
- [ ] Any difference from the original design (including Ubuntu version) is documented and justified.

## 9. Honest completion statement

The repository contains the Member 1 architecture and compliance documentation, C3 source/deployment files and unit tests, and C6 environment notes. The saved session confirms some setup smoke tests, but does not yet prove all Assignment 02 acceptance criteria. Keep remaining items open until they have live evidence.
