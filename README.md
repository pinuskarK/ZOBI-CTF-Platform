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

# Member 3 (IT24101628) : Challenges 2, 4, 6
The member 3's readme will discuss on how challenges 2, 4, 6 work, how participants solve them, and how organisers prepare and deploy the challenge files.

# Challenge 2 --- The Lab Assistant's Message: Cryptography
## Objective
Decode the message left by the lab assistant, recover the Challenge 2 flag, and discover the ZOBI research portal website url that connects to the challenge 3.

## How It Works
The file lab_assistant_msg.txt contains a message encrypted with a Caesar cipher using a shift of 3. Participants must identify the cipher and reverse the shift to read the original message.
The decoded message directs the player to the web portal and tells its login page may be vulnerable. This provides a narrative clue for the challenge 3.

**File Provided:** lab_assistant_msg.txt (Contains an encrypted message including the the clue and the flag)

**Participant Workflow**
1. Download lab_assistant_msg.txt in challenge 2.
2. Inspect the file and identify that it may have used cryptography and use Caesar cipher.
3. Try reversing a Caesar shift of 3.
4. Read the decoded message and identify the flag.
5. Submit the exact flag in the Challenge 2 submission field.
6. Follow the clue about the web portal to continue the investigation.

**Hints provided:**
- Hint 1: “Lab assistant used a very simple and a common substitution”
- Hint 2: "Think about an ancient Roman ruler."
- Hint 3: "Try a Caesar cipher decoder." 

**Solution:**\
The message uses a Caesar cipher with a shift of 3. The file can be decoded manually or with a Caesar cipher tool on the internet. 

**Flag:**\
flag{caesar_cipher_master}
Player must use the exact capitalization and spelling configured in the central flag validator. 

**Build Instructions:**\
No server is required for this challenge as this is a file based challenge.

**Deployment:**
- Provide only lab_assistant_msg.txt as the Challenge 2 download.
- Configure the portal to accept the exact Challenge 2 flag.
- Ensure the decoded clue correctly points participants toward the intended next stage.
- Do not include plaintext solution files or organiser-only flag files in the participant download.

**Reset:**\
No server side state needs resetting since this is only a file based challenge. Participants can download a fresh copy of lab_assistant_msg.txt

**Verification Status:**
- Confirm that the final message decodes correctly using a Caesar shift of 3.
- Confirm that the decoded flag matches the portal configuration.
- Confirm that the decoded clue is consistent with the integrated challenge sequence.
- Final portal download and flag submission require integration testing.

**Difficulty:**\
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

**Note:**\
Each file records a different part of the incident. Participants must understand what happened by reading all the files leading into the digital forensics.
The evidence shows unusual access to research files, a USB device connected during the same period, access to cure.txt, and an outbound transfer to the suspicious destination 198.51.100.23.

**Participant Workflow:**
1. Download and extract alex_recovered_files.zip.
2. Read deleted_message.txt to understand the incident and note the suspicious IP address.
3. Examine system.log and access.log to identify unusual activity and the relevant timestamps.
4. Inspect usb_history.txt to identify the connected device and the research files read during its session.
5. Examine network.log and find the outbound connection to the suspicious IP address mentioned in deleted_message.txt.
6. Correlate the file access times with the outbound transfer and inspect the connection entry in network.log to find the flag.
7. Submit the flag in challenge 4.

**Flag:**\
flag{forensic_trail_investigate}
The flag is included in line 18 of the network.log connection-closed entry. It was done to ensure that the player has read and checked the destination ip in the network.log

**Hints Provided:**
- Hint 1: "These files show unusual activities around the time the research disappeared. Read all files to understand what happened."
- Hint 2: "The doctor’s message gives a very important detail to further discover what happened."
- Hint 3: "Try checking the network activity of the destination mentioned in the recovered message."

**Deployment:**
- Provide alex_recovered_files.zip as the Challenge 4 download.
- Configure the portal to accept the exact Challenge 4 flag.
- Ensure that the Challenge 5 packet capture uses the same suspicious destination IP and compatible incident details.
- Preserve the archive and evidence files exactly as tested after uploading them.

**Reset:**\
No live service or server side challenge reset is required. Participants can download a fresh copy of the archive.

**Verification Status:**
- Confirm that the archive contains all five evidence files.
- Confirm that the timestamps and file names are consistent across the logs.
- Confirm that the workstation and suspicious destination IP addresses match the intended storyline.
- Confirm that the flag is present in network.log and matches the portal configuration.
- Final portal download and flag submission require integration testing.
  
**Difficulty:**\
This is a medium difficulty digital forensics challenge because participants must compare multiple evidence sources, identify relevant events in timestamped logs, and reconstruct a likely sequence of activity.

# Challenge 6 --- The CURE Research Server: Linux/System Security

## Objective
Using the information received by challenge 5, investigate the Linux server's permissions, identify a weakness in the backup script, demonstrate privilege escalation through PATH hijacking, and retrieve the final flag from `/root/cure.txt` to complete the investigation.This challenge demonstrates how insecure script execution and incorrect privilege configurations can allow a restricted user to gain elevated privileges on a Linux system.

## How It Works
- Challenge 6 is the hardest and the last challenge which uses advanced Linux and system security hosted on a KVM/QEMU virtual machine. The VM is connected to an isolated network which uses the guest IP address `10.10.20.50`. (this ip was obtained by challenge 5 .pcap file).
- Participants begin with the restricted `researcher` account where the username and password were obtained from Challenge 5, and participants connect to the target through SSH using the ZOBI central server.
- The main investigation target is the backup script located at `/opt/zobi-c6/backup.sh`. The script calls the `tar` utility by its command name instead of specifying its absolute path. This creates a potential path hijacking  vulnerability when the script is executed with elevated privileges and the environment allows the modified PATH to take effect.
- Participants need to create a replacement script named `tar` in the `/tmp` directory. The script records the current user identity and attempts to read the protected flag file. They then make the replacement script executable and execute the backup script with a modified PATH that places `/tmp` first.
-- When the backup script calls `tar`, the system executes the replacement script instead of the actual one. Because the backup script runs with root privileges, the replacement script can now also execute with root privileges. 
- Participants needs to verify the result by examining the output file, which contains the root identity and the final flag.

**Participant Workflow:**
1. Obtain the SSH username and password from Challenge 5.
2. Connect to the ZOBI central server and access the target VM using SSH.
3. Investigate the current user's permissions and identify commands that can be executed with elevated privileges.
4. Use sudo -l to examine the available sudo permissions and identify the backup script as the investigation target.
5. Examine the backup script and identify that it calls `tar` without specifying its absolute path.
6. Create a replacement script named `tar` in `/tmp` that records the current user identity and attempts to read the protected flag.
7. Make the replacement script executable using `chmod +x`.
8. Execute the backup script with a modified PATH that places `/tmp` before the standard utility directories.
9. Examine the generated proof file to verify root-level execution and retrieve the flag.

**Hints Provided:**
- Hint 1: Logging into the server does not mean you have full privileges.\
- Hint 2: Find out what your current user is allowed to execute with elevated privileges.\
- Hint 3: Investigate sudo -l and examine anything that can be executed as root.\

**Flag:** ZOBI{c6_path_hijack_root_access_8f2d6a}\

**Build Instructions:**
- Create the target VM using KVM/QEMU and name it zobi-c6-cure.
- Configure the guest IP address as `10.10.20.50`.
- Connect the VM to the isolated `zobi_c6_isolated` network.
- Create the restricted `researcher` account and configure SSH access.
- Store the backup script at `/opt/zobi-c6/backup.sh`.
- Configure the intended sudo permissions and script execution conditions so that the path hijacking vulnerability can be demonstrated.
- Create the protected flag file at `/root/cure.txt`.
- Ensure the backup script invokes `tar` by command name and that the modified PATH is honored during privileged execution.
- Prepare the CTFd challenge with the correct flag, description, connection details, and three progressive hints.
- Test the complete solution using the participant account before deploying the challenge.

**Deployment:**
- Start the zobi-c6-cure VM and verify that it is connected to the isolated network.
- Confirm that the guest is reachable at `10.10.20.50` through the ZOBI central server.
- Verify that the `researcher` account can connect using SSH with the intended credentials from Challenge 5.
- Confirm that the backup script and sudo permissions support the intended exploitation path.
- Configure CTFd to accept the exact Challenge 6 flag.
- Provide the connection details and hints to participants without exposing the solution or protected flag in the challenge description.
- Ensure that the VM remains isolated from unrelated systems and services.

**Reset:**
- After a participant finishes or modifies the environment, restore the VM to its clean snapshot. This resets any temporary replacement scripts, proof files, account changes, and other modifications made during exploitation.
- Before making the challenge available again, verify that the backup script, sudo permissions, SSH access, and flag file are restored to their intended states.

**Verification Status:**
- Confirm that the VM starts correctly and uses the intended isolated network.
- Confirm that SSH access works with the `researcher` account and the credentials supplied by Challenge 5.
- Confirm that the intended sudo permissions are configured correctly.
- Confirm that the backup script calls `tar` by command name and permits the intended path hijacking demonstration.
- Confirm that the replacement script can execute with root privileges under the intended conditions.
- Confirm that the proof file records `uid=0(root)` and contains the correct flag.
- Confirm that `/root/cure.txt` contains the configured final flag.
- Confirm that CTFd accepts the exact flag and marks the challenge as completed.
- Confirm that restoring the VM snapshot returns the challenge to its original state.

**Difficulty:**\
This is a hard challenge involving Linux and system security challenge as participants must understand restricted user permissions, investigate sudo privileges, identify a path hijacking vulnerability, and demonstrate privilege escalation to retrieve a protected file. It requires participants to combine Linux command line knowledge with an understanding of how privileged scripts execute other programs.
