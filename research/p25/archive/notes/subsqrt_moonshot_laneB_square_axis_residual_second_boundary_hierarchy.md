# Subsqrt Moonshot Lane B Square-Axis Residual Second-Boundary Hierarchy

Date: 2026-06-12

## Result

For the full `18`-point residual, an exhaustive scan of all unordered
two-direction boundaries

```text
(1 - T_a)(1 - T_b)
```

over `C_507` gives:

```text
direction pairs checked: 128271
minimal support: 8
minimal pairs: 8
```

The minimal pairs are exactly:

```text
±D paired with ±X or ±(X + Y)
```

The signed `Y` direction is not minimal at this residual level; `±D` paired
with `±Y` has support `11`.  This matches the quotient relation `D^3 = Y`:
the outer `D` boundary has already collapsed one `Y`-direction boundary onto
the seed.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_residual_second_boundary_hierarchy_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_residual_second_boundary_hierarchy_gate.py
```

Observed:

```text
square_axis_residual_second_boundary_hierarchy_rows = 1 / 1
```

## Consequence

This is the two-direction boundary version of the residual/seed hierarchy:

```text
outer S-orbit direction D first;
then non-Y signed seed-frame directions X and X+Y.
```

This sharpens the producer contract:

```text
reject full-residual support-8 second-boundary explanations unless one
direction is ±D and the other is ±X or ±(X+Y);
reject treating ±Y as a minimal second-boundary partner at the residual level.
```

The preceding checkpoint is:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/subsqrt_moonshot_laneB_square_axis_residual_boundary_hierarchy.md
```
