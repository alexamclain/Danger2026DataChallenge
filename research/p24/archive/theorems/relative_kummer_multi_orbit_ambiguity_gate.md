# Relative Kummer Multi-Orbit Ambiguity Gate

Date: 2026-06-06

This gate corrects the selected-chain Kummer normal form in the case where
Frobenius has more than one orbit on primitive relative characters, and tests
the natural repair by cross-orbit glue invariants.

For a cyclic prime-degree child layer of degree `r`, with children `y_u`,

```text
T_s = sum_u zeta_r^(s*u) y_u
K_s = T_s^r
```

If `q` has one orbit on `s=1,...,r-1`, then choosing an `r`th root of one
`K_s` and propagating by Frobenius gives only the `r` cyclic relabelings of
the child fiber.  The unordered child polynomial is selected.

If `q` has `g > 1` primitive-character orbits, then each orbit has its own
root-of-unity phase.  Frobenius compatibility still makes the inverse DFT
children descend to `F_q`, but the independent phases need not come from one
global cyclic shift.  Thus the Kummer powers alone do not select the unordered
child polynomial.

The finite repair is to add invariant ratios, using the orbit with
representative `1` as gauge:

```text
G_a = T_a / T_1^a
```

for one representative `a` of each other primitive-character Frobenius orbit.
These ratios are unchanged by a single global cyclic relabeling
`T_s -> zeta_r^(c*s) T_s`, but they reject independent phases on the other
orbits.

## Finite Check

Command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/relative_kummer_multi_orbit_ambiguity_gate.py --trials 3
```

Output:

```text
case q=3 r=5 zeta_degree=4 orbit_count=1
  total_assignments_per_trial=5
  noncyclic_descending_assignments=0
  glue_preserving_assignments=15
  min_unique_polynomials=1
  max_unique_polynomials=1
  min_glue_unique_polynomials=1
  max_glue_unique_polynomials=1

case q=11 r=7 zeta_degree=3 orbit_count=2
  total_assignments_per_trial=49
  noncyclic_descending_assignments=126
  glue_preserving_assignments=21
  noncyclic_glue_preserving_assignments=0
  min_unique_polynomials=7
  max_unique_polynomials=7
  min_glue_unique_polynomials=1
  max_glue_unique_polynomials=1

case q=5 r=13 zeta_degree=4 orbit_count=3
  total_assignments_per_trial=2197
  noncyclic_descending_assignments=6552
  glue_preserving_assignments=39
  noncyclic_glue_preserving_assignments=0
  min_unique_polynomials=42
  max_unique_polynomials=46
  min_glue_unique_polynomials=1
  max_glue_unique_polynomials=1
```

The exact number of distinct unordered polynomials can collide in tiny finite
fields, but the noncyclic descents are already enough to falsify uniqueness.

## p24 Consequence

For the p24 layers:

```text
157 layer: ord_157(p)=156, one primitive-character orbit.
211 layer: ord_211(p)=35, six primitive-character orbits.
```

So the `157` layer still has the clean Kummer normal form.  The `211` layer
has independent cross-orbit phases.  Modulo the one global cyclic relabeling,
the Kummer-only formal ambiguity is

```text
211^(6-1) = 418227202051.
```

The gate also gives the positive finite target: five invariant ratios

```text
G_a = T_a / T_1^a
```

for representatives of the other five p24 `211`-layer Frobenius orbits restore
child-polynomial selection in the toy model.  Therefore a producer theorem may
target Kummer orbit/minpoly data plus these five glue invariants, instead of
the selected degree-211 child polynomial.

The finite implication and slot accounting are Lean-checked in:

```text
p24/lean/KummerCrossOrbitGlueGate.lean
```

For p24 this accounting is five extension-field glue objects, or
`5*35=175` base-field coordinates under conservative serialization.

## Updated Pass/Fail Rule

Pass:

```text
construct 157-layer Kummer orbit data, and for the 211 layer construct either
selected child-polynomial data, full relative morphism data, or Kummer data
plus explicit cross-orbit phase glue such as `T_a/T_1^a`.
```

Fail:

```text
produce only six independent 211-layer K_s Frobenius orbits/minpolys, only
orbit norms, or only abstract quotient roots.
```
