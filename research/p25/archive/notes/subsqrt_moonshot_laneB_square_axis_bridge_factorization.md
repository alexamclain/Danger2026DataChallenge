# Subsqrt Moonshot Lane B Square-Axis Bridge Factorization

Date: 2026-06-12

## Result

The unique nontrivial inversion-partner repair is not just a legal six-point
row.  It has a unique oriented `S`-edge factorization:

```text
bridge = S * X * Y^-2 * (1 - X^2 * Y^3)
```

where

```text
S = 1 + D + D^2
X = 43
Y = 9
X^2Y^3 = 113
```

The signed support is:

```text
+1 at {25,197,369}   = S * X * Y^-2
-1 at {138,310,482} = S * X^3 * Y
```

Among all oriented factorizations of the form

```text
S * x^base * (1 - x^step),
```

the only match is:

```text
base = 25
step = 113 = X^2Y^3.
```

## Geometry

The step `X^2Y^3` has quotient coordinate:

```text
(right,c) = (2,94)
```

It maps the top-fiber trace-zero partner slice to the bottom-fiber trace-one
anomaly slice:

```text
residue delta = +3
fiber delta   = -6
local h delta = +2
trace bit     = 0 -> 1
```

The bridge traces to six signed points on `C_3 x C_13`:

```text
((0,6), +1), ((0,7), -1)
((1,4), +1), ((1,8), -1)
((2,5), +1), ((2,9), -1)
```

## Fourier Profile

The weighted bridge has exactly three zeros on the `C_507` Fourier side:

```text
{0,169,338}
```

So the bridge has degree zero and the two forced `S`-factor zeros, but no hidden
low-frequency or proper-quotient compression.

## Consequence

The producer target is now an `S`-parallel edge in the specific direction
`X^2Y^3`, not merely any admissible six-point completion.  A useful candidate
must realize this top-to-bottom local edge while preserving the raw
kernel-trivial/block-constant constraints.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_bridge_factorization_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_bridge_factorization_gate.py
```
