# Trace-GCD Sub-Sqrt Certificate Manifest

Date: 2026-06-05

This is the finite landing surface for the current mixed representative
trace-GCD route for

```text
p = 10^24 + 7.
```

It is not the arithmetic producer theorem.  It records the exact verifier
payloads that would prove the selected p24 row once a class-field/operator
identity supplies honest values or honest zero-detection.

## Fixed p24 Data

```text
h = 205880396014 = 66254 * 3107441
m = 66254 = 2 * 157 * 211
n = 3107441
sqrt(p) = 1000000000000

left factor  = 157,  ord_p(157) = 156
right factor = 211,  ord_p(211) = 35

right Frobenius orbits = {0} plus six length-35 orbits
unit 2 mod 211 cycles the six nonzero right orbits
selected representative:
  deleted orbit = O4
  prefix blocks = O2,O3,O5,O6
  prefix dimension = 4 * 35 = 140
  tail block = O1
  tail coordinates = first 16 Lang coordinates of O1
```

The determinant sequence is

```text
Delta(t) = det(P V_t A),        t mod 211,
```

where `A` is the transported tail map from the four-prefix trace kernel,
`V_t` is right multiplication by `zeta_211^t`, and `P` selects the 16 tail
coordinates.

The finite target is

```text
Delta(t) != 0 for every t mod 211.
```

By the Schubert/support dictionary, this is equivalent to avoiding all
translated bad Schubert intersections for the 54-coordinate erasure support
`O4 + first19(O1)`.  The selected representative then feeds the existing
unit-orbit/inversion gates for the six deletion rows.

## Payload Options

### 1. Pointwise value certificate

Supply

```text
Delta_0,...,Delta_210 in F_p
Inv_0,...,Inv_210 in F_p
```

and verify

```text
Delta_t * Inv_t = 1 mod p,      for all t.
```

Payload count:

```text
422 base-field elements
422 / sqrt(p) = 4.22e-10.
```

This is the safest finite certificate.  It still needs a producer theorem
identifying the supplied `Delta_t` as the actual trace-GCD determinants
without enumerating the class set.

### 2. Seven orbit-product certificate

Supply one product and inverse for each orbit of multiplication by `p` on
`Z/211Z`:

```text
Pi_O = prod_{t in O} Delta(t),
Pi_O_inv,
O in {0} plus six length-35 orbits.
```

Payload count:

```text
14 base-field elements
14 / sqrt(p) = 1.4e-11.
```

The conditional unit-2 compression shrinks this further if the producer proves
right-unit equivariance of the actual determinant-line/Fitting sections up to
p-unit transition factors:

```text
Pi_O0, Pi_O0_inv,
Pi_Orep, Pi_Orep_inv
```

Payload count:

```text
4 base-field elements
4 / sqrt(p) = 4e-12.
```

The finite p24 orbit action is checked in:

```text
p24/trace_gcd_unit2_orbit_compression_audit.py
p24/lean/UnitOrbitGate.lean
p24/lean/TraceGcdDiamondEquivarianceGate.lean
p24/lean/TraceGcdTwoOrbitCompressionGate.lean
```

The actual-CM warning audit:

```text
p24/trace_gcd_actual_cm_unit_action_falsifier.py
```

shows the theorem must use p-unit-scale determinant-line comparisons, not
literal equality of printed orbit products.

The proof-facing split is:

```text
p24/trace_gcd_diamond_fitting_equivariance_target.md
p24/trace_gcd_two_linearized_resultant_target.md
p24/trace_gcd_two_resultant_proof_route_synthesis.md
p24/trace_gcd_semilinear_fitting_nonintersection_attack.md
p24/trace_gcd_two_resultant_theorem_manifest.py
```

After the diamond/Fitting equivariance theorem, the arithmetic nonvanishing
problem is reduced to the fixed orbit and one nonzero representative orbit.

The CS-theory side door to the same nonintersection lemma is now split into a
proved finite coordinate identity and a still-missing arithmetic bridge:

```text
p24/trace_gcd_difference_dft_bridge.md
p24/trace_gcd_difference_dft_bridge_audit.py
p24/trace_gcd_lambda_profile_bridge.md
p24/trace_gcd_lambda_profile_bridge_audit.py
p24/trace_gcd_lambda_plateau_rowspace_audit.py
p24/trace_gcd_lambda_plateau_det_ratio_audit.py
p24/trace_gcd_trace_pairing_subspace_bridge.md
p24/trace_gcd_trace_pairing_subspace_bridge_audit.py
p24/trace_gcd_trace_pairing_subspace_bridge_toy.py
p24/trace_gcd_residual_product_punit_theorem.md
p24/trace_gcd_residual_moore_chow_section.md
p24/trace_gcd_residual_moore_chow_toy.py
p24/trace_gcd_residual_schur_pivot_target.md
p24/trace_gcd_residual_schur_complement_toy.py
p24/trace_gcd_prefix_adjoint_trace_independence.md
p24/trace_gcd_prefix_adjoint_trace_toy.py
p24/trace_gcd_prefix_hilbert90_nonintersection.md
p24/trace_gcd_prefix_hilbert90_toy.py
p24/trace_gcd_prefix_coinvariant_fitting_target.md
p24/lean/TraceGcdPrefixAdjointGate.lean
p24/lean/TraceGcdPrefixCoinvariantFittingGate.lean
p24/trace_gcd_dual_sparse_uncertainty_bridge.md
p24/lean/TraceGcdDualSparseBridgeGate.lean
p24/lean/TraceGcdTracePairingSubspaceBridgeGate.lean
```

The audited identity says cyclic difference is p-unit diagonal scaling on
nonzero right Fourier coordinates.  The lambda-level audit also verifies that
the centered profile word, right periods, and Lang/Fitting coordinates carry
the same parameter and the same right-orbit zero conditions.  What remains is
proving that the same trace-GCD bad kernel parameter is constant on the
selected 157-term plateau; direct rowspace equality is false on the holdout.
The rowspace bridge audit currently passes only vacuously in small rows
because their selected leading maps already have full rank.
The determinant-ratio audit shows nonzero but varying leading/plateau ratios
in the square holdout, so there is no obvious universal scalar comparison.
The trace-pairing/subspace bridge audit then identifies the selected
trace-GCD leading determinant with the same nonzero event as the incremental
Moore residual norm product on the same coordinates; this sharpens the
producer theorem but does not prove p24.
The low-rank bridge toy checks the all-coordinate residual-product convention:
dependent coordinates make the product zero.
The residual Moore/Chow toy further identifies the actual section: the full
residual product is the Moore determinant, the full Moore determinant is a
fixed Moore-basis unit times the coordinate Chow determinant, and the
prefix/tail split uses the Moore determinant of prefix-annihilator tail
images rather than raw tail coordinates.
The Schur-complement toy gives an ordinary base-field representative of the
same quotient-tail section: after a p-unit prefix Plucker pivot, the
quotient-tail Moore p-unit is equivalent to a `16 x 16` Schur complement
p-unit.
The prefix-adjoint note removes one coordinate choice from the prefix side:
the rank-140 prefix theorem is equivalent to injectivity of

```text
R^4 -> L,
(y_j) |-> Tr_{E/L}(sum_{j in {2,3,5,6}} y_j*S_j).
```

Thus a named prefix Plucker pivot is a consequence of a relative-trace
independence theorem for four actual CM periods.  The toy checks this
surjectivity/adjoint-injectivity equivalence in coprime finite extensions
with a positive-dimensional kernel control.
The Hilbert-90 note gives the same theorem a coboundary form:

```text
R^4 -> E/(tau_R - 1)E,
(y_j) -> [sum_{j in {2,3,5,6}} y_j*S_j],
```

and asks that this quotient map be injective.  This is the most
class-field-facing prefix target now: no nonzero four-prefix resolvent
combination is a relative trace coboundary.
Because the map is `140 -> 156` in scalar dimensions, the intrinsic p-local
determinant object is the maximal-minor/Fitting ideal

```text
Fitt_16(coker(R^4 -> E/(tau_R-1)E)).
```

Unitness of that ideal is exactly the coordinate-free prefix p-unit theorem.
The normal-basis coefficient note then removes the quotient notation:
choosing a trace-dual normal basis of `R/F_p`, the prefix theorem is exactly
rank `140` of the coefficient family

```text
Tr_{E/L}(alpha_i * H_{157,211}(1,v_j)),
j in {2,3,5,6}, 0 <= i < 35.
```

The accompanying toy checks the reconstruction identity and rank equivalence:

```text
p24/trace_gcd_prefix_normal_basis_coefficients.md
p24/trace_gcd_prefix_normal_basis_toy.py
```

The p24 right field has a canonical type-6 Gaussian normal basis because
`211=6*35+1`; this makes the same prefix determinant a cyclic convolution of
six-term Gaussian periods with the right Frobenius orbit of
`H_{157,211}(1,v_j)`:

```text
p24/trace_gcd_prefix_gaussian_period_basis.md
p24/trace_gcd_prefix_gaussian_normal_basis_toy.py
```

The right-cycle DFT of this Gaussian convolution is useful only after
faithful scalar extension to `L tensor F_p(mu_35)`.  Collapsing the DFT
coefficients into `L` can change `F_p`-rank; the boundary toy records this:

```text
p24/trace_gcd_prefix_gaussian_dft_scalar_extension_boundary.md
p24/trace_gcd_prefix_gaussian_dft_boundary_toy.py
```

The Gaussian DFT factor `G_a` is a unit, but because it is a target-algebra
unit rather than a base scalar, one cannot remove all `G_a` factors
frequency-by-frequency in the full `140`-column rank test:

```text
p24/trace_gcd_prefix_gaussian_unit_factor_boundary.md
p24/trace_gcd_prefix_unit_scaling_pitfall_toy.py
```

After decomposition

```text
L tensor F_p(mu_35) ~= L^4,
```

the full rank theorem becomes a four-component twisted kernel
transversality statement:

```text
p24/trace_gcd_prefix_tensor_component_rank_criterion.md
p24/trace_gcd_prefix_tensor_component_rank_toy.py
```

The component equations can be written using one collapsed Gaussian
frequency table `V_{a,j}`:

```text
sum_{a,j} x_{a,j}^{p^r} V_{p^r a,j} = 0,   r=0,1,2,3.
```

This bookkeeping is recorded in:

```text
p24/trace_gcd_prefix_component_frobenius_bookkeeping.md
p24/trace_gcd_prefix_component_frobenius_toy.py
```

This now has an equivalent invariant-core form.  Let

```text
C = ker(M_0),       M_0(x)=sum_{a,j} x_{a,j}V_{a,j},
(T x)_{b,j}=x_{p^{-1}b,j}^p.
```

Then the prefix theorem is:

```text
core_T(C) = {x : T^r x in C for r=0,1,2,3} = {0}.
```

The first component kernel has dimension at least `101` over `K`; the
nontrivial claim is that this large kernel contains no nonzero semilinear
`T`-stable core.  This is the current best CS/probability-facing
subspace-evasive formulation:

```text
p24/trace_gcd_prefix_semilinear_core_criterion.md
p24/trace_gcd_prefix_semilinear_core_toy.py
```

Semilinear descent further reduces nonzero core detection to fixed
relations:

```text
core_T(C) != 0
  <=>
ker(M_0) cap Fix(T) != 0.
```

The fixed coordinates have p24 shape:

```text
F_p^28 + K^28 -> L,
```

where each length-4 frequency orbit contributes a linearized packet
`sum_{r=0}^3 z^{p^r} V_{p^r a,j}`.  This is recorded in:

```text
p24/trace_gcd_prefix_semilinear_descent_fixed_relation.md
p24/trace_gcd_prefix_semilinear_descent_toy.py
```

The trace-adjoint of this fixed map is a syndrome map

```text
L -> F_p^28 + K^28
```

with length-4 orbit coordinates

```text
sum_{r=0}^3 Tr_{L/K}(lambda V_{p^r a,j})^{p^{4-r}}.
```

Surjectivity of this syndrome map is equivalent to the prefix theorem and
gives the most explicit rank-metric / linearized-polynomial certificate
surface currently available:

```text
p24/trace_gcd_prefix_semilinear_fixed_adjoint.md
p24/trace_gcd_prefix_semilinear_fixed_adjoint_toy.py
```

Choosing an `F_p`-basis `theta_t` of `K`, the `K`-syndrome coordinates are
represented by the `L/F_p` trace-pairing elements

```text
sum_r theta_t^{p^r} V_{p^r a,j}.
```

Therefore the prefix theorem is equivalent to full `F_p`-rank of `140`
explicit syndrome coordinate elements in `L`, or to nonzero Moore residual
product:

```text
p24/trace_gcd_prefix_syndrome_moore_certificate.md
p24/trace_gcd_prefix_syndrome_moore_toy.py
```

The handoff from this prefix-only p-unit to the representative `140+16`
two-resultant surface is:

```text
p24/trace_gcd_prefix_syndrome_resultant_bridge.md
p24/trace_gcd_prefix_syndrome_resultant_bridge_toy.py
```

It records the finite fact that prefix syndrome surjectivity leaves a
`16`-dimensional kernel in `L`, and the selected tail resultant is exactly the
test that the first `16` tail coordinates are injective on that kernel.

The actual-CM holdout audit:

```text
p24/trace_gcd_two_resultant_holdout_audit.py
```

checks this two-resultant surface on the pinned `D=-13319` row and the
independent `D=-26759` holdout.  It reports:

```text
selected_two_punit_groups=4/4
punit_transport_edges=8/8
literal_equal_nonzero_edges=0/8
split_norm_matches=12/12
naive_base_polynomial_groups=0/4
```

This supports the fixed-plus-one-crossed-norm theorem shape and keeps the
semilinear/crossed-product distinction explicit.

The executable schema is:

```text
p24/trace_gcd_orbit_norm_certificate_verifier.py --unit2-schema
```

and a conditional compressed payload is checked with:

```text
p24/trace_gcd_orbit_norm_certificate_verifier.py --unit2 certificate.json
```

This verifies only the two unit equations.  Soundness still requires producer
honesty for those two values and the diamond p-unit transition theorem around
the six nonzero orbits.

This is valid only with an explicit soundness theorem:

```text
Delta(t) = 0  =>  Pi_{orbit(t)} = 0.
```

Equivalently, the producer must prove that each supplied `Pi_O` is the actual
orbit product of the actual determinant sequence.  Orbit products alone are
not enough; otherwise one could supply unrelated nonzero scalars.

The correct algebraic interpretation is crossed-product, not ordinary
base-factor evaluation:

```text
Pi_O = det(e_i |-> Delta(q^i*t_0) e_{i+1})
```

for each Frobenius orbit `O`.  Since p24 nonzero orbit lengths are `35`, the
weighted-cycle sign is positive.  This is recorded in:

```text
p24/lang_trace_gcd_crossed_product_orbit_boundary.md
p24/lean/TraceGcdCrossedProductGate.lean
```

The matrix-level version replaces each scalar weight
`Delta(t)` by the actual square tail-on-kernel matrix `M_t`:

```text
Pi_O = det(e_i |-> M_{q^i*t_0} e_{i+1})
```

for p24 nonzero orbits, because `16*(35-1)` is even.  This Fitting-object
form is recorded in:

```text
p24/lang_trace_gcd_block_cycle_norm_boundary.md
p24/lean/TraceGcdBlockCycleGate.lean
```

The current faithful small-row microscope for these actual orbit products is:

```text
p24/trace_gcd_actual_cm_orbit_norm_miner.py
p24/trace_gcd_actual_cm_orbit_norm_mining.md
```

On the pinned actual-CM row `D=-13319, q=13463, h=140, m=28, n=5,
right=7`, it computes six positive-size orbit norms and reports:

```text
nonzero_orbits=6
zero_or_bad_orbits=0
```

This validates the finite Fitting payload shape on actual small CM data.  It
does not replace the p24 producer theorem proving that the seven p24 orbit
products are honest p-units.

The verifier-side block-cycle contract, exact p24 Frobenius orbits, and
payload accounting are pinned in:

```text
p24/trace_gcd_block_cycle_certificate_spec.md
p24/trace_gcd_block_cycle_certificate_manifest.py
p24/trace_gcd_orbit_norm_certificate_verifier.py
```

The verifier script checks the finite 14-element payload:

```text
Pi_O * Pi_O_inv = 1 mod p,  O=O0,...,O6.
```

It deliberately prints `producer_honesty_required=1`, because nonzero scalars
are meaningful only after the arithmetic theorem identifies them with the
actual phase-aware Fitting orbit norms.

### 3. Split-algebra Bezout/resultant certificate

Supply a split-algebra representative

```text
f(Y) = det(P diag(Y^v) A)
```

and a Bezout identity in the product/splitting algebra:

```text
U(Y) f(Y) + V(Y) (Y^211 - 1) = 1.
```

This proves `gcd(f,Y^211-1)=1`, hence every `Delta(t)=f(zeta_211^t)` is
nonzero.  It is a good verifier surface when the producer theorem naturally
constructs `f`, but it must live in the correct split algebra; the actual
small trace-GCD rows are not raw Frobenius-compatible as base-field
sequences.

The factorwise safe version, if the producer naturally constructs it, is:

```text
for each irreducible factor Phi_O of Y^211-1,
  supply the actual descended/twisted residue of f_trace in the correct
  orbit algebra and a Bezout inverse there.
```

This is not the same as fitting the raw printed determinant values by
ordinary residues in `F_p[Y]/Phi_O`: the small actual-CM row fails Frobenius
compatibility on every nontrivial orbit.  Raw split values or explicit split
residues have the same coefficient scale as the pointwise value payload
(`2*211 = 422` field elements).  The finite factor gate and the small-row
incompatibility audit are:

```text
p24/lean/TraceGcdCyclicFactorGate.lean
p24/lang_trace_gcd_factor_bezout_boundary.md
```

### 4. One operator-norm certificate

Supply

```text
Norm_trace = det(m_f on F[Y]/(Y^211 - 1)),
Norm_trace_inv
```

and verify `Norm_trace * Norm_trace_inv = 1`.  Payload count:

```text
2 base-field elements
2 / sqrt(p) = 2e-12.
```

This is the smallest payload, but it has the strongest honesty requirement:

```text
(exists t, Delta(t)=0)  =>  Norm_trace = 0.
```

The current operator-norm theorem gives the correct formal target:

```text
prod_t Delta(t)
  = det(m_f on F[Y]/(Y^211 - 1))
  = Res(Y^211 - 1, f(Y)).
```

The missing theorem is to construct the actual p-integral `f` or norm from
the embedded class-field trace-GCD data and prove it is a p-unit.

The selected Lang-head projection itself is not the source of the missing
p-unit: in the split exterior expansion, every fixed head minor is a p-unit
by a consecutive-row Vandermonde calculation.  See:

```text
p24/trace_gcd_fourier_minor_unit_theorem.md
p24/fourier_head_minor_unit_audit.py
p24/trace_gcd_cm_plucker_fitting_norm_frontier.md
```

So the one-operator producer must prove noncancellation for the actual CM
Plucker/Fitting coefficients, or identify the whole determinant section with
a p-unit class-field norm.

The end-to-end finite implication from this two-element payload to the mixed
rank certificate is checked in:

```text
p24/lean/TraceGcdOperatorRepresentativeGate.lean
```

It packages the chain:

```text
operator norm p-unit
+ honest zero-detection for the actual Delta(t) sequence
=> selected representative determinant nonzero
+ right-unit propagation over six deletion rows
=> delete-one separation
=> right support >= 2
=> mixed rank certificate.
```

The intrinsic Chow/Borcherds version of this same two-element surface is:

```text
Pi_all = prod_{t mod 211} Chow_t(W,C)
```

or an explicitly constructed phase-aware product `Psi_all` with

```text
Psi_all = p-unit * Pi_all.
```

If `Psi_all` is a p-unit by a zero-local-intersection formula, then every
translated Chow value is nonzero.  The finite gate is:

```text
p24/lean/TraceGcdChowBorcherdsPUnitGate.lean
```

and the handoff is recorded in:

```text
p24/trace_gcd_global_chow_borcherds_handoff.md
```

The relative Kummer route must construct the determinant/Plucker object
itself, not merely prove coordinatewise relative traces nonzero:

```text
p24/trace_gcd_kummer_determinant_boundary.md
p24/trace_gcd_plucker_kummer_payload.md
```

In this form the payload may be `Theta(t)=unit*Delta(t)^r` rather than
`Delta(t)` itself.  It has the same finite nonzero force, but may be more
natural for an embedded class-field/Kummer producer theorem.

The producer must also prove that `Theta(t)` descends from the hidden cyclic
labeling.  If only an orbit of Plucker coordinates descends, use the
orbit-product payload instead.

### 5. Hermitian-Schur Gram-product certificate

The orbitwise Schur bridge gives another sub-sqrt landing surface.  For each
right Frobenius orbit `O`, define:

```text
Pi_O = prod_{t in O} det(B_t | ker A_t)
P_O  = prod_{t in O} det(A_t G^{-1} A_t^T)
L_O  = prod_{t in O} det([A_t;B_t] G^{-1} [A_t;B_t]^T)
K_O  = prod_{t in O} det(N_t^T G N_t)
```

where `G` is the trace-pairing matrix in the chosen basis and `N_t` is a
kernel basis for the transported prefix matrix `A_t`.  The finite Schur bridge
proves nonzero `Pi_O` from the zero-detection implication:

```text
Pi_O = 0  =>  L_O = 0 or K_O = 0.
```

For a nondegenerate ambient trace pairing, `ker A_t` is the orthogonal
complement of the prefix row space.  Therefore a prefix Gram p-unit implies
the corresponding kernel Gram p-unit.  The natural minimal Gram payload
supplies:

```text
P_O, P_O_inv, L_O, L_O_inv for seven orbits
```

with size:

```text
28 base-field elements
28 / sqrt(p) = 2.8e-11.
```

The conservative payload also includes kernel Gram products:

```text
P_O, P_O_inv, L_O, L_O_inv, K_O, K_O_inv for seven orbits
```

with size:

```text
42 base-field elements
42 / sqrt(p) = 4.2e-11.
```

The finite implication is Lean-checked in:

```text
p24/lean/TraceGcdSchurBridgeGate.lean
```

The prefix/full refinement, including why kernel Gram is not an independent
arithmetic payload, is recorded in:

```text
p24/trace_gcd_prefix_full_gram_payload_refinement.md
p24/trace_gcd_prefix_gram_self_orthogonal_obstruction.md
p24/trace_gcd_metric_schur_refinement.md
p24/trace_gcd_prefix_subcode_distance_boundary.md
```

and the actual-CM falsifier is:

```text
p24/orbitwise_schur_bridge_falsifier.py
p24/orbitwise_schur_bridge_falsifier.md
```

This surface is attractive only if a Hermitian packet/autocorrelation theorem
can prove the actual Gram products are p-units.  It is stronger than the
direct Fitting determinant route because finite-field Gram nondegeneracy does
not follow from rank.  The sharp missing prefix lemma is:

```text
For each selected trace-GCD prefix row space U_t,
U_t cap U_t^perp = 0.
```

Equivalently, no nonzero prefix-supported trace word is orthogonal to every
prefix-supported trace word.  This is the self-orthogonal-line obstruction
isolated in the note above.  In matrix terms this is the metric-aware
condition `det(A_t G^{-1} A_t^T) != 0`; ordinary `det(A_t A_t^T)` is only a
coordinate-dot plumbing check.

The actual-CM descent audit:

```text
p24/lang_trace_gcd_plucker_kummer_descent_boundary.md
p24/lang_trace_gcd_orbit_product_formula_boundary.md
```

supports the orbit-product interpretation: in the pinned row, individual
values and tested nontrivial powers descend only on the trivial orbit, while
all Frobenius orbit products are nonzero.  A follow-up formula audit finds no
fixed-row equality or small-power shortcut among those orbit products.

The finite Plucker/Kummer orbit-norm gate is recorded in:

```text
p24/lean/PluckerKummerOrbitNormGate.lean
```

## Lean Gate

The payload distinction is Lean-checked in:

```text
p24/lean/TraceGcdPayloadGate.lean
```

The key interfaces are:

```text
PointwiseUnitPayload
OrbitProductSound
CompressedNormSound
```

The pointwise payload proves all `Delta(t)` nonzero directly.  The seven
orbit-product and one-norm payloads prove it only after the corresponding
soundness theorem is supplied.  This closes the finite verifier gap in the
previous resultant spec.

## Current Producer Theorem Target

The best current arithmetic target is:

```text
Construct a p-integral class-field element f_trace(Y) such that
  f_trace(zeta_211^t) = unit(t) * det(P V_t A)
for every t mod 211,
and prove
  Res(Y^211 - 1, f_trace(Y)) is a p-unit.
```

The unit factors must be p-units, covered by the integrality note.  This
single theorem would instantiate the one-norm payload.  A weaker theorem that
constructs the 211 values, or the seven orbit products, would still beat
`sqrt(p)` by many orders of magnitude.

Related notes:

```text
p24/trace_gcd_local_unit_proof_target.md
p24/lang_trace_gcd_resultant_certificate_spec.md
p24/lang_trace_gcd_operator_norm_theorem.md
p24/lang_trace_gcd_integrality_lift.md
p24/lang_trace_gcd_schubert_orbit_theorem.md
p24/trace_gcd_schubert_support_dictionary.md
p24/punit_route_comparison_frontier.md
```
