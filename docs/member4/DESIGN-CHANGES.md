# ZOBI CTF — Design Changes and Deployment Deviations

**Owner:** Member 4 — Integration, Testing & Documentation  
**Baseline:** Approved Assignment 01 architecture/report  
**Status:** Initial comparison notes; confirm every item against the approved report and live configuration before final submission.

## Comparison table

| Area | Baseline / expectation | Current implementation notes | Reason / impact | Verification status |
|---|---|---|---|---|
| Challenge delivery | Six ordered stages: C1 steganography, C2 cryptography, C3 web security, C4 digital forensics, C5 network analysis, C6 Linux/system security | CTFd is hosted on the central server; challenge files/services are configured separately | Centralises participant access while keeping challenge types distinct | Partial — confirm all six are visible and ordered |
| CTFd network port | Participant portal exposed through selected host port | Lab URL has been used on port 8081 | Avoids conflict with existing host services | Verify listener and firewall |
| C3 implementation | Isolated web-security challenge | Flask challenge deployed as Docker service on host port 5003 | Supports repeatable delivery of intentionally vulnerable login challenge | Local health/SQLi test recorded; participant and isolation tests pending |
| C6 virtual machine | Report baseline specifies Ubuntu 20.04, 4 GB RAM, 30 GB disk, isolated 10.10.20.0/24 network | Lab notes record Ubuntu Server 26.04.1, 1.5 GB RAM, 12 GB disk, static guest IP 10.10.20.50, isolated libvirt network | Running VM differs from report baseline; update final report or rebuild to approved specification | Verify live configuration and obtain team approval |
| C6 access path | C5 should provide connection details for C6 | Host-to-guest SSH was tested; Windows client needs a jump host to reach isolated guest | Preserves guest isolation but participant instructions must be clear | C5-to-C6 participant path not yet verified |
| Final completion page | Final flag submission should indicate CTF completion | Custom completion/results page proposed; not confirmed implemented | Makes narrative ending clear and may show score/status | Pending implementation and acceptance test |
| Reset/recovery | Stages should be recoverable to known baseline | No verified full-box reset execution recorded here | Avoids claiming recovery capabilities that may not exist | Pending |

## Finalisation steps

1. Compare this table with exact Assignment 01 requirements.
2. Verify implementation details on the live host.
3. Record the reason and evidence for each accepted deviation.
4. Obtain team approval for deviations affecting isolation, usability, or assignment compliance.
5. Update the final report to match the final tested deployment.
