# ZOBI — Zombie Outbreak Breach Investigation

ZOBI is the IE3132 Assignment 02 CTF environment. The intended player path is C1 → C2 → C3 → C4 → C5 → C6 across steganography, cryptography, web security, digital forensics, network analysis, and Linux/system security.

## Branch responsibilities

- Member 1 branch: platform architecture, C3 container implementation, central host and C6 infrastructure notes, setup and platform inventory checks.
- Member 2 branch: C1 and C5 challenge artefacts/build material.
- Member 3 branch: challenge evidence and supporting artefacts.
- Member 4 branch: integrated stage artefacts, test plan/results, risk register, design-change record and recovery runbook.

## Member 4 integrated repository

This branch includes:
- C1 photograph and C2 encoded message.
- C3 Flask/SQLite Docker application source and configuration.
- C4 forensic log artefacts.
- C5 participant PCAP, Scapy generator, organiser transmission source, and expected-answer file.
- C6 VM documentation (the actual VM disk and secrets remain outside Git).
- Artifact integrity, HTTP smoke-test and C5 PCAP validation scripts.
- Member 4 integration plan, test results, risk and recovery documents.

## Run repository checks

From the repository root:

    python3 scripts/testing/check_artifacts.py
    python3 scripts/testing/smoke_test.py

If Scapy is installed in a test environment, validate the C5 artefact:

    python3 scripts/testing/validate_c5_pcap.py

The artifact checker verifies that expected files exist. The HTTP smoke test checks reachability. The PCAP validator checks basic structure and clue markers. None of these proves CTFd flag validation, challenge progression, network isolation, reset/recovery or the full C1-to-C6 path.

## C5 build

The C5 PCAP is in challenges/C5-networking/last_transmission.pcap. The generator is in challenges/C5-networking/build/create_pcap.py and reads build/transmission.txt. From that build directory, run:

    python3 create_pcap.py
    cp last_transmission.pcap ../last_transmission.pcap

Compare the rebuilt capture with the approved source before updating the CTFd attachment. The organiser source includes expected-answer and lab connection details; keep the repository access-controlled.

## Important live acceptance status

Repository artefacts have been integrated, but the following must still be performed in the actual lab before claiming final completion:

- Confirm each CTFd attachment matches its repository artefact.
- Submit the configured correct and incorrect flags for every stage.
- Verify each prerequisite/unlock rule and test premature access.
- Solve C5 manually in Wireshark and verify the live CTFd submission.
- Test the C5-to-C6 handoff with a clean participant account.
- Execute the approved reset/recovery procedures and re-test.
- Capture current service, firewall, network, log and resource evidence.

Keep live flags, passwords, private keys, tokens and administrator credentials out of public documentation and recordings. If any live C6 credential has been exposed through a public repository or recording, treat it as compromised and rotate it.