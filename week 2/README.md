# MapReduce Engine

A from-scratch MapReduce **engine** in Python — the software that lets
you plug in different mapper/reducer logic to solve word count, student
count, sales totals, etc. This implementation follows the split →
map → partition → sort → reduce pipeline, with real forked mapper and
reducer subprocesses, exactly as described in `MapReduce_Explained.pdf`.

## Project layout

```
MapReduce/
├── master.py         Controls the whole workflow
├── splitter.py        Splits the input into chunks
├── mapper.py           Converts each record into a (key, value) pair
├── partitioner.py       Uses hash(key) % num_reducers to route data
├── sorter.py             Sorts each partition so identical keys are together
├── reducer.py             Aggregates values per key into final counts
├── input.txt                Sample input data
├── chunks/           (created at runtime) input split into pieces
├── map_output/       (created at runtime) raw (key, 1) pairs per mapper
├── partitions/        (created at runtime) partition_0.txt, partition_1.txt, ...
├── sorted/             (created at runtime) sorted partitions
└── output/              (created at runtime) part-0.txt, part-1.txt, final_output.txt
```

## The idea (from the guide)

> Instead of one worker, use many workers.

A huge input file is split into chunks. Many **mappers** run at the same
time, each turning its chunk into simple `(key, 1)` pairs — they don't
count anything, they just tag every occurrence. A **hash partitioner**
sends every occurrence of the same key to the same partition file, using
`hash(key) % num_reducers`, so nothing gets split across reducers. Each
partition is **sorted** so identical keys sit next to each other. Then
many **reducers** run at the same time, each summing the values for its
keys. The master combines all reducer outputs into the final result.

```
INPUT FILE
   -> Split into chunks
   -> Fork many mapper processes            [parallel]
   -> (key, 1) pairs
   -> Hash Partitioner
   -> partition_0.txt, partition_1.txt, ...
   -> Sort each partition
   -> Fork many reducer processes           [parallel]
   -> Final Output File
```

## Running it

```bash
python3 master.py input.txt 2 2
```

Arguments: `<input_file> <num_mappers> <num_reducers>` (defaults:
`input.txt`, 2 mappers, 2 reducers).

The included `input.txt` counts students per degree/department (one
department per line, same idea as the guide's opening example: "count
how many students belong to each department"):

```
CSE
ECE
CSE
MECH
ECE
CSE
IT
CSE
ECE
IT
MECH
CSE
CIVIL
ECE
CSE
IT
MECH
CIVIL
CSE
ECE
```

Expected final output (`output/final_output.txt`):

```
CIVIL   2
CSE     7
ECE     5
IT      3
MECH    3
```

Run it with:

```bash
python3 master.py input.txt 3 2
```

## Using it for something else

The engine itself never changes — only `mapper.py` and `reducer.py` do.
To count something other than degrees, just point `input.txt` at your own
one-key-per-line data (e.g. one product name per line, one city per
line); `mapper.py` and `reducer.py` already do plain counting, so no code
changes are needed. For a different aggregation (sums, averages, max),
edit the reducer's aggregation logic and, if needed, what the mapper
extracts as the key/value.

## Why forked subprocesses?

`master.py` launches each mapper and each reducer with
`subprocess.Popen`, so they are genuinely independent OS processes
running concurrently — not just function calls in a loop. This is what
lets the engine process large files faster: instead of one process
reading a million lines one at a time, several processes each read a
fraction of the file at the same time.

## Inspecting intermediate stages

After a run, every intermediate stage is left on disk so you can see
exactly what each step produced:

```bash
cat chunks/chunk_0.txt          # a mapper's input chunk
cat map_output/map_0.txt        # that mapper's (key, 1) pairs
cat partitions/partition_0.txt  # everything hashed to reducer 0
cat sorted/sorted_0.txt         # partition 0, sorted by key
cat output/part-0.txt           # reducer 0's aggregated output
cat output/final_output.txt     # combined final result
```
