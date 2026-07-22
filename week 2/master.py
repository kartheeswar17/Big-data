#!/usr/bin/env python3
"""
master.py

Step 4, 17, and "Complete Flow" of the guide.
The master controls the entire MapReduce Engine workflow, exactly as in
the flow diagram:

    INPUT FILE
        -> Split into chunks                (splitter.py)
        -> Fork many mapper processes        (mapper.py)        [parallel]
        -> (word, 1) pairs
        -> Hash Partitioner                  (partitioner.py)
        -> partition_0.txt, partition_1.txt, ...
        -> Sort each partition               (sorter.py)
        -> Fork many reducer processes       (reducer.py)       [parallel]
        -> Final Output File

The mapper and reducer stages use subprocess.Popen so that each mapper
and each reducer really is an independent OS process running at the same
time, not just a function call.

Usage:
    python3 master.py [input_file] [num_mappers] [num_reducers]

Defaults: input.txt, 2 mappers, 2 reducers.
"""
import subprocess
import sys
import os
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHUNKS_DIR = os.path.join(BASE_DIR, "chunks")
MAP_OUTPUT_DIR = os.path.join(BASE_DIR, "map_output")
PARTITIONS_DIR = os.path.join(BASE_DIR, "partitions")
SORTED_DIR = os.path.join(BASE_DIR, "sorted")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")


def clean_dirs():
    """Wipe intermediate directories so each run starts fresh."""
    for d in (CHUNKS_DIR, MAP_OUTPUT_DIR, PARTITIONS_DIR, SORTED_DIR, OUTPUT_DIR):
        if os.path.exists(d):
            shutil.rmtree(d)
        os.makedirs(d)


def run(cmd):
    """Run a helper script and return its completed process (captures stdout)."""
    return subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(BASE_DIR, "input.txt")
    num_mappers = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    num_reducers = int(sys.argv[3]) if len(sys.argv) > 3 else 2

    print(f"[MASTER] Input file : {input_file}")
    print(f"[MASTER] Mappers    : {num_mappers}")
    print(f"[MASTER] Reducers   : {num_reducers}\n")

    clean_dirs()

    # ---------------- STEP 1: SPLIT ----------------
    print("[MASTER] Step 1/5 -- Splitting input into chunks...")
    result = run([sys.executable, os.path.join(BASE_DIR, "splitter.py"),
                  input_file, str(num_mappers), CHUNKS_DIR])
    chunk_files = result.stdout.decode().strip().splitlines()
    for c in chunk_files:
        print(f"    -> {os.path.basename(c)}")

    # ---------------- STEP 2: MAP (forked, parallel) ----------------
    print("\n[MASTER] Step 2/5 -- Forking mapper processes...")
    mapper_procs = []
    mapper_outputs = []
    for i, chunk in enumerate(chunk_files):
        out_path = os.path.join(MAP_OUTPUT_DIR, f"map_{i}.txt")
        mapper_outputs.append(out_path)
        out_f = open(out_path, "w")
        proc = subprocess.Popen(
            [sys.executable, os.path.join(BASE_DIR, "mapper.py"), chunk],
            stdout=out_f,
        )
        mapper_procs.append((proc, out_f, i))
        print(f"    -> Forked Mapper {i} (pid={proc.pid}) on {os.path.basename(chunk)}")

    for proc, out_f, i in mapper_procs:
        proc.wait()
        out_f.close()
        print(f"    <- Mapper {i} finished")

    # ---------------- STEP 3: PARTITION ----------------
    print("\n[MASTER] Step 3/5 -- Hash partitioning intermediate data (hash(key) % reducers)...")
    run([sys.executable, os.path.join(BASE_DIR, "partitioner.py"),
         str(num_reducers), PARTITIONS_DIR] + mapper_outputs)
    for r in range(num_reducers):
        print(f"    -> partition_{r}.txt")

    # ---------------- STEP 4: SORT ----------------
    print("\n[MASTER] Step 4/5 -- Sorting each partition...")
    sorted_files = []
    for r in range(num_reducers):
        part_path = os.path.join(PARTITIONS_DIR, f"partition_{r}.txt")
        sorted_path = os.path.join(SORTED_DIR, f"sorted_{r}.txt")
        run([sys.executable, os.path.join(BASE_DIR, "sorter.py"), part_path, sorted_path])
        sorted_files.append(sorted_path)
        print(f"    -> sorted_{r}.txt")

    # ---------------- STEP 5: REDUCE (forked, parallel) ----------------
    print("\n[MASTER] Step 5/5 -- Forking reducer processes...")
    reducer_procs = []
    reducer_outputs = []
    for r, sorted_file in enumerate(sorted_files):
        out_path = os.path.join(OUTPUT_DIR, f"part-{r}.txt")
        reducer_outputs.append(out_path)
        out_f = open(out_path, "w")
        proc = subprocess.Popen(
            [sys.executable, os.path.join(BASE_DIR, "reducer.py"), sorted_file],
            stdout=out_f,
        )
        reducer_procs.append((proc, out_f, r))
        print(f"    -> Forked Reducer {r} (pid={proc.pid}) on sorted_{r}.txt")

    for proc, out_f, r in reducer_procs:
        proc.wait()
        out_f.close()
        print(f"    <- Reducer {r} finished")

    # ---------------- COMBINE FINAL OUTPUT ----------------
    final_path = os.path.join(OUTPUT_DIR, "final_output.txt")
    combined = {}
    for out_path in reducer_outputs:
        with open(out_path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                key, value = line.split("\t")
                combined[key] = combined.get(key, 0) + int(value)

    with open(final_path, "w") as f:
        for key in sorted(combined.keys()):
            f.write(f"{key}\t{combined[key]}\n")

    print(f"\n[MASTER] Done. Final output -> {final_path}\n")
    print("Result:")
    with open(final_path) as f:
        print(f.read())


if __name__ == "__main__":
    main()
