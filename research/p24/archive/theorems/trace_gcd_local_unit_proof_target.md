# Trace-GCD Local-Unit Proof Target

Date: 2026-06-05

This note is the current proof-facing version of the p24 trace-GCD route.  It
is narrower than a blanket MDS theorem and more intrinsic than a raw list of
determinants.

## Representative Field-Intersection Statement

Let

```text
L = F_p(mu_157),        [L:F_p] = 156
R = F_p(mu_211),        [R:F_p] = 35
E = L R
```

and let the six mixed periods be

```text
S_j = H_{157,211}(1,v_j) in E,
```

where `v_j` runs through the six nonzero Frobenius-orbit representatives
modulo `211`.

For the representative row use

```text
deleted O4
prefix B = {O2,O3,O5,O6}
tail T = first 16 Lang coordinates of O1.
```

Let

```text
A_B : L -> R^4
lambda |-> (Tr_{E/R}(lambda*S_j))_{j in B}.
```

The first local-unit theorem is:

```text
dim_Fp ker(A_B) = 16.
```

Let `K = ker(A_B)`, and let

```text
tau_1,...,tau_16 : K -> F_p
```

be the selected first-16 Lang coordinate functionals of the `O1` trace block.
The second local-unit theorem is:

```text
det(tau_a(k_b))_{1<=a,b<=16} is a p-unit
```

for any `F_p` basis `k_1,...,k_16` of `K`.

Together:

```text
four full right blocks cut L down to the expected 16-dimensional residual
subspace, and the chosen 16 tail coordinates separate that residual.
```

This is the representative `140+16` p-unit theorem.

## Orbit-Norm Strengthening

The selected determinant depends on the right origin.  Let

```text
Delta(t) = det(tail_16 on K_t),        t mod 211,
```

where `K_t` is the transported prefix kernel.

The stronger current certificate target is orbitwise:

```text
Pi_O = prod_{t in O} Delta(t)
```

for the seven Frobenius orbits on `Z/211Z`.

Equivalently, for a nonzero orbit

```text
O = {t0, q*t0, ..., q^34*t0},
q = p mod 211 = 114,
```

form the block-cycle/Fitting operator

```text
B_O e_i = M_{q^i t0} e_{i+1},
Delta(q^i t0) = det(M_{q^i t0}).
```

Since `k=16` and `|O|=35`,

```text
det(B_O) = prod_{t in O} Delta(t)
```

with positive sign.

Thus the producer theorem can be phrased as:

```text
for every O, the finite p-integral failure module coker(B_O) has unit
zeroth Fitting ideal at the selected prime over p.
```

Equivalently:

```text
there is no nonzero orbit-family of transported prefix-kernel sections whose
block-cycle tail image is zero.
```

This is the exact local-intersection statement the class-field proof should
attack.

## Why Not Prove Full MDS First?

The support dictionary shows that the bad event is a codeword of scalar
support at most

```text
35 + 19 = 54.
```

A scalar `[210,156,55]` MDS theorem would prove the representative row, since
`55` is the Singleton bound.  But this is stronger than needed.

Small actual-CM audits keep the MDS language plausible but not proof-like:

```text
Lang arc-strength audit on D=-13319, q=13463, pair=(4,7):
  subset_total=15
  subset_full=15
  subset_bad=0
  random_full_arc_count=50/50

Lang projective-relation audit on the same row:
  degree=2 relation_nullity=0
  random_positive_nullity_count=0/50
```

So the tested actual-CM row is a full arc, but it is not visibly a
low-degree rational-normal/GRS object in the natural Lang coordinates, and
random controls satisfy the same small full-arc test.  A full-MDS proof would
therefore still need a hidden class-field block equivalence or a p-unit
identity.  It is not currently easier than the representative local-unit
theorem.

## Productive Computation From Here

Computation should be used only for bounded falsification of theorem shapes:

```text
1. test block-cycle/Fitting determinant identities on small actual-CM rows;
2. test whether proposed prefix kernels have stable annihilator or residual
   norm formulas;
3. check equivariant Lang-coordinate conventions under right-unit and
   inversion actions;
4. mine unusually stable residual products only when they suggest an exact
   class-field identity.
```

The finite singular-control toy for item 1 is:

```text
p24/block_cycle_fitting_zero_detection_toy.py
```

The Hermitian/Gram bridge falsifier for item 2 is:

```text
p24/orbitwise_schur_bridge_falsifier.py
p24/orbitwise_schur_bridge_falsifier.md
```

It checks the orbitwise identity

```text
prod_O det([A_t;B_t] G^{-1} [A_t;B_t]^T) det(N_t^T G N_t)
  = prod_O det(A_t G^{-1} A_t^T) det(B_t N_t)^2
```

on actual small-CM trace-GCD rows in `--metric-aware` mode.  The pinned right-7
row and tiny nonzero prefix rows pass, but this remains a stronger Gram p-unit
route than the direct Fitting determinant.

It should not be used for:

```text
1. p24 class-set enumeration;
2. raw p24 determinant scans;
3. full-origin products unless a closed formula supplies them;
4. more random-rank sweeps without a new theorem candidate.
```

## Current Finite Evidence

The representative block-cycle formula is mechanically checked by:

```text
p24/lean/TraceGcdBlockCycleGate.lean
p24/lang_trace_gcd_block_cycle_norm_audit.py
```

The exact p24 orbit and payload contract is:

```text
p24/trace_gcd_block_cycle_certificate_spec.md
p24/trace_gcd_block_cycle_certificate_manifest.py
```

The representative linearized trace-gcd gate is:

```text
p24/lean/TraceGcdLocalUnitGate.lean
p24/lean/TraceGcdOperatorRepresentativeGate.lean
p24/lean/TraceGcdGate.lean
p24/linearized_trace_gcd_certificate_boundary.md
```

`TraceGcdLocalUnitGate.lean` joins the local `140+16` trace-gcd statement to
the seven-orbit Fitting-unit payload: if the honest block-cycle norms are
units and every determinant zero would zero its orbit Fitting norm, then the
representative determinant is nonzero.  It also checks the p24 number facts
`4*35+16=156`, `35+19<55`, and positive block-cycle sign.

`TraceGcdOperatorRepresentativeGate.lean` is the one-operator analogue: if an
honest global operator norm for `Delta(t)` is a p-unit and detects every
possible determinant zero, then the selected representative determinant is
nonzero, unit-2 propagation supplies all six deletion rows, and the existing
support-to-rank handoff gives the mixed rank certificate.

The local intersection / trace-pairing formulation is:

```text
p24/hermitian_mixed_trace_intersection_theorem.md
p24/lean/MixedTraceIntersectionGate.lean
```

The p24 local arithmetic needed by any p-adic/local-intersection proof is:

```text
p24/trace_gcd_p24_local_invariants.py
p24/trace_gcd_p24_local_intersection_invariants.md
p24/trace_gcd_ordinary_fitting_disjointness_criterion.md
```

It fixes the split ordinary prime orientations by
`sqrt(D_K)=+/-t/2 mod p`, verifies `p` is unramified in `K`, and checks that
all certificate levels are prime to `p`.  This removes denominator ambiguity
from the local-unit target.  The ordinary Fitting criterion then says the
remaining p-unit theorem is exactly zero local intersection with the actual
phase-aware orbit Schubert/Fitting divisor; it does not construct that
divisor.

The remaining missing theorem is arithmetic:

```text
prove the p-integral representative prefix/tail Fitting determinant, or its
seven right-origin orbit norms, is a p-unit at p = 10^24 + 7.
```

## Lemma Stack To Prove

An independent proof-synthesis pass converged on the following exact lemma
stack.  This is the checklist for turning the finite verifier surface into an
actual certificate producer.

```text
1. Embedded construction:
   build A, V_t, P, K_t, M_t, and f_trace from the conductor-2 CM torsor and
   relative class-character/Kummer data, not from class-set enumeration.

2. p-integral freeness:
   prove the chosen Lang/DFT coordinates, prefix kernels, and determinant
   lines have p-unit denominators; prove prefix rank 140 and kernel rank 16.

3. Honesty/comparison:
   prove the supplied seven norm scalars are exactly det(B_O) for the actual
   trace-GCD maps.

4. Fitting local unit:
   prove Fitt_0(coker B_O) is the unit ideal at the selected prime.

5. Schubert/local-intersection bridge:
   identify det(B_O) with the pullback of the relevant Schubert degeneracy
   divisor and show the p24 CM point has zero local p-intersection with it.

6. Phase-aware class-field control:
   construct the non-genus 157/211 relative phase data paired to the
   conductor-2 j torsor, and show it controls the Plucker/Fitting determinant
   itself, not merely coordinate nonvanishing.
```

The plausible proof route is therefore:

```text
p-integral crossed-product/Fitting order
  -> block-cycle determinant-line section
  -> Schubert/local-intersection divisor
  -> phase-aware class-field or Borcherds/Fitting p-unit formula.
```

A determinant-level Kummer variant remains live if it controls the Plucker
determinant orbit norms directly.  A full-origin Borcherds product formula
would also work, but only if it is a closed formula; computing the full
Hilbert class product would reintroduce the sqrt-scale enumeration.

The class-field-facing version of this same target is recorded in:

```text
p24/trace_gcd_classfield_producer_target_20260605.md
```

under the embedded Plucker/Fitting orbit-norm theorem.  Its key distinction is
that relative `157/211` Kummer or class-character data must construct
`f_trace` or `det(B_O)` itself.  Coordinate p-units, abstract quotient roots,
or a selected child label do not prove determinant nonvanishing.

The latest selected-Schubert p-unit contract is pinned in:

```text
p24/trace_gcd_selected_schubert_punit_frontier.md
p24/lean/TraceGcdSelectedSchubertPUnitGate.lean
```

It restates this local-unit theorem as:

```text
construct an honest p-integral determinant section whose norm detects the
translated Schubert bad divisors, then prove the total norm or the seven
orbit norms are p-units at the selected p24 prime.
```

## Shortcuts Already Rejected

The current local artifacts reject these replacements for the lemma stack:

```text
ordinary residues in F_p[Y]/Phi_O:
  raw determinant values are not Frobenius-compatible;

ordinary Hilbert-90 or power collapse:
  orbit products are not Delta(t0)^35 on nonconstant orbits;

individual Plucker-Kummer descent:
  only the trivial orbit descends in the pinned actual-CM audit;

small fixed-row product relations:
  no equality or small power relation among orbit products was found;

degree-35 spectral collapse:
  p24 exterior support is full by k=3;

coordinatewise Kummer p-units:
  nonzero entries do not prevent determinant collapse;

16 x 16 monodromy compression:
  basis-dependent without a coherent transported-kernel-basis theorem;

abstract bnrclassfield or plain-j selector routes:
  they do not supply an embedded non-genus phase/recovery pairing;

Siegel/Ramachandra distribution relations:
  they live in ray-kernel directions and do not hit the p24 unramified
  157/211 phase layers.
```
