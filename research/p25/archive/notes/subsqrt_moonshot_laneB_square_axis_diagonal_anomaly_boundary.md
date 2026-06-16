# Subsqrt Moonshot Lane B Square-Axis Diagonal-Anomaly Boundary

Date: 2026-06-12

## Result

The selected-defect-visible anomaly

```text
A = (1 + D + D^2) * X^3 * Y = {138, 310, 482}
```

is a length-three segment in the `D` direction.  Since `D^3 = Y` on the
quotient, its `D` boundary telescopes:

```text
(1 - D) A = X^3*Y - X^3*Y^2.
```

In coordinates this is the two-point edge:

```text
+ (q=138, right=0, c=46, h=2, s=0, t=1, fiber=3)
- (q=147, right=0, c=49, h=2, s=0, t=2, fiber=3)
```

The opposite boundary similarly connects the `t=0` and `t=1` bottom-fiber
slices at `s=2`.

## Rigidity

Among all `506` nonzero first-difference directions on the anomaly:

```text
support 2: directions +D, -D
support 4: directions +2D, -2D
support 6: all other 502 directions
```

So the anomaly has a unique minimal boundary frame: the signed `D` direction.

## Producer Consequence

This does not solve the coefficient problem, but it gives a sharper positive
target than a generic "cancel the diagonal defect" instruction.

A plausible local/source correction would have to behave like a mixed
`D`-antiderivative of a local `Y` edge in the `h=2` bottom boundary fiber,
while still satisfying the raw trace and selected-defect contracts.  Candidates
that cannot see the signed `D` direction, or that only produce row/C/additive
corrections, should be killed quickly.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_diagonal_anomaly_boundary_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_diagonal_anomaly_boundary_gate.py
```
