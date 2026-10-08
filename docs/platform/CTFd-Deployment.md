# CTFd Deployment

## Platform

ZOBI uses CTFd as the participant-facing Capture The Flag platform.

## Server Environment

- Host OS: Ubuntu Server 26.04.1 LTS
- Container Platform: Docker
- Container Orchestration: Docker Compose
- CTFd: Docker-based deployment

## CTFd Services

The CTFd deployment consists of:

- CTFd application
- MariaDB database
- Redis cache
- Nginx
- Permissions initialization container

## Current Development Ports

| Service | Port |
|---|---:|
| CTFd application | 8001 |
| CTFd Nginx | 8081 |

The ports are currently configured this way to avoid conflicts with the existing ZOBI development services.

## CTFd Configuration

### Event

**Name:** ZOBI - Zombie Outbreak Breach Investigation

### Description

ZOBI is a cybersecurity Capture The Flag platform designed to provide practical challenges in steganography, cryptography, web security, digital forensics, networking, and Linux/system security.

### Team Configuration

- Mode: Team Mode
- Team size: 4
- Team creation: Enabled
- Maximum teams: Unlimited
- Team disbanding: Enabled for inactive teams

### Visibility

- Challenge visibility: Private during development
- Account visibility: Public
- Score visibility: Public
- Registration visibility: Public

### Challenge Settings

- View self submissions: Disabled
- Maximum attempts behavior: Timeout
- Timeout duration: 300 seconds
- Public hints: Disabled
- Challenge ratings: Public

## Deployment

CTFd is deployed using Docker Compose.

The CTFd source is maintained separately from this project repository because the complete CTFd source tree does not need to be duplicated inside the ZOBI project repository.

## Development Status

CTFd has been successfully deployed and initialized on the ZOBI Ubuntu Server.

Final production networking, HTTPS integration, challenge integration, isolation, logging, backup, and recovery procedures remain part of the platform implementation.
