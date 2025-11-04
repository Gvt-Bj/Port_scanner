#!/usr/bin/env python3
"""
port_scanner.py
Simple TCP connect port scanner By Garvit Bajaj :)
Usage examples:
    python3 port_scanner.py example.com           # scans common ports
    python3 port_scanner.py 192.168.56.101 1 1024 # scans ports 1-1024
"""

import socket
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

# a small list of common ports (used if user doesn't provide range)
COMMON_PORTS = [
    21, 22, 23, 25, 53, 80, 110, 111, 123, 139, 143, 161, 162, 389,
    443, 445, 587, 636, 993, 995, 1723, 3306, 3389, 5900, 8080
]

def scan_port(host: str, port: int, timeout: float) -> tuple:
    """Try to connect to (host,port). Return (port, is_open)."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        result = s.connect_ex((host, port))
        s.close()
        return (port, result == 0)
    except Exception:
        # any error -> treat as closed/filtered
        try:
            s.close()
        except Exception:
            pass
        return (port, False)

def resolve_host(target: str) -> str:
    """Resolve hostname to IPv4 address (raises on failure)."""
    return socket.gethostbyname(target)

def main():
    parser = argparse.ArgumentParser(description="Minimal TCP port scanner (connect scan).")
    parser.add_argument("target", help="IP or hostname to scan")
    parser.add_argument("start", nargs="?", type=int, help="start port (inclusive)", default=None)
    parser.add_argument("end", nargs="?", type=int, help="end port (inclusive)", default=None)
    parser.add_argument("-t", "--timeout", type=float, default=0.8, help="socket timeout in seconds")
    parser.add_argument("-w", "--workers", type=int, default=100, help="concurrent worker threads")
    args = parser.parse_args()

    # determine ports to scan
    if args.start is None or args.end is None:
        ports = COMMON_PORTS
    else:
        if args.start < 1 or args.end > 65535 or args.start > args.end:
            print("Invalid port range. Use 1-65535 and start <= end.")
            return
        ports = list(range(args.start, args.end + 1))

    try:
        ip = resolve_host(args.target)
    except socket.gaierror:
        print(f"Could not resolve '{args.target}'")
        return

    print(f"Scanning {args.target} ({ip})")
    print(f"Ports: {ports[0]}{'-' + str(ports[-1]) if len(ports) > 1 else ''}  Timeout: {args.timeout}s")
    start_time = datetime.now()

    open_ports = []
    # thread pool for concurrency
    with ThreadPoolExecutor(max_workers=args.workers) as exe:
        futures = { exe.submit(scan_port, ip, p, args.timeout): p for p in ports }
        for fut in as_completed(futures):
            p = futures[fut]
            try:
                port, is_open = fut.result()
            except Exception:
                continue
            if is_open:
                print(f"[+] Port {port:5d} OPEN")
                open_ports.append(port)
            else:
                # minimal output for closed ports — comment out next line if you want quieter run
                pass

    elapsed = (datetime.now() - start_time).total_seconds()
    print(f"\nScan completed in {elapsed:.2f}s")
    if open_ports:
        print("Open ports: " + ", ".join(str(p) for p in sorted(open_ports)))
    else:
        print("No open ports found (within scanned range).")

if __name__ == "__main__":
    main()
