# Trace-GCD Selected Schubert P-Unit Frontier

Date: 2026-06-06

This note pins the current proof target after the selected-erasure correction,
the metric-Schur correction, and the latest synthesis pass.

## Exact Object

The sharpest trace-GCD object is still the determinant sequence

```text
Delta(t) = det(P V_t A),        t mod 211,
```

where `A` is the transported map from the four-prefix trace kernel and `P`
selects the 16 Lang tail coordinates.  The bad event is the selected Schubert
intersection

```text
Bad(t):  V_t W_trace cap ker(P) != {0}.
```

Equivalently:

```text
Delta(t) = 0  <=>  Bad(t).
```

The p-unit theorem should construct an honest p-integral determinant section

```text
f_trace = det(P V_univ A) in O_F[Y]/(Y^211 - 1)
```

or its semilinear/crossed-product replacement, and prove the seven orbit norms

```text
Pi_O = prod_{t in O} Delta(t)
```

are p-units at the selected prime above

```text
p = 10^24 + 7.
```

For p24 the orbits are `{0}` plus six length-35 nonzero Frobenius orbits, so
the finite payload is:

```text
7 products + 7 inverses = 14 F_p elements.
```

The new Lean gate

```text
p24/lean/TraceGcdSelectedSchubertPUnitGate.lean
```

formalizes the final finite implication:

```text
honest norm detects Schubert bad events
+ norm is a p-unit
=> no Schubert bad event
=> selected trace-GCD row is good.
```

The one-operator version is checked in:

```text
p24/lean/TraceGcdOperatorRepresentativeGate.lean
```

There the payload is only:

```text
Norm_trace, Norm_trace^{-1}
```

provided the producer proves that any translated Schubert bad event, or
equivalently any zero of `Delta(t)`, forces this actual global norm to vanish.
This is the same determinant section, but with the orbit products multiplied
before the finite handoff.

## Theorem To Prove

The proof-facing theorem is:

```text
For the conductor-2 p24 CM torsor with trace -1178414874616, the mixed
trace-GCD determinant-line section f_trace is p-integral, descends to the
right 211 crossed-product orbit algebra, and every orbit reduced norm Pi_O
is a p-unit at the selected split prime over p.
```

The geometric form is:

```text
the p24 CM point W_trace has zero local intersection with

  D_trace = sum_t {W : V_t W cap ker(P) != {0}}

at the selected prime above p.
```

The embedded class-field form is:

```text
construct the same determinant section from the non-genus 157/211 relative
phase data paired to the conductor-2 j torsor, without class-set enumeration.
```

## Fixed Side Now Settled

The split Cauchy-Binet expansion of one nonzero right orbit has terms

```text
det(P_U) det(W_U) zeta_211^(t * sum_U u),
```

with `|U|=16`.  For the selected first-16 Lang coordinates, every fixed
projection minor `det(P_U)` is a p-unit by a consecutive-row Vandermonde
calculation.  The p24 audit also shows that distinct 3-subset sums from a
length-35 orbit already fill all of `Z/211Z`.

This refinement is recorded in:

```text
p24/trace_gcd_fourier_minor_unit_theorem.md
p24/fourier_head_minor_unit_audit.py
p24/trace_gcd_cm_plucker_fitting_norm_frontier.md
```

The remaining theorem is therefore not fixed Fourier-minor nonvanishing.  It
is p-adic noncancellation of the actual CM Plucker/Fitting expansion, or an
explicit class-field/Borcherds identity proving the corresponding orbit norm
is a p-unit.

## Why This Is Narrower Than MDS

The live prefix theorem is selected erasure, not global distance.

For a four-orbit prefix:

```text
|S| = 140,
|T_nonzero| = 70.
```

The exact theorem is:

```text
no nonzero lambda in U_S has nonzero-right trace word supported in T_nonzero.
```

A global `[210,140,71]` distance theorem would imply this, but is stronger
than necessary.  The finite separation is recorded in:

```text
p24/trace_gcd_selected_erasure_vs_global_distance.md
p24/selected_erasure_vs_global_distance_toy.py
```

## Metric-Gram Alternate

The Gram bridge is valid only with the trace metric

```text
G_ij = Tr_{L/F_p}(b_i b_j).
```

The invariant identity is:

```text
det([A;B] G^{-1} [A;B]^T) det(N^T G N)
  = det(A G^{-1} A^T) det(BN)^2.
```

Thus a stronger sufficient theorem is:

```text
P_O = prod_t det(A_t G^{-1} A_t^T)          is a p-unit,
L_O = prod_t det([A_t;B_t]G^{-1}[A_t;B_t]^T) is a p-unit,
```

for every right Frobenius orbit `O`.  This gives a 28-element payload with
inverses.  It is alive only if `P_O` and `L_O` can be identified with actual
Hermitian/autocorrelation packet norms; otherwise it is probably harder than
the direct Fitting norm.

The bounded actual-CM metric-aware scan:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/orbitwise_schur_bridge_falsifier.py \
  --metric-aware --include-linear \
  --max-factor-degree 10 --max-extension-degree 10 \
  --min-left-orbit-len 2 --require-square-tail --min-prefix-len 1 \
  --max-rows 4 --max-cases 30 --max-abs-D 60000 \
  --q-stop 250000 --max-origin-shifts 60
```

found four actual small-CM rows with:

```text
tail_zero=0,
schur_fail=0,
prefixGram0=0,
fullGram0=0,
kernelGram0=0,
right_class_mismatches=0,
orbitSchur=1.
```

This is finite plumbing evidence, not p24 proof.

## Relation To The Embedded Tower

The selected-chain verifier surface has size:

```text
2 + 157 + 211 + 3107441 = 3107811 << sqrt(p).
```

The finite-field degree lower bound says this recovery degree is not an
accident: any single coset selector constant on the recovery subgroup must
have degree at least `3107441`.  That is still far below `sqrt(p)`, so it is a
positive target, not a no-go.

The trace-GCD p-unit route is the compressed determinant version of the same
embedded phase problem.  It may avoid outputting the selected recovery
polynomial, but it cannot avoid constructing the non-genus 157/211 phase data
or an equivalent determinant-level class-field identity.

## Rejected Replacements

The current artifacts demote these candidates:

```text
ordinary coordinate Gram:
  basis-dependent; must use the trace metric;

coordinatewise Kummer p-units:
  nonzero entries do not prevent determinant collapse;

abstract bnrclassfield roots:
  quotient roots are unpaired with embedded j fibers;

bounded modular/local selectors:
  finite-field fiber degree forces degree at least |H|;

global MDS first:
  sufficient but stronger than selected erasure;

raw base-field residues in F_p[Y]/Phi_O:
  actual determinant sequences are not ordinary Frobenius-compatible.
```

## Next Proof Move

The next useful theorem attempt should construct the divisor or determinant
section itself:

```text
1. define the p-integral crossed-product/Fitting order for f_trace;
2. identify its zero divisor with D_trace on the period/Schubert image;
3. prove the p24 CM point has zero local p-intersection with D_trace,
   either by a phase-aware class-field identity or a Borcherds/Siegel-unit
   comparison.
```

Short computations should only falsify these theorem shapes on small CM rows
or check determinant-line descent conventions.  They should not enumerate the
p24 class set or run sqrt-scale candidate searches.

The orbit-level exterior expansion of the same determinant is recorded in:

```text
p24/trace_gcd_orbit_exterior_schubert_expansion.md
p24/trace_gcd_cm_plucker_fitting_norm_frontier.md
```

It shows that each nonzero right orbit is a 35-dimensional Schubert translate
problem with `binom(35,16)=4059928950` exterior terms.  This is the exact
noncancellation point a p-unit/class-field proof has to address.

The companion toy:

```text
p24/orbit_exterior_schubert_toy.py
```

finds a small orbit where all fixed Schubert coefficients and all Plucker
coordinates are nonzero but one translated determinant vanishes.  This is the
finite warning that coordinatewise Kummer/Plucker nonvanishing cannot replace
the selected Schubert p-unit theorem.

The faithful pinned small-CM norm triangle is:

```text
p24/trace_gcd_actual_cm_norm_triangle_audit.py
```

It confirms that the scalar orbit products, actual block-cycle/Fitting
determinants, and split-interpolant orbit norms agree on the same trace-GCD
row, while ordinary base-polynomial descent still fails.  This supports the
current producer target: construct the actual crossed-product/Fitting norm
and prove it is a p-unit.

The p-local ordinary-prime criterion for the same target is:

```text
p24/trace_gcd_ordinary_fitting_disjointness_criterion.md
```

It makes the remaining theorem concrete: zero local intersection of the
selected p24 ordinary CM point with the actual phase-aware orbit
Schubert/Fitting divisor.

The semilinear descent warning is:

```text
p24/trace_gcd_semilinear_descent_frontier.md
```

Principal Frobenius explains complete splitting of the CM roots over `F_p`,
but the `211` phase still has six length-35 cyclotomic Frobenius orbits.
That is why the orbit-product payload is honest while naive base-polynomial
descent is not.

The intrinsic Grassmannian phrasing is:

```text
p24/trace_gcd_chow_norm_theorem_candidate.md
```

It identifies `Delta(t)` with the Chow/Schubert hyperplane evaluation of the
translated complementary 19-plane against the actual CM 16-plane.  The seven
orbit products are therefore orbit Chow norms; this is the cleanest divisor
language for a future local-intersection or Borcherds comparison.

The easiest plain-divisor recognition has now been tested in:

```text
p24/trace_gcd_chow_plain_divisor_scan.py
p24/trace_gcd_chow_plain_divisor_boundary.md
```

On the pinned small actual-CM row, the determinant has the expected right
period but has random-sized rational interpolation in the plain `j` coordinate
and no low-bidegree expression in the oriented edge `(j_i,j_{i+1})`.  This
keeps the Borcherds/Fitting route alive only in its phase-aware form: the
section must be the pulled-back Chow divisor, not an already-visible
low-degree function of `j`.

The resulting phase-aware theorem target is now consolidated in:

```text
p24/trace_gcd_phase_aware_chow_borcherds_target.md
```

It states the needed comparison `s_O = p-unit * Psi_O`, with `Psi_O` an
explicit class-field/Borcherds/Fitting product whose divisor is the pulled
back orbit Chow divisor up to terms away from the selected p24 prime.

The small phase-coordinate check is:

```text
p24/trace_gcd_chow_phase_coordinate_scan.py
p24/trace_gcd_chow_phase_coordinate_boundary.md
```

It verifies exact right-phase descent and one-orbit DFT support in the pinned
right-`7` row, but also records the p24 full exterior-support warning.  Thus
the p24 proof should still target seven orbit norms unless a separate
one-orbit cancellation theorem is proved.

The bounded phase-unit dictionary test is:

```text
p24/trace_gcd_chow_phase_divisor_span_scan.py
p24/trace_gcd_chow_phase_divisor_span_boundary.md
```

It found no non-random product formula from small right-binomial units and
small Heegner-fiber units.  This pushes the proof target back toward the
exact Schubert-Fitting section or a direct orbit-norm p-unit theorem.
