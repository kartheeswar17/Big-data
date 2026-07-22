#!/usr/bin/env python3
"""
mapper.py

Step 7-9 of the guide: "What is a Mapper?"
The mapper does NOT count anything. It just says "I saw this key once"
for every line it reads, turning raw records into intermediate
(key, value) pairs:

    Apple           ->   Apple   1
    Orange          ->   Orange  1
    Apple           ->   Apple   1

Each mapper process only ever sees its own chunk file — this is what
lets many mappers run at the same time on different pieces of the input.

Usage:
    python3 mapper.py <chunk_file>

Writes "key<TAB>1" pairs to stdout (redirected to a map-output file by
the master).
"""
import sys


def main():
    if len(sys.argv) != 2:
        print("Usage: mapper.py <chunk_file>", file=sys.stderr)
        sys.exit(1)

    chunk_file = sys.argv[1]

    with open(chunk_file, "r") as f:
        for line in f:
            key = line.strip()
            if not key:
                continue
            # Every occurrence becomes (key, 1) — never pre-aggregated.
            print(f"{key}\t1")


if __name__ == "__main__":
    main()
