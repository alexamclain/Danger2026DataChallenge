# Subsqrt Moonshot Lane B Square-Axis Diagonal-Anomaly Rigidity

Date: 2026-06-12

## Result

The scalar-balance selected-defect obstruction is now localized inside the
square-axis residual geometry.

The visible defect

```text
(right,c) = (0,46), (1,47), (2,48)
```

is exactly the single group-ring `S` layer

```text
(1 + D + D^2) * X^3 * Y = {138, 310, 482}.
```

Equivalently, it is the fixed `h=2, t=1` middle slice of the bottom boundary
fiber:

```text
q = 43*(h+1) + 172*s + 9*t
h = 2
t = 1
s = 0,1,2
```

In local square-axis coordinates this is:

```text
fiber b = 3
residues a = 7,8,9
right = 0,1,2
c - right = 46 mod 169
residue - right = 7 mod 13
```

## Rigidity

The defect is not row-only, C-only, or row-plus-column separated.  On the three
active columns its mixed second differences are:

```text
{-2, -1, 1}
```

so the additive row-plus-column explanation is nonzero in both the quotient
field and the raw split field.

It is also not the pullback of a subset along any proper divisor modulus of
`507`; the smallest proper-divisor pullback containing the same residues is
size `9` at modulus `169`, not size `3`.

## Producer Consequence

The coefficient problem has sharpened again.  A viable producer does not merely
need to "fix the q-binomial coefficient"; it must cancel or absorb the specific
`h=2, t=1` middle slice of the `h=2` boundary row, while preserving the raw
selected-defect and Kummer/trace contracts.

This makes the next plausible positive search target a genuinely mixed
local/source correction for the fixed `S*X^3Y` slice.  Row corrections, C-axis
corrections, row-plus-column coboundaries, and proper congruence pullbacks are
now ruled out as explanations for this leftover defect.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_diagonal_anomaly_rigidity_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_diagonal_anomaly_rigidity_gate.py
```
