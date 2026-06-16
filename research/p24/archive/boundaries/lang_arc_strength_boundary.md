# Lang Arc-Strength Boundary

Date: 2026-06-05

This note records the small actual-CM test for a full Moore-arc strengthening
of the representative Lang/Moore p-unit theorem.

## Tool

Added:

```text
p24/lang_arc_strength_audit.py
```

It reuses the actual CM/Hermitian/Lang construction from the pivot miner, then
enumerates all subsets of size `left_orbit_len` among the transformed
coordinates when the subset count is small enough.

## Results

Pinned row with two length-3 right blocks:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/lang_arc_strength_audit.py \
  --only-D -13319 --only-q 13463 --q-start 13463 --q-stop 13464 \
  --only-m 28 --only-left 7 --only-right 7 --include-linear \
  --max-factor-degree 8 --max-extension-degree 8 \
  --min-left-orbit-len 3 --min-right-orbits 2 \
  --max-subsets 1000 --random-trials 200
```

reported:

```text
left_orbit_len=3
right_orbit_lengths=[3,3]
coordinate_count=6
coordinate_rank=3
subset_total=20
subset_full=20
subset_bad=0
delete_one_leading_full=[1,1]
random_full_arc_count=199/200
```

Pinned row with three length-1 right blocks:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/lang_arc_strength_audit.py \
  --only-D -5444 --only-q 2657 --q-start 2657 --q-stop 2658 \
  --only-m 12 --only-left 3 --only-right 4 --include-linear \
  --max-factor-degree 8 --max-extension-degree 8 \
  --min-left-orbit-len 2 --min-right-orbits 2 \
  --max-subsets 1000 --random-trials 200
```

reported:

```text
left_orbit_len=2
right_orbit_lengths=[1,1,1]
coordinate_count=3
coordinate_rank=2
subset_total=3
subset_full=3
subset_bad=0
delete_one_leading_full=[1,1,1]
random_full_arc_count=200/200
```

## Interpretation

The tested actual-CM rows satisfy the stronger full ordinary Moore-arc
condition.  However, the random baselines are also almost always full arcs, so
this does not yet expose a special CM identity.

The result keeps the LRS/MSRD import plausible but narrows the proof burden:

```text
small-row full arcs are not enough;
one needs a class-field/skew-polynomial identity proving the p24 selected
support minor or a genuine LRS/MSRD block equivalence.
```

The finite support-count implication for the p24 numbers is checked in:

```text
p24/lean/MSRDSupportGate.lean
```
