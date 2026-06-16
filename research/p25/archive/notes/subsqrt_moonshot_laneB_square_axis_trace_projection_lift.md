# Subsqrt Moonshot Lane B Square-Axis Trace-Projection Lift

Date: 2026-06-12

## Result

Quotient trace-correctness is weaker than the raw Lane B producer contract.
For the `C_3 x C_169` residual, both of the following can trace to the same
`18` quotient classes:

```text
block-constant lift: 18 classes * 25 kernel layers = 450 raw positions
sparse section lift: 18 classes * 1 representative    = 18 raw positions
```

Only the block-constant lift is kernel-trivial.  The sparse section has full
hidden `C_25` kernel Fourier support.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_trace_projection_lift_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_trace_projection_lift_gate.py
```

Observed:

```text
case = square_axis_C3xC169
raw_order = 12675
quotient_order = 507
B = 25
selected_qs = 18
modulus = 126751

block_constant_kernel_trivial:
  raw_support = 450
  normalized_trace_hits = 507 / 507
  quotient_support = 18 / 18
  block_constancy_hits = 507 / 507
  kernel_mode_support = [0]

sparse_section_trace_correct:
  raw_support = 18
  normalized_trace_hits = 507 / 507
  quotient_support = 18 / 18
  block_constancy_hits = 489 / 507
  kernel_mode_support = [0,1,2,...,24]

block_plus_hidden_kernel_mode:
  raw_support = 450
  normalized_trace_hits = 507 / 507
  quotient_support = 18 / 18
  block_constancy_hits = 489 / 507
  kernel_mode_support = [0,1]

hidden_kernel_mode_only:
  raw_support = 450
  normalized_trace_hits = 489 / 507
  quotient_support = 0 / 18
  block_constancy_hits = 489 / 507
  kernel_mode_support = [1]

projection_summary:
  trace_correct_lifts = 3 / 4
  kernel_trivial_trace_correct_lifts = 1 / 3
  sparse_trace_correct_but_not_block_constant = 1
  hidden_modes_do_not_change_trace = 1

square_axis_trace_projection_lift_rows = 1 / 1
```

## Consequence

This separates two different standards:

```text
trace-correct:       normalized B-trace equals the quotient residual;
producer-contract:  trace-correct plus kernel-trivial/block-constant lift.
```

The quotient residual alone does not force the stronger condition.  A sparse
`18`-point raw section can trace to the same quotient payload, but it carries
all `25` kernel modes and fails block constancy on exactly the selected `18`
blocks.  Adding hidden kernel modes to the block lift also preserves the
quotient trace while breaking block constancy.

Therefore the current Lane B harness is intentionally stricter than quotient
trace correctness:

```text
accept the 450-point kernel-trivial block lift;
reject sparse trace-correct lifts with hidden C_25 support;
reject block lifts contaminated by trace-zero kernel modes.
```

This is the producer-facing refinement after the kernel-character trace
obstruction:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/subsqrt_moonshot_laneB_square_axis_kernel_character_trace.md
```
