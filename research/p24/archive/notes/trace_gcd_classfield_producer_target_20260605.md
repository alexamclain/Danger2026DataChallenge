# Trace-GCD Class-Field Producer Target

Date: 2026-06-05

This note consolidates the current producer theorem after the payload gate,
the embedded-tower sidecar, and the origin-norm power audit.

## Bottom Line

The trace-GCD operator norm can plausibly live in the surviving
growing-degree embedded class-field lane.  It is not a bounded local selector.
The missing theorem is to construct the actual embedded p-integral
trace-GCD cyclic element from non-genus relative class-character data paired
to the conductor-2 `j` torsor.

The finite object remains:

```text
f_trace(Y) = det_Q(P V_univ A) in O_F[Y]/(Y^211 - 1),
Pi_right = Res(Y^211 - 1, f_trace)
         = prod_{t mod 211} det(P V_t A).
```

The theorem to prove is:

```text
f_trace is p-integral and Pi_right is a p-unit
at the selected prime above p = 10^24 + 7.
```

The finite handoff from this single global norm to the mixed rank certificate
is now isolated in:

```text
p24/lean/TraceGcdOperatorRepresentativeGate.lean
```

It requires the honesty theorem:

```text
exists t with Delta(t)=0  =>  Pi_right=0.
```

Thus a producer may target either the seven orbit norms or the single global
operator norm.  The single-norm route has the smallest payload
`Pi_right, Pi_right^{-1}`, but only if the class-field/Fitting construction
really identifies it with the norm of the actual trace-GCD determinant
section.

## Growing-Degree Recast

For the third p24 trace:

```text
h = 2 * 157 * 211 * 3107441,
H = <g^66254>,
|H| = 3107441.
```

A compatible embedded tower has relative degrees:

```text
2, 157, 211, 3107441.
```

The `2` layer is genus-facing.  The odd `157` and `211` layers require
non-genus relative class-character traces:

```text
T_s(aK) = sum_{k in K} chi_s(k) j_{ak}.
```

Equivalently, in Kummer normal form, they require primitive relative Kummer
powers for:

```text
157 layer: one Frobenius orbit of length 156;
211 layer: six Frobenius orbits of length 35.
```

Those data determine embedded child polynomials by inverse Fourier/Kummer
reconstruction.  The final recovery relation has degree `3107441`, still far
below `sqrt(p)`.

The trace-GCD route does not necessarily need to output the selected child
chain.  It may instead use the same embedded relative phase data to construct
`f_trace` and prove its norm p-unit.

The fixed Lang-head side of the orbit exterior expansion is no longer an
open source of vanishing: all selected fixed Fourier minors are p-units by
the Vandermonde argument in:

```text
p24/trace_gcd_fourier_minor_unit_theorem.md
```

Thus a producer theorem should spend its arithmetic content on the actual CM
Plucker/Fitting determinant section, not on projection-side superregularity.
The sharpened exterior determinant-line target is:

```text
p24/trace_gcd_cm_plucker_fitting_norm_frontier.md
```

The pinned actual-CM consistency audit for this target is:

```text
p24/trace_gcd_actual_cm_norm_triangle_audit.py
```

It checks that the orbit product, actual block-cycle determinant, and
split-interpolant norm agree, while the split interpolant is not an ordinary
base polynomial.  This keeps the producer theorem pointed at the
crossed-product/Fitting class-field object.

The p-local ordinary-prime criterion for this object is:

```text
p24/trace_gcd_ordinary_fitting_disjointness_criterion.md
```

It reduces the final local step to proving that the actual phase-aware
Fitting divisor has zero local intersection with the selected p24 ordinary
CM point.

The semilinear descent caveat is:

```text
p24/trace_gcd_semilinear_descent_frontier.md
```

Principal Frobenius at `p` fixes the unramified CM root torsor, but the
`157/211` Fourier phases are still moved by cyclotomic Frobenius.  Therefore
the producer must construct the determinant in the crossed-product/Fitting
phase algebra, not as an ordinary base-field polynomial.

## What the Origin-Norm Audit Adds

The new audit:

```text
p24/lang_trace_gcd_origin_norm_power_audit.py
p24/lean/OriginNormPowerGate.lean
```

checks that, in the pinned actual-CM row, larger origin products are powers of
the reduced right product:

```text
prod_{alpha mod m : fixed beta} Delta_origin(alpha,beta)
  = Pi_right^(m/d),

prod_{all origins} Delta_origin
  = Pi_right^(n*m/d).
```

Pinned row:

```text
D=-13319, q=13463, h=140, m=28, n=5, d=7

omitted=0:
  Pi_right=6352, Pi_right^4=1718, Pi_right^20=3871

omitted=1:
  Pi_right=6639, Pi_right^4=5193, Pi_right^20=4697
```

For p24 the predicted exponents are:

```text
m/d = 314,
n*m/d = 975736474.
```

Thus a full-origin norm formula would imply the right norm p-unit, but only
if that full-origin norm is available by a closed modular/class-field product
formula.  Enumerating the full origin set is not a certificate-scale producer.

## Route Separation

There are now two surviving positive theorem types:

```text
selected-chain producer:
  output one embedded 2/157/211/recovery chain, including the degree-3107441
  recovery polynomial;

p-unit producer:
  construct f_trace or an equivalent determinant section and prove
  Pi_right is a p-unit.
```

The trace-GCD route is the second type.  The selected-chain route is the most
literal `j` producer.  Both require embedded non-genus relative phase data;
neither is supplied by abstract class-field roots alone.

## Closed Weaker Versions

Current notes rule out or demote:

```text
bounded local selectors:
  p24/finite_field_selector_degree_theorem.md

abstract unpaired class-field towers:
  p24/prime_torsor_obstruction_theorem.md

low-degree parent-period formulas:
  p24/tower_phase_coefficient_complexity_boundary.md

right degree-35 spectral collapse:
  p24/lang_trace_gcd_spectral_scan_boundary.md

Kummer orbit norm as selected-chain data:
  p24/relative_kummer_orbit_norm_boundary.md
```

Kummer orbit norms may still be useful for p-unit/nonvanishing if one proves
that the trace-GCD determinant section factors through those nonzero Kummer
powers.  They do not reconstruct the selected child chain by themselves.

The finite Kummer nonvanishing bridge and its determinant caveat are recorded
in:

```text
p24/trace_gcd_kummer_nonvanishing_bridge.md
p24/relative_kummer_nonvanishing_bridge_toy.py
p24/lean/KummerNonvanishingGate.lean
p24/trace_gcd_kummer_determinant_boundary.md
```

The determinant boundary shows that coordinatewise Kummer p-units are too
weak: a determinant can vanish by row dependence while every primitive
Kummer coordinate is nonzero.  The needed theorem is therefore a
Plucker/Fitting Kummer zero-detection statement for `f_trace` itself.

The positive determinant-level payload is:

```text
p24/trace_gcd_plucker_kummer_payload.md
p24/plucker_kummer_payload_toy.py
p24/lean/PluckerKummerGate.lean
p24/plucker_kummer_descent_toy.py
p24/lean/PluckerKummerDescentGate.lean
p24/lang_trace_gcd_plucker_kummer_descent_boundary.md
p24/lean/PluckerKummerOrbitNormGate.lean
p24/lang_trace_gcd_orbit_product_formula_boundary.md
```

It replaces entrywise Kummer p-units by Kummer powers of the Plucker
coordinate `Delta(t)=det(P V_t A)` itself.

The producer must still prove descent.  If the selected Plucker coordinate is
only permuted through an orbit, not scaled on one determinant line, then the
safe invariant is the orbit product/norm rather than an individual power
`Delta(t)^r`.

The pinned actual-CM row supports this conservative interpretation:

```text
raw_descended_orbits=1/3
nontrivial_power_descended_orbits_any_tested=1/3
orbit_product_nonzero_count=3/3
```

So the next producer theorem should be phrased in terms of determinant
orbit norms unless a separate semi-invariance lemma is proved.

The follow-up orbit-product formula audit finds no small fixed-row
compression:

```text
nontrivial orbit products distinct,
no pair power relations with coefficients <= 5,
no total product relation with coefficients <= 5.
```

Thus a further reduction below seven orbit products needs an actual new
equivariance or product theorem, not just the visible small-CM pattern.

## Small Tests

The minimal checks that support the current target are:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/lang_trace_gcd_operator_norm_toy.py \
  --field-q 337 --right 7 --orbit-generator 2 --k 2 --trials 5
```

which reports `identity_mismatches=0`, and:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/relative_tower_character_toy.py
```

which reports:

```text
relative_child_polynomial_is_equivalent_to_relative_character_traces=1
abstract_tower_degrees_do_not_supply_these_traces=1
```

The new origin-norm power audit is:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/lang_trace_gcd_origin_norm_power_audit.py \
  --only-D -13319 --only-q 13463 --q-start 13463 --q-stop 13464 \
  --only-m 28 --only-left 4 --only-right 7 \
  --include-linear --max-factor-degree 8 --max-extension-degree 8 \
  --min-left-orbit-len 2 --require-square-tail \
  --max-origin-shifts 140
```

It reports `failures=0`.

## Next Theorem Attempt

The sharpest next theorem to try to prove is:

```text
There is a p-integral determinant section Psi_trace on the embedded
relative class-field tower whose restriction to the right 211-origin algebra
is f_trace, and whose divisor avoids the selected p24 CM orbit at the prime
above p.
```

More concretely, prove either:

```text
1. f_trace can be expressed as a determinant/norm polynomial in the
   non-genus relative Kummer powers for the 157 and 211 tower layers, and
   those Kummer powers are p-units; or

2. the full-origin product of the trace-GCD determinant section is a known
   Borcherds/local-intersection value and is a p-unit, after which the
   origin-norm power theorem gives Pi_right != 0.
```

The first would stay closer to the small 211-term finite certificate.  The
second would import heavier CM product machinery, but the new power relation
shows it would land on the right finite object if the determinant section can
be modularized.

The accounting boundary for this second route is:

```text
p24/trace_gcd_full_origin_norm_boundary.md
p24/trace_gcd_full_origin_borcherds_gate.md
p24/full_origin_norm_vs_class_enumeration_accounting.py
```

It records the important distinction: a full-origin norm computed from the
full Hilbert class polynomial is still class-number scale, while a closed
phase-aware Borcherds/Fitting formula could still give the needed sub-sqrt
producer.

## Embedded Plucker/Fitting Orbit-Norm Theorem

The current class-field formulation is sharper than an individual Kummer
descent theorem.  For the conductor-2 p24 CM torsor:

```text
D_K = -652834595820939249713143
h = 2 * 157 * 211 * 3107441
G = <g>
H = <g^66254>,      |H| = 3107441
```

pair the embedded quotient tower

```text
G > <g^2> > <g^314> > <g^66254>
relative degrees 2, 157, 211
```

with relative class-character/Kummer data for the odd layers.  The theorem
to prove is:

```text
Construct the actual p-integral mixed trace-GCD determinant section

  f_trace(Y) = det_Q(P V_univ A) in O_F[Y]/(Y^211 - 1)

from the embedded conductor-2 CM torsor and the 157/211 relative phase data,
and prove that for every Frobenius orbit O on Z/211Z,

  Pi_O = prod_{t in O} f_trace(zeta_211^t)

is a p-unit at the selected prime over p = 10^24 + 7.
```

Equivalently:

```text
the seven block-cycle/Fitting determinants det(B_O) are p-units.
```

This is stronger than proving one selected determinant, but it remains far
below class-set scale: the verifier payload is still seven orbit norms and
seven inverses.

The exact class-field inputs are:

```text
1. fixed embedded conductor-2 CM torsor, not abstract class-field roots;
2. oriented generator/action compatible with the split-prime generator;
3. genus/top-layer pairing for the degree-2 split;
4. non-genus embedded relative traces or Kummer powers for the 157 layer
   and the six 211-layer Frobenius orbits;
5. determinant-level construction of f_trace, not coordinate p-units;
6. p-integrality of DFT, roots of unity, Lang/Moore bases, kernel transport,
   and tail coordinate choices;
7. honesty theorem comparing the constructed section to the actual
   trace-GCD determinant section;
8. p-unit valuation theorem for the seven orbit norms.
```

The small falsifiers now point exactly here:

```text
p24/lang_trace_gcd_operator_norm_toy.py:
  product/resultant/operator-norm packaging is algebraically sound.

p24/lang_trace_gcd_plucker_kummer_descent_audit.py:
  individual Kummer descent is too strong;
  orbit-norm descent is the safe determinant-level invariant.

p24/block_cycle_fitting_zero_detection_toy.py:
  the singular branch of the block-cycle/Fitting zero-detection is finite
  linear algebra once the block-cycle determinant is honest.

p24/orbitwise_schur_bridge_falsifier.py:
  the Hermitian/Gram Schur bridge is finite-algebraically sound orbitwise on
  the pinned actual-CM rows, but asks for stronger Gram p-units than the
  direct trace-GCD Fitting determinant.

p24/lean/TraceGcdSchurBridgeGate.lean:
  if Schur zero-detection is honest and the prefix/full Gram orbit products
  are p-units, then the trace-GCD orbit products are p-units; kernel Gram
  nonzero follows from prefix Gram nondegeneracy.  The minimal Gram payload is
  28 base-field elements, conservative payload 42.

p24/trace_gcd_prefix_full_gram_payload_refinement.md:
  separates the full Gram factor, which is a full-window Moore/trace-Gram
  p-unit, from the prefix Gram factor, which is the genuinely stronger
  finite-field trace-form nondegeneracy condition.

p24/trace_gcd_prefix_gram_self_orthogonal_obstruction.md:
  identifies that prefix Gram condition as the absence of nonzero vectors in
  U_t cap U_t^perp for the transported trace-GCD prefix row spaces.

p24/trace_gcd_metric_schur_refinement.md:
  corrects the Gram bridge to the invariant metric identity with
  A G^{-1} A^T and N^T G N; ordinary lower-dimensional dot Grams are
  coordinate-dependent.

p24/trace_gcd_prefix_subcode_distance_boundary.md:
  restates prefix Gram nondegeneracy as the support-specific distance theorem:
  no nonzero lambda in U_S has nonzero-right trace word supported inside the
  70-coordinate nonzero complement.  This is useful language but not a generic
  cyclic-code shortcut.
```

This theorem avoids enumeration only if the section `f_trace`, or the seven
`Pi_O`, is produced from embedded relative class-character/Kummer formulas.
It fails if the construction is merely abstract `bnrclassfield` data,
coordinatewise Kummer p-units, a canonical child selector, a Hilbert-class
full-origin product, or anything that does not identify the determinant
section itself.
