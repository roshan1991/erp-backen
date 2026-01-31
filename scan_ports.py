import sys
import os
import socket

def test_port(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    result = sock.connect_ex((host, port))
    sock.close()
    return result == 0

ports = [5432, 5433]
host = "localhost"

print(f"Scanning ports on {host}...")
running_postgres_port = None

for port in ports:
    is_open = test_port(host, port)
    status = "OPEN" if is_open else "CLOSED"
    print(f"Port {port}: {status}")
    if is_open:
        # Simple check, we assume if it's open it's likely our DB if we are lucky
        # In a real scenario we might try to handshake, but open port is good first step
        running_postgres_port = port

if running_postgres_port:
    print(f"Found active service on port {running_postgres_port}")
else:
    print("No active service found on standard Postgres ports.")
