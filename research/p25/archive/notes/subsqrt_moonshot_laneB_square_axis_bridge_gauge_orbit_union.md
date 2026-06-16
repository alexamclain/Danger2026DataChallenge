# p25 Lane B Square-Axis Bridge Gauge-Orbit Union

## Question

The half-Frobenius raw-gauge law says `p^39` moves the bridge by a nontrivial
raw permutation:

```text
(right,c) -> (2*right,-c).
```

Could a smaller `p^39`-stable fragment replace the full `C_25` kernel trace in
a sign-local-system producer?

## Result

The answer is no for any fragment that is supposed to pass the bridge harness.

The `p^39` action splits the `150` raw bridge points into:

```text
3 orbits of size 2
6 orbits of size 4
6 orbits of size 20
```

Every orbit touches exactly one positive/negative quotient pair.  All
`32767` nonempty unions of these `15` orbits were scanned.

Only the full union is:

```text
raw_support = 150
quotient_support = 6
trace_correct = true
block_constancy_hits = 507
kernel_modes = (0,)
raw_relation_mismatches = 0
target_exact = true
harness_ok = true
```

There are `7` kernel-trivial/block-constant/raw-relation-compatible unions.
They are exactly:

```text
3 proper support-50 quotient-pair subbridges
3 proper support-100 two-pair subbridges
1 full support-150 bridge
```

The six proper kernel-trivial unions fail the six-point bridge trace because
their quotient support is only `2` or `4`.

All other proper gauge-stable unions expose nontrivial `C_25` kernel modes or
raw relation failures.

## Interpretation

Gauge stability alone does have small fragments.  That is the useful warning.

But bridge-harness acceptance forces the full `C_25` trace over all three
positive/negative quotient pairs.  A sign-local-system producer cannot replace
the primitive bridge by one small Frobenius orbit, or by a proper union of
orbits, unless it supplies an additional mechanism that restores the missing
quotient pairs and the exact trace.

This tightens the previous raw-gauge checkpoint:

- a sparse kernel section is not stable;
- a proper gauge-stable fragment is not trace-correct;
- the full `150`-point bridge is the unique accepted gauge-stable union.

## Gate

```sh
env PYTHONDONTWRITEBYTECODE=1 \
  python3 research/p25/p25_laneB_square_axis_bridge_gauge_orbit_union_gate.py
```

Expected line:

```text
square_axis_bridge_gauge_orbit_union_rows=1/1
```
