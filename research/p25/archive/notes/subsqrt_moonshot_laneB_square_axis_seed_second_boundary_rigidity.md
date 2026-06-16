# Subsqrt Moonshot Lane B Square-Axis Seed Second-Boundary Rigidity

Date: 2026-06-12

## Result

For the two-direction boundary operator

```text
(1 - T_a)(1 - T_b)
```

on the six-term seed in `Z[C_507]`, an exhaustive scan over all unordered
nonzero direction pairs gives:

```text
direction pairs checked: 128271
minimal support: 8
minimal pairs: 12
```

The `12` minimal pairs are exactly the distinct signed pairs from:

```text
±Y, ±X, ±(X + Y)
```

excluding same-direction and opposite-direction pairs.  Every off-frame pair
has support at least `10`.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_seed_second_boundary_rigidity_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_seed_second_boundary_rigidity_gate.py
```

Observed:

```text
square_axis_seed_second_boundary_rigidity_rows = 1 / 1
```

## Consequence

This extends the modular-unit style falsifier from one direction to two.  A
candidate producer that tries to explain the seed as a small product or ratio
of two directional unit boundaries is forced back onto the signed
`X/Y/X+Y` frame.

This sharpens the producer contract:

```text
reject off-frame two-direction boundary explanations;
reject same/opposite frame pairs as minimal second-boundary explanations;
accept only distinct signed X/Y/X+Y frame pairs for support-8 boundaries.
```

The preceding checkpoint is:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/subsqrt_moonshot_laneB_square_axis_seed_boundary_rigidity.md
```
