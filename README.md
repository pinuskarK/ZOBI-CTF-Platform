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

# Member 3: Challenges 2, 4, 6
The member 3's readme will discuss on how challenges 2, 4, 6 work, how participants solve them, and how organisers prepare and deploy the challenge files.

# Challenge 2 --- The Lab Assistant's Message: Cryptography
## Objective
Decode the message left by the lab assistant, recover the Challenge 2 flag, and discover the ZOBI research portal website url that connects to the challenge 3.

## How It Works
The file lab_assistant_msg.txt contains a message encrypted with a Caesar cipher using a shift of 3. Participants must identify the cipher and reverse the shift to read the original message.
The decoded message directs the player to the web portal and tells its login page may be vulnerable. This provides a narrative clue for the challenge 3.

File Provided: lab_assistant_msg.txt (Contains an encrypted message including the the clue and the flag)

Participant Workflow
1. Download lab_assistant_msg.txt in challenge 2.
2. Inspect the file and identify that it may have used cryptography and use Caesar cipher.
3. Try reversing a Caesar shift of 3.
4. Read the decoded message and identify the flag.
5. Submit the exact flag in the Challenge 2 submission field.
6. Follow the clue about the web portal to continue the investigation.

Hints provided for the user:\
- Hint 1: “Lab assistant used a very simple and a common substitution”
- Hint 2: "Think about an ancient Roman ruler."
- Hint 3: "Try a Caesar cipher decoder." 

Solution:\
The message uses a Caesar cipher with a shift of 3. The file can be decoded manually or with a Caesar cipher tool on the internet. 

Flag:\
flag{caesar_cipher_master}
Player must use the exact capitalization and spelling configured in the central flag validator. 

Build Instructions:\
No server is required for this challenge as this is a file based challenge.

Deployment:
- Provide only lab_assistant_msg.txt as the Challenge 2 download.
- Configure the portal to accept the exact Challenge 2 flag.
- Ensure the decoded clue correctly points participants toward the intended next stage.
- Do not include plaintext solution files or organiser-only flag files in the participant download.

Reset:\
No server side state needs resetting since this is only a file based challenge. Participants can download a fresh copy of lab_assistant_msg.txt

Verification Status:
- Confirm that the final message decodes correctly using a Caesar shift of 3.
- Confirm that the decoded flag matches the portal configuration.
- Confirm that the decoded clue is consistent with the integrated challenge sequence.
- Final portal download and flag submission require integration testing.

Difficulty:\
This is an easy cryptography challenge because participants only need to understand its encrypted, understand its Caesar Cipher and need to shift 3 times to get the plaintext.

# Challenge 4 --- What Happened Here?: Digital Forensics
## Objective
Examine recovered workstation records such as system logs, USB history, access logs, and network activity to reconstruct suspicious events involving Dr. Alex's research and recover the flag.

## How It Works
The challenge provides a folder named alex_recovered_files including five files recovered from Dr. Alex's computer:
- deleted_message.txt : a message left by Dr Alex
- system.log : recorded events and suspicious file access
- usb_history.txt : records usb devices and the file operations
- access.log : records user activities and file access
- network.log : records the connections, suspicious outbound transfer and the challenge flag

Note:\
Each file records a different part of the incident. Participants must understand what happened by reading all the files leading into the digital forensics.
The evidence shows unusual access to research files, a USB device connected during the same period, access to cure.txt, and an outbound transfer to the suspicious destination 198.51.100.23.

Participant Workflow:
1. Download and extract alex_recovered_files.zip.
2. Read deleted_message.txt to understand the incident and note the suspicious IP address.
3. Examine system.log and access.log to identify unusual activity and the relevant timestamps.
4. Inspect usb_history.txt to identify the connected device and the research files read during its session.
5. Examine network.log and find the outbound connection to the suspicious IP address mentioned in deleted_message.txt.
6. Correlate the file access times with the outbound transfer and inspect the connection entry in network.log to find the flag.
7. Submit the flag in challenge 4.

Flag:\
flag{forensic_trail_investigate}
The flag is included in line 18 of the network.log connection-closed entry. It was done to ensure that the player has read and checked the destination ip in the network.log

Hints:
- Hint 1: "These files show unusual activities around the time the research disappeared. Read all files to understand what happened."
- Hint 2: "The doctor’s message gives a very important detail to further discover what happened."
- Hint 3: "Try checking the network activity of the destination mentioned in the recovered message."

Deployment:
- Provide alex_recovered_files.zip as the Challenge 4 download.
- Configure the portal to accept the exact Challenge 4 flag.
- Ensure that the Challenge 5 packet capture uses the same suspicious destination IP and compatible incident details.
- Preserve the archive and evidence files exactly as tested after uploading them.

Reset:\
No live service or server side challenge reset is required. Participants can download a fresh copy of the archive.

Verification Status:
- Confirm that the archive contains all five evidence files.
- Confirm that the timestamps and file names are consistent across the logs.
- Confirm that the workstation and suspicious destination IP addresses match the intended storyline.
- Confirm that the flag is present in network.log and matches the portal configuration.
- Final portal download and flag submission require integration testing.
  
Difficulty:\
This is a medium difficulty digital forensics challenge because participants must compare multiple evidence sources, identify relevant events in timestamped logs, and reconstruct a likely sequence of activity.
