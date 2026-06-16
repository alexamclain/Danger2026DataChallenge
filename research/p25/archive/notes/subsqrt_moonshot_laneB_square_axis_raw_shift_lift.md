# Subsqrt Moonshot Lane B Square-Axis Raw-Shift Lift

Date: 2026-06-12

## Result

The square-axis quotient shifts from the `C_3 x C_169` normal form lift to the
actual raw local source cycle, but the relation `D^3 = Y` is only true after
quotienting by the `B = 25` trace kernel.

On the quotient:

```text
q = 169*right + 3*c  mod 507
D = x^172 = (right+1, c+1)
X = x^43  = (right+1, c+127)
Y = x^9   = (right,   c+3)
D^3 = Y
```

On the raw source cycle:

```text
raw_order = 12675 = 25 * 507
3*172 = 516 = 9 + 507
```

So `D^3` and `Y` land on the same quotient coordinate, but differ by exactly
one raw trace-kernel layer.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_raw_shift_lift_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_raw_shift_lift_gate.py
```

Observed:

```text
case = square_axis_C3xC169
raw_order = 12675
quotient_order = 507
B = 25

D:
  step = 172
  vector = (1,1)
  coordinate_hits = 12675 / 12675
  kernel_delta_counts = {0: 8375, 1: 4300}

X:
  step = 43
  vector = (1,127)
  coordinate_hits = 12675 / 12675
  kernel_delta_counts = {0: 11600, 1: 1075}

Y:
  step = 9
  vector = (0,3)
  coordinate_hits = 12675 / 12675
  kernel_delta_counts = {0: 12450, 1: 225}

D_cubed:
  step = 516
  quotient_step = 9
  vector = (0,3)
  coordinate_hits = 12675 / 12675
  kernel_delta_counts = {1: 12450, 2: 225}

D_cubed_vs_Y:
  quotient_hits = 12675 / 12675
  raw_same_hits = 0 / 12675
  kernel_offsets = {1: 12675}

selected_word_raw_steps:
  max_step = 491
  all_below_quotient_order = 1
  raw_steps_match_selected_qs = 1

square_axis_raw_shift_lift_rows = 1 / 1
```

## Consequence

The quotient-shift normal form is genuinely visible on the raw local source:
the shifts are raw exponent additions by `172`, `43`, and `9`.  But a producer
cannot impose the quotient relation `D^3 = Y` before trace-down, because on the
raw cycle `D^3` is `Y` followed by one `507`-step kernel translate.

That makes a concrete falsifier for proposed modular-unit or CM-Artin
pullbacks:

```text
accept candidates that realize D, X, Y as the measured raw source shifts;
reject candidates that force D^3 and Y to be equal on raw representatives;
require the one-layer B-kernel monodromy to disappear only after trace-down.
```

The selected residual word itself is still raw-small: its largest shift is
`491 < 507`, so the `18`-point residual comb can be read before wrapping the
quotient cycle.  The monodromy enters when the producer tries to use the
structural relation `D^3 = Y`, not in the displayed selected word.

This is the first producer-facing refinement after the quotient-shift normal
form:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/subsqrt_moonshot_laneB_square_axis_quotient_shift_normal_form.md
```
