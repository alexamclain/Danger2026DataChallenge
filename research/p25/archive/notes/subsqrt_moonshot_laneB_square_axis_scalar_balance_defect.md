# Subsqrt Moonshot Lane B Square-Axis Scalar-Balance Defect

Date: 2026-06-12

## Result

The scalar-balanced q-binomial anomaly is degree-zero, but it is not invisible
to the Lane B value-side contract.

The scalar background cancels under

```text
selected_defect(r,c) = g(r,c) - g(r,0)
```

so the selected defect of the scalar-balanced correction is exactly the
selected defect of the negative anomaly orbit.  In quotient coordinates the
visible defect is:

```text
(right,c) = (0,46), (1,47), (2,48)
```

with value `-1` on all three points.

## Failure Mode

This three-point diagonal defect:

```text
row sums = (-1, -1, -1)
c=0 fiber = 0
inversion sums = {0, -1}
```

So it fails the selected-defect value identities and the raw producer
identities.  The same result holds in both the quotient field and the raw split
field.

## Producer Consequence

Scalar balancing repairs degree, but it does not put the q-binomial anomaly in
a harmless homogeneous kernel.  A viable producer must cancel or absorb the
three-point diagonal defect before the selected-defect/value-side test, not
merely add a dense scalar background.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_scalar_balance_defect_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_scalar_balance_defect_gate.py
```
