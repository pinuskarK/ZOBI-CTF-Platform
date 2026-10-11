# C5 Integration Status — The Last Transmission

**Current state:** source artefacts are integrated into the Member 4 branch. Live acceptance is pending.

## Artefacts

- Participant file: challenges/C5-networking/last_transmission.pcap
- Generator: challenges/C5-networking/build/create_pcap.py
- Organiser source: challenges/C5-networking/build/transmission.txt
- Expected answer: challenges/C5-networking/flag.txt
- Stage instructions: challenges/C5-networking/README.md
- Structural validator: scripts/testing/validate_c5_pcap.py

The organiser source contains the expected answer and lab connection details. Restrict repository access to the project team. Do not use the organiser source as the CTFd participant attachment.

## Validate repository files

From the repository root:

    python3 scripts/testing/check_artifacts.py

With Scapy installed in a disposable test environment:

    python3 scripts/testing/validate_c5_pcap.py

The validator checks packet count and presence of expected clue markers. It is not a substitute for manually opening the PCAP in Wireshark.

## Manual participant solve

1. Download the actual CTFd attachment using a clean participant account.
2. Compare its checksum with the approved source PCAP.
3. Open it in Wireshark and apply a filter based on the suspicious destination identified in C4.
4. Select the relevant TCP connection and use Follow → TCP Stream.
5. Confirm the reconstructed transfer contains the intended C5 result and only the required next-stage clue.
6. Submit the expected C5 answer in CTFd and record the accepted score.
7. Submit a deliberately incorrect test value and record that it is rejected.
8. Use the recovered connection information to reach C6 only through the intended lab route.
9. Record the C5-to-C6 handoff using a clean participant account.

## Acceptance record

| Test | Result | Evidence |
|---|---|---|
| Source artefact present | Repository check required | Save command output |
| PCAP structurally valid | Validator not yet run in the live project environment | Save output |
| Manual Wireshark solve | Pending | Screenshot or screen recording |
| CTFd correct flag accepted | Pending | Submission/score screenshot |
| CTFd wrong flag rejected | Pending | Submission screenshot |
| C5 clue reaches C6 correctly | Pending | Sanitised terminal evidence |
| C1-to-C6 end-to-end path | Pending | Full clean-account walkthrough |
| Reset and recovery | Pending | Before/after evidence |

Do not change any result to PASS until the actual test has been performed.