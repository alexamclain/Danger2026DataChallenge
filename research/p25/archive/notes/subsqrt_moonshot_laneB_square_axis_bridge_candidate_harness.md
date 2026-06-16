# P25 Lane B Square-Axis Bridge Candidate Harness

## Purpose

This checkpoint turns the current bridge geometry into a producer-facing
finite contract.  A proposed CM-Artin, Jacobi, or modular-unit object can now
be compared against the exact local bridge rather than judged by a looser
shadow such as trace support or pure C-axis characters.

The target is the signed bridge

```text
S * X * Y^-2 * (1 - X^2 * Y^3)
```

on `C_3 x C_169`, with the kernel-trivial raw lift on `C_12675`.

## Gate

File:

```text
research/p25/p25_laneB_square_axis_bridge_candidate_harness_gate.py
```

Raw candidate mode:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_bridge_candidate_harness_gate.py \
  --raw-candidate PATH
```

The raw file must contain exactly `12675` integers.  This mode prints
`square_axis_bridge_candidate_harness_raw_candidate_rows=1/1` only if the
candidate is the exact kernel-trivial anti-invariant bridge.

The harness audits four candidates:

```text
kernel_trivial_block_bridge
trace_correct_sparse_section
positive_D_segment_only
separated_axis_hull_bridge
```

Only the first candidate passes.

The pass contract requires:

```text
exact signed quotient trace
kernel-trivial block lift
raw D^3 = Y relation
exact C_75 x C_169 source graph
full mixed quotient character payload
```

## Results

The control bridge has:

```text
raw_support = 150
quotient_support = 6
kernel_modes = (0,)
raw_relation_mismatches = 0
pure C characters = 168
mixed right/C characters = 336
```

The trace-correct sparse section still fails:

```text
trace_correct = true
kernel_modes = all 25 modes
block_constancy_hits < 507
raw_relation_mismatches > 0
```

The positive segment alone is kernel-trivial but not the signed bridge:

```text
quotient_support = 3
trace_correct = false
```

The separated axis hull is also kernel-trivial, but it is not a bridge
producer:

```text
raw_support = 450
trace_correct = false
mixed right/C characters = 0
```

## Consequence

Trace correctness, kernel trace, and pure C-axis character support are no
longer enough.  A future moonshot candidate has to recover the anti-invariant
bridge as a block-constant raw source graph with the mixed right/C payload.
This is the finite acceptance harness for the next modular-unit or CM-Artin
producer attempt.
