# ZOBI CTF — Test Results Register

**Owner:** Member 4 — Integration, Testing & Documentation  
**Status:** Partial evidence recorded; full end-to-end acceptance remains pending.  
**Rule:** Mark a test PASS only after running it against the current deployment and saving evidence.

## Results based on work recorded so far

| ID | Area | Known observation | Status | Evidence still needed |
|---|---|---|---|---|
| M4-01 | C1 steganography | Extracted the hidden note from mystery_photo.jpg with Steghide using a blank passphrase. | PASS — extraction method only | Screenshot of participant solving the CTFd challenge and submitting the flag |
| M4-02 | C2 cryptography | lab_assistant_msg.txt is intended to be decoded with a Caesar shift; decoded text points to C3. | PARTIAL | Confirm file is attached to CTFd and test with a participant account |
| M4-03 | C3 web security | Flask health endpoint responded and the intended SQL-injection test returned the challenge flag in the lab. | PASS — local challenge test only | Participant browser test, CTFd submission, and network-boundary test |
| M4-04 | C4 digital forensics | Five evidence logs were packaged into C4_evidence.zip and the ZIP contents were listed successfully. | PASS — archive preparation only | Upload to CTFd and solve with a clean participant account |
| M4-05 | C5 network analysis | Intended to reveal C6 connection details. | NOT VERIFIED | Inspect PCAP, validate host details, and prove C5-to-C6 progression |
| M4-06 | C6 Linux/system security | C6 VM was reachable from the host over the isolated lab network; the intended PATH-hijack path was tested. | PASS — privilege-escalation path only | Participant access via C5, final flag submission, and CTFd completion state |
| M4-07 | CTFd progression | CTFd is available at the lab URL on port 8081. | PARTIAL | Confirm all six challenges are visible and dependencies are enforced |
| M4-08 | End-to-end run | No complete clean-account C1-to-C6 run is confirmed in current evidence. | NOT RUN | Record start/end time, screenshots, scores, and defects |

## Live execution log

| Date/time | Test ID | Tester/account (no password) | Actual result | Evidence file/path | Defect ID |
|---|---|---|---|---|---|
| Pending | — | — | — | — | — |

## Evidence hygiene

- Use dummy accounts where possible.
- Redact passwords, tokens, private keys, and live flags from screenshots.
- Keep raw evidence in the approved evidence folder with timestamps.
- Record the commit hash for each code or configuration fix.
