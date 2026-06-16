# Subsqrt Moonshot Lane B Square-Axis Bridge Hilbert-90 Source Chain Lift Selection

Date: 2026-06-12

## Result

The `C_13` projective shadow of the curved Hilbert-90 source chain has
thirteen primitive `C_169` lifts, but only one lift appears in the
bridge-compatible optimal support-`3` source-boundary witnesses.

Active lift:

```text
C_13 shadow: (1,2,10)
C_169 lift:  (1,18,150)
```

The support-`3` witness census is:

```text
total optimal support-3 antiderivative witnesses: 8
one-point-per-source-row graph witnesses:        4
bridge-compatible graph witnesses:               4
nonbridge nongraph controls:                     4
```

The four bridge-compatible graph witnesses are exactly:

```text
mask 1, direction 197: -[0]   -[172] -[482]
mask 1, direction 310:  [172] +[197] +[369]
mask 6, direction 197: -[138] -[310] -[335]
mask 6, direction 310:  [0]   +[25]  +[335]
```

All four use projective lift `(1,18,150)`.

The other twelve primitive `C_169` lifts with the same `C_13` shadow have zero
bridge-compatible support-`3` source-graph witnesses in the classified
minimal-potential boundary problem.

## Interpretation

The projective-shape gate said that matching the `C_13` shadow leaves thirteen
possible primitive `C_169` lifts.  This gate sharpens the selection rule:

```text
C_13 shadow (1,2,10)
  -> select nonsplit C_169 lift (1,18,150)
  -> select rigid source-boundary direction 197/310
  -> apply inversion / Hilbert-90 boundary to the bridge
```

The nonbridge support-`3` controls are not source graphs: they do not have one
point in each source row.  So a producer cannot claim success by matching a
support-`3` antiderivative shape that collapses rows or by choosing another
`C_169` lift of the same `C_13` projective shadow.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_bridge_hilbert90_source_chain_lift_selection_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p25 python3 research/p25/p25_laneB_square_axis_bridge_hilbert90_source_chain_lift_selection_gate.py
```

Standalone marker:

```text
square_axis_bridge_hilbert90_source_chain_lift_selection_rows=1/1
```
