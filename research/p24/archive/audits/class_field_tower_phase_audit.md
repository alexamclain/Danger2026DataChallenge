# Embedded class-field tower phase audit

This note records the next attempted positive route after the finite-field
degree theorem.

## p24 target shape

For the best certificate-oriented trace,

```text
t = -1178414874616
D_K = -652834595820939249713143
h = 205880396014 = 2 * 157 * 211 * 3107441
G = Cl(O_K) cyclic
```

The good oriented composite class is

```text
a = 2 * 463 * 223^(-1)
```

with

```text
quotient_index = 66254 = 2 * 157 * 211
recovery_subgroup_size = 3107441
```

The attractive tower dream is:

```text
degree 2 quotient
then degree 157 refinement
then degree 211 refinement
then degree 3107441 recovery
```

Each individual degree is far below `sqrt(p) = 10^12`.  The question is
whether the small quotient factors can be made embedded and phase-aware
without constructing the full CM root set.

## Toy calibration

I added:

```text
p24/tower_phase_refinement_toy.py
```

It uses the exact CM torsor

```text
D = -5000
q = 1259
h = 30 = 2 * 3 * 5
```

with a generator cycle from the norm-3 split prime.  The toy chooses the
recovery subgroup

```text
H = <g^6>, |H| = 5
```

and decomposes the quotient `G/H` of size `6` through a tower `2*3`:

```text
H=<g^6> <= K=<g^2> <= G.
```

The run gives:

```text
top_periods=[1126, 532]
top_polynomial_degree=2
top_polynomial_coeffs_ascending=[1007, 860, 1]

fine_periods=[159, 1062, 1004, 254, 1222, 475]
fine_polynomial_degree=6
fine_polynomial_coeffs_ascending=[973, 398, 995, 1054, 224, 860, 1]

parent=0 top_value=1126 child_polynomial=[563, 777, 133, 1]
parent=1 top_value=532  child_polynomial=[648, 958, 727, 1]
```

There is a bivariate relative refinement relation `F(Z,Y)` of degree `3` in
`Y` and degree `1` in the top period `Z`; specializing `Z` to one of the two
top roots gives the correct three fine children, and the wrong parent has no
cross zeros.

## Interpretation

This is a positive shape result:

```text
class-field towers really can reduce the visible root degrees.
```

But it exposes the exact missing object.  The two relative degree-3 child
polynomials are not determined by the abstract factorization `30=2*3*5` or by
the degree-2 top polynomial alone.  In the toy they were constructed from the
embedded `j`-cycle.

For p24, replacing `2*3` by `2*157*211` gives the same tower shape, but the
relative refinements are precisely the embedded quotient-phase data we do not
know how to compute without class enumeration or an equivalent non-genus
period theorem.

## Updated route boundary

The viable sub-sqrt class-field route is now:

```text
construct the relative tower refinements for quotient factors 2,157,211
directly over F_p, and then recover a j-root from a degree-3107441 polynomial.
```

The no-go theorem says no bounded local invariant can provide those
refinements.  The toy says a tower helps after the relative refinements exist,
but it does not generate the phase data by itself.

So the missing theorem has become more explicit:

```text
Compute embedded relative class-period refinements along a prescribed smooth
quotient tower without first constructing the full CM torsor.
```

The oriented-composite toy supports the same boundary:

```text
PYTHONDONTWRITEBYTECODE=1 python3 p24/oriented_composite_path_toy.py
```

For `D=-5000`, the oriented product `3*17^(-1)` has index `6` and order `5`.
Local oriented path invariants still had `30` distinct values, while only
whole-cycle aggregation collapsed to `6` period values:

```text
distinct_path_sums=30
distinct_path_products=30
distinct_period_sums=6
period_sum_polynomial_degree=6
```

This is the miniature analogue of the p24 class `2*463*223^(-1)`: binary
orientation labels make the desired class action well-defined, but they do
not by themselves supply the quotient period or a seedless root selector.

I do not currently know such a theorem in the CM/class-invariant literature.

## Section obstruction and relative characters

I added:

```text
p24/tower_section_obstruction.md
p24/relative_tower_character_toy.py
```

The section obstruction is a small but useful theorem.  For a nontrivial
refinement layer

```text
L <= K <= G,
```

there is no `G`-equivariant section

```text
G/K -> G/L
```

unless `K=L`.  Thus a seedless modular rule cannot canonically name one child
inside a parent tower fiber.  The unordered relative child polynomial is still
allowed, but a child label or phase needs extra information.

The relative-character toy verifies the exact finite-field algebra behind
that extra information.  In the same `D=-5000`, `h=30` tower, the two
degree-3 child polynomials are recovered from relative character traces on
`K/H`.  Since `F_1259` does not contain a primitive third root of unity, the
nontrivial traces live in `F_{1259^2}`, and inverse DFT descends back to the
child periods:

```text
parent=0 child_periods=[159, 1004, 1222]
  relative_character_traces=[(1126,0), (196,1041), (414,218)]
  child_polynomial=[563, 777, 133, 1]

parent=1 child_periods=[1062, 254, 475]
  relative_character_traces=[(532,0), (587,1038), (808,221)]
  child_polynomial=[648, 958, 727, 1]
```

This pins down the p24 constructive lemma:

```text
compute the relative non-genus class-character traces for the 157 and 211
refinement layers, embedded relative to j, without class enumeration.
```

The first degree-2 layer for the third trace is only genus information
because

```text
D_K = -599 * 1089874116562502921057,
```

so known genus machinery may plausibly handle that constant-bit split.  The
odd `157` and `211` refinements remain the real missing theorem.

## Degree-5 sidecar analogue

The degree-157 theorem target also has a small `5`-child analogue:

```text
D = -711
q = 727
h = 20 = 2 * 5 * 2
ell = 2
```

It gives a genus parent followed by a degree-5 refinement:

```text
top_periods=[635, 334]
parent 0 child polynomial=[372, 709, 415, 16, 92, 1]
parent 1 child polynomial=[338, 93, 520, 109, 393, 1]
wrong_parent_cross_zeros=0
```

As in the `D=-5000` tower, these child polynomials exist once the embedded
cycle is known.  But comparing the abstract degree-5 class-field quotient
roots with the embedded child sets gives:

```text
affine_maps=0
mobius_maps=0
```

So the extra odd-child example supports the same conclusion: abstract
class-field quotient equations and genus data do not supply the embedded
non-genus phase.

## Coefficient-Complexity Refinement

I added a direct stress test for one remaining optimistic compression:

```text
p24/tower_phase_coefficient_complexity_scan.py
p24/tower_phase_coefficient_complexity_boundary.md
```

For a toy tower

```text
h = a * b * r,
```

the relative child polynomial above parent period `Z_u` is

```text
C_u(Y) = prod_v (Y - y_{u+a*v}).
```

The coefficient of `Y^(b-1)` is always `-Z_u`, so it is a forced
degree-one relation.  The scan removes that tautology and asks whether the
remaining coefficients are low-degree functions of the parent period.

Two seconds-scale small-CM runs found:

```text
informative_coeff_slots=17, informative_full_degree_coeffs=17
informative_coeff_slots=41, informative_full_degree_coeffs=41
```

with no low-BM coefficient sequence.  This disfavours a tiny interpolation
formula for the p24 relative phase.  It does not kill the tower route: the
generic second odd-step table size is still only

```text
314 * 210 = 65940
```

which is quotient-scale.  It does mean the producer theorem must construct
the embedded relative class-character traces or quotient-scale child
polynomials directly; it cannot rely on a hidden low-degree parent-period
collapse.
