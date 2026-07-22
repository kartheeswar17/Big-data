#!/usr/bin/env python3
"""
reducer.py

Step 15 of the guide: "Reducer"
Receives a SORTED partition file where identical keys are already
grouped together, e.g.:

    Apple 1
    Apple 1
    Apple 1
    Apple 1
    Banana 1
    Banana 1

...and adds up the values for each key:

    Apple 4
    Banana 2

Usage:
    python3 reducer.py <sorted_partition_file>

Writes "key<TAB>total" pairs to stdout (redirected to an output file by
the master).
"""
import sys


def main():
    if len(sys.argv) != 2:
        print("Usage: reducer.py <sorted_partition_file>", file=sys.stderr)
        sys.exit(1)

    input_path = sys.argv[1]

    current_key = None
    total = 0

    with open(input_path, "r") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue

            key, value = line.split("\t")
            value = int(value)

            if key == current_key:
                total += value
            else:
                if current_key is not None:
                    print(f"{current_key}\t{total}")
                current_key = key
                total = value

    if current_key is not None:
        print(f"{current_key}\t{total}")


if __name__ == "__main__":
    main()
