# Subsqrt Moonshot Lane B Square-Axis Residual Boundary Hierarchy

Date: 2026-06-12

## Result

The full `18`-point square-axis residual has a different first-boundary
hierarchy from the six-term seed because of the outer `S` orbit factor.

Exhausting all `506` nonzero directions in `C_507` gives:

```text
support size 6:   2 directions
support size 12:  2 directions
support size 18: 10 directions
support size 36: 444 directions
```

The only support-`6` directions are:

```text
D  = 172
-D = 335
```

The signed seed-frame directions:

```text
±Y, ±X, ±(X + Y)
```

appear at support `18` on the full residual, not at the absolute minimum.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_residual_boundary_hierarchy_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_residual_boundary_hierarchy_gate.py
```

Observed:

```text
square_axis_residual_boundary_hierarchy_rows = 1 / 1
```

## Consequence

This prevents a bad transfer from the seed-only boundary gates to the full
residual.  A producer must explain the residual in the correct order:

```text
outer S-orbit boundary first;
inner no-borrow seed frame second.
```

This sharpens the producer contract:

```text
reject full-residual first-boundary explanations that ignore the S orbit;
reject claims that seed-frame directions are the minimal full-residual
first-boundary directions;
accept only explanations where the D/S orbit is the outer minimal boundary.
```

The preceding checkpoint is:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/subsqrt_moonshot_laneB_square_axis_seed_second_boundary_rigidity.md
```
