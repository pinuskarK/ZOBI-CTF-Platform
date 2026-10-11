from pathlib import Path
from datetime import datetime, timezone, timedelta
from scapy.all import Ether, IP, TCP, Raw, wrpcap

packets = []
lab_timezone = timezone(timedelta(hours=5, minutes=30))

def timestamp(clock):
    return datetime.fromisoformat(
        "2026-09-18T" + clock
    ).replace(tzinfo=lab_timezone).timestamp()

def connection(destination, source_port, start, request, response,
               transfer_start=None, close=None):
    client = "192.168.10.25"
    client_seq = 10000 + source_port
    server_seq = 90000 + source_port
    now = start

    def add(from_client, flags, seq, ack, payload=b""):
        nonlocal now
        src, dst = (
            (client, destination) if from_client
            else (destination, client)
        )
        sport, dport = (
            (source_port, 80) if from_client
            else (80, source_port)
        )
        src_mac, dst_mac = (
            ("02:00:00:00:00:25", "02:00:00:00:00:01")
            if from_client else
            ("02:00:00:00:00:01", "02:00:00:00:00:25")
        )
        packet = (
            Ether(src=src_mac, dst=dst_mac)
            / IP(src=src, dst=dst)
            / TCP(sport=sport, dport=dport, flags=flags,
                  seq=seq, ack=ack)
        )
        if payload:
            packet = packet / Raw(load=payload)
        packet.time = now
        packets.append(packet)
        now += 0.01

    # Establish the TCP connection.
    add(True, "S", client_seq, 0)
    add(False, "SA", server_seq, client_seq + 1)
    client_seq += 1
    server_seq += 1
    add(True, "A", client_seq, server_seq)

    if transfer_start is not None:
        now = transfer_start

    # Split the HTTP request across multiple TCP packets.
    chunks = [request[i:i + 180]
              for i in range(0, len(request), 180)]
    for index, chunk in enumerate(chunks):
        if transfer_start is not None:
            now = transfer_start + index * (
                3.5 / max(1, len(chunks) - 1)
            )
        add(True, "PA", client_seq, server_seq, chunk)
        client_seq += len(chunk)
        add(False, "A", server_seq, client_seq)

    add(False, "PA", server_seq, client_seq, response)
    server_seq += len(response)
    add(True, "A", client_seq, server_seq)

    if close is not None:
        now = close

    # Close the connection cleanly.
    add(True, "FA", client_seq, server_seq)
    client_seq += 1
    add(False, "A", server_seq, client_seq)
    add(False, "FA", server_seq, client_seq)
    server_seq += 1
    add(True, "A", client_seq, server_seq)

def http_response(body):
    return (
        b"HTTP/1.1 200 OK\r\n"
        b"Content-Type: text/plain\r\n"
        + f"Content-Length: {len(body)}\r\n".encode()
        + b"\r\n" + body
    )

# Background traffic gives players other streams to investigate.
for index, resource in enumerate(["status", "sensor", "heartbeat"]):
    request = (
        f"GET /{resource} HTTP/1.1\r\n"
        "Host: 192.168.10.10\r\n\r\n"
    ).encode()
    connection(
        "192.168.10.10",
        41000 + index,
        timestamp("09:47:00") + index * 20,
        request,
        http_response(b"Lab systems operational.\n")
    )

# Simulated outbound transfer to the suspicious address.
message = Path("transmission.txt").read_bytes()
body = (
    b"Filename: cure.txt\n\n"
    + message
    + b"\nResearch transfer padding:\n"
    + b"ARCHIVED-RESEARCH-DATA\n" * 100
)
request = (
    b"POST /upload/cure.txt HTTP/1.1\r\n"
    b"Host: 198.51.100.23\r\n"
    b"Content-Type: text/plain\r\n"
    + f"Content-Length: {len(body)}\r\n".encode()
    + b"\r\n" + body
)

connection(
    "198.51.100.23",
    49215,
    timestamp("09:48:51"),
    request,
    http_response(b"Transfer received.\n"),
    transfer_start=timestamp("09:49:12"),
    close=timestamp("09:49:18")
)

packets.sort(key=lambda packet: float(packet.time))
wrpcap("last_transmission.pcap", packets)
print("Created last_transmission.pcap")
print("Packets:", len(packets))
