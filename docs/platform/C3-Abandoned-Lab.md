# C3 – The Abandoned Lab

## Overview

- **Stage:** 3
- **Category:** Web Security
- **Difficulty:** Moderate
- **Technology:** Flask, SQLite, Docker
- **Host port:** 5003
- **Container:** zobi-c3-web-security
- **Docker network:** zobi_challenges

## Challenge Scenario

A research portal was abandoned after a mysterious incident at the laboratory. Participants must investigate the portal's authentication mechanism, gain access to the protected archive, and retrieve the Stage 3 flag.

The recovered records mention that the remaining evidence was transferred to Dr. Alex's computer in the observation room.

## Deployment

Run these commands from the challenge directory:

```bash
cd ~/ZOBI-CTF-Platform/challenges/C3-web-security
sudo docker compose up -d --build
