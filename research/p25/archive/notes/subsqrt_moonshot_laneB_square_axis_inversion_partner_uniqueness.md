# Subsqrt Moonshot Lane B Square-Axis Inversion-Partner Uniqueness

Date: 2026-06-12

## Result

The six-point inversion-partner repair is unique among equal-weight local
`S`-layer completions.

Starting from the illegal anomaly correction

```text
- S * X^3 * Y
```

we tested every possible repair layer

```text
+ S * x^base,  base = 0..506.
```

Only two layers pass the selected-defect and raw-producer identities in both
the quotient and raw split fields:

```text
base = 138 = X^3Y      trivial cancellation
base = 25  = X Y^-2    nontrivial inversion-partner completion
```

Thus the only nontrivial equal-weight `S`-layer completion is:

```text
completion = S * X * Y^-2 * (1 - X^2 * Y^3)
```

with q-support:

```text
partner layer = {25,197,369}
anomaly layer = {138,310,482}
```

## Geometry

The anomaly layer is the bottom-fiber trace-one slice:

```text
residues = 7,8,9
fiber = 3
local h = 2
trace bit = 1
```

The partner layer is the top-fiber trace-zero slice:

```text
residues = 4,5,6
fiber = 9
local h = 0
trace bit = 0
```

The shift from partner to anomaly is fixed:

```text
X^2 * Y^3 = 113
```

The completed six-point row still has signed `D` as its only minimal
first-boundary direction; the minimum boundary support is `4`.

## Consequence

The producer target is no longer merely "cancel the anomaly."  A local
equal-weight producer must explain why the bottom trace-one anomaly slice is
paired with the top trace-zero inversion slice.  The useful target is the
anti-invariant bridge

```text
S * X * Y^-2 * (1 - X^2 * Y^3),
```

not a dense scalar balance, not a row-constant selected-kernel balance, and not
an arbitrary second `S` layer.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_inversion_partner_uniqueness_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_inversion_partner_uniqueness_gate.py
```
