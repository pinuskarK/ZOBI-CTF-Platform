# C6 — The CURE Research Server: Platform and VM Notes

## Role in the platform

C6 is the Hard capstone for Linux/System Security. Unlike C3, it is a dedicated KVM/QEMU virtual machine. The participant is expected to investigate the guest's permissions and backup-script configuration, follow the intended lab-only path, and retrieve the challenge result.

## Observed live configuration

| Setting | Value |
|---|---|
| VM name | zobi-c6-cure |
| Guest address | 10.10.20.50/24 |
| libvirt network | zobi_c6_isolated |
| Bridge | virbr-c6 |
| Host-side gateway | 10.10.20.1/24 |
| Guest interface on host | vnet0 |
| VNC listener | 127.0.0.1:5900 |
| Intended guest account | researcher |
| Challenge script noted during inspection | /opt/zobi-c6/backup.sh |
| Flag file found by filename search | /root/cure.txt |

The host reported Ubuntu Server 26.04.1 LTS. Verify the guest's own OS release and VM CPU/RAM/disk settings before reporting them. Finding the flag filename does not prove its contents or that the intended escalation path passed.

## Host-side status and connectivity checks

Run these on the central Ubuntu host:

    sudo virsh list --all
    sudo virsh domiflist zobi-c6-cure
    sudo virsh net-info zobi_c6_isolated
    sudo virsh net-dumpxml zobi_c6_isolated
    ping -c 4 10.10.20.50
    nc -zv -w 3 10.10.20.50 22
    sudo ss -ltnp | grep 5900

Expected evidence from the recorded setup was: VM running, guest connected to the isolated network, host-to-guest ping replies, TCP 22 reachable from the host, and VNC bound to loopback. Re-run the commands and save fresh outputs for the final demo.

## Console access

The VNC console was accessed from Windows through an SSH local-forwarding tunnel to the Ubuntu host. Keep VNC bound to loopback; do not publish port 5900 to the LAN or Internet. For example, start the tunnel in Windows PowerShell:

    ssh -L 5900:127.0.0.1:5900 pinuskar@192.168.8.188

Then connect the VNC viewer to 127.0.0.1:5900. Use the actual authorised host account for the deployment; never commit private keys or passwords.

## Intended challenge concept

The notes identify /opt/zobi-c6/backup.sh and record that it invokes tar by command name. This is a clue for investigating executable lookup and the PATH environment variable. It is not proof of a vulnerability by itself: verify the script's owner/mode, sudo permissions, environment handling and writable paths inside the guest. The intended challenge may demonstrate PATH hijacking only if those conditions permit it.

The protected result file was found by filename search at /root/cure.txt. Read it only through the authorised challenge path in the guest, then compare the actual result with the C6 flag configured in CTFd. Do not copy the live flag into this repository.

## Isolation and security checks

- Keep the VM NIC on zobi_c6_isolated; confirm the subnet and interface using virsh and guest network commands.
- Test reachability from the host and from the participant client separately.
- Confirm that direct access from the participant LAN to the guest is blocked unless specifically required.
- Keep VNC bound to host loopback and use SSH forwarding.
- Ensure that the intended privilege escalation is confined to the guest; do not attempt host escape.
- Use a known-good snapshot or documented restore method, if available, and test that the restored VM is still solvable.

## Acceptance evidence

- [ ] VM state, guest OS version and resource allocation captured.
- [ ] Guest interface and isolated network captured.
- [ ] researcher account permissions and script permissions inspected.
- [ ] Intended path reproduced inside the VM.
- [ ] Flag value matched against CTFd and accepted by the participant workflow.
- [ ] Incorrect flag rejected by CTFd.
- [ ] Host/guest and participant/guest connectivity matrix recorded.
- [ ] Approved reset/restore performed and retested.

Status remains pending for any item without fresh evidence. The VM disk and secrets are managed outside this source repository.
