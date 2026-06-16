# P25 Lane B: Robert KSY Kubert-Lang D-Slice Weight Rigidity

Updated: 2026-06-13 17:15 PDT

## Purpose

The anti-invariant selector-rigidity gate fixes the quotient center and `D`
step up to unavoidable orientation/reversal symmetries.

This gate fixes that geometry and asks whether the three `D` slices can carry
nontrivial weights.

## Result

For raw:

```text
C = (47,28)
K = (57,0)
D = (22,3)
offsets = -1,0,1
```

the three K-traced slice footprints are disjoint:

```text
slice supports        = 100,100,100
pairwise intersections = 0,0,0
union support          = 300
```

This proves integer-weight rigidity for the exact theta2 footprint: because
the supports do not overlap, every slice coefficient is visible independently.

## Bounded Scan

As an audit, all `5^3=125` triples with weights in `{-2,-1,0,1,2}` were
checked.

The only exact accepted matches are:

```text
(-1,-1,-1) -> theta2,    recovered sign +1
( 1, 1, 1) -> theta2^-1, recovered sign -1
```

No missing slice, doubled slice, or mixed-sign slice passes the theta2
candidate harness.

## Local Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_d_slice_weight_rigidity_gate.py
```

Expected marker:

```text
robert_ksy_theta2_kubert_lang_d_slice_weight_rigidity_rows=1/1
```

## Interpretation

The moonshot theorem target cannot be weakened to a weighted subproduct on the
accepted `C,D,K` geometry.  It must produce the full equal-weight
length-three `D` segment, up to global orientation.
