# Lane B: Bridge Hilbert-90 Source-Chain Corner C169 Lift Selector

Date: 2026-06-12

Gate:
`research/p25/p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_c169_lift_selector_gate.py`

## Result

The cleaner corner formulation now directly selects the active `C_169` lift.

Among the thirteen primitive `C_169` projective lifts of the same `C_13`
shadow `(1,2,10)`, the row-balanced half-bridge corner graphs land only on:

```text
(1,18,150)
```

The two corner graph witnesses are:

```text
center=122, unit=1,   sign=+1: q=(0,172,482), c169=(0,3,144),   diffs=(3,141,25)
center=385, unit=506, sign=-1: q=(0,25,335),  c169=(0,25,166),  diffs=(25,141,3)
```

Both have projective `C_169` shape `(1,18,150)`.  All twelve other lifts of
the same `C_13` shadow have zero row-balanced half-bridge corner witnesses.

## Interpretation

The producer target has tightened again:

```text
half-bridge corner + C_3 row balance
  => active C_169 lift (1,18,150)
```

This means the active lift no longer needs to be explained using the full
minimal-potential boundary search.  The remaining hard part is lower in the
producer stack: realize the raw `K` trace / block-constant lift and account
for the unchanged Kummer cost.

Standalone marker:

```text
square_axis_bridge_hilbert90_source_chain_corner_c169_lift_selector_rows=1/1
```
