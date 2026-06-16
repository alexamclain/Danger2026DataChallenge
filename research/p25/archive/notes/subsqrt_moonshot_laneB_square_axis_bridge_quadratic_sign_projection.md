# Subsqrt Moonshot Lane B Square-Axis Bridge Quadratic Sign Projection

## Result

The twisted-orientation route requires a quadratic sign local system

```text
alpha^(p^39) = -alpha.
```

This checkpoint records what happens if we try to remove that sign system by
ordinary trace or by taking a base-field invariant projection such as
coefficient-square / norm / absolute value.

For the accepted signed bridge:

```text
ordinary p^39 trace on quotient = 0
ordinary p^39 trace on raw lift = 0
```

Every one of the `15` raw `p^39` orbits is sign-balanced:

```text
3 orbits:  1 positive, 1 negative
6 orbits:  2 positive, 2 negative
6 orbits: 10 positive, 10 negative
```

The invariant projection that forgets the quadratic sign is the unsigned hull.
It is tempting because it preserves several harness-adjacent invariants:

```text
raw support = 150
quotient support = 6
block constancy = 507/507
kernel modes = {0}
raw D^3=Y relation mismatches = 0
mixed quotient characters = 336
```

But it is not the bridge:

```text
quotient trace = +1 on all six bridge cells
integer degree = 150
normalized quotient degree = 6
trace_correct = false
bridge_harness_ok = false
```

## Interpretation

The quadratic sign twist cannot be eliminated by a base-field invariant
projection.  Ordinary trace kills the signed bridge; coefficient-square/norm
forgets the orientation and gives the unsigned hull.

A serious arithmetic producer must therefore realize the anti-invariant line
itself, or give an equivalent nonsplit identity.  It is not enough to produce
a semilinearly fixed object and then pass to an invariant scalar shadow.

## Verification

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_bridge_quadratic_sign_projection_gate.py
```

Command:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_bridge_quadratic_sign_projection_gate.py
```

Expected terminal marker:

```text
square_axis_bridge_quadratic_sign_projection_rows=1/1
```
