# C6 — Linux/System Security: Backup Path Investigation

**Stage:** 6  
**Domain:** Linux privilege escalation / system security  
**Environment:** Dedicated Ubuntu Server VM on the isolated ZOBI lab network  
**Status:** Challenge is reported complete in the live lab. This repository guide documents the known setup and validation requirements; the VM disk image, live credentials and flag are not stored here.

## Scenario

The researcher account has permission to run an administrative backup script. The script invokes a utility by its command name rather than an absolute trusted path. The sudo rule preserves the caller's PATH through the `SETENV` permission. In a deliberately vulnerable, isolated CTF VM, this combination allows a participant to investigate command lookup and demonstrate the intended privilege-escalation path.

This challenge must run only in the dedicated lab VM. Do not reuse this sudo policy on a real or shared server.

## Known lab configuration

- Guest IP in the project notes: `10.10.20.50`
- Isolated libvirt network: `zobi_c6_isolated`
- Subnet: `10.10.20.0/24`
- Challenge script path in the live VM: `/opt/zobi-c6/backup.sh`
- Challenge account: `researcher`
- The C5 PCAP is intended to reveal the participant's connection details. C5's PCAP and build materials are now integrated into the Member 4 branch; the live participant handoff into C6 still requires acceptance testing.
- Do not commit passwords, private keys, or the live C6 flag.

Verify the actual VM settings before recording the final demo. These values are environment-specific.

## Intended learning outcomes

1. Inspect the current user and permitted sudo commands.
2. Read the permitted script and identify unsafe command lookup.
3. Explain how PATH search order can change which executable is invoked.
4. Demonstrate the issue only inside the isolated challenge VM.
5. Retrieve the challenge result using the intended path and submit it through CTFd.

## Deployment files

- `backup.sh` — intentionally vulnerable teaching script.
- `researcher-sudoers.example` — example rule to be reviewed and installed by the VM administrator only.
- `validate_setup.sh` — non-exploitative administrator checklist for the VM configuration.

These files are templates for controlled lab deployment. They do not install a user, set a password, create a flag, or configure the VM network automatically.

## Administrator setup checklist

1. Create or restore the dedicated Ubuntu VM from the team's approved baseline.
2. Configure its NIC only on the isolated `zobi_c6_isolated` network.
3. Create the intended unprivileged `researcher` account using a locally managed secret that is not committed to Git.
4. Install the challenge script as root-owned and not writable by the participant.
5. Review the sudoers example with `visudo -cf` before installing any rule.
6. Place the real flag in a root-owned, participant-unreadable file in the VM; never add it to this repository.
7. Confirm the challenge is not reachable from outside the intended lab boundary.
8. Run the setup validator and save sanitised output.
9. Test the C5-to-C6 path using a clean participant account and record the live result.

## Evidence to collect

- Sanitised output of `ip addr` and `ip route` showing the isolated guest network.
- `sudo -l` output with usernames/host details reviewed before sharing.
- Ownership and permissions of the script and result file.
- Evidence that the intended solve path works in the lab.
- CTFd accepted submission and score.
- Recovery/snapshot name and successful post-recovery validation.

Do not mark the full C1-to-C6 integration as complete until C5 is finished and the handoff has been tested.
