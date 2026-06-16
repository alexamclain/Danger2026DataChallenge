# Trace-GCD Orbit-Norm Producer Frontier

Date: 2026-06-05

## Current Best Target

The sharpest current theorem shape is a right-`211`
determinant packet-norm / crossed-product cyclic-algebra unit theorem.

For the p24 mixed trace-GCD route, the finite determinant sequence is:

```text
Delta(t) = det(P V_t A),      t mod 211.
```

The finite verifier only needs:

```text
Delta(t) != 0 for all t mod 211.
```

After the descent and formula audits, the honest compressed producer target is
orbitwise:

```text
Pi_O = prod_{t in O} Delta(t),
O = Frobenius orbit on Z/211Z.
```

Equivalently, `Pi_O` is the reduced norm of the crossed-product weighted
cycle with weights `Delta(t)` around the Frobenius orbit.  For p24 the
nonzero orbit length is `35`, so the weighted-cycle determinant has positive
sign:

```text
det(e_i |-> Delta(q^i*t_0) e_{i+1}) = Pi_O.
```

This exact finite algebra is recorded in:

```text
p24/lang_trace_gcd_crossed_product_orbit_boundary.md
p24/lang_trace_gcd_block_cycle_norm_boundary.md
p24/trace_gcd_block_cycle_certificate_spec.md
p24/lean/TraceGcdCrossedProductGate.lean
p24/lean/TraceGcdBlockCycleGate.lean
```

For p24 there are:

```text
one fixed orbit {0},
six length-35 nonzero orbits,
payload = 7 products + 7 inverses = 14 F_p elements.
```

This beats `sqrt(p)` by many orders of magnitude if the producer theorem is
honest.

## Equivalent Algebra Form

Let:

```text
B = O_F[Y]/(Y^211 - 1),
f_trace(Y) = det_B(P V_univ A),
V_univ = sum_v E_v Y^v.
```

Let `Phi_O(Y)` be the irreducible factor over `F_p` corresponding to a
Frobenius orbit `O`, and:

```text
B_O = F_p[Y]/(Phi_O(Y)).
```

Then:

```text
Pi_O = Norm_{B_O/F_p}(f_trace mod Phi_O)
```

for the actual determinant section.  The desired theorem is:

```text
for every O, Norm_{B_O/F_p}(f_trace mod Phi_O) is a p-unit.
```

Equivalently:

```text
f_trace is a unit in B tensor O_F/p,
gcd(f_trace, Y^211 - 1) = 1 mod p.
```

The one-norm form multiplies the seven `Pi_O`; the seven-orbit form is safer
for a producer because each orbit norm can be tied to a specific irreducible
factor.

## Theorem Candidates Still Alive

### 1. Fitting/Determinant-Line Norm

Construct the trace-GCD tail map over the cyclic algebra `B` and identify:

```text
f_trace = Fitt_0(coker(P V_univ A)).
```

Then prove the localized cokernel vanishes after reducing at the selected
prime:

```text
coker(P V_univ A) tensor B_O = 0
```

for every orbit factor `O`.  This is the cleanest algebraic statement because
nonvanishing becomes a Fitting-unit claim.

### 2. Schubert/Local-Intersection Norm

Interpret:

```text
Pi_O = product of local Schubert sections over O
```

at the CM trace-GCD plane:

```text
W_trace = A(K) subset F_p(mu_211).
```

Then prove the CM point has zero local intersection at the selected prime
with the corresponding orbit-Schubert divisor.  A Borcherds/automorphic
product formula would finish this if it compares that divisor to a p-unit CM
value.

### 3. Determinant-Level Kummer Orbit Norm

Construct local Plucker-Kummer values:

```text
Theta(t) = unit(t) * Delta(t)^r,
```

but do not require individual descent.  Instead construct:

```text
Theta_O = prod_{t in O} Theta(t)
```

and prove it is a p-unit.  The finite implication is checked by:

```text
p24/lean/PluckerKummerOrbitNormGate.lean
```

This is the Kummer version of the same orbit-norm theorem.

### 4. Crossed-Product Fitting Norm

Construct the orbit weighted-cycle/reduced-norm object directly as a Fitting
determinant in the semilinear Frobenius orbit algebra.  This avoids pretending
that the values are ordinary base-factor evaluations, while retaining the
same seven scalar payload.

The sharper matrix-level form constructs the block-cycle operator from the
actual tail-on-kernel maps:

```text
B_O e_i = M_{q^i t_0} e_{i+1},       Delta(q^i t_0)=det(M_{q^i t_0}).
```

For p24 nonzero right orbits this is a `560 x 560` operator, and:

```text
det(B_O) = prod_{t in O} Delta(t).
```

This is currently the most concrete Fitting-object target for the trace-GCD
route.

Equivalently, prove the local-intersection/kernel statement:

```text
For each right Frobenius orbit O, there is no nonzero section in the
direct sum of transported prefix kernels whose block-cycle tail image is zero.
```

The finite kernel implication is recorded in:

```text
p24/lean/TraceGcdLocalUnitGate.lean
p24/lean/TraceGcdBlockCycleGate.lean
p24/lang_trace_gcd_block_cycle_norm_boundary.md
```

The current proof-facing local-unit version is:

```text
p24/trace_gcd_local_unit_proof_target.md
```

It states the same theorem as a field-intersection/Fitting problem:
four full `R=F_p(mu_211)` trace blocks cut `L=F_p(mu_157)` down to a
16-dimensional residual kernel, and the selected 16 Lang tail coordinates are
nonsingular on that kernel; orbitwise, the transported failure modules have
unit zeroth Fitting ideal.

The same orbit theorem now has an exterior Schubert expansion in:

```text
p24/trace_gcd_orbit_exterior_schubert_expansion.md
```

For each nonzero right orbit, the determinant is a
`binom(35,16)=4059928950` term Cauchy-Binet polynomial in the CM Plucker
coordinates of a 16-plane.  This makes the proof obligation sharper:
Chebotarev nonzero Fourier minors and coordinatewise nonzero Plucker entries
do not prove the theorem; one needs a p-adic noncancellation or Fitting/class
field p-unit identity for the orbit product.

A tempting further compression is:

```text
det(B_O) = det(M_{r-1} ... M_0),
```

which would shrink each p24 nonzero orbit from a `560 x 560` determinant to a
`16 x 16` determinant.  This is only basis-safe after a coherent
transported-kernel-basis theorem.  The pinned row has `prefix_len=0`, and a
bounded search found no useful nonzero-prefix calibration row, so this remains
a conditional refinement.

Source:

```text
p24/lang_trace_gcd_monodromy_basis_boundary.md
```

### 5. Orbitwise Hermitian-Schur Bridge

The sidecar-suggested Gram bridge is now tested in:

```text
p24/orbitwise_schur_bridge_falsifier.py
p24/orbitwise_schur_bridge_falsifier.md
```

It verifies on actual small-CM rows the finite identity:

```text
L_O K_O = P_O Pi_O^2,
Pi_O = prod_{t in O} det(B_t | ker A_t).
```

The finite implication is Lean-gated in:

```text
p24/lean/TraceGcdSchurBridgeGate.lean
```

The refined prefix/full payload target is documented in:

```text
p24/trace_gcd_prefix_full_gram_payload_refinement.md
p24/trace_gcd_prefix_gram_self_orthogonal_obstruction.md
p24/trace_gcd_metric_schur_refinement.md
p24/trace_gcd_prefix_subcode_distance_boundary.md
```

The natural minimal payload is `28` field elements (`P_O,L_O` and inverses
for seven orbits).  The kernel Gram p-unit is then a finite consequence of
prefix Gram nondegeneracy, because the prefix kernel is the orthogonal
complement for the ambient trace pairing.  The conservative prefix/full/kernel
Gram payload is `42` field elements.  Both are sub-sqrt, but both need an
arithmetic theorem identifying the actual Gram products and proving they are
p-units.  The prefix theorem is exactly the exclusion of nonzero vectors in
`U_t cap U_t^perp` for the selected 140-dimensional trace-GCD prefix row
spaces, equivalently the support-specific parameter statement that no nonzero
`lambda in U_S` has nonzero-right trace word supported inside the
70-coordinate nonzero complement.
The Gram matrices here are metric-aware
`A_t G^{-1} A_t^T`, not coordinate-dot lower-dimensional Grams.

If `P_O`, `L_O`, and `K_O` could be identified with Hermitian packet
autocorrelation norms and proved to be p-units, this would imply the
trace-GCD orbit norm theorem.  The caveat is important: finite-field Gram
nondegeneracy is strictly stronger than rank, and the current nontrivial
calibration rows are still very small.  This is a bridge to a possible
Hermitian p-unit proof, not a smaller verifier surface than the direct
Fitting norm.

## Shortcuts Now Ruled Out or Demoted

### Individual Plucker-Kummer Descent

The pinned actual-CM row reports:

```text
raw_descended_orbits=1/3
nontrivial_power_descended_orbits_any_tested=1/3
```

So individual powers `Delta(t)^r` should not be assumed to descend unless a
separate semi-invariant Plucker-line theorem is proved.

Source:

```text
p24/lang_trace_gcd_plucker_kummer_descent_boundary.md
```

### Fixed-Row Unit Equality or Small Power Relations

The orbit-product formula audit reports:

```text
nontrivial orbit products distinct,
no pair power relations with coefficients <= 5,
no total product relation with coefficients <= 5.
```

Source:

```text
p24/lang_trace_gcd_orbit_product_formula_boundary.md
```

Right-unit equivariance can still propagate p-unitness between fully
transported certificate rows.  It does not supply equality of orbit products
inside one fixed row.

### Coordinatewise Kummer Nonvanishing

Coordinate Kummer p-units do not prevent determinant rank collapse.  The
payload must be attached to the Plucker/Fitting determinant itself.

Source:

```text
p24/trace_gcd_kummer_determinant_boundary.md
```

### Base-Field Interpolant/Resultant

A raw polynomial interpolating the printed determinant values over `F_p` is
not an honest producer object.  The small actual-CM rows are not raw
Frobenius-compatible as base-field sequences, so the safe algebra is the
split/cyclic product algebra with explicit orbit factors or descended norm
scalars.

The factorwise audit makes this concrete in the pinned row:

```text
frobenius_compatibility_mismatches=6/7,
split_interpolation_eval_mismatches=0,
base_polynomial_possible=0,
ordinary_base_factor_residues_possible=0.
```

The corresponding finite gate is:

```text
p24/lean/TraceGcdCyclicFactorGate.lean
p24/lang_trace_gcd_factor_bezout_boundary.md
```

The crossed-product audit gives the positive replacement:

```text
weighted_shift_match=1,
ordinary_power_match=0 on nonconstant orbits.
```

The crossed-weight spectral audit gives the limit of this replacement:

```text
small right-7 row:
  one full nonzero Fourier orbit, BM order=3;

p24 right-211 tail-16 exterior support:
  full Fourier support is available by k=3.
```

So a one-degree-35 recurrence/norm theorem for p24 would need special
CM/Plucker cancellations, not just crossed-product algebra.

Source:

```text
p24/lang_trace_gcd_crossed_weight_spectral_boundary.md
```

### Degree-35 Spectral Collapse

The small right-7 trace-GCD row has one-orbit DFT support, but p24 exterior
support is full by `k=3`.  Therefore a p24 one-degree-35 support theorem would
require special CM/Plucker cancellations, not just the crossed-product or
exterior-power formalism.

### Full-Origin Norm by Class-Set Product

A full-origin norm is a power of the reduced right product in the pinned row,
but computing it by class-set enumeration is `sqrt(p)`-scale in disguise.
It helps only if a closed formula supplies the norm.

Source:

```text
p24/trace_gcd_full_origin_norm_boundary.md
```

## What Would Count As Progress

A successful producer theorem may provide any of:

```text
1. the seven Pi_O and proof they are the actual orbit norms;
2. seven block-cycle/crossed-product reduced norms and p-unit witnesses;
3. factorwise Bezout/unit witnesses for the actual descended/twisted orbit
   residue in every orbit algebra;
4. determinant-level Kummer orbit norms Theta_O with zero-detection.
```

All four instantiate the existing finite gates.  The arithmetic burden is
constructing the actual `f_trace`/orbit norms from the embedded CM tower
without enumerating the class set.

Computation is useful here only as a bounded theorem debugger: exact orbit
manifests, small-CM falsification, randomized finite-algebra stress tests,
and Lean verifier gates.  It should not be used to enumerate the p24 class
set or to compute class-set products directly.

The class-field-facing producer theorem is now phrased as the embedded
Plucker/Fitting orbit-norm theorem in:

```text
p24/trace_gcd_classfield_producer_target_20260605.md
```

It requires relative `157/211` phase data to construct the determinant
section `f_trace` itself, then prove the seven orbit norms are p-units.

## Verification Commands

Current finite/formula checks:

```text
lean p24/lean/PluckerKummerOrbitNormGate.lean

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/lang_trace_gcd_plucker_kummer_descent_audit.py \
  --only-D -13319 --only-q 13463 --q-start 13463 --q-stop 13464 \
  --only-m 28 --only-left 4 --only-right 7 \
  --include-linear --max-factor-degree 8 --max-extension-degree 8 \
  --min-left-orbit-len 2 --require-square-tail \
  --max-origin-shifts 140

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/lang_trace_gcd_orbit_product_formula_audit.py \
  --only-D -13319 --only-q 13463 --q-start 13463 --q-stop 13464 \
  --only-m 28 --only-left 4 --only-right 7 \
  --include-linear --max-factor-degree 8 --max-extension-degree 8 \
  --min-left-orbit-len 2 --require-square-tail \
  --max-origin-shifts 140 --relation-bound 5
```

These checks do not prove the p24 certificate.  They sharpen the remaining
theorem and rule out over-compressed theorem candidates.
