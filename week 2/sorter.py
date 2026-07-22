#!/usr/bin/env python3
"""
sorter.py

Step 14 of the guide: "Why Sorting?"
A partition file has the same key scattered throughout it, e.g.:

    Apple 1
    Banana 1
    Apple 1
    Mango 1
    Apple 1

After sorting, identical keys sit next to each other, which is what lets
the reducer group and aggregate them with a single pass instead of
scanning the whole file for every key.

Usage:
    python3 sorter.py <input_partition_file> <output_sorted_file>
"""
import sys


def sort_partition(input_path, output_path):
    with open(input_path, "r") as f:
        lines = [line.rstrip("\n") for line in f if line.strip()]

    # Sort by key (the part before the tab)
    lines.sort(key=lambda line: line.split("\t")[0])

    with open(output_path, "w") as f:
        for line in lines:
            f.write(line + "\n")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: sorter.py <input_partition_file> <output_sorted_file>", file=sys.stderr)
        sys.exit(1)

    sort_partition(sys.argv[1], sys.argv[2])
