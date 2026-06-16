# Subsqrt Moonshot Lane B Robert Sparse-Source Candidate Harness

Date: 2026-06-13

## Result

Added a sparse-source intake wrapper for Robert/Siegel and modular-unit
producer candidates.

The existing source-matrix harness accepts a full row-major `C_75 x C_169`
table, but a theorem or hand calculation is likely to emit only nonzero
divisor terms.  The new harness accepts triples

```text
right_log  c_log  coefficient
```

coalesces them in `C_75 x C_169`, converts by CRT to raw `C_12675` exponent
order, and reuses the bridge candidate contract.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_robert_sparse_source_candidate_harness_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_sparse_source_candidate_harness_gate.py
```

Observed:

```text
source_group=C_75xC_169
raw_order=12675
target input terms=150
active source terms=150
duplicate source terms=0
raw support=150
bridge contract ok=1
robert_sparse_source_candidate_harness_rows=1/1
```

## Consequence

A literature hit no longer needs to expand a full matrix before its first
falsifier.  It can emit the sparse nonzero source-coordinate terms of a
candidate divisor quotient, then run:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_sparse_source_candidate_harness_gate.py \
  --sparse-source PATH
```

Pass condition:

```text
coalesced sparse vector has 150 active source terms
converted raw vector has support 150
exact signed quotient trace
kernel-trivial block lift
raw D^3=Y relation
exact C_75 x C_169 source graph
full mixed quotient character payload
```

Discard condition:

```text
wrong support count
trace-correct but non-block-constant sparse section
separated right-trace-times-C hull
missing inversion partner
non-kernel raw representative shift
```
