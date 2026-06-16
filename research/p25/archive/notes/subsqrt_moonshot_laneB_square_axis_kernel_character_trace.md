# Subsqrt Moonshot Lane B Square-Axis Kernel-Character Trace

Date: 2026-06-12

## Result

The raw-shift lift shows that `D^3` and `Y` differ by one generator of the
`B = 25` trace kernel on the raw `C_12675` source cycle.  The natural tempting
explanation is to use a nontrivial `C_25` kernel character: it sees the
one-layer monodromy as a phase.

That explanation cannot by itself produce the quotient residual.  Over the
split field

```text
126751 = 10 * 12675 + 1
```

every nontrivial `C_25` kernel character has zero trace to `C_3 x C_169`.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_kernel_character_trace_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_kernel_character_trace_gate.py
```

Observed:

```text
case = square_axis_C3xC169
raw_order = 12675
quotient_order = 507
B = 25
modulus = 126751
zeta25_order_ok = 1
zeta_raw_order_ok = 1

mode 0:
  trace_sum = 25
  D3_over_Y_phase = 1
  selected_trace_nonzero = 18 / 18
  selected_normalized_ones = 18 / 18

mode 1:
  trace_sum = 0
  D3_over_Y_phase = 106085
  selected_trace_nonzero = 0 / 18
  selected_normalized_ones = 0 / 18

mode_summary:
  rows_ok = 25 / 25
  nontrivial_zero_trace = 24 / 24
  nontrivial_phase_visible = 24 / 24

trace_dimensions:
  raw_dimension = 12675
  quotient_image_dimension = 507
  nontrivial_kernel_dimension = 12168

square_axis_kernel_character_trace_rows = 1 / 1
```

## Consequence

A raw producer cannot explain the quotient-shift residual using only a
nontrivial kernel character.  Such modes do detect the raw relation

```text
D^3 = Y + one kernel step
```

but their trace to the quotient is zero.  Therefore a valid producer needs a
kernel-trivial component that survives trace-down to the `18` residual quotient
classes, while any nontrivial kernel monodromy must cancel or vanish under
trace.

This gives a stricter producer falsifier:

```text
reject candidates whose only explanation of D^3/Y is a nontrivial C_25 phase;
reject candidates whose trace-surviving component is absent or not the residual comb;
accept only candidates where kernel monodromy is paired with a kernel-trivial quotient payload.
```

The immediately preceding raw-shift checkpoint is:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/subsqrt_moonshot_laneB_square_axis_raw_shift_lift.md
```
