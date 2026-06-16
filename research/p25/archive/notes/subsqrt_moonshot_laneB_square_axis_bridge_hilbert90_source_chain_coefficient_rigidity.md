# Subsqrt Moonshot Lane B Square-Axis Bridge Hilbert-90 Source Chain Coefficient Rigidity

Date: 2026-06-12

## Result

The active Hilbert-90 source-chain support and its rigid `197/310` boundary
direction force the coefficient vector.

For each of the four bridge-compatible source graphs, form the linear map:

```text
coefficients on three source points
  -> first boundary in direction 197 or 310
  -> inversion / Hilbert-90 boundary
  -> signed bridge
```

Over the verifier field `F_2029`, the matrix has:

```text
rank = 3
kernel dimension = 0
```

The unique solutions are exactly the recorded all-equal vectors:

```text
mask 1, direction 197, support [0,172,482]:
  coefficients = (-1,-1,-1)

mask 1, direction 310, support [172,197,369]:
  coefficients = (1,1,1)

mask 6, direction 197, support [138,310,335]:
  coefficients = (-1,-1,-1)

mask 6, direction 310, support [0,25,335]:
  coefficients = (1,1,1)
```

Among the eight sign patterns in `{+/-1}^3`, only the recorded all-equal sign
pattern works for each support.

## Interpretation

The producer target is now:

```text
active C_169 lift (1,18,150)
one of the four source-graph supports
the rigid first-boundary direction 197/310
the recorded all-equal coefficient vector
inversion / Hilbert-90 boundary to the signed bridge
```

This kills the remaining local coefficient escape at this frontier.  A
candidate cannot hit the active support and direction with nonuniform row
weights or a different sign pattern and still recover the bridge.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_bridge_hilbert90_source_chain_coefficient_rigidity_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p25 python3 research/p25/p25_laneB_square_axis_bridge_hilbert90_source_chain_coefficient_rigidity_gate.py
```

Standalone marker:

```text
square_axis_bridge_hilbert90_source_chain_coefficient_rigidity_rows=1/1
```
