# Subsqrt Moonshot Lane B Square-Axis Inversion-Partner Repair

Date: 2026-06-12

## Result

The scalar-balance selected-defect obstruction leaves the three-point diagonal
defect

```text
(right,c) = (0,46), (1,47), (2,48)
value = -1
```

This defect fails because the off-`C=0` inversion sums are not constant.  The
local non-cancelling completion is to add `+1` at the three inversion partners:

```text
(0,123), (1,121), (2,122)
```

In exponent coordinates the completed six-point row is

```text
{25, 138, 197, 310, 369, 482}
```

with signs `-1` on the original anomaly layer and `+1` on the inversion-partner
layer.

## Gate

The completed row has:

```text
degree = 0
row sums = (0,0,0)
c=0 fiber = 0
inversion sums = {0}
selected-defect value identities = pass
raw producer identities = pass
```

The same assertions pass in both the quotient field and the raw split field.
The row is anti-invariant under inversion, so the selected defect is itself.

## Consequence

This is a positive artifact, not a certificate.  It says the fixed diagonal
anomaly can be made value-side legal by pairing it with its inversion-partner
slice, avoiding the dense scalar background and the row-constant selected-kernel
repair.

A viable producer candidate should now be tested for a genuinely mixed source
mechanism that creates this six-point anti-invariant completion, or an equivalent
selected-defect completion.  Candidates that still explain only the original
three-point anomaly, a dense scalar background, a sparse raw section with
unresolved degree, or a row-constant kernel balance remain falsified.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_inversion_partner_repair_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_inversion_partner_repair_gate.py
```
