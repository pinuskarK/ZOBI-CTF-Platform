# ZOBI - Zombie Outbreak Breach Investigation

ZOBI is a cybersecurity Capture The Flag (CTF) platform designed to provide practical hands-on challenges across multiple cybersecurity domains.

## Challenge Domains

- C1 - Steganography
- C2 - Cryptography
- C3 - Web Security
- C4 - Digital Forensics
- C5 - Networking
- C6 - Linux/System Security

## Platform Architecture

ZOBI uses a hybrid infrastructure consisting of:

- CTFd participant platform
- Docker containers for isolated web-based challenges
- KVM/QEMU virtual machines for system-level challenges
- File-based challenges
- Central Ubuntu Server infrastructure
- Network isolation and controlled access

## Repository Structure

```text
ZOBI-CTF-Platform/
├── challenges/
├── infrastructure/
├── scripts/
├── configs/
├── docs/
└── ctfd/
