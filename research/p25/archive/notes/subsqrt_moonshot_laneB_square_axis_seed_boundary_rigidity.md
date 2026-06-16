# Subsqrt Moonshot Lane B Square-Axis Seed Boundary Rigidity

Date: 2026-06-12

## Result

The six-term no-borrow seed has a minimal first-difference boundary only in
the signed frame directions:

```text
Y     = 9
X     = 43
X + Y = 52
```

For the first-difference operator `(1 - T_d)` on `Z[C_507]`, an exhaustive
scan over all `506` nonzero directions gives:

```text
support size 6:   6 directions
support size 10: 12 directions
support size 12: 488 directions
```

The six minimal directions are exactly:

```text
+Y, +X, +X+Y, -X-Y, -X, -Y
```

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_seed_boundary_rigidity_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_seed_boundary_rigidity_gate.py
```

Observed:

```text
square_axis_seed_boundary_rigidity_rows = 1 / 1
```

## Consequence

This is the modular-unit style version of the seed-frame rigidity result.  If
a producer tries to explain the seed by a small single-direction boundary or
cyclotomic-unit ratio, the direction is forced to be one of the signed
`X/Y/X+Y` frame directions.  Every unrelated direction has boundary support at
least `10`, not `6`.

This sharpens the producer contract:

```text
reject unrelated small-boundary directions;
accept only single-direction boundary explanations tied to signed X/Y/X+Y.
```

The preceding checkpoint is:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/subsqrt_moonshot_laneB_square_axis_seed_frame_rigidity.md
```
