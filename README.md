# ZOBI — Zombie Outbreak Breach Investigation

ZOBI is a cybersecurity Capture The Flag (CTF) project based on investigating a zombie outbreak and recovering stolen cure research.

Participants complete connected challenges, recover flags, and follow clues to the next stage.

## Challenge Domains

- C1 — Steganography
- C2 — Cryptography
- C3 — Web Security
- C4 — Digital Forensics
- C5 — Networking
- C6 — Linux/System Security

## Platform Overview

The current custom ZOBI participant portal provides:

- Registration and login
- PostgreSQL user management
- Challenge dashboard
- Flag validation
- Submission logging
- Nginx reverse proxy
- HTTPS

CTFd was considered as an alternative platform. The final platform choice is managed by Member 1.

Challenge 6 is accessed through SSH on the ZOBI central server rather than completed through the website.

## Repository Structure

The Member 2 challenge files are organised as follows:

```text
ZOBI-CTF-Platform/
├── README.md
└── challenges/
    ├── challenge1/
    │   ├── mystery_photo.jpg
    │   └── flag.txt
    └── challenge5/
        ├── last_transmission.pcap
        ├── flag.txt
        └── build/
            ├── create_pcap.py
            └── transmission.txt
```

Other members maintain the remaining challenges and infrastructure.

## Member 2 — Challenges 1 and 5

This section documents how these challenges work, how participants solve them, and how organisers deploy and rebuild them.

**Organiser documentation:** This README contains solutions, flags, and lab credentials. Keep it in the private organiser repository. Participants should receive only the intended challenge files and hints.

---

## Challenge 1 — Hidden Message in a Photograph

### Objective

Investigate a suspicious photograph, extract a hidden message, and recover the Challenge 1 flag.

The extracted message also directs participants to investigate `lab_assistant_msg.txt`, connecting this challenge to the next stage.

### How It Works

Steghide embeds `hidden_message.txt` inside a JPEG image.

The resulting `mystery_photo.jpg` looks like an ordinary photograph but contains the hidden text.

An empty passphrase is used.

### Files

| File | Purpose | Participant access |
| --- | --- | --- |
| `mystery_photo.jpg` | JPEG containing the hidden message | Yes |
| `flag.txt` | Expected flag for portal validation | No |
| `original_photo.jpg` | Original JPEG used to build the challenge | No |
| `hidden_message.txt` | Message embedded inside the JPEG | No |
| `test_extracted.txt` | Local extraction test output | No |

The original image, hidden message, and extraction test file are currently local build files. They are not included in the repository structure shown above.

### Participant Workflow

1. Download `mystery_photo.jpg` from the ZOBI portal.
2. Investigate the image using a steganography tool.
3. Extract the embedded message with Steghide.
4. Read the extracted text and recover the flag.
5. Submit the flag in the Challenge 1 submission field.
6. Follow the clue referring to `lab_assistant_msg.txt`.

### Solution

Requirements: Steghide.

Run the following command from the directory containing the downloaded image:

```bash
steghide extract -sf mystery_photo.jpg -xf recovered_note.txt -p ""
```

Read the extracted message:

```bash
cat recovered_note.txt
```

The empty string after `-p` specifies the empty passphrase.

### Flag

```text
FLAG{photograph_secret_recovered}
```

### Hidden Message

```text
ZOBI RESEARCH LAB — RECOVERED NOTE

FLAG{photograph_secret_recovered}

The lab assistant left another message.
Find lab_assistant_msg.txt and investigate its contents.
```

### Build Instructions

Requirements:

- Steghide
- `original_photo.jpg`
- `hidden_message.txt`

From the directory containing those files, run:

```bash
steghide embed -cf original_photo.jpg -ef hidden_message.txt -sf mystery_photo.jpg -p ""
```

Verify the generated image:

```bash
steghide extract -sf mystery_photo.jpg -xf test_extracted.txt -p ""
cat test_extracted.txt
```

Confirm that the extracted text contains the correct flag and next-stage clue.

### Suggested Hints

1. There is more to the photograph than meets the eye.
2. Look for information hidden inside the image.
3. Try Steghide with an empty passphrase.

### Deployment

- Provide `mystery_photo.jpg` as the Challenge 1 download.
- Configure the portal to accept the exact flag listed above.
- Preserve the original file bytes when uploading and serving the image.
- Avoid image compression or conversion, which may damage the embedded data.
- Keep the flag file, build inputs, and solution documentation private.

### Reset

No server-side challenge state needs resetting.

Participants can download a fresh copy of the image. Organisers can restore the tested image or rebuild it using the build instructions.

### Verification Status

- Hidden message successfully embedded.
- Hidden message successfully extracted.
- Flag and next-stage clue checked.
- Challenge image and flag file pushed to the Member 2 branch.
- Final portal download and flag submission still require integration testing.

---

## Challenge 5 — Last Transmission

### Objective

Analyse a packet capture, investigate the suspicious IP address discovered in Challenge 4, and recover the Challenge 5 flag.

The recovered transmission also provides SSH access details for continuing the investigation on the ZOBI central server.

### How It Works

A Python script uses Scapy to generate a synthetic packet capture.

The capture contains background HTTP traffic and a suspicious HTTP transfer from Dr Alex's workstation to `198.51.100.23`.

The suspicious transfer contains:

- A reference to the stolen `cure.txt` file
- The Challenge 5 flag
- ZOBI central-server SSH access details

The message is split across TCP packets. Participants can reconstruct it using Wireshark's **Follow TCP Stream** feature.

The capture is generated locally. The build script does not send traffic to the listed IP addresses.

### Files

| File | Purpose | Participant access |
| --- | --- | --- |
| `last_transmission.pcap` | Packet capture to investigate | Yes |
| `flag.txt` | Expected flag for portal validation | No |
| `build/create_pcap.py` | Script used to generate the capture | No |
| `build/transmission.txt` | Message included in the suspicious transfer | No |

### Connection to Challenge 4

Participants obtain the suspicious IP address from Challenge 4 and use it to identify the relevant traffic in Challenge 5.

| Detail | Value |
| --- | --- |
| Workstation | DR-ALEX-PC |
| Workstation IP | `192.168.10.25` |
| Suspicious destination IP | `198.51.100.23` |
| Destination port | TCP `80` |
| Protocol | Plaintext HTTP |
| File reference | `cure.txt` |
| Event date | `2026-09-18` |
| Connection start | `09:48:51` |
| Transfer start | `09:49:12` |
| Connection close | `09:49:18` |
| Timestamp timezone | UTC+05:30 |

The capture represents the transfer portion of the investigation. It does not reproduce every event recorded in Challenge 4.

Wireshark's displayed times may differ depending on the viewer's timezone settings.

### Participant Workflow

1. Obtain the suspicious IP address from Challenge 4.
2. Download `last_transmission.pcap` from the ZOBI portal.
3. Open the capture in Wireshark.
4. Filter traffic involving the suspicious IP.
5. Follow the relevant TCP stream.
6. Read the reconstructed transmission.
7. Submit the recovered flag in the Challenge 5 submission field.
8. Use the recovered SSH details to continue to Challenge 6.

### Solution

Requirements: Wireshark.

Open `last_transmission.pcap` and apply this display filter:

```text
ip.addr == 198.51.100.23
```

Select a packet from the suspicious connection, then choose:

```text
Right-click → Follow → TCP Stream
```

Read the reconstructed HTTP request body. It contains the transfer record, flag, and central-server access details.

TCP stream 3 was the suspicious connection in the tested capture.

### Flag

```text
FLAG{last_transmission_recovered}
```

### Recovered Transmission

```text
ZOBI RESEARCH LAB — TRANSFER RECORD

File reference: cure.txt
Workstation: DR-ALEX-PC
The cure research was transferred. Investigate the central server to recover the remaining evidence.

FLAG{last_transmission_recovered}

ZOBI CENTRAL SERVER ACCESS
Service: SSH
Host: 10.10.20.50
Port: 22
Username: researcher
Password: researcher@2026

Continue your investigation on the central server.
```

### Continuing to Challenge 6

From a terminal with access to the lab network, run:

```bash
ssh researcher@10.10.20.50
```

When prompted, enter the lab password:

```text
researcher@2026
```

Challenge 6 is completed through the central server using SSH.

Member 1 must ensure that the server is reachable from the participant environment and that these credentials match the deployed account.

### Build Requirements

- Python 3
- Scapy
- `create_pcap.py`
- `transmission.txt`

Wireshark is used to inspect the generated capture.

### Build Instructions

From the repository root, run:

```bash
cd challenges/challenge5/build
python3 create_pcap.py
cp last_transmission.pcap ../last_transmission.pcap
```

The script reads `transmission.txt` from its working directory and creates `last_transmission.pcap` in that directory.

The copy command updates the participant capture in the parent challenge folder.

If the flag or SSH details change, update `transmission.txt`, rebuild the capture, and update the corresponding flag configuration and documentation.

### Suggested Hints

1. Use the suspicious IP address found in Challenge 4.
2. Filter the capture to focus on that address.
3. A complete message may be spread across multiple TCP packets.
4. Use Follow TCP Stream to reconstruct the transmission.

### Deployment

- Provide `last_transmission.pcap` as the Challenge 5 download.
- Configure the portal to accept the exact flag listed above.
- Keep `flag.txt`, the build directory, and solution documentation private.
- Ensure the Challenge 4 suspicious destination uses TCP port `80`, matching this capture.
- Ensure the central server is reachable at `10.10.20.50` on SSH port `22`.
- Ensure the deployed SSH account matches the credentials inside the capture.

### Reset

No live network service is required for the packet-analysis challenge.

Participants can download a fresh copy of the capture. Organisers can restore the tested file or regenerate it using the build script.

Any Challenge 6 server reset is managed separately by the central-server administrator.

### Verification Status

- Capture successfully generated with 74 packets.
- Capture opened successfully in Wireshark.
- Suspicious-IP filter tested.
- Relevant TCP stream reconstructed successfully.
- Flag and SSH details confirmed in the reconstructed message.
- Capture, flag file, generator, and transmission text pushed to the Member 2 branch.
- Final portal download and flag submission still require integration testing.
- Live SSH connectivity and login still require testing in the final lab environment.

### Difficulty

The current implementation is a basic packet-analysis challenge using IP filtering and TCP-stream reconstruction.
