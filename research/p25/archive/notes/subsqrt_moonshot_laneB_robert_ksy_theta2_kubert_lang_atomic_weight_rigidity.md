# P25 Lane B: Robert KSY Kubert-Lang Atomic Weight Rigidity

Updated: 2026-06-13 17:20 PDT

## Purpose

The selector and `D`-slice rigidity gates force the accepted raw geometry:

```text
C = (47,28)
K = (57,0)
D = (22,3)
A = C + jD + kK,  j=-1,0,1; k=0..24
```

This gate allows an independent weight on every one of the `75` atoms and asks
whether any nonuniform `K` trace or atom weighting can still produce the exact
theta2/theta2-inverse payload.

## Result

Each atom contributes a disjoint normalized-y footprint:

```text
atom count                    = 75
support per atom              = 4
pairwise intersecting atoms   = 0
union support                 = 300
rank from disjoint support    = 75
nullity                       = 0
```

Since the supports are disjoint, the exact theta2 target reads off every atom
weight independently.

Solutions:

```text
theta2^-1 target -> all 75 weights are +1
theta2 target    -> all 75 weights are -1
```

Controls rejected:

```text
missing one atom
alternating K-layer weights
```

## Local Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_atomic_weight_rigidity_gate.py
```

Expected marker:

```text
robert_ksy_theta2_kubert_lang_atomic_weight_rigidity_rows=1/1
```

## Interpretation

The moonshot theorem target must produce the exact equal-weight K-traced
anti-invariant product, or an exactly equivalent accepted theta2 payload.

There is no hidden nonuniform `K` trace, missing-factor, or atomic-weight null
direction inside the accepted finite geometry.
