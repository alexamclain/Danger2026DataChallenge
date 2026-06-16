# Tower Kummer Glue Complexity Boundary

Date: 2026-06-06

This note tests the cross-orbit glue invariants introduced by:

```text
p24/relative_kummer_multi_orbit_ambiguity_gate.py
p24/lean/KummerCrossOrbitGlueGate.lean
```

For a multi-orbit prime relative layer, the corrected Kummer payload includes
invariants such as

```text
G_a = T_a / T_1^a
```

for one representative `a` of each primitive-character Frobenius orbit other
than the orbit of `1`.  These invariants restore child-polynomial selection in
finite algebra.  This boundary asks whether they also have a low-degree
formula in the parent period in small actual-CM towers.

## Scan

The scan is:

```text
p24/tower_kummer_glue_complexity_scan.py
```

Cheap harness-sized run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/tower_kummer_glue_complexity_scan.py \
  --max-cases 3 --max-h 100 --q-stop 80000 \
  --max-rows-per-case 4 --summary-only
```

reported:

```text
rows=3
good_distinct_nonzero_rows=3
glue_coordinate_slots=8
full_degree_coordinates=8
low_degree_coordinates=0
low_bm_coordinates=0
glue_values=21
full_frobenius_degree_glue_values=21
proper_frobenius_descent_glue_values=0
nonsplit_glue_values=3
nonsplit_full_frobenius_degree_glue_values=3
nonsplit_proper_frobenius_descent_glue_values=0
zero_denominator_rows=0
max_interp_degree_seen=2
```

A larger parent-count-forced run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/tower_kummer_glue_complexity_scan.py \
  --max-cases 5 --min-parent 4 --max-parent 30 \
  --max-h 220 --q-stop 180000 --max-rows-per-case 4
```

reported:

```text
rows=5
good_distinct_nonzero_rows=5
glue_coordinate_slots=15
full_degree_coordinates=15
low_degree_coordinates=0
low_bm_coordinates=0
glue_values=45
full_frobenius_degree_glue_values=45
proper_frobenius_descent_glue_values=0
nonsplit_glue_values=13
nonsplit_full_frobenius_degree_glue_values=13
nonsplit_proper_frobenius_descent_glue_values=0
zero_denominator_rows=0
max_interp_degree_seen=4
avg_interp_degree_over_rows=3.200000
```

The printed rows include multi-orbit `r=5` and `r=7` layers, including cases
with four and six primitive-character Frobenius orbits.

## Consequence

This supports the corrected selected-chain theorem shape:

```text
Kummer orbit data + cross-orbit glue invariants
```

is a valid finite payload, but the glue invariants should not be expected to
drop out as low-degree functions of the parent period or descend to smaller
cyclotomic subfields in nonsplit rows.  The producer theorem must construct
the embedded glue objects themselves, or construct the selected degree-211
child polynomial / full relative morphism directly.

In p24 terms, this keeps the Kummer-with-glue surface far below sqrt.  The
five glue objects are extension-field invariants; with conservative base-field
serialization each costs the `211`-layer Frobenius orbit degree `35`, so:

```text
3107811 + 5 extension objects = 3107816 extension-object slots
3107811 + 5*35 base coordinates = 3107986 base-field slots
3107986 / sqrt(p) ~= 3.107986e-6
```

but does not by itself produce the missing class-set-free arithmetic data.
