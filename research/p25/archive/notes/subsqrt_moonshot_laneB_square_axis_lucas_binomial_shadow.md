# Subsqrt Moonshot Lane B Square-Axis Lucas-Binomial Shadow

Date: 2026-06-12

## Result

The square-axis no-borrow seed is not just an arbitrary six-term subset.  It
is exactly the Lucas/binomial support

```text
selected(h,t) = 1 iff binom(h,t) is nonzero mod 3
```

for `h,t in {0,1,2}`.  Equivalently, with `X = x^43`, `Y = x^9`,

```text
seed_support = supp X * (1 + X*(1+Y) + X^2*(1+Y)^2)
```

This is a positive producer clue: the no-borrow triangle can be read as a
tiny symmetric-power / Lucas-support shadow.

## Coefficient Obstruction

The honest binomial coefficient vector on the seed is

```text
[1, 1, 1, 1, 2, 1]
```

with the coefficient anomaly at

```text
X^3 * Y = 138
```

and, after multiplying by `S = 1 + x^172 + x^344`, at

```text
138, 310, 482
```

Thus the support matches the target residual, but the naive binomial
coefficient shadow does not equal the all-one residual payload.  The anomaly
cannot be removed by a global scalar, row/column scaling, or separable
`h/t/S`-layer rescaling: the equations force `2 = 1`; in characteristic `2`
the anomalous coefficient vanishes and the support is wrong.

## Producer Consequence

This sharpens the next search:

```text
use the Lucas/no-borrow support as a positive hint;
reject naive symmetric-power or eta shadows unless they include a genuinely
mixed coefficient twist that flattens the coefficient-2 orbit.
```

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_lucas_binomial_shadow_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_lucas_binomial_shadow_gate.py
```
