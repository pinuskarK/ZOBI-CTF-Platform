#!/usr/bin/env python3
"""Verify that completed-stage challenge artefacts exist in this checkout.

This is a repository-integrity check, not proof that the challenges work in CTFd.
C5 is intentionally excluded because the project owner reports it is unfinished.
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]

REQUIRED = {
    "C1 mystery photograph": "challenges/C1-steganography/mystery_photo.jpg",
    "C2 encoded message": "challenges/C2-cryptography/lab_assistant_msg.txt",
    "C3 Flask app": "challenges/C3-web-security/app.py",
    "C3 database initialiser": "challenges/C3-web-security/init_db.py",
    "C3 Dockerfile": "challenges/C3-web-security/Dockerfile",
    "C3 Compose file": "challenges/C3-web-security/compose.yaml",
    "C3 Python requirements": "challenges/C3-web-security/requirements.txt",
    "C4 access log": "challenges/C4-digital-forensics/access.log",
    "C4 deleted message": "challenges/C4-digital-forensics/deleted_message.txt",
    "C4 network log": "challenges/C4-digital-forensics/network.log",
    "C4 system log": "challenges/C4-digital-forensics/system.log",
    "C4 USB history": "challenges/C4-digital-forensics/usb_history.txt",
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
    print("C5 is excluded intentionally because it is not finished.")
    print("This script checks repository files only, not runtime services or CTFd submissions.")
    return 1 if failures else 0

if __name__ == "__main__":
    sys.exit(main())
