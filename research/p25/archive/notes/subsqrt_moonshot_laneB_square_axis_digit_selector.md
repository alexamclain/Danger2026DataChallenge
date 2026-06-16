# Subsqrt Moonshot Lane B Square-Axis Digit Selector

Date: 2026-06-12

## Result

The local triangular exponent comb has a compact base-`43` digit rule.

Write:

```text
q = 43*m + r,  0 <= r < 43
```

Then the `18` square-axis residual classes are exactly:

```text
1 <= m <= 11
m mod 4 != 0
r = 9*t
0 <= t <= (m - 1) mod 4
```

Equivalently, set:

```text
h = (m - 1) mod 4
```

Then the selector on `(h,t)` is the lower-triangular matrix:

```text
[[1, 0, 0],
 [1, 1, 0],
 [1, 1, 1]]
```

Observed:

```text
q_count = 18 / 18
digit_hits = 18 / 18
h_counts = [3, 6, 9]
s_counts = [6, 6, 6]
t_counts = [9, 6, 3]
high_digits = [1, 2, 3, 5, 6, 7, 9, 10, 11]
low_residues = [0, 9, 18]
rank_f2 = 3
rank_odd = 3
mixed_second_difference_nonzero = 1
```

This is not merely a congruence selector modulo a proper divisor of `507`.
Every proper modulus overselects:

```text
mod 1:   lifted_count = 507
mod 3:   lifted_count = 507
mod 13:  lifted_count = 351
mod 39:  lifted_count = 234
mod 169: lifted_count = 54
```

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_digit_selector_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_digit_selector_gate.py
```

Observed:

```text
square_axis_digit_selector_rows = 1 / 1
conclusion = reported_p25_laneB_square_axis_digit_selector_gate
```

## Consequence

The residual selector is simple, but not separable into an obvious proper
congruence projection.  It is a digit-coupled object:

```text
high digit m controls how many low residues r = 0,9,18 survive
```

A producer that only hits the right residues modulo `169`, `43`, `39`, or a
product of small projections will still overselect.  The positive arithmetic
target is now:

```text
produce the base-43 digit coupling t <= (m - 1) mod 4
```

This is a sharper way to say what the square-axis boundary residual needs: not
just frequency mass, not just a local graph, but a rank-3 lower-triangular
digit selector on the exponent comb.

The carry/no-borrow normal form of the same digit selector is recorded in:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/subsqrt_moonshot_laneB_square_axis_no_borrow_digit.md
```
