#!/usr/bin/env python3
"""Check that the expected integration artefacts exist in this checkout.

This is a repository-integrity check only. It does not prove that live
services, flags, challenge solutions, CTFd progression, or reset procedures work.
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]

REQUIRED = {
    "C1 participant photograph": "challenges/C1-steganography/mystery_photo.jpg",
    "C2 encoded message": "challenges/C2-cryptography/lab_assistant_msg.txt",
    "C3 Flask app": "challenges/C3-web-security/app.py",
    "C3 database initializer": "challenges/C3-web-security/init_db.py",
    "C3 Dockerfile": "challenges/C3-web-security/Dockerfile",
    "C3 Compose file": "challenges/C3-web-security/compose.yaml",
    "C3 Python requirements": "challenges/C3-web-security/requirements.txt",
    "C3 environment template": "challenges/C3-web-security/.env.example",
    "C3 unit tests": "challenges/C3-web-security/tests/test_app.py",
    "C4 access log": "challenges/C4-digital-forensics/access.log",
    "C4 deleted message": "challenges/C4-digital-forensics/deleted_message.txt",
    "C4 network log": "challenges/C4-digital-forensics/network.log",
    "C4 system log": "challenges/C4-digital-forensics/system.log",
    "C4 USB history": "challenges/C4-digital-forensics/usb_history.txt",
    "C5 participant PCAP": "challenges/C5-networking/last_transmission.pcap",
    "C5 PCAP generator": "challenges/C5-networking/build/create_pcap.py",
    "C5 organiser transmission source": "challenges/C5-networking/build/transmission.txt",
    "C5 organiser expected flag": "challenges/C5-networking/flag.txt",
    "C5 stage README": "challenges/C5-networking/README.md",
    "C5 PCAP validator": "scripts/testing/validate_c5_pcap.py",
    "C5 integration status": "docs/member4/C5-INTEGRATION-STATUS.md",
    "Combined repository check runner": "scripts/testing/run_repository_checks.sh",
    "C6 integration notes": "challenges/C6-linux-security/README.md",
    "C6 backup challenge script": "challenges/C6-linux-security/backup.sh",
    "C6 sudoers example": "challenges/C6-linux-security/researcher-sudoers.example",
    "C6 setup validator": "challenges/C6-linux-security/validate_setup.sh",
    "Member 4 integration plan": "docs/member4/INTEGRATION_TEST_PLAN.md",
    "Member 4 results register": "docs/member4/TEST_RESULTS.md",
    "Member 4 recovery runbook": "docs/member4/RESET-RECOVERY.md",
    "Member 4 risk register": "docs/member4/RISK-REGISTER.md",
    "Member 4 design comparison": "docs/member4/DESIGN-CHANGES.md",
    "Member 4 stage integration guide": "docs/member4/STAGE-INTEGRATION-GUIDE.md",
}

def main() -> int:
    failures = 0
    for label, relative in REQUIRED.items():
        path = ROOT / relative
        if path.is_file() and path.stat().st_size > 0:
            print(f"[PASS] {label}: {relative} ({path.stat().st_size} bytes)")
        else:
            print(f"[FAIL] {label}: missing or empty — {relative}")
            failures += 1

    print()
    print(f"Checked {len(REQUIRED)} required files; failures: {failures}.")
    print("This checks repository files only, not live challenge acceptance.")
    return 1 if failures else 0

if __name__ == "__main__":
    sys.exit(main())
