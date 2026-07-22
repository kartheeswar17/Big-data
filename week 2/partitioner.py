#!/usr/bin/env python3
"""
partitioner.py

Step 10-13 of the guide: "Why Partitioning?" / "Hash Function" / "Partition Files"
Decides, for every intermediate (key, value) pair produced by the mappers,
which reducer is responsible for it — using:

    hash(key) % number_of_reducers

This guarantees every occurrence of the same key always lands in the same
partition file, so one reducer sees ALL of a key's values and can produce
a correct total.

Usage:
    python3 partitioner.py <num_reducers> <partitions_dir> <map_output_file1> [map_output_file2 ...]

Writes partitions_dir/partition_<r>.txt for r in [0, num_reducers).
"""
import sys
import os


def partition(mapper_output_files, num_reducers, partitions_dir):
    os.makedirs(partitions_dir, exist_ok=True)

    handles = []
    for r in range(num_reducers):
        path = os.path.join(partitions_dir, f"partition_{r}.txt")
        handles.append(open(path, "w"))

    try:
        for map_file in mapper_output_files:
            with open(map_file, "r") as f:
                for line in f:
                    line = line.rstrip("\n")
                    if not line:
                        continue
                    key = line.split("\t")[0]
                    reducer_id = hash(key) % num_reducers
                    handles[reducer_id].write(line + "\n")
    finally:
        for h in handles:
            h.close()


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(
            "Usage: partitioner.py <num_reducers> <partitions_dir> "
            "<map_output_file1> [map_output_file2 ...]",
            file=sys.stderr,
        )
        sys.exit(1)

    n_reducers = int(sys.argv[1])
    out_dir = sys.argv[2]
    map_files = sys.argv[3:]

    partition(map_files, n_reducers, out_dir)
    print(f"Partitioned {len(map_files)} mapper output file(s) into {n_reducers} partition(s)")
