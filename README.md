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
The challenges use a participant platform for downloads, instructions, and flag submission, alongside isolated challenge services and the ZOBI central server.
- CTFd participant platform, as stated in the current Challenge 3 description and Member 3 documentation
- Isolated web challenge service for the Research Portal
- File-based challenges for steganography and packet analysis
- Central server accessed through SSH for Challenge 6
- Network isolation and controlled access

The group previously developed a custom ZOBI portal. Member 1 should confirm the final participant platform and update this architecture section to match the deployed setup.

# Member 2: Challenges 1, 3, 5

This README explains how Challenges 1, 3, and 5 work, how participants solve them, and how organisers prepare and deploy them. Challenge 3 belongs to Member 2's assigned scope, while another group member implemented its service.

This is organiser documentation containing solutions, flags, and lab credentials. Keep it private and provide participants only with the intended challenge resources.

# Challenge 1 --- Hidden Message in a Photograph: Steganography

## Objective
Extract a hidden message from a suspicious photograph, recover the Challenge 1 flag, and discover the clue leading to the lab assistant's message in Challenge 2.

## How It Works
Steghide embeds a text file inside a JPEG photograph using an empty passphrase. The resulting image looks like an ordinary photograph but contains a flag and a reference to `lab_assistant_msg.txt`.

File Provided: `mystery_photo.jpg` (contains the embedded message, flag, and next-stage clue).

## Participant Workflow
1. Download `mystery_photo.jpg` from Challenge 1.
2. Inspect the image and consider whether it contains hidden information.
3. Use Steghide to extract the embedded message with an empty passphrase.
4. Read the extracted text and identify the flag.
5. Submit the exact flag in the Challenge 1 submission field.
6. Follow the reference to `lab_assistant_msg.txt` to continue to Challenge 2.

## Hints
- Hint 1: "There's more to it than meets the eye."
- Hint 2: "Information can be hidden inside an ordinary image."
- Hint 3: "Try Steghide with an empty passphrase."

## Solution
From the directory containing the downloaded image, run:

```bash
steghide extract -sf mystery_photo.jpg -xf recovered_note.txt -p ""
cat recovered_note.txt
```

The extracted message contains the flag and directs participants to investigate `lab_assistant_msg.txt`. Participants can use their own Steghide installation; no server-side extraction tool is required.

## Flag
```text
FLAG{photograph_secret_recovered}
```

Use the exact capitalization and spelling configured in the central flag validator.

## Build Instructions
Requirements: Steghide, `original_photo.jpg`, and `hidden_message.txt`.

The hidden message is:

```text
ZOBI RESEARCH LAB — RECOVERED NOTE

FLAG{photograph_secret_recovered}

The lab assistant left another message.
Find lab_assistant_msg.txt and investigate its contents.
```

Run from the directory containing the build inputs:

```bash
steghide embed -cf original_photo.jpg -ef hidden_message.txt -sf mystery_photo.jpg -p ""
```

Test extraction:

```bash
steghide extract -sf mystery_photo.jpg -xf test_extracted.txt -p ""
cat test_extracted.txt
```

The repository contains `challenges/challenge1/mystery_photo.jpg` and `flag.txt`. The original image and hidden-message build inputs were kept locally and should be supplied privately if the organiser needs to rebuild the image.

## Deployment
- Provide only `mystery_photo.jpg` as the Challenge 1 download.
- Configure the portal to accept the exact Challenge 1 flag.
- Preserve the JPEG bytes; do not recompress or convert the image after embedding.
- Ensure the extracted clue matches the Challenge 2 filename.
- Keep original build inputs, extracted solution files, and `flag.txt` out of participant downloads.

## Reset
No server-side state needs resetting because this is a file-based challenge. Participants can download a fresh copy of the image. Organisers can restore the tested image or rebuild it from the original inputs.

## Verification Status
- Embedding and local extraction were completed successfully.
- The extracted flag and next-stage clue were checked.
- The challenge image and flag file were pushed to the Member 2 branch.
- Final portal download and correct/incorrect flag validation require integration testing.

## Difficulty
This is an easy steganography challenge because participants need to identify an appropriate extraction tool and recover a message using an empty passphrase.

# Challenge 3 --- The Abandoned Lab: Web Security

## Objective
Investigate the Research Portal login form, identify its SQL injection vulnerability, access the relevant research evidence, and recover the Challenge 3 flag.

## How It Works
Participants access the Research Portal through a web browser at:

```text
http://192.168.8.188:5003
```

The challenge demonstrates insecure handling of login input in a database query. Participants investigate how the application processes input and use the intended SQL injection path to access research evidence containing the flag.

The main lesson is that SQL injection can occur when an application handles user input insecurely. Parameterized queries separate input values from SQL instructions and prevent this form of injection.

Resource Provided: A browser-accessible Research Portal login page.

## Participant Workflow
1. Decode the Challenge 2 message and follow its Research Portal clue.
2. Open `http://192.168.8.188:5003` from the participant lab environment.
3. Inspect the login form and observe its responses to input.
4. Identify the SQL injection vulnerability and follow the intended challenge path.
5. Access the relevant research evidence and recover the flag.
6. Submit the exact flag through the Challenge 3 field on CTFd, or the final participant platform selected by the group.
7. Follow any next-stage clue provided by the deployed research evidence.

## Hints
Suggested hints to confirm against the implemented service:
- Hint 1: "Investigate how the Research Portal handles login input."
- Hint 2: "The login form may trust input that changes a database query."
- Hint 3: "Consider SQL injection and how it affects authentication."

## Solution
The intended solution is to exploit the deliberately vulnerable login input, access the protected research evidence, and read the flag.

**Exact tested solution pending:** The supplied description does not specify the working injection input, which login field accepts it, or the exact evidence page. Obtain these details from the implementing member and document the verified steps here before the final submission. Do not treat an untested example payload as the confirmed solution.

## Flag
**To be confirmed by the implementing member:** Insert the exact Challenge 3 flag from the deployed service and central flag validator. Preserve its capitalization and spelling.

## Build Instructions
The Research Portal has been implemented by another group member. Use that member's actual source files and deployment configuration.

Before final submission, add the following verified details:
- Source directory and required dependencies
- Exact build and start commands
- Database initialization and flag placement
- Port mapping and the participant-accessible URL

The current description does not establish the framework, database engine, or container commands, so those details are not assumed here.

## Deployment
- Make the Research Portal reachable at `http://192.168.8.188:5003` from the participant lab network.
- Ensure the decoded Challenge 2 URL matches the deployed address.
- Configure the participant platform to accept the exact Challenge 3 flag.
- Verify that the intended SQL injection path exposes the correct evidence and flag.
- Keep the deliberately vulnerable service isolated from unrelated systems.
- Keep organiser source, database credentials, and solution documentation out of participant downloads.
- Confirm any evidence or download linking Challenge 3 to Challenge 4 against the final deployed service.

## Reset
Use the implementing member's verified reset procedure to restore the initial application and database state. Document the exact reset command and confirm that it preserves the intended flag and vulnerable login behaviour.

## Verification Status
The supplied description reports that the Research Portal was created. The following checks remain unverified in this README:
- Confirm that the URL is reachable from the participant environment.
- Confirm the exact working SQL injection input and evidence location.
- Confirm that the recovered flag matches the participant platform configuration.
- Confirm that a correct flag is accepted and an incorrect flag is rejected.
- Confirm that the challenge remains isolated from unrelated systems.
- Confirm that the reset procedure restores a working challenge.

## Difficulty
Provisional difficulty: easy to medium. The final rating depends on the tested injection path, available hints, and the steps required to locate the research evidence.

# Challenge 5 --- Last Transmission: Networking

## Objective
Analyse a packet capture using the suspicious IP address discovered in Challenge 4, reconstruct the relevant transmission, recover the Challenge 5 flag, and discover SSH access details for Challenge 6.

## How It Works
A Python script uses Scapy to generate a synthetic packet capture containing background HTTP traffic and a suspicious transfer from Dr Alex's workstation to `198.51.100.23` on TCP port `80`.

The suspicious HTTP request references `cure.txt` and contains the flag and central-server access details. Its contents are split across TCP packets, allowing participants to reconstruct the message using Wireshark's Follow TCP Stream feature.

File Provided: `last_transmission.pcap`.

This is a locally generated investigation artifact. The generator does not send traffic to the listed addresses.

## Connection to Challenge 4
- Workstation: DR-ALEX-PC
- Workstation IP: `192.168.10.25`
- Suspicious destination: `198.51.100.23`
- Destination port: TCP `80`
- File reference: `cure.txt`
- Event date: `2026-09-18`
- Connection start: `09:48:51`
- Transfer start: `09:49:12`
- Connection close: `09:49:18`
- Timestamp timezone: UTC+05:30

The capture represents the transfer portion of the incident rather than every event in the Challenge 4 logs. Wireshark may display different clock times depending on the viewer's timezone settings.

## Participant Workflow
1. Obtain the suspicious destination IP from Challenge 4.
2. Download and open `last_transmission.pcap` in Wireshark.
3. Filter traffic involving `198.51.100.23`.
4. Select a packet from the suspicious connection.
5. Use Follow TCP Stream to reconstruct the transmission.
6. Read the transfer record and recover the flag.
7. Submit the exact flag in the Challenge 5 submission field.
8. Use the recovered SSH details to continue the investigation on the central server.

## Hints
- Hint 1: "Use the suspicious IP address discovered in Challenge 4."
- Hint 2: "A message may be spread across multiple TCP packets."
- Hint 3: "Follow the relevant TCP stream to reconstruct the transmission."

## Solution
Open the capture in Wireshark and apply this display filter:

```text
ip.addr == 198.51.100.23
```

Select a packet from that connection and choose **Right-click → Follow → TCP Stream**. Read the reconstructed HTTP request body to find the flag and SSH details. TCP stream 3 was the suspicious stream in the tested capture.

## Flag
```text
FLAG{last_transmission_recovered}
```

Use the exact capitalization and spelling configured in the central flag validator.

## Recovered Central-Server Details
- Service: SSH
- Host: `10.10.20.50`
- Port: `22`
- Username: `researcher`
- Password: `researcher@2026`

From a terminal connected to the lab network, participants can continue with:

```bash
ssh researcher@10.10.20.50
```

Enter the recovered password when prompted. Challenge 6 is completed through SSH on the central server rather than through the website.

## Build Instructions
Requirements: Python 3 and Scapy. Wireshark is used for verification.

Repository files:
- `challenges/challenge5/last_transmission.pcap`
- `challenges/challenge5/flag.txt`
- `challenges/challenge5/build/create_pcap.py`
- `challenges/challenge5/build/transmission.txt`

From the repository root, run:

```bash
cd challenges/challenge5/build
python3 create_pcap.py
cp last_transmission.pcap ../last_transmission.pcap
```

The script reads `transmission.txt` and writes the capture in its working directory. The copy command updates the participant file in the parent directory.

If the flag or SSH details change, update `transmission.txt`, regenerate the capture, and update the corresponding platform configuration and documentation.

## Deployment
- Provide only `last_transmission.pcap` as the Challenge 5 download.
- Configure the portal to accept the exact Challenge 5 flag.
- Ensure the Challenge 4 suspicious connection uses the same destination IP and TCP port `80` as this capture.
- Preserve the tested capture during upload and download.
- Keep `flag.txt`, build files, and solution documentation private.
- Ensure the central server is reachable at `10.10.20.50:22` and its account matches the credentials embedded in the capture.

## Reset
No live network service or server-side reset is required for packet analysis. Participants can download a fresh capture. Organisers can restore the tested file or regenerate it using the build script.

Resetting Challenge 6 is a separate responsibility of the central-server administrator.

## Verification Status
- The capture was generated successfully with 74 packets.
- The capture opened successfully in Wireshark.
- Suspicious-IP filtering and TCP-stream reconstruction were tested.
- The reconstructed flag and SSH details were checked.
- The capture, flag file, generator, and transmission text were pushed to the Member 2 branch.
- Final portal download and correct/incorrect flag validation require integration testing.
- Live SSH reachability and login require testing in the final lab environment.

## Difficulty
This is an easy networking challenge because participants use a known suspicious IP address and reconstruct plaintext traffic using Follow TCP Stream.
