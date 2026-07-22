#!/usr/bin/env python3
"""
splitter.py

Step 6 of the guide: "Splitting"
Cuts the huge input file into N smaller chunks so that N mappers can each
work on one chunk independently and in parallel.

Usage:
    python3 splitter.py <input_file> <num_chunks> <chunks_dir>

Prints the path of every chunk file it creates (one per line) so the
master can pick them up.
"""
import sys
import os
import math


def split_file(input_path, num_chunks, chunk_dir):
    os.makedirs(chunk_dir, exist_ok=True)

    with open(input_path, "r") as f:
        lines = [line for line in f if line.strip()]

    total_lines = len(lines)
    if num_chunks < 1:
        num_chunks = 1
    chunk_size = math.ceil(total_lines / num_chunks) if total_lines else 0

    chunk_paths = []
    for i in range(num_chunks):
        start = i * chunk_size
        end = min(start + chunk_size, total_lines)
        chunk_lines = lines[start:end]

        chunk_path = os.path.join(chunk_dir, f"chunk_{i}.txt")
        with open(chunk_path, "w") as cf:
            cf.writelines(chunk_lines)
        chunk_paths.append(chunk_path)

    return chunk_paths


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: splitter.py <input_file> <num_chunks> <chunks_dir>", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    n_chunks = int(sys.argv[2])
    chunks_dir = sys.argv[3]

    paths = split_file(input_file, n_chunks, chunks_dir)
    for p in paths:
        print(p)
