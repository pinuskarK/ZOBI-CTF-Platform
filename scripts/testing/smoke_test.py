#!/usr/bin/env python3
"""Non-destructive reachability checks for the ZOBI CTF lab.

Checks HTTP availability only. It does not submit flags, exploit challenges,
authenticate over SSH, or prove challenge progression. Use only in the
authorised project environment.
"""
from __future__ import annotations

import os
import sys
import urllib.error
import urllib.request

checks: list[tuple[str, str]] = [
    ("Flag API", os.getenv("ZOBI_FLAG_API_URL", "http://127.0.0.1:8080").rstrip("/") + "/"),
    ("C3 health", os.getenv("ZOBI_C3_URL", "http://192.168.8.188:5003").rstrip("/") + "/health"),
]
ctfd_url = os.getenv("ZOBI_CTFD_URL")
if ctfd_url:
    checks.append(("CTFd", ctfd_url.rstrip("/") + "/"))

timeout = float(os.getenv("ZOBI_HTTP_TIMEOUT", "4"))
failed = False
for label, url in checks:
    request = urllib.request.Request(url, headers={"User-Agent": "ZOBI-CTF-smoke-test/1.0"}, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            status = response.status
            passed = 200 <= status < 400
            print(f"[{'PASS' if passed else 'FAIL'}] {label}: HTTP {status} — {url}")
            failed = failed or not passed
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        print(f"[FAIL] {label}: {url} — {exc}")
        failed = True
print("\nScope: HTTP reachability only; full integration and flag progression require manual tests.")
sys.exit(1 if failed else 0)
