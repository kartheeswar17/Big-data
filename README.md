# JioHotstar Log Pipeline — Binary Partitioning Assignment

A simulated real-time log ingestion pipeline. Three fake branch servers stream
log lines over TCP; a multi-threaded harvester daemon reads the raw byte
stream, validates each line with a regex, and writes valid records into
compact custom binary files, partitioned by (service, severity level). A
reader script proves the binary files contain real, structured, recoverable
data — not just raw bytes.

## Files

| File | Role |
|---|---|
| `server.py` | Simulates 3 branch servers (`jiohotstar-mumbai`, `jiohotstar-delhi`, `jiohotstar-bangalore`), each on its own TCP port, streaming random log lines forever once a client connects. |
| `log harvester daemon.py` | Connects to all 3 servers (one thread each), slices the raw byte stream into lines, validates with regex, encodes valid records into a custom binary format, and writes them into per-(service, level) `.bin` files under `partitions/`. |
| `read binary.py` | Decodes one `.bin` partition file back into human-readable log lines. |
| `verify pipeline.py` | Scans **all** `.bin` files in `partitions/`, decodes each, and prints a summary table (record counts per file, per service, per level, and a grand total). |

## Requirements

- Python 3.8+ (no external packages — everything used is from the standard library: `socket`, `threading`, `struct`, `re`, `os`, `time`, `glob`)

## How to run

Run these in order, in **separate terminals**, all from the same project
folder (e.g. `C:\Bigdata\weeek 1`).

### 1. Start the simulated servers

```
python server.py
```

Wait until you see:

```
All simulated branch servers are up. Press Ctrl+C to stop.
```

Leave this terminal open — the servers only stream logs while a client is
connected, and must keep running for the rest of the demo.

### 2. Start the harvester daemon

In a **second terminal**:

```
python "log harvester daemon.py"
```

This connects to all 3 servers and starts writing partition files. You'll see
`[partition] created new partition file: ...` lines as new (service, level)
combinations appear, plus a live stats snapshot every 3 seconds.

Let it run for 10–30 seconds, then stop it with `Ctrl+C` — this closes and
flushes all open partition files cleanly.

### 3. Inspect a single partition file

```
python "read binary.py" partitions/jiohotstar-mumbai_ERROR.bin
```

Prints every decoded record in that file as
`timestamp | level | service | message`.

### 4. Verify the whole pipeline at once

```
python "verify pipeline.py"
```

Scans every `.bin` file under `partitions/` and prints a summary table:
record counts per file, per service, per level, and a grand total. Use this
as proof-of-correctness evidence instead of checking files one by one.

## How it works

### Log line format (plain text, sent over TCP)

```
2026-07-10 13:40:16 | ERROR | jiohotstar-mumbai | Stream#7680 failed due to CDN unavailability
```

Validated by this regex in the harvester:

```
^(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s*\|\s*
(?P<level>INFO|WARNING|ERROR|DEBUG)\s*\|\s*
(?P<service>[\w\-]+)\s*\|\s*
(?P<message>.+)$
```

The simulator occasionally sends a garbled line
(`CORRUPTED_LINE_NO_STRUCTURE_HERE`) on purpose — the harvester silently
drops any line that fails validation and counts it under `REJECTED` in its
stats.

### Why byte-slicing is needed

TCP is just a byte stream — one `recv()` call does **not** correspond to one
log line. A line can arrive split across two `recv()` calls, or several
lines can arrive in a single `recv()` call. The harvester keeps a rolling
buffer per connection and splits on `\n` manually, carrying any incomplete
trailing fragment over to the next `recv()`.

### Binary record format

Each record is packed with `struct`, network byte order (`!`):

| Field | Type | Size |
|---|---|---|
| Timestamp | fixed-width ASCII string | 19 bytes |
| Level code | unsigned byte (`DEBUG=0, INFO=1, WARNING=2, ERROR=3`) | 1 byte |
| Service name length | unsigned short | 2 bytes |
| Service name | UTF-8 | variable |
| Message length | unsigned short | 2 bytes |
| Message | UTF-8 | variable |

Each record is itself prefixed with a 4-byte unsigned int giving its total
length, so the reader can walk the file and slice out one record at a time
without needing delimiters inside the binary data.

### Partitioning

A new `.bin` file is created the first time a given `(service, level)`
combination is seen, e.g. `jiohotstar-mumbai_ERROR.bin`,
`jiohotstar-delhi_INFO.bin`. A per-file lock prevents concurrent threads from
corrupting the same partition if two branches happen to log the same
service/level combination at once (not applicable here since each branch has
a unique name, but included for correctness/reuse).

## Troubleshooting

- **`ConnectionRefusedError: [WinError 10061]`** — the harvester started
  before the simulator, or the simulator isn't running. Start `server.py`
  first and confirm it prints "All simulated branch servers are up" before
  starting the harvester.
- **`can't open file '...': [Errno 2] No such file or directory`** — filename
  mismatch. Check the exact filename with `dir` and match it exactly,
  wrapping in quotes if it contains spaces (e.g. `"log harvester daemon.py"`).
- **No `.bin` files found** — make sure you ran `read binary.py` /
  `verify pipeline.py` from the same folder where the harvester created
  `partitions/`, or pass the folder path explicitly:
  `python "verify pipeline.py" path\to\partitions`.
- **Some expected partitions are missing** — this is normal for short runs;
  which (service, level) combinations appear depends on random log content.
  Run the harvester a bit longer to get full coverage of all 12 combinations
  (3 services × 4 levels).
