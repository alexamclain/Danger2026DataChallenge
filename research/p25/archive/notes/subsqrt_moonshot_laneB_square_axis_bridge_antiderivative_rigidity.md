# Subsqrt Moonshot Lane B Square-Axis Bridge Antiderivative Rigidity

Date: 2026-06-12

## Result

The bridge has no alternate equally sparse first-difference explanation.

For the signed bridge

```text
 S * X * Y^-2  -  S * X^3 * Y
```

we solved, for every nonzero direction `d` in `C_507`,

```text
F(q) - F(q + d) = bridge(q).
```

Only two directions admit a support-`3` antiderivative:

```text
d = 113 = X^2Y^3      F = - S * X^3Y
d = 394 = -X^2Y^3     F = + S * X * Y^-2
```

The next-best directions already need support `6`:

```text
d = 197
d = 310
```

Across all `506` nonzero directions:

```text
possible directions   = 468
impossible directions = 38
minimum support       = 3
second support        = 6
```

## Degree-Zero Cost

The two support-`3` directions are primitive one-cycle directions on `C_507`.
Their sparse antiderivatives have degree `-3` and `+3`.

Forcing degree zero over the split field `F_2029` adds a nonzero scalar
background to every quotient point, so the support becomes:

```text
507 / 507
```

## Consequence

A first-difference producer cannot dodge the known bridge geometry.  The only
sparse antiderivative is the original top-to-bottom bridge edge and its
reverse, and it is not degree zero.  A degree-zero first-difference repair
collapses back to the dense scalar-background failure mode.

So the next producer attempt should realize the specific block-constant bridge
as a finite-field identity, structured divisor, or equivalent value-side
completion.  It should not rely on an alternate sparse boundary direction.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_bridge_antiderivative_rigidity_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_bridge_antiderivative_rigidity_gate.py
```
