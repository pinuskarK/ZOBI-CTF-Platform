# C5 — The Last Transmission

**Stage:** 5  
**Domain:** Network analysis / packet analysis  
**Difficulty:** Moderate–Hard  
**Participant artefact:** last_transmission.pcap

## Build artefacts

- last_transmission.pcap — packet capture served to participants.
- build/create_pcap.py — Scapy generator for the synthetic traffic.
- build/transmission.txt — organiser-side source message included in the suspicious HTTP transfer.
- flag.txt — organiser-side expected answer.

Keep this repository restricted to the project team. The source message contains lab connection information and the expected answer. Never upload build inputs or solution files as participant attachments.

## Intended solve path

1. Obtain the suspicious destination clue from C4.
2. Open the PCAP in Wireshark.
3. Filter for the destination identified by the C4 evidence.
4. Select the suspicious TCP conversation and use Follow → TCP Stream.
5. Reconstruct the HTTP request body and identify the C5 flag and the next-stage connection clue.
6. Submit the configured C5 flag in CTFd, then use the clue to continue to C6.

## Rebuild

Run from this directory on a machine with Python 3 and Scapy installed:

    cd build
    python3 create_pcap.py
    cp last_transmission.pcap ../last_transmission.pcap

The generator reads build/transmission.txt relative to its current working directory. Compare the generated capture with the tested artifact before replacing the participant attachment.

## Acceptance checks

- [ ] PCAP opens in Wireshark and contains the intended traffic.
- [ ] C4's clue identifies the intended stream without relying on a guessed address.
- [ ] Follow TCP Stream reconstructs the expected record.
- [ ] Correct C5 flag is accepted and incorrect flag rejected by CTFd.
- [ ] The captured next-stage details match the actual isolated C6 VM and are not exposed elsewhere.
- [ ] C5-to-C6 transition works with a clean participant account.
- [ ] C6 access secret is rotated if it has been exposed in a public repository or recording.

The presence of a PCAP and generator is not, by itself, proof that the CTFd attachment, flag, or C5-to-C6 handoff has passed live acceptance testing.
