# Subsqrt Moonshot Lane B Square-Axis Bridge Orbit-Weight Rigidity

## Result

The half-Frobenius gauge-orbit support scan killed smaller `p^39`-stable
bridge fragments.  This checkpoint kills the next coefficient loophole.

Keep the full anti-invariant orbit shape, but assign an independent scalar
weight to each of the `15` raw `p^39` bridge orbits.  Work over the same split
verifier field `F_126751`.

The linear systems are:

```text
orbit variables = 15
orbit sizes     = 2^3, 4^6, 20^6
bridge q-values = 25, 138, 197, 310, 369, 482

trace only:
  equations = 6
  rank = 3
  solution dimension = 12

block/kernel constancy only:
  equations = 107
  rank = 12
  solution dimension = 3

trace + block/kernel constancy:
  equations = 113
  rank = 15
  solution dimension = 0
  unique solution = (1, 1, ..., 1)
```

So the weaker tests really do leave non-uniform coefficient families, but the
producer-facing bridge harness forces the original equal-weight `150`-point
bridge.

## Interpretation

A future sign-local-system candidate cannot replace the bridge by a
non-uniform half-Frobenius orbit coefficient system.  If it satisfies both the
six-point quotient trace and the raw block/kernel relation, its orbit weights
are forced to be the all-ones bridge weights.

This strengthens the current Lane B contract:

- support minimality is forced by the gauge-orbit union gate;
- coefficient minimality is forced by this orbit-weight gate;
- the remaining escape is a genuine arithmetic realization of the equal-weight
  anti-invariant bridge, not a hidden orbit-weight deformation.

## Verification

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_bridge_orbit_weight_rigidity_gate.py
```

Command:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_bridge_orbit_weight_rigidity_gate.py
```

Expected terminal marker:

```text
square_axis_bridge_orbit_weight_rigidity_rows=1/1
```
