# C6 — The CURE Research Server

C6 is the Hard Linux/System Security challenge, hosted in a dedicated KVM/QEMU Ubuntu guest. The live lab notes identify guest 10.10.20.50/24 on the isolated libvirt network zobi_c6_isolated, with the challenge script at /opt/zobi-c6/backup.sh and intended account researcher.

## Repository files

- backup.sh — intentionally vulnerable backup-script template; the command name tar is deliberately not an absolute path.
- researcher-sudoers.example — narrowly scoped, intentionally vulnerable sudoers example for the dedicated CTF VM.
- validate_setup.sh — read-only checks for account, file ownership/permissions, sudoers syntax and the flag-file permissions.

These are reproducible templates. Compare them with the actual running VM before claiming the committed source is byte-for-byte identical to the live challenge. The VM disk, live flag, passwords and private keys must not be committed.

## Lab-only safety boundary

The combination of SETENV/PATH control and a privileged script that resolves tar through PATH is intentionally vulnerable. Use only in a disposable, isolated CTF VM. Never install this sudoers policy on a real, shared or production system.

## Administrator deployment outline

1. Create/restore the dedicated Ubuntu guest and attach its NIC only to the approved isolated libvirt network.
2. Create the researcher account using a local secret that is not committed to Git.
3. Create /home/researcher/research with harmless challenge test files.
4. Install backup.sh as root-owned and not writable by researcher; preserve the intended script path /opt/zobi-c6/backup.sh.
5. Review researcher-sudoers.example with visudo -cf before installing it as /etc/sudoers.d/zobi-c6-researcher.
6. Create /root/cure.txt with the actual flag from the CTFd source of truth; keep it root-owned and mode 0600.
7. Run validate_setup.sh as root and save sanitised output.
8. Demonstrate the intended path only inside the VM, then compare the recovered result with the CTFd-configured value.
9. Revert to an approved snapshot or use the documented reset procedure and re-test.

Do not use the example sudoers policy outside the isolated challenge. Verify actual file permissions and sudo configuration: the appearance of tar by command name alone does not prove that PATH hijacking is exploitable.
