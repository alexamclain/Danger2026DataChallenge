# Kummer Orbit Minpoly Producer Frontier

Date: 2026-06-06

This note sharpens the selected-chain theorem target after the payload gate.
The useful Kummer object is not a single orbit norm.  It is the Frobenius
minimal polynomial, or equivalently enough orbit data to identify the Kummer
power itself up to Frobenius.

## Candidate Theorem

For a prime relative layer `L < K` of degree `r`, with child periods

```text
y_u = sum_{l in L} j_{a u l},
```

define relative resolvents and Kummer powers:

```text
T_s(aK) = sum_u zeta_r^(s u) y_u
K_s(aK) = T_s(aK)^r.
```

The selected-chain producer can be restated as:

```text
construct the Frobenius orbit/minimal-polynomial data for the embedded K_s
values in the 157 and 211 layers, plus one selected degree-3107441 recovery
polynomial, without enumerating the h CM roots.
```

For p24 this means:

```text
157 layer: one Frobenius orbit of 156 primitive Kummer powers
211 layer: six Frobenius orbits of 35 primitive Kummer powers
           plus five cross-orbit glue invariants, or selected child data
informative field slots: 156 + 210 = 366
211-layer phase glue: 5 invariant ratios such as T_a/T_1^a if using Kummer powers
```

The forced trace coefficient in each child polynomial is supplied by the
parent.  Thus:

```text
top degree-2 slots
+ 2 forced child-trace slots
+ 366 informative Kummer orbit slots
+ 3107441 selected recovery slots
= 3107811 selected-chain slots.
```

If the five glue invariants are charged as extension-field objects, the
surface becomes:

```text
3107811 + 5 = 3107816
```

For conservative base-field serialization, each glue object has the
`211`-layer Frobenius orbit degree `ord_211(p)=35`, so the verifier-facing
surface becomes:

```text
3107811 + 5*35 = 3107986
```

which is still far below `sqrt(p)`.  The finite implication and both counts
are Lean-checked in:

```text
p24/lean/KummerCrossOrbitGlueGate.lean
```

Lean checks this equivalence in:

```text
p24/lean/PhaseLiftedTowerPayloadGate.lean
```

## Small-Row Evidence

I reran the three relevant cheap audits.

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/relative_kummer_orbit_norm_toy.py
```

In the `D=-5000`, `h=30=2*3*5`, relative-degree-3 toy:

```text
parent=0:
  norm_descending_polynomial_count=210
  trace_norm_descending_polynomial_count=1
parent=1:
  norm_descending_polynomial_count=210
  trace_norm_descending_polynomial_count=1
```

Interpretation:

```text
Norm(K) alone is p-unit/nonzero data, not selected-child data.
Trace(K) plus Norm(K), the degree-2 Frobenius minpoly of K, identifies the
unordered child polynomial in this toy.
```

The Kummer complexity scan remains negative for low-degree parent formulas:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/tower_kummer_phase_complexity_scan.py \
  --max-cases 4 --max-h 80 --q-stop 60000 \
  --max-rows-per-case 4 --summary-only
```

It reported:

```text
good_distinct_rows=8
kummer_coordinate_slots=21
full_degree_coordinates=21
low_degree_coordinates=0
low_bm_coordinates=0
```

So the Kummer minpoly target is a normal form for phase, not evidence for a
low-degree collapse in the parent period.

The same is now true for the corrected cross-orbit glue invariants.  The scan

```text
p24/tower_kummer_glue_complexity_scan.py
p24/tower_kummer_glue_complexity_boundary.md
```

found `8/8` full-degree glue coordinates in a cheap run and `15/15`
full-degree glue coordinates in a parent-count-forced run, with no low-degree
or low-BM coordinates.  Its Frobenius descent audit also found `21/21` and
`45/45` glue values at full Frobenius degree, with `0` proper descents
(`3/3` and `13/13` in the nonsplit subrows).  Thus `T_a/T_1^a` is the right
finite glue payload, not a cheap parent-period formula or smaller-subfield
object.

The abstract-to-embedded pairing scan also remains negative below the generic
interpolation threshold:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/abstract_embedded_graph_relation_scan.py \
  --degrees 1,1 1,2 2,1 --random-controls 8 --random-trials 80
```

It reported:

```text
degA=1 degY=1: actual_success_matchings=0, random=0/8
degA=1 degY=2: actual_success_matchings=120, random=8/8
degA=2 degY=1: actual_success_matchings=120, random=8/8
```

So abstract quotient roots still do not supply the embedded pairing.  The
first relations that exist are generic interpolation artifacts.

I also tested a prerequisite suggested by the abstract-to-embedded Kummer
pairing idea:

```text
p24/abstract_tower_fiber_map_scan.py
p24/abstract_tower_fiber_map_boundary.md
p24/abstract_tower_morphism_payload_boundary.md
```

In two fundamental `h=30`, `a=5`, `r=3`, `n=2` rows (`D=-671` and `D=-815`),
the degree-15 abstract quotient roots did not admit a balanced rational map of
degree `1`, `2`, or `3`, nor a balanced polynomial map of degree `1` through
`7`, down to the degree-5 abstract parent roots.  Thus even the abstract
relative fibers are not exposed by a cheap root-set map.

## Consequence

The next theorem is no longer:

```text
find any Kummer compression.
```

It is specifically:

```text
construct the embedded Frobenius minpolys/orbits of the relative Kummer powers
class-set-free.
```

This theorem needs one correction.  It would produce the same finite
selected-chain verifier surface as the child-polynomial version only in a
one-Frobenius-orbit relative layer.  The p24 `157` layer has this shape, but
the `211` layer does not: `ord_211(p)=35`, so the primitive characters split
into six Frobenius orbits.

The multi-orbit ambiguity/glue gate

```text
p24/relative_kummer_multi_orbit_ambiguity_gate.py
p24/relative_kummer_multi_orbit_ambiguity_gate.md
```

shows that independent root-of-unity phases on the six `211`-layer Kummer
orbits still descend to base-field child fibers and need not be one global
cyclic relabeling.  Modulo the global cyclic shift, the formal p24 ambiguity
is

```text
211^(6-1) = 418227202051.
```

So the corrected Kummer theorem is:

```text
construct the embedded 157-layer Kummer orbit, and for the 211 layer construct
either selected child-polynomial data, full relative morphism data, or the six
Kummer orbits plus explicit cross-orbit phase glue such as `T_a/T_1^a` for the
five non-base primitive-character Frobenius orbits.
```

Kummer powers remain more class-field-shaped because they are invariant under
cyclic relabeling inside one Frobenius orbit, but in the 211 layer they are
not by themselves a seedless child selector.

The theorem must also carry the relative fiber structure.  A pair of split
abstract quotient root sets is insufficient before any embedded comparison is
attempted.

If direct selected-chain Kummer data is too hard, the allowed larger theorem is
to construct the full embedded relative morphism.  Its p24 payload is:

```text
2*157 + 314*211 = 66568
```

before the selected recovery fiber, and Lean checks that the resulting full
relative-table surface is still sub-sqrt.

The complement-generator audit also rules out the easiest Hecke-walk version
of this theorem: no signed split-prime-power word of norm at most `66254`
inside the balanced complement `K` has order `2`, `157`, `211`, `314`, `422`,
`33127`, or `66254`.

## Pass/Fail Rule For Future Computation

A proposed computation helps only if it distinguishes one of these:

```text
pass:
  produces embedded K_s Frobenius minpolys/orbits together with the needed
  211-layer cross-orbit phase glue, or proves a p-unit theorem whose divisor
  retains the same phase;

fail:
  produces only Norm(K_s), only six independent 211-layer K_s orbits, only
  abstract quotient roots, or a relation that appears only at the random
  interpolation threshold.
```

This is the current cleanest finite-field identity target for the selected
chain route, with the 211-layer phase-glue caveat made explicit.
