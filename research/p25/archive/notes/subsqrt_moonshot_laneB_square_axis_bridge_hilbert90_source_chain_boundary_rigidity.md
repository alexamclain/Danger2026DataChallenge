# Subsqrt Moonshot Lane B Square-Axis Bridge Hilbert-90 Source Chain Boundary Rigidity

Date: 2026-06-12

## Result

The curved three-point Hilbert-90 source chain has a rigid first-boundary
orientation.  For each of the four bridge-compatible witnesses, all `506`
nonzero first-boundary directions were scanned.

Universal distribution:

```text
support 4: 6 directions
support 6: 500 directions
```

The six sparse directions are exactly the pair-difference directions of the
three-point chain:

```text
q directions: 25, 172, 197, 310, 335, 482
source coords:
  25  -> (1,25)
  172 -> (1,3)
  197 -> (2,28)
  310 -> (1,141)
  335 -> (2,166)
  482 -> (2,144)
```

But only the recorded primitive direction recovers the four-block Hilbert-90
potential and then the signed bridge after inversion:

```text
mask 1, chain -[0]-[172]-[482]:
  only direction 197 works

mask 1, chain [172]+[197]+[369]:
  only direction 310 works

mask 6, chain -[138]-[310]-[335]:
  only direction 197 works

mask 6, chain [0]+[25]+[335]:
  only direction 310 works
```

For the canonical witness:

```text
A = -[0] - [172] - [482]
(1 - T_197)A = -[0] + [197] + [369] - [482]
inversion_boundary((1 - T_197)A) = bridge
```

The other five sparse directions, including the visible `D` directions
`172/335` and the endpoint directions `25/482`, miss the signed bridge.  All
support-`6` directions also miss the bridge.

## Interpretation

The producer target is now a three-stage rigid object:

```text
curved three-point source graph A
recorded first boundary (1 - T_197)A or (1 - T_310)A
inversion / Hilbert-90 boundary to the signed bridge
```

This kills an easy escape: a candidate cannot realize the right curved
three-point support but take a different sparse first boundary, such as a
`D`-segment edge or endpoint edge.  The orientation is part of the target.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_bridge_hilbert90_source_chain_boundary_rigidity_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p25 python3 research/p25/p25_laneB_square_axis_bridge_hilbert90_source_chain_boundary_rigidity_gate.py
```

Standalone marker:

```text
square_axis_bridge_hilbert90_source_chain_boundary_rigidity_rows=1/1
```
