# Subsqrt Moonshot Lane B Robert Source-Matrix Harness

Date: 2026-06-13

## Result

Added a producer-facing intake wrapper for Robert elliptic-unit,
Siegel-Ramachandra, and mixed modular-unit probes that naturally emit values in
local source coordinates:

```text
C_75 x C_169
right_log = e mod 75
c_log     = e mod 169
```

The existing bridge candidate harness expects raw exponent order on
`C_12675`.  The new wrapper converts a row-major `75 x 169` table to raw order
by CRT and then reuses the exact bridge candidate profile.

## Why This Matters

The next Robert elliptic-unit microscope should produce a finite table like:

```text
M[right_log, c_log] ~= K-traced finite residue of x(Q_c)-x(P_right)
```

or a signed/logged variant of it.  That table can now be checked directly
without hand-converting to raw exponent order.

## Command

Default round-trip positive control:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_source_matrix_harness_gate.py
```

Candidate mode:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_source_matrix_harness_gate.py \
  --source-matrix PATH
```

`PATH` must contain exactly `12675` integers in row-major order:

```text
right_log = 0, c_log = 0..168
right_log = 1, c_log = 0..168
...
right_log = 74, c_log = 0..168
```

The converted raw vector must pass the full bridge producer contract:

- exact signed quotient trace;
- kernel-trivial block lift;
- raw `D^3 = Y` relation;
- exact `C_75 x C_169` source graph;
- full mixed quotient character payload.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_robert_source_matrix_harness_gate.py
```
