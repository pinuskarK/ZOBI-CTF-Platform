# Member 1 — Assignment 02 Final Compliance and Deployment Checklist

This file audits the Member 1 branch against the IE3132 Assignment 02 requirements. It is an implementation checklist, not a claim that unexecuted tests have passed.

## Branch and change audit

- Branch: `member1-platform`
- Main Member 1 implementation record: [MEMBER1_PLATFORM_ARCHITECTURE_IMPLEMENTATION.md](./MEMBER1_PLATFORM_ARCHITECTURE_IMPLEMENTATION.md)
- The Member 1 documentation commit was pushed and subsequently fetched from GitHub.
- Existing branch files were left in place; the implementation record was added under `docs/`.

## Assignment 02 requirements mapped to evidence

| Assignment requirement | Current evidence | Final status |
|---|---|---|
| Deploy the box from scratch in the real environment | Ubuntu host, Docker, CTFd and API were configured; no clean rebuild from repository was evidenced | Partially evidenced |
| Show architecture as built, network segments, ports and services | Host address, CTFd URL, Docker bridge interfaces and C6 isolated libvirt network documented | Partially evidenced; capture a current service/port inventory |
| Demonstrate flag submission and validation | Custom Flask API health check and one test POST recorded | Partial; must test actual CTFd correct/incorrect flags for all stages |
| Demonstrate isolation and privilege restrictions | C6 VM is on a separate libvirt network; VNC bound to loopback; host-to-guest connectivity checked | Partial; still needs a documented allowed/blocked path matrix and firewall review |
| Demonstrate logging | Logging directory exists in the project workspace | Not enough evidence to claim centralized logging is configured and working |
| Demonstrate reset/recovery | A backups directory exists; no repeatable restore result was recorded | Not yet verified |
| Show resource usage | Design resource estimates exist in the Assignment 01 report | Actual runtime resource measurements still needed |
| Provide reproducible setup/run/reset instructions | This branch has architecture notes; no verified clean deployment guide/compose bundle is evidenced by this audit | Add/verify complete setup, run and reset guide |
| Six working stages, 4+ domains, required progression | Six stage names are listed, but C4, all dependencies and the complete end-to-end run are not fully evidenced | Not yet fully verified |
| At least one self-developed solver/exploit script per member | Member 1 platform setup is documented; a Member 1 authored operational validation/reset script is not evidenced in this audit | Add/identify and demonstrate relevant original script |

## Actual environment and design differences

- The report describes Ubuntu Server 20.04, while the implementation observed during setup reported Ubuntu Server 26.04.1 LTS. Explain this deviation and any compatibility consequences in Member 4's video segment.
- The live CTFd URL observed was `http://192.168.8.188:8081/`.
- The custom Flask API has a systemd unit named `zobi-flag-api.service`; it must not be described as the sole CTFd flag validator unless the CTFd configuration actually calls it. A successful test POST to the custom API is not proof that CTFd validates all stage flags through that API.
- C6 guest address: `10.10.20.50/24`; isolated libvirt network: `zobi_c6_isolated`; bridge: `virbr-c6`; gateway: `10.10.20.1`.
- Observed VNC endpoint: host loopback `127.0.0.1:5900`, accessed through SSH forwarding. Do not expose this port publicly.
- Docker bridge addresses were observed, but the exact bridge-to-challenge mapping still needs confirmation using `docker network inspect`.

## Required commands for a final evidence capture

Run on the Ubuntu host and save the outputs to the team's evidence folder:

```bash
date -Is
hostnamectl
lsb_release -a
docker --version
sudo systemctl is-active docker
sudo docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Ports}}\t{{.Status}}'
sudo docker network ls
sudo systemctl status zobi-flag-api.service --no-pager
sudo virsh list --all
sudo virsh net-info zobi_c6_isolated
sudo ss -ltnp
free -h
df -h /
```

For each Docker network, inspect its real subnet and connected containers:

```bash
sudo docker network inspect bridge
```

For C6 host-to-guest checks:

```bash
ping -c 4 10.10.20.50
nc -zv -w 3 10.10.20.50 22
```

Record the date, expected result, actual result and screenshot/log for each test. Do not include API secrets, passwords, or actual final flags in public logs.

## Final pre-demonstration checklist

- [ ] A second person can deploy the submitted project using only the repository README.
- [ ] All six stages and their attachments are present in CTFd.
- [ ] Correct and incorrect flags have been tested for every stage.
- [ ] C1→C6 progression and blocked premature access have been tested.
- [ ] The actual ports and Docker/libvirt networks are documented.
- [ ] Firewall rules and host/guest isolation have been checked.
- [ ] Logs are visible for service startup and validation events without leaking secrets.
- [ ] Reset/recovery was run and a post-reset smoke test passed.
- [ ] CPU, memory and disk usage were captured; capacity claims are labelled as measured or estimated.
- [ ] Member 1 demonstrates deployment, architecture, flag validation, isolation, reset and resource usage in the real running environment.

## Completion statement

The repository now contains Member 1's implementation record and this Assignment 02 compliance checklist. The documented smoke tests are useful evidence, but this checklist intentionally leaves end-to-end flag testing, clean deployment, complete isolation verification, logging, reset/recovery, and measured resource use open until actual test results are captured.
