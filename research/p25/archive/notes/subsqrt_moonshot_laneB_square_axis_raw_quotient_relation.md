# Subsqrt Moonshot Lane B Square-Axis Raw Quotient Relation

Date: 2026-06-12

## Result

The quotient normal form satisfies:

```text
D^3 = Y
```

On the raw `C_12675` source cycle, `D^3` and `Y` differ by one `C_25` kernel
layer.  Therefore a raw lift satisfies the relation on values only when the
lift is kernel-trivial/block-constant.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_raw_quotient_relation_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_raw_quotient_relation_gate.py
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
  trace_correct = 1
  block_constant = 1
  kernel_modes = [0]
  D3_equals_Y_hits = 12675 / 12675
  mismatches = 0

sparse_section_trace_correct:
  trace_correct = 1
  block_constant = 0
  kernel_modes = [0,1,2,...,24]
  D3_equals_Y_hits = 12639 / 12675
  mismatches = 36
  mismatch_q_count = 18
  mismatch_per_q_values = [2]

block_plus_hidden_kernel_mode:
  trace_correct = 1
  block_constant = 0
  kernel_modes = [0,1]
  D3_equals_Y_hits = 12225 / 12675
  mismatches = 450
  mismatch_q_count = 18
  mismatch_per_q_values = [25]

relation_summary:
  trace_correct_lifts = 3 / 4
  trace_correct_and_raw_D3_equals_Y = 1 / 3
  only_block_constant_lift_satisfies_raw_relation = 1

square_axis_raw_quotient_relation_rows = 1 / 1
```

## Consequence

The trace-projection gate showed that quotient trace-correctness alone permits
sparse or hidden-kernel lifts.  This gate adds the quotient algebra itself:
requiring raw values to respect the lifted relation `D^3 = Y` eliminates those
extra lifts and selects the kernel-trivial `450`-point block lift.

So the producer target can be stated more tightly:

```text
trace to the quotient residual;
remain block-constant on every B=25 kernel block;
and satisfy the raw lifted quotient relation D^3 = Y on values.
```

Discard conditions:

```text
reject sparse trace-correct sections: they fail D^3=Y on 36 raw positions;
reject hidden trace-zero kernel contamination: it fails D^3=Y on 450 raw positions;
keep only lifts where quotient trace, block constancy, and raw quotient algebra agree.
```

The preceding trace-projection checkpoint is:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/subsqrt_moonshot_laneB_square_axis_trace_projection_lift.md
```
