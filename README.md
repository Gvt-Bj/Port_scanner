# Port_scanner

A tiny, human-readable TCP connect port scanner written in Python. It behaves like a minimal `nmap` for basic port discovery — easy to read, modify, and use in lab environments.

> **Warning / Ethics**
> Only scan hosts you own or have **explicit permission** to test. Running port scans against networks you don't control can be illegal and disruptive.

---

## Features

* Simple, minimal and easy-to-read source code.
* Uses TCP connect (`socket.connect_ex`) — no raw sockets required (no root needed).
* Scans either a short list of common ports or a user-specified port range.
* Concurrent scanning using a thread pool for speed.
* Configurable timeout and worker threads.

## Requirements

* Python 3.7+
* Standard library only (no external packages required)

## Files

* `mini_scanner.py` — the scanner script.

## Usage

Make the script executable (optional):

```bash
chmod +x mini_scanner.py
```

Run the scanner against a host (scans common ports by default):

```bash
python3 mini_scanner.py example.com
```

Scan a port range (inclusive):

```bash
python3 mini_scanner.py 192.168.56.101 1 1024
```

Optional flags:

* `-t`, `--timeout` — socket timeout in seconds (default `0.8`).
* `-w`, `--workers` — number of concurrent worker threads (default `100`).

Example with flags:

```bash
python3 mini_scanner.py 192.168.56.101 1 1024 -t 0.6 -w 200
```

## Example output

```
Scanning 192.168.56.101 (192.168.56.101)
Ports: 1-1024  Timeout: 0.8s
[+] Port  22 OPEN
[+] Port  80 OPEN

Scan completed in 1.23s
Open ports: 22, 80
```

## How it works (brief)

* Resolves the target hostname to an IPv4 address.
* Builds a list of ports to scan (either the built-in common ports or a provided range).
* Uses a `ThreadPoolExecutor` to concurrently try `socket.connect_ex()` to each port.
* Reports open ports and prints a short summary with elapsed time.

## Possible improvements

* Add banner grabbing to collect service banners from open ports.
* Add CSV/JSON output for reports.
* Implement a SYN scan using `scapy` (requires root and raw sockets).
* Add `/etc/services` parsing or a small port→service mapping for nicer output.

## Contributing

Contributions are welcome. Open an issue or submit a pull request with clear details and tests/examples.
