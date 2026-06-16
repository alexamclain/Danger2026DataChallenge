# Subsqrt Moonshot Lane B Square-Axis Bridge Signed Product Rigidity

Date: 2026-06-12

## Result

The bridge has no unrelated signed `2 x 3` product explanation.

We enumerated every normalized collision-free signed product in `Z[C_507]`:

```text
(1 + epsilon*x^d) * (three signed points)
```

with `epsilon = +/-1`, `d != 0`, and the three-point support drawn from the
bridge support.  Exactly two normalized products match the signed bridge:

```text
(1 - x^113) * (+S * X * Y^-2)
(1 - x^394) * (-S * X^3 * Y)
```

These are the same product, seen in the forward and reverse bridge directions.

## Consequence

A small signed-product producer cannot use an unrelated `2 x 3` decomposition.
The only product structure is the known one:

```text
S layer times the top-to-bottom bridge edge.
```

So the producer target remains the specific `S`-parallel edge

```text
S * X * Y^-2 * (1 - X^2Y^3),
```

not an alternate signed product or hidden rank-one factorization.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_bridge_signed_product_rigidity_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_bridge_signed_product_rigidity_gate.py
```
