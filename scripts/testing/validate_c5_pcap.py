#!/usr/bin/env python3
"""Validate the C5 PCAP's basic structure and required clue markers.

Requires Scapy: python3 -m pip install scapy
This checks the organiser's PCAP artefact only; it does not prove CTFd scoring
or that the C5-to-C6 participant handoff works in the live deployment.
"""
from pathlib import Path
import sys

try:
    from scapy.all import IP, Raw, rdpcap
except ImportError:
    print("ERROR: Scapy is required. Install it in a disposable test environment.")
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[2]
pcap_path = ROOT / "challenges/C5-networking/last_transmission.pcap"
if not pcap_path.is_file():
    print(f"FAIL: missing PCAP: {pcap_path}")
    sys.exit(1)

packets = rdpcap(str(pcap_path))
payloads = []
destinations = set()
for packet in packets:
    if IP in packet:
        destinations.add(packet[IP].dst)
    if Raw in packet:
        payloads.append(bytes(packet[Raw].load))
joined = b"\n".join(payloads)
required_markers = {
    "suspicious destination": b"198.51.100.23",
    "file reference": b"cure.txt",
    "C5 flag marker": b"FLAG{last_transmission_recovered}",
    "C6 guest address": b"10.10.20.50",
    "C6 username": b"researcher",
}
failures = []
print(f"PCAP: {pcap_path.name}; packets: {len(packets)}; bytes: {pcap_path.stat().st_size}")
if len(packets) != 74:
    failures.append(f"expected 74 packets from the recorded build, found {len(packets)}")
for label, marker in required_markers.items():
    if marker in joined:
        print(f"[PASS] {label} marker present")
    else:
        print(f"[FAIL] {label} marker missing")
        failures.append(label)
if "198.51.100.23" not in destinations:
    failures.append("suspicious destination is not present as an IP destination")
if failures:
    print("PCAP validation failed: " + "; ".join(failures))
    sys.exit(1)
print("PASS: basic PCAP structure and intended clue markers are present.")
print("Next: solve manually in Wireshark and verify the CTFd submission and C6 handoff.")
