# Subsqrt Moonshot Lane B Square-Axis Scalar-Balance Escape

Date: 2026-06-12

## Result

The two-`S`-orbit repair is impossible, but there is one scalar-balanced
representative of the anomaly correction:

```text
-1_{S*X^3Y} + (3/507) * 1_{C_507}
```

In the raw split field `F_126751`,

```text
3/507 = 126001.
```

So the scalar-balanced vector has two values:

```text
126000 on {138, 310, 482}
126001 on the other 504 quotient classes
```

It has degree zero, and removing the scalar background recovers exactly the
three-point anomaly orbit.

## Cost Of The Escape Hatch

The scalar-balanced representative is completely nonlocal:

```text
quotient support = 507 / 507
raw block lift support = 12675 / 12675
kernel modes = {0}
```

It is compatible with the raw `D^3 = Y` block-constant relation, but only by
becoming dense on every quotient class and every raw block.

Fourier also does not make it cheap:

```text
weighted Fourier zeros = {0, 169, 338}
```

The new zero at `0` is just degree zero; the nonzero-frequency profile is still
the same `S`-orbit profile.

## Producer Consequence

The q-binomial path is not dead solely because the anomaly has nonzero degree:
scalar balancing is a real escape hatch.  But it is expensive in a different
way.  A viable producer using the Lucas/q-binomial support must explain a
dense scalar background while still returning the exact all-one raw `Y[e]`
contract after normalization.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_scalar_balance_escape_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_scalar_balance_escape_gate.py
```
