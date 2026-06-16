# Lean Notes

The Lean files here formalize only the finite algebra and certificate logic,
using Lean core rather than Mathlib.

`RelativeResolvent.lean` checks the split-algebra reduction:

```text
split component at (u,l) = root-of-unity multiple of P_u(a).
```

The checked Lean theorem abstracts this to the two facts actually needed:
the level-zero component is `P_u(a)`, and a zero fiber makes its whole split
block zero.  From these it proves that all split components vanish if and only
if all relative fibers vanish.

This is intentionally not a formal proof of the p24 CM nonvanishing theorem.
Lean is useful here for pinning down the finite group/indexing part; the open
arithmetic input is still the p-adic/unit or trace-formula statement proving
nonvanishing for the selected CM embedding.

`CertificateLogic.lean` checks the abstract implication graph around that
arithmetic input:

```text
invertible finite transform:
  all encoded coordinates vanish iff all source coordinates vanish;

content/Bezout certificate:
  if a linear combination of the packet residues is 1, the packet is not
  the zero vector;

product certificate:
  product nonzero is sufficient but stronger than needed;

energy certificate:
  if harmful vanishing forces E_a=0, then E_a!=0 rules it out.

all-packets wrapper:
  content or energy certificates for every orbit rule out every harmful
  Frobenius packet.

global packet norm wrapper:
  one nonzero product/global norm certificate rules out zero packet norms in
  every Frobenius packet.
```

`ZeroLemmaGate.lean` checks the finite logical gate behind the correspondence
zero-lemma attempt:

```text
harmful vanishing gives classNumber zeros;
a nonzero modular function gives at most poleDegree zeros;
poleDegree < classNumber rules out harmful vanishing.
```

It also records the correspondence-window specialization used in
`correspondence_zero_lemma_window.md`: if `classNumber = order * index` and
`poleDegree = order * delta`, then the zero lemma would fire from
`delta < index`.

The same file now records the selected-scalar obstruction used in
`l1_zero_lemma_boundary.md`: a scalar zero on one relative orbit would need
`delta < 1`, and a finite family of scalar functions does not help when the
total pole-degree units are at least the number of pieces.

`TowerTrace.lean` checks the finite tower bookkeeping behind the degree-157
target:

```text
relative trace data plus an inverse transform determines the child periods;
an exact decoded child relation transfers to the true child periods;
an equivariant canonical child section is impossible once the parent returns
  to itself but the child has moved.
```

`PhaseLiftedTowerGate.lean` checks the finite implication behind the
phase-lifted decomposed CM tower certificate:

```text
phase tower root chain
  => strict embedded j root;
strict j root plus Montgomery lift
  => target-trace Montgomery A;
target A plus odd-part projection
  => DANGER3 triple.
```

The open arithmetic input is still the producer theorem for the embedded
`157` and `211` relative phase relations and the selected degree-`3107441`
recovery polynomial.

`PhaseLiftedTowerPayloadGate.lean` checks the finite payload taxonomy for that
same route:

```text
selected-chain payload = 3107811;
full-relative-table payload = 3174011;
formal m+n count = 3173695;
informative child phase payload = 366.
```

It also records the important honesty distinction: selected-chain and
full-relative-table payloads are class-set-free shapes, while the full
`h`-element class table is rejected even though `h < sqrt(p)` for this fixed
instance.  The goal needs a sub-sqrt payload with a class-set-free producer,
not a dense class table whose asymptotic scale is still sqrt-like.

The same gate records the Kummer normal-form payload equality:

```text
top degree-2 slots
+ two forced child-trace slots
+ 366 informative Kummer orbit/minpoly slots
+ selected recovery degree 3107441
= selected-chain payload 3107811.
```

The theorem frontier for that version is
`p24/kummer_orbit_minpoly_producer_frontier.md`.  The prerequisite audit for
abstract relative fiber grouping is
`p24/abstract_tower_fiber_map_boundary.md`.  The payload accounting for the
honest full relative morphism fallback is
`p24/abstract_tower_morphism_payload_boundary.md`.  The low-norm internal
generator boundary for the balanced complement is
`p24/complement_subgroup_generator_boundary.md`.

`TraceGcdAnchorTraceAveragePayloadGate.lean` checks the newer anchor
trace-average sub-surface:

```text
defect H-coset sums = 7;
trace-average plus selected-child profile = 132508;
7 < 132508 < selected-chain payload 3107811 < sqrt(p).
```

It deliberately requires a producer-soundness proposition: equal defect sums
are a tiny verifier payload only when tied to the embedded CM trace-defect
profile.

`TraceGcdAdmissibleJacobiDecompositionGate.lean` checks the corrected finite
handoff for the current Jacobi route:

```text
admissible C-axis Jacobi decomposition
  => no forbidden right-nontrivial/C-trivial bidegrees
  => final internal trace zero
  => product-coboundary/character-payload pipeline
  => 1092 H-coset verifier equations.
```

It also records the rank correction: the termwise-safe admissible p24 span has
rank `621`, while the broader rank-`625` C-axis family includes leaky
directions and needs a separate cancellation hypothesis.  The same gate now
records the spectral rank formula `1 + 7*88 + 4 = 621`, matching the
conjugate-`C/E` pair fingerprint in
`p24/trace_gcd_fixed_frequency_p24_admissible_jacobi_spectral_boundary.md`.

`TraceGcdJacobiAnchorCorrectionGate.lean` records the newest product-formula
handoff:

```text
punctured Hasse-Davenport pair-products and nonzero right-row ratios
  + one selected degenerate-anchor correction
  => full multiplicative producer identities
  => selected-defect value identities
  => 1092 H-coset verifier equations.
```

The corresponding Python gate checks the literal finite-field Jacobi model:
normalizing only `J(1,1)=q-2` by `(q-2)^(-1)` repairs both the C-zero
pair-products and the selected row-product ratio in the sampled right-mixed
rows.

`TraceGcdReducedAnchorAdjacentBridgeGate.lean` records the finite bridge
between that reduced-anchor fingerprint and the older adjacent-anchor route:

```text
reduced anchor's C/E-trivial row-sum slice
  + all six nonfixed right channels
  + invertible adjacent difference
  + opposite raw b=0 leak cancellation
  => old adjacent-anchor projector target.
```

It deliberately keeps the full punctured right-zero row as an external
realization requirement for the CM/Lang producer.

`TraceGcdReducedAnchorSliceDecompositionGate.lean` records the complementary
C-slice split:

```text
reduced anchor = C/E-trivial row-sum slice + C/E-nontrivial residual;
old adjacent-anchor theorem sees only the row-sum slice;
p24 residual has 7*(179-1)=1246 C/E-nontrivial Fourier channels.
```

The residual is the current explicit CM/Lang unit target beyond the old
covariance machinery.

`TraceGcdReducedAnchorCyclotomicDivisorGate.lean` records the next sharpening:
after multiplying the residual by `c`, it is the degree-zero principal divisor

```text
sum_{k != 0} [zeta_c^k] - (c-1)[1]
  = div(Phi_c(X)/(X-1)^(c-1)).
```

For p24 this names the concrete candidate residual unit
`Phi_179(X)/(X-1)^178`; the open arithmetic input is still the p-integral
selected CM/Lang specialization of that divisor.

`TraceGcdReducedAnchorDiamondNormGate.lean` sharpens the producer shape again:
the same residual is the diamond norm over `(Z/cZ)^*` of the one-point divisor
`[zeta_c]-[1]`.  This is a diamond/unit norm on the C-axis multipliers, not
the cyclic `C/E` trace norm.  For p24, this suggests constructing one
p-integral selected CM/Lang factor and taking its `178`-term diamond norm to
obtain `Phi_179(X)/(X-1)^178`.

`TraceGcdAnchorKummerDescentGate.lean` records the positive replacement after
the residual-factor search rules out separate base-field factors.  In an
auxiliary Kummer extension with `beta^c=s`, the row-sum slice and the
cyclotomic residual split, their product descends to the base selected anchor
correction, and the `R_c` exponent is forced to be `1`.  For p24 this points
to an auxiliary Kummer/norm/divisor realization of
`Phi_179(X)/(X-1)^178`, followed by sign normalization and p-integral descent.

`KummerCrossOrbitGlueGate.lean` records the finite correction to the Kummer
normal form:

```text
multi-orbit Kummer phase glue
  => one global cyclic phase
  => selected child polynomial;

selected-chain Kummer payload plus five 211-layer glue extension objects
  = 3107816 extension-object slots;
conservative base-field serialization of those five degree-35 glue orbits
  = 3107986 base-field slots < sqrt(10^24+7).
```

The open arithmetic input is to construct the embedded 211-layer Kummer
orbits and glue invariants, such as `T_a/T_1^a`, without class-set
enumeration.

`CenteredArcProductGate.lean` checks the finite gate behind the compact
centered-profile product route:

```text
seven Frobenius-orbit product p-units
  => every cyclic right-window determinant is nonzero
  => the selected leading difference minor is nonzero
  => the centered marginal has full row rank.
```

It also records the p24 plateau dimensions:

```text
plateau constraints = 156;
full ambient plateau subspace dimension = 55 in F_p^211;
effective centered ambient dimension = 210;
effective centered plateau subspace dimension = 54;
156 + 54 = 210;
nonzero right orbits = 6 of size 35;
orbit factors including t=0 = 7.
```

The arithmetic theorem remains the nonvanishing of the actual p24
centered-marginal orbit products, recorded in
`p24/centered_marginal_cyclic_resultant_theorem.md` and calibrated in
`p24/centered_marginal_transversality_boundary.md`.

`UnitOrbitGate.lean` checks the finite propagation used by the p24 right-unit
compression:

```text
one representative on a six-cycle
  + p-unit-preserving arrows along the cycle
  => all six nonzero orbit p-units;

the fixed zero orbit p-unit
  + the six-cycle representative
  => all seven right-orbit p-units.
```

It also records the concrete payload comparison:

```text
4 < 14 < sqrt(10^24+7).
```

The arithmetic input remains the determinant-line comparison theorem; the
small actual-CM falsifier in
`p24/trace_gcd_actual_cm_unit_action_falsifier.md` shows why the arrows must
be p-unit-scale, not literal scalar equalities.

`TraceGcdDiamondEquivarianceGate.lean` combines the determinant-line unit
scaling with the six-cycle propagation:

```text
Xi_next = epsilon * Xi_current, epsilon a p-unit
  + Xi_current a p-unit
  => Xi_next a p-unit;

fixed orbit p-unit
  + one nonzero representative p-unit
  + p-unit transition factors around the unit-2 cycle
  => all seven orbit p-units.
```

The proof-facing target is
`p24/trace_gcd_diamond_fitting_equivariance_target.md`.

`TraceGcdTwoOrbitCompressionGate.lean` packages the full conditional
4-field certificate implication:

```text
fixed orbit norm p-unit
  + one nonzero representative orbit norm p-unit
  + p-unit determinant-line transition factors around O1,...,O6
  + orbit-norm zero-detection for Schubert/Fitting bad events
  => no translated bad event.
```

This is the Lean counterpart of
`p24/trace_gcd_orbit_norm_certificate_verifier.py --unit2-schema`.

`TraceGcdLinearizedResultantNormGate.lean` records the linearized-resultant
interpretation of the remaining two p-unit statements:

```text
fixed orbit: Res_p-lin(P_K0,T_0) is a p-unit;
nonzero orbit: Norm_O1(Res_p-lin(P_Kt,T_t)) is a p-unit.
```

The proof-facing note is
`p24/trace_gcd_two_linearized_resultant_target.md`.

`TraceGcdTracePairingSubspaceBridgeGate.lean` records the newest finite bridge
between the trace-GCD determinant and the Moore/subspace-polynomial residual
product:

```text
trace-pairing determinant nonzero
  <=> selected leading Lang coordinates span the left field
  <=> incremental residual norm product nonzero.
```

It proves that a p-unit residual product rules out the same bad-lambda event
as a p-unit trace-GCD determinant.  The audit and proof-facing note are:

```text
p24/trace_gcd_trace_pairing_subspace_bridge_audit.py
p24/trace_gcd_trace_pairing_subspace_bridge.md
```

`TraceFrameSelectedTailCrossedProductGate.lean` records the finite handoff for
the corrected trace-frame selected-tail theorem:

```text
selected-tail bad event at beta
  => its beta-orbit product vanishes;
crossed-product reduced norm = beta-orbit product;
all reduced norms p-units, or one global norm p-unit detecting zero factors
  => K_sel,beta = {0} for every beta.
```

The proof-facing note is
`p24/trace_frame_selected_tail_crossed_product_target.md`.

`TraceFrameSelectedTailTensorFactorGate.lean` records the finite compression
gate for the corrected selected-tail determinant line:

```text
one representative selected-tail norm p-unit
  + representative norm detects representative tail determinant zero
  + tensor-factor p-unit transport of the selected-tail line
  => every tensor-factor selected-tail determinant is nonzero
  => no selected-tail bad event in any tensor factor.
```

The proof-facing note is
`p24/trace_frame_selected_tail_tensor_factor_equivariance_boundary.md`.

`TraceFrameSelectedTailPhaseProducerGate.lean` records the finite handoff for
a stronger embedded-tower producer interface:

```text
selected-tail bad event
  => selected-tail determinant or reduced norm is zero;
phase/Kummer payload detects that zero;
phase/Kummer payload is a p-unit, orbitwise or globally
  => no selected-tail bad event.
```

This is the Lean counterpart of
`p24/selected_tail_phase_fitting_producer_frontier.md`.  It lets the missing
arithmetic theorem target a Plucker/Fitting Kummer payload instead of the raw
selected-tail determinant, while keeping the finite zero-detection requirement
explicit.

`TraceFrameSelectedTailBorcherdsGate.lean` adds the local-intersection layer
for the same selected-tail object:

```text
zero local intersection for a phase-aware Borcherds/Chow value
  => that value is a p-unit;
p-unit comparison to the selected-tail phase payload
  => selected-tail phase payload is nonzero;
phase payload detects selected-tail norm zero
  => no selected-tail bad event.
```

The proof-facing note is
`p24/selected_tail_borcherds_local_intersection_frontier.md`.

`TraceFramePrefixTailCrossedPackageGate.lean` records the denominator-safe
package for using that selected-tail theorem:

```text
prefix Schubert p-units Xi_A, Xi_B, Xi_AB
  + selected-tail crossed-product p-units
  => every beta packet has prefix good and K_sel = {0}
  => every trace-frame packet is good.
```

This is the finite version of the Fitting/determinant-line package where the
selected-tail determinant is used only after the prefix chart is certified.

`TraceGcdResidualPrefixTailGate.lean` records the p24 `140+16` residual-product
split:

```text
prefix p-unit + quotient-tail p-unit
  => full residual-product p-unit.
```

The audit is:

```text
p24/trace_gcd_residual_prefix_tail_bridge_audit.py
```

`TraceGcdPrefixSyndromeResultantBridgeGate.lean` records the newer handoff from
the prefix-only syndrome/Moore p-unit to the representative tail resultant:

```text
prefix syndrome p-unit
  => 16-dimensional residual kernel;
tail resultant p-unit
  => selected tail injects on that kernel;
both
  => no representative `140+16` bad event.
```

The finite toy and proof-facing note are:

```text
p24/trace_gcd_prefix_syndrome_resultant_bridge_toy.py
p24/trace_gcd_prefix_syndrome_resultant_bridge.md
```

`TraceGcdFullCoinvariantTailGate.lean` records the square coinvariant version
of the same fixed `140+16` resultant:

```text
R^4 + C_tail -> E/(tau_R - 1)E
```

has source and target dimension `4*35+16=156`; a p-unit determinant for this
map gives the full fixed trace-GCD rank without choosing a prefix-kernel
basis.  The actual-CM bridge verifies that this determinant line is the
trace-pairing determinant divided by the trace Gram unit and has the same zero
event as the residual prefix/tail product on small CM rows.  The same fixed
determinant also has a scalar-extended Gaussian DFT form where the selected
tail is a degree-`<16` Reed-Solomon subspace across the 35 right frequencies.
The RS-tail semilinear-core refinement uses Hilbert 90 to descend the
four-component product-algebra kernel condition to a single fixed-relation
map:

```text
F_p^28 + K^28 + F_p^16 -> L,
28 + 4*28 + 16 = 156.
```

The same fixed determinant now has a trace-adjoint syndrome form:

```text
L -> F_p^28 + K^28 + F_p^16.
```

Surjectivity of this syndrome is equivalent to p-unitness of `det(Psi_RS)`.
This is the proof-facing dual of the explicit RS-tail fixed columns.

The Moore/Schur split now records the same fixed unit as a `140+16` theorem:
the prefix Moore determinant is nonzero and the sixteen RS-tail columns are
independent after quotienting by the prefix span.

The same gate also records the visible-LRS accounting boundary:
the full fixed-source object has `6*(7+7*4)=210` natural columns, the selected
RS-tail square uses `4*(7+7*4)+16=156`, and the unused erasure count is `54`.
It also records that the five selected blocks have `2^5-1=31` nonempty block
subsets for the support-profile gate.  The full Plucker chart has
`156*(35+19)=8424` selected-basis/omitted-column entries.  This is bookkeeping
only; it does not formalize an MSRD theorem.  The sharpened block/skew Cauchy
candidate is a Sylvester displacement identity `A C - C B = R S` for
transported CM/Lang operators; it is not yet a Lean theorem because the
arithmetic operators still have to be identified.  The finite handoff from
low-rank full-column operator boundary to bounded chart displacement is
recorded in Lean; the arithmetic work is to construct `T,A,B` from the CM/Lang
model before seeing the chart.  The current actual-CM boundary audit records
that the smaller rows do not contain a nontrivial selected-basis calibration
row for this full chart.

The first operator candidate for that handoff is the common cyclic/Lang shift on
the six right blocks.  The p24 selected/omitted pattern is four full selected
blocks, one split tail block, and one wholly omitted block, so the expected
operator boundary has rank `2` from the two tail cut edges.  This remains a toy
and bookkeeping statement until the same shift is constructed integrally on the
actual CM columns.

`TraceGcdFrequencyDefectGate.lean` records the non-circular selected-basis
handoff before the Plucker chart is formed:

```text
19 ordinary frequency gates
  + 16 defect frequency gates
  + 16x16 tail Vandermonde p-unit
  => selected 156-coordinate projection is a p-unit.
```

It also checks the p24 numerical profile `19+16=35`,
`19*4+16*5=156`, `4*35+16=156`, `35+(35-16)=54`, and
`gcd(10^24+7,35)=1`.  The open arithmetic input is still proving the local
frequency Plucker minors and defect tail residues are p-units.  The matching
actual-CM frequency-profile audit currently reports no clean p24-like
calibration row among the smaller uploaded rows, so it is boundary evidence
rather than positive proof evidence.  The current non-Lean refinement packages
those local frequency gates as cyclic resultants once the CM/Lang polynomial
sections are identified; the accompanying descent toy rejects post-fit
splitting-field interpolants unless the values satisfy semilinear Frobenius
compatibility.  The p24 support accounting note corrects the easy
overstatement here: Frobenius-stable size-16 supports are either four
length-4 orbits (`35` choices) or four fixed frequencies plus three length-4
orbits (`1225` choices).  Reducing to the pure length-4 selector needs a
no-fixed-defect arithmetic theorem.  The fixed-frequency ordinary gate records
the finite form of that theorem: at each fixed `a in 5Z/35Z`, prove the tail
local value lies in the prefix image, equivalently `rank(P_a,tau_a)=rank(P_a)`.
The fixed-frequency annihilator bridge records the dual trace-pairing form:
every trace functional killing `V_{a,2},V_{a,3},V_{a,5},V_{a,6}` must also kill
`V_{a,1}`.  That is the proof-facing CM/Lang identity; prefix Plucker
p-unitness remains a separate local ordinary gate.  The cyclic syzygy gate
packages the seven fixed-frequency relations as one identity over
`F_p[y]/(y^7-1)`.  `TraceGcdFixedFrequencyOrder7Gate.lean` now formalizes
the finite handoff from order-7 augmentation plus negation covariance and
prefix Plucker p-units to no fixed defects, reducing stable supports from
`1260` to `35`.  The open arithmetic input is still the augmentation
identity itself.

`TraceGcdRightAxisAnchorDescentGate.lean` records the sharper seven-coset
right-axis reduction.  Under the p24 shift-6 covariance equations
`Y_{c+6}=rho(Y_c)`, equality of all seven H-coset sums is equivalent to the
single anchor descent statement `rho(Y_0)=Y_0`.  This pins the live arithmetic
target to covariance plus one anchored fixed-field identity for the internally
traced `G_chi` profile.

The finite duality toy, actual-CM bridges, Gaussian/RS-tail target, and
proof-facing note are:

```text
p24/trace_gcd_full_coinvariant_tail_toy.py
p24/trace_gcd_actual_cm_square_coinvariant_audit.py
p24/trace_gcd_full_gaussian_rs_tail_target.md
p24/trace_gcd_rs_tail_semilinear_core_theorem.md
p24/trace_gcd_rs_tail_semilinear_core_toy.py
p24/trace_gcd_rs_tail_fixed_adjoint_toy.py
p24/trace_gcd_rs_tail_syndrome_moore_schur_toy.py
p24/trace_gcd_rs_tail_block_support_profile_toy.py
p24/trace_gcd_rs_tail_full_plucker_chart_cauchy_toy.py
p24/trace_gcd_rs_tail_block_skew_cauchy_displacement_toy.py
p24/trace_gcd_rs_tail_block_skew_cauchy_theorem_candidate.md
p24/trace_gcd_plucker_displacement_handoff_toy.py
p24/lean/TraceGcdPluckerDisplacementHandoffGate.lean
p24/trace_gcd_rs_tail_shift_displacement_boundary_toy.py
p24/trace_gcd_rs_tail_cyclic_operator_boundary_toy.py
p24/trace_gcd_rs_tail_frequency_defect_gate_theorem.md
p24/trace_gcd_rs_tail_frequency_defect_gate_toy.py
p24/trace_gcd_rs_tail_frequency_moore_schur_factor_toy.py
p24/trace_gcd_rs_tail_frequency_resultant_gate.md
p24/trace_gcd_rs_tail_frequency_resultant_gate_toy.py
p24/trace_gcd_rs_tail_cyclic_section_descent.md
p24/trace_gcd_rs_tail_cyclic_section_descent_toy.py
p24/trace_gcd_rs_tail_defect_support_accounting.md
p24/trace_gcd_rs_tail_defect_support_accounting.py
p24/trace_gcd_rs_tail_fixed_frequency_ordinary_gate.md
p24/trace_gcd_rs_tail_fixed_frequency_ordinary_gate.py
p24/trace_gcd_fixed_frequency_annihilator_bridge.md
p24/trace_gcd_fixed_frequency_annihilator_bridge_toy.py
p24/trace_gcd_fixed_frequency_relation_section_toy.py
p24/trace_gcd_fixed_frequency_cyclic_syzygy.md
p24/trace_gcd_fixed_frequency_cyclic_syzygy_toy.py
p24/lean/TraceGcdFrequencyDefectGate.lean
p24/lean/TraceGcdFixedFrequencyOrder7Gate.lean
p24/lean/TraceGcdRightAxisAnchorDescentGate.lean
p24/trace_gcd_actual_cm_full_plucker_chart_boundary.py
p24/trace_gcd_actual_cm_frequency_defect_boundary.py
p24/trace_gcd_rs_tail_visible_lrs_signature_toy.py
p24/trace_gcd_actual_cm_rs_tail_semilinear_core_audit.py
p24/trace_gcd_full_gaussian_rs_tail_toy.py
p24/trace_gcd_actual_cm_gaussian_rs_tail_audit.py
p24/trace_gcd_full_coinvariant_tail_target.md
```

`TraceGcdCrossedCoinvariantNormGate.lean` records the nonzero-orbit analogue:
the transported square coinvariant maps `Phi_t` are packaged by a crossed
norm/block-cycle determinant.  A p-unit crossed norm makes every local
`Phi_t` nonsingular and therefore rules out the corresponding trace-GCD bad
event on that orbit.  The actual-CM square-map audit checks the same
block-cycle/skew reduced norm identity on the two rows used by the
two-resultant holdout.  The toy, actual-CM audit, and note are:

```text
p24/trace_gcd_crossed_coinvariant_norm_toy.py
p24/trace_gcd_actual_cm_square_coinvariant_block_cycle_audit.py
p24/trace_gcd_crossed_coinvariant_norm_target.md
```

The current proof-route synthesis and actual-CM holdout evidence are recorded
in:

```text
p24/trace_gcd_two_resultant_proof_route_synthesis.md
p24/trace_gcd_two_resultant_holdout_audit.py
p24/trace_gcd_actual_cm_square_coinvariant_block_cycle_audit.py
```

The holdout audit reports:

```text
selected_two_punit_groups=4/4
punit_transport_edges=8/8
split_norm_matches=12/12
naive_base_polynomial_groups=0/4
block_cycle_matches=12/12
square_coinvariant_block_cycle_is_skew_reduced_norm=1
```

so the Lean gates are now aligned with the strongest observed theorem surface:
one fixed p-linearized resultant, one nonzero crossed norm, and p-unit
determinant-line transport.

`TraceGcdDualSparseBridgeGate.lean` records the finite CS-theory side door:
if the same nonzero p24 bad parameter had both the representative
leading-erasure support bound and the centered plateau-difference support
bound, prime cyclic uncertainty would rule it out:

```text
54 + 54 < 212.
```

The proof-facing note is
`p24/trace_gcd_dual_sparse_uncertainty_bridge.md`.  The finite
cyclic-difference/DFT coordinate identity feeding this gate is recorded in
`p24/trace_gcd_difference_dft_bridge.md` and audited by
`p24/trace_gcd_difference_dft_bridge_audit.py`; it proves p-unit diagonal
equivalence on nonzero right frequencies.  The parameter-level bridge through
the centered profile and Lang/Fitting coordinates is recorded in
`p24/trace_gcd_lambda_profile_bridge.md` and audited by
`p24/trace_gcd_lambda_profile_bridge_audit.py`.  The Lean gate deliberately
does not assert the remaining arithmetic plateau-vanishing bridge between the
two sparse avatars.

`CenteredBorcherdsPUnitGate.lean` checks the finite handoff for a
phase-aware Borcherds/Fitting proof of those same orbit products:

```text
zero local intersection for phase-aware values Psi_O
  + p-unit comparison Psi_O -> orbit product Pi_O
  + orbit-product zero detection
=> every cyclic right-window determinant is nonzero.
```

The centered-specific arithmetic target is recorded in
`p24/centered_marginal_phase_borcherds_target.md`.

The corresponding determinant-line/Fitting object is named in:

```text
p24/centered_marginal_crossed_product_fitting_target.md
```

`CenteredFullOriginBorcherdsGate.lean` checks the finite handoff for the
full-origin centered version:

```text
zero local intersection for Psi_C,full
  + p-unit comparison to the full-origin centered Chow product
  + full-origin product detects right-product zero
=> every centered right-window determinant is nonzero.
```

It records the p24 power:

```text
n*m/211 = 975736474.
```

The corresponding note is
`p24/centered_marginal_full_origin_borcherds_gate.md`.

The centered origin-norm power bridge used by this gate is recorded and
audited in:

```text
p24/centered_marginal_origin_norm_power_theorem.md
p24/centered_marginal_origin_norm_power_audit.py
```

`CenteredHermitianPluckerGate.lean` records the finite handoff for the
Hermitian-orthogonal Pluecker reformulation exposed by
`p24/centered_marginal_padic_filtration_boundary.md`:

```text
exact orthogonal Pluecker comparison Delta_C(t) = diagonal pairing
  + a local initial-dominance theorem for that diagonal pairing
  + p-units are nonzero
=> no centered Schubert bad event.
```

The small actual-CM audit shows this is not an enumerable expansion shortcut:
the hard degree-`12` rows retain full matched Pluecker support after
orthogonalization.  Its only plausible use is as a clean landing surface for a
new selected-prime local dominance theorem.

The corresponding executable verifier skeleton is:

```text
p24/phase_chain_certificate_verifier.py
```

It checks the selected-chain polynomial roots and optional `j(A)` / DANGER3
replay; it deliberately leaves producer honesty to the arithmetic theorem.

`QuotientRecoveryCertificateGate.lean` checks the smaller generic implication
behind quotient-plus-selected-recovery certificates:

```text
embedded quotient root plus paired recovery root
  => strict embedded j root;
strict j root plus Montgomery lift
  => target-trace Montgomery A;
target A plus odd-part projection
  => DANGER3 triple.
```

For the first p24 strict trace this specializes to the degree-19 quotient and
degree-14670196166 selected recovery surface in
`p24/first_trace_order19_certificate_spec.md`.  The open arithmetic input is
the producer theorem pairing the supplied quotient root with the actual
embedded conductor-2 CM recovery fiber.

`BetaOrbitTensorFactorBridge.lean` checks the finite logic behind the
beta-orbit/tensor-factor bridge:

```text
560 nonzero E-Frobenius beta orbits
  = 8 H-packets * 70 E-tensor factors;

factorwise nonvanishing in those scalar-extension factors
  => every beta orbit is good
  => the selected beta orbit is good.
```

The order arithmetic is recorded in
`p24/beta_orbit_tensor_factor_bridge.md`; Lean only checks the implication
once that indexing is supplied.

`TraceFrameNormCompressedCertificateGate.lean` checks the finite implication
for the current smallest trace-frame certificate surface:

```text
one degree-8 determinant-line norm nonzero
  => all representative packet leading determinants nonzero
  => tensor-factor equivariance spreads nonzero-ness to all 70 factors
  => beta-orbit/tensor-factor coverage makes every beta orbit good.
```

The open arithmetic input is the p-integral class-field/Fitting theorem that
constructs the supplied norm scalar and proves it is the actual
determinant-line/reduced-norm product for the selected p24 CM torsor.

`TraceFrameBorcherdsPUnitGate.lean` checks the finite implication for a
possible Borcherds/local-intersection proof of that same leading norm:

```text
phase-aware Borcherds value p-unit
and comparison to the leading norm up to p-units
  => leading norm p-unit/nonzero.
```

It deliberately does not construct the divisor or prove a local valuation
formula; those remain the arithmetic input.

`TraceFramePrefixIntersectionGate.lean` checks the finite logic behind the
factorized trace-frame prefix theorem:

```text
nonzero forced prefix-intersection vector
  => prefix projection alone is not injective;

prefix-zero source is parametrized by the forced A/B intersection;
the residual tail kills only the zero intersection parameter;
kernelLift(0)=0;

therefore prefix + residual-tail coordinates are injective.
```

It deliberately does not prove the dimension count
`dim(Top_2(A) cap Top_2(B)) = 10`; that is the arithmetic p-unit input
recorded in `p24/trace_frame_prefix_intersection_boundary.md`.

`QuotientSupport.lean` checks the finite support gate behind the
quotient-spectrum refinement: if an additive selector is already supported on
the quotient characters, then quotient-packet cancellation forces it to equal
the subgroup projector everywhere.  It also records the counter-gate showing
that agreement on quotient characters alone is not enough without the support
hypothesis.

`RayKernelVerticality.lean` checks the finite gate behind
`ray_kernel_embedding_boundary.md`: once a level-1 value factors through the
ray-to-Hilbert projection, every local ray-kernel element fixes it.  If the
kernel action is transitive on the vertical fiber, any kernel-invariant
construction is constant on that fiber.  The arithmetic input is still class
field theory and Shimura reciprocity; Lean verifies only the torsor logic.

`RelativeNormalityGate.lean` checks the finite certificate gate behind the
prime relative-normality refinement.  Here "determinant" means the reduced
augmentation determinant, concretely `Res(Phi_n,J_u)` for the relative fiber,
not the full circulant determinant including the trivial period:

```text
coordinate determinant nonzero for every quotient coordinate
  => every packet coordinate is nonzero
  => no packet is all zero
  => the harmful packet is ruled out.
```

The open input is the arithmetic theorem that the actual p24 relative
normality determinants are p-units at the selected prime.

`PacketFactorGate.lean` checks the finite logical distinction behind
`relative_packet_factor_vanishing_shape.md`:

```text
one packet factor zero
  does not imply all primitive packet factors are zero;

coordinate/resultant nonvanishing for every coordinate
  implies exact packet content nonzero
  implies harmful all-zero packets are ruled out.
```

This keeps the proof target from silently replacing `J_u mod f_a = 0` by the
stronger `J_u mod Phi_n = 0`.

`GlobalContentGate.lean` checks the weaker aggregate/content gate now used by
the exact relative-resolvent target:

```text
global/content certificate:
  every packet vector is not all zero
  => every harmful all-zero packet is ruled out;

projection certificate:
  a nonzero scalar projection of a packet, such as a quotient moment or
  Hermitian energy, proves that packet is not all zero;

projection-family certificate:
  if all-zero packets force every member of a finite projection family to
  vanish, then any one nonzero projection, such as one of
  M0, P2, P157, P211, proves packet content;

Bezout/content certificate:
  a packetwise combination equal to 1 proves the same exact content condition.
```

The arithmetic target behind this gate can be either the exact global gcd

```text
gcd(Phi_n, J_0, ..., J_{m-1}) = 1
```

or a structured scalar projection whose resultant with `Phi_n` is a p-unit.

`CenteredProfileGate.lean` checks the finite logic for the alternate
centered-profile mixed-rank certificate:

```text
leading centered-profile Moore p-unit
  => full centered-profile span
  => centered mixed marginal rank;

full-square centered-profile trace-Gram p-unit
  => leading centered-profile Moore p-unit
  => centered mixed marginal rank;

base-field inversion-Gram p-unit
  => full-square centered-profile trace-Gram p-unit
  => centered mixed marginal rank;

dropped-row base minor p-unit
  => base-field inversion-Gram p-unit
  => centered mixed marginal rank;

leading centered difference-marginal minor p-unit
  => centered mixed marginal rank;

contained normal Frobenius orbit
  => full centered-profile span
  => centered mixed marginal rank.
```

The open arithmetic input is either the p-unitness of
`M_profile_leading`, the p-unitness of the direct difference minor
`Delta_C_leading`, or a proof that the actual profile span contains a normal
Frobenius orbit in `F_p(mu_157)`.

`CenteredProfilePayloadGate.lean` checks the finite payload counts for the
same centered-profile route:

```text
centered 156 x 210 matrix entries = 32760;
leading 156 x 156 minor entries = 24336;
explicit matrix plus rank witness = 57096;
determinant scalar plus inverse = 2;
right pointwise product plus inverses = 422;
right orbit norms plus inverses = 14.
```

The comparison note is `p24/centered_profile_payload_frontier.md`.

`TraceOriginProductGate.lean` checks the finite implication behind the
trace-gcd origin-product reduction:

```text
origin covariance maps every CM origin to a reduced right-cycle factor;
all reduced right-cycle factors are nonzero;
therefore the selected origin trace-gcd determinant is nonzero.
```

For p24 this leaves the arithmetic input:

```text
prod_{t mod 211} Delta_i(t) != 0 mod p.
```

The DFT/Lang covariance formula supporting the gate is recorded in
`lang_origin_covariance_theorem.md`; Lean checks only the finite
product-to-selected-origin logic.

`MomentLambdaGate.lean` checks the finite packaging logic behind the
two-moment target:

```text
{M0,M1} nonzero in every packet
  => exact packet content
  => no harmful all-zero packet;

chosen lambda avoids the packetwise forbidden lambda values
  => M0 + lambda*M1 nonzero in every packet
  => the same conclusion.
```

The existence or discovery of a safe lambda is left as finite certificate data,
and the p24 arithmetic input remains the selected-prime nonvanishing of the
actual moment pair.

`AxisInjectivityGate.lean` checks the finite implication behind the refined
`L1` axis-support theorem:

```text
axis evaluation map W_axis -> packet field is injective
+ L1 coefficient function is nonzero in W_axis
=> selected L1 packet value is nonzero
=> the packet content vector is not all zero
=> harmful all-zero packet vanishing is ruled out.
```

For p24 the open arithmetic theorem is the injectivity of the 368-dimensional
axis coefficient space in every packet.

The same file now also includes a small coordinate-minor gate:

```text
injectivity of (coordinate projection after axis evaluation)
  => injectivity of the axis evaluation map.
```

This is the formal interface behind `axis_coefficient_minor_boundary.md`.

```text
W_axis = {a0 + g_2(r mod 2) + g_157(r mod 157) + g_211(r mod 211)}
```

inside each degree-388430 Frobenius packet field.

The same file also records the parent-theorem gate:

```text
full relative K-normality
  => axis injectivity
  => selected L1 nonvanishing.
```

Here "full relative K-normality" is the injectivity of all `m=66254`
complement-coordinate weights into the packet field.  The arithmetic theorem
can be stated as a Moore determinant nonvanishing or, after adjoining `mu_m`,
as rank of the full `K`-character resolvents.

It also checks the abstract change-of-basis step:

```text
precompose an evaluation map with a bijective transform
  => injectivity is preserved in both directions.
```

This is the finite logic behind replacing complement-coordinate rank by
`K`-character rank after adjoining the required roots of unity.

`AxisModuleDirectSumGate.lean` checks the finite logic behind the current
module-level refinement:

`MixedMooreGate.lean` checks the finite logic behind the mixed
Moore-circulant/Gabidulin refinement of the Hermitian Schur correction:

```text
every rank failure gives a nonzero skew-linearized annihilator;
the six seed cycles are annihilator-free;
therefore the mixed block has no rank failure.
```

The open p24 arithmetic input is the annihilator-free theorem for the actual
six mixed Hermitian seed cycles.  Lean verifies only that this is a sufficient
replacement for the raw `156 x 210` mixed determinant.

`MixedTraceDualGate.lean` checks the finite logic behind the trace-dual
version of the same mixed theorem:

```text
six relative traces separate every nonzero left character
  <=> the dual trace map has no nonzero common kernel.
```

The arithmetic input is still the p24 separation theorem for
`lambda |-> (Tr_{E/F_p(mu_211)}(lambda*S_j))_j`.

`MixedTraceIntersectionGate.lean` checks the equivalent intersection phrasing:

```text
L ∩ span_R{S_1,...,S_6}^perp = {0}
  <=> six relative traces separate every nonzero left character.
```

Again, Lean checks only the finite logic; the arithmetic theorem is the
selected-prime p-unit/transversality statement for the actual mixed periods.

```text
constant component + 2-axis + 157-axis + 211-axis
  have trivial component kernels
+ their images are direct in the packet field
=> the full axis evaluation is injective.
```

For p24 this leaves the arithmetic theorem as a selected-prime direct-sum
statement for the four smooth-axis images inside each degree-388430 packet.
The gate is recorded in `axis_module_direct_sum_gate.md`.

`CrtMarginalAnnihilatorGate.lean` checks the finite logic behind the
trace-frame CRT marginal theorem:

```text
directness of E*S_k and the selected Delta_c^(k) marginal-difference spaces
+ trivial component kernels
  => injectivity of the combined top-coefficient map.
```

This is the formal interface for
`tensor_factor_marginal_annihilator_theorem.md`.  The open arithmetic theorem
is the p24 nonvanishing of the corresponding marginal exterior products
`Omega_1`, `Omega_211`, and `Omega_3`.

`ScalarExtensionGate.lean` checks the descent step needed by the corrected
K-character strategy:

```text
axis map injective after adjoining independent K-character roots
  => original base-field packet axis map injective.
```

This is the formal interface for tensor-separating the K-character roots from
the H-packet root after `axis_frobenius_cocycle_boundary.md` ruled out the
naive packet-Frobenius submodule shortcut.

The p24 degree accounting and small tensor-rank tests for that route are in
`k_character_tensor_rank_theorem.md`.  The per-factor refinement is tested by
`k_character_tensor_factor_rank_scan.py`: it checks whether one irreducible
factor of `A tensor F_p(mu_m)` already carries full axis rank.

`TensorFactorProjectionGate.lean` checks the finite gate behind the current
one-factor coordinate-minor certificate:

```text
coordinate projection after one tensor factor is injective
  => tensor-extended axis map is injective.
```

Combined with `ScalarExtensionGate.lean`, this proves that a nonzero
one-factor `368 x 368` minor is a valid base packet axis-injectivity
certificate.  The chain is documented in `one_factor_certificate_chain.md`.

`TraceFrameGate.lean` names the same finite implication for the newer
intermediate-field target:

```text
twisted trace frame after one tensor factor is injective
  => tensor-extended axis map is injective.
```

For p24 the proposed trace frame uses three traces to the degree-179
intermediate field inside the degree-5549 tensor factor.

`TraceFrameAnnihilatorGate.lean` records the equivalent kernel-avoidance
view:

```text
trace-frame kernel lies in a fixed annihilator subspace
axis image avoids that annihilator
  => trace-frame axis map is injective.
```

For p24 the annihilator is the trace-orthogonal complement of
`span_C{1, theta, theta^2}` inside the degree-31 extension `B/C`.

`TraceFrameSchubertPacketNormGate.lean` records the finite bookkeeping for
the current four-factor Schubert package:

```text
global norm of Xi_A, Xi_B, Xi_AB, Xi_tail nonzero
  => every H-packet has nonzero Delta_A, Delta_B, Delta_AB, Delta_tail
  => every H-packet trace-frame certificate is good
  => no harmful packet collapse.
```

The corresponding arithmetic target is documented in
`trace_frame_schubert_packet_norm.md`: construct the four equivariant
degree-8 relative norm elements in
`Q(mu_m) Q(zeta_n)^<p>` and prove they are p-units at the selected prime.
The determinant-line descent theorem needed before this p-unit step is
isolated in `trace_frame_schubert_equivariant_descent.md`.

`SchubertEquivariantDescentGate.lean` checks the still more local
zero/nonzero step:

```text
global determinant-line residue = unit * packet determinant
global norm nonzero
  => packet determinant nonzero.
```

`TraceFrameLeadingNormGate.lean` records the denominator-free single-leading
variant:

```text
global norm of Xi_lead nonzero
  => every H-packet has nonzero Delta_lead
  => every H-packet trace-frame certificate is good
  => no harmful packet collapse.
```

The corresponding theorem target is documented in
`trace_frame_single_leading_punit.md`.  This route avoids packetwise
kernel-basis denominators by using the full leading Plucker coordinate before
splitting it into prefix and residual-tail factors.

`AxisInjectivityGate.lean` also records the finite gate behind
`trace_gram_axis_certificate.md` and
`hermitian_trace_gram_axis_certificate.md`:

```text
pairing separates the kernel of the axis evaluation map
  => kernel is trivial
  => axis evaluation is injective.
```

The open arithmetic theorem is the nonvanishing of the `368 x 368`
ordinary or Hermitian trace-Gram determinant for each p24 packet.  The
Hermitian version is the better p24-shaped target because the packet degree is
even and the middle Frobenius sends the H-character to its inverse.

This lets the notes cleanly separate three things:

```text
Lean-checked finite logic:
  indexing, all-zero equivalences, and certificate contrapositives;

toy-code checks:
  small CM cycles and packet/energy identities;

open arithmetic theorem:
  prove the selected p24 relative content vector or scalar energy is nonzero
  at the chosen prime over p.
```

`TwoTorsionGate.lean` checks the finite linear-algebra part of the
conductor-2/nonsplit Montgomery gate:

```text
identity Frobenius on E[2]       => full fixed 2-torsion;
nontrivial unipotent Frobenius   => one fixed coordinate line.
```

The CM input remains external: prove whether `pi-1` is divisible by `2` in
`O_K` or in `Z+2O_K`.  The Lean file only pins down the resulting finite
two-torsion implication.
### MixedSubspacePolynomialGate

`MixedSubspacePolynomialGate.lean` records the finite implication behind the
latest rank-metric restatement.  Once the `p`-linearized subspace polynomial
of the `210` trace-dual mixed coordinates has degree `156`, the coordinates
span `F_p(mu_157)`.  Equivalently, absence of a common annihilator of
`p`-degree `<156` implies the mixed trace-intersection theorem.

It also records the current representative p24 prefix-tail gate:

```text
prefixRank = 4*35 and tailAug = 16
=> FullSpan leadingRank 156.
```

The open input is the arithmetic p-unit theorem proving that the actual
representative `140+16` Moore residual product has those ranks.

### MixedRightOrbitSupportGate

`MixedRightOrbitSupportGate.lean` records the finite consequences of the
right-orbit support strengthening.  If every nonzero left twist has at least
two nonzero right-orbit traces, then the original six-orbit trace separation
holds and any delete-one set of five right orbit packets still separates.

### ConjugateTailGate

`ConjugateTailGate.lean` records the finite implication behind the
opposite-orbit tail compression.  If a conjugation symmetry preserves the
shared four-block prefix kernel and swaps the two opposite tail zero
predicates, then tail injectivity for one representative implies tail
injectivity for its opposite partner.  This is the formal gate used by
`opposite_conjugation_tail_theorem.md` to reduce the p24 opposite-pair proof
surface from six tail p-units to three representative tail p-units, after the
Lang-coordinate window convention is fixed.

### UnitOrbitGate

`UnitOrbitGate.lean` records the finite orbit-compression logic behind the
right-unit action `mu_211 -> mu_211^2`.  If p-unit nonvanishing is preserved
around a three-cycle or six-cycle of algebra automorphisms, then one
representative proves the whole orbit.  This is the formal gate used by
`right_unit_equivariance_theorem.md` to reduce the equivariant p24 proof
surface to one representative prefix p-unit and one representative tail
p-unit.

### RepresentativeOnePUnitGate

`RepresentativeOnePUnitGate.lean` packages the current smallest finite
mixed-route handoff in one theorem:

```text
one representative leading p-unit L_rep
  + right-unit propagation around the six deletion rows
  + delete-one separation from those rows
  + support >= 2 => mixed rank
=> mixed rank certificate.
```

It also records the verifier payload count for this compressed surface:

```text
L_rep plus inverse = 2 field elements < sqrt(p).
```

### RepresentativeDualObstructionGate

`RepresentativeDualObstructionGate.lean` records the finite kernel statement
behind the one-punit representative row.  The representative bad event is a
nonzero source element whose four full prefix blocks vanish and whose
16-coordinate tail projection also vanishes.  Ruling out that bad event is
the same as tail injectivity on the prefix kernel, and it implies separation
by the representative leading coordinate window.

### TraceGcdGate

`TraceGcdGate.lean` records the finite packaging for the linearized trace-gcd
version of the same representative theorem:

```text
kernelDim = 16 and tailRankOnKernel = 16
=> trace-gcd degree = 0.
```

It also abstracts the square tail determinant certificate:

```text
det(tail on K) != 0
=> tailRankOnKernel = kernelDim
=> trace-gcd degree = 0.
```

The open arithmetic input is proving these two rank facts for the actual p24
relative trace maps.

### TraceOriginProductGate

`TraceOriginProductGate.lean` records the finite interface for the
origin-product strengthening of the trace-GCD theorem:

```text
right-component product nonzero
+ origin covariance by p-unit factors
=> selected representative tail-on-kernel determinant nonzero.
```

The open arithmetic input is constructing the right-translation determinant
sequence and proving its 211-term cyclic resultant is a p-unit for the actual
p24 CM embedding.

### TraceGcdSchubertOrbitGate

`TraceGcdSchubertOrbitGate.lean` records the equivalent Schubert-orbit
avoidance interface:

```text
product_t Delta(t) nonzero
+ Delta(t) nonzero iff W cap V_t^{-1}C = {0}
=> W avoids every translated Schubert divisor.
```

The open arithmetic input is still proving the product/norm p-unit for the
actual p24 CM trace-GCD plane.

`TraceGcdSelectedSchubertPUnitGate.lean` records the same target in the
current local-intersection language:

```text
honest norm detects translated Schubert bad events;
the norm or each orbit norm is a p-unit;
therefore no translated bad event occurs.
```

It also records the p24 payload gaps:

```text
pointwise values + inverses: 422 field elements;
seven orbit products + inverses: 14 field elements;
metric prefix/full Gram products + inverses: 28 field elements;
```

all far below `sqrt(p)=10^12`.  The arithmetic input is the selected
Schubert/Fitting p-unit theorem isolated in
`p24/trace_gcd_selected_schubert_punit_frontier.md`.

The exterior Cauchy-Binet location of the same arithmetic input is recorded
in `p24/trace_gcd_orbit_exterior_schubert_expansion.md`: per nonzero right
orbit, the Schubert determinant is a `binom(35,16)` term character polynomial
in the CM Plucker coordinates, so the missing theorem is p-adic
noncancellation or an equivalent Fitting/class-field p-unit identity.
The finite cancellation boundary is exercised by
`p24/orbit_exterior_schubert_toy.py`.

`TraceGcdChowNormGate.lean` records the same implication with the intrinsic
Grassmannian name:

```text
Chow zero detects the translated Schubert bad event;
orbit Chow norm units detect and exclude all Chow zeros;
therefore the selected trace-GCD row is good.
```

The arithmetic target is described in
`p24/trace_gcd_chow_norm_theorem_candidate.md`.
The p-integral determinant-line model for the same Chow values is recorded in
`p24/trace_gcd_chow_integral_model.md`.
The bounded actual-CM diagnostic
`p24/trace_gcd_chow_plain_divisor_boundary.md` rules out the easiest
plain-`j` or one-edge low-degree divisor recognition for this Chow value; a
Borcherds/Fitting proof still has to construct the phase-aware Chow divisor.
That sharpened target is summarized in
`p24/trace_gcd_phase_aware_chow_borcherds_target.md`.
The companion phase-coordinate scan
`p24/trace_gcd_chow_phase_coordinate_boundary.md` records exact right-phase
descent in the pinned small row and the p24 full-support warning.
The bounded phase-unit span scan
`p24/trace_gcd_chow_phase_divisor_span_boundary.md` tests the first simple
product-formula dictionary and finds only full-rank/random containment.
The global scalar miner
`p24/trace_gcd_global_product_mining_boundary.md` tests the two-element
`Pi_all` surface on the same pinned row; it finds low-weight scalar matches
but no matching phase-vector formulas, so the arithmetic input for the global
gate must be divisor/local-intersection honest rather than scalar-only.

`TraceGcdChowBorcherdsPUnitGate.lean` records the sharper phase-aware
Borcherds/Fitting handoff:

```text
zero local intersection for Psi_O;
p-unit comparison Psi_O -> actual Chow orbit norm;
Chow orbit norm zero-detection;
therefore no translated Schubert bad event.
```

`DeterminantLineUnitScaleGate.lean` records the basis-change hygiene used by
the trace-GCD block-cycle/Fitting surface:

```text
unit-scaled determinant-line representatives have the same zero status;
p-unitness transfers across p-unit basis scalings;
therefore a finite certificate is independent of compatible p-integral
source/target basis choices.
```

It deliberately leaves construction of `Psi_O` and the local valuation formula
as the arithmetic input.
The same file also records the global full-divisor variant `Psi_all`, where
one p-unit comparison to `prod_t Chow_t(W,C)` is enough.  This is summarized in
`p24/trace_gcd_global_chow_borcherds_handoff.md`.

`TraceGcdFullOriginBorcherdsGate.lean` records the corresponding full-origin
variant:

```text
zero local intersection for psiFull;
p-unit comparison psiFull -> actual full-origin determinant norm;
full-origin norm detects right-product zero;
right product detects Chow zeros;
therefore no translated Schubert bad event.
```

This is the finite plumbing behind
`p24/trace_gcd_full_origin_borcherds_gate.md`; the open input is still the
closed phase-aware Borcherds/Fitting product formula.

### TraceGcdCyclicFactorGate

`TraceGcdCyclicFactorGate.lean` records the safe factorwise Bezout interface
for the same trace-GCD determinant sequence:

```text
actual orbit-algebra residue has a unit/Bezout witness
+ any zero Delta(t) would make that factor residue nonunit
=> all Delta(t) are nonzero.
```

This is the algebraic replacement for unsafe base-field interpolation of raw
determinant values.  The small actual-CM audit in
`lang_trace_gcd_factor_bezout_boundary.md` shows why the replacement matters:
the split interpolant evaluates correctly but does not have base-field
coefficients, and ordinary `F_q[Y]/Phi_O` residues cannot produce the raw
nonconstant base-field values on nontrivial Frobenius orbits.

### TraceGcdCrossedProductGate

`TraceGcdCrossedProductGate.lean` records the positive replacement for those
ordinary factor residues:

```text
crossed-product reduced norm = actual Frobenius orbit product
+ crossed-product norms are nonzero
=> every trace-GCD determinant value is nonzero.
```

For p24 the nonzero right-orbit length is `35`, so the weighted-cycle
determinant has positive sign.  The actual-CM audit in
`lang_trace_gcd_crossed_product_orbit_boundary.md` confirms the finite shape
and shows that ordinary-power collapse fails on nonconstant orbits.

### TraceGcdBlockCycleGate

`TraceGcdBlockCycleGate.lean` lifts the crossed-product gate from scalar
weights to the actual tail-on-kernel matrices:

```text
block-cycle determinant = actual orbit product
+ block-cycle determinants are nonzero
=> every trace-GCD determinant value is nonzero.
```

It also records the kernel/local-intersection form:

```text
any orbit block-cycle bad section forces a local bad tail-on-kernel vector;
no local bad vectors
  => no orbit block-cycle bad section.
```

For p24 each nonzero right orbit gives a `35*16 = 560` dimensional block
operator.  The audit in `lang_trace_gcd_block_cycle_norm_boundary.md` checks
the identity on the pinned actual-CM row.

### Kummer / Plucker-Kummer Gates

`KummerNonvanishingGate.lean` records the finite bridge from a primitive
relative Kummer p-unit to a nonzero relative trace/evaluation.  This is useful
for linear cyclic layers, but it does not prove a determinant is nonzero.

`PluckerKummerGate.lean` records the corrected determinant-level interface:

```text
Plucker-Kummer payload nonzero
+ determinant zero forces Plucker-Kummer zero
=> determinant nonzero.
```

`PluckerKummerDescentGate.lean` adds the descent condition needed by the
class-field producer: if every local Plucker-Kummer payload equals one
descended scalar and that scalar is nonzero, then all Plucker values in the
hidden cyclic orbit are nonzero.  Without descent, the producer should use an
orbit product/norm payload.

`PluckerKummerOrbitNormGate.lean` records that fallback explicitly:

```text
local Plucker-Kummer values detect Plucker zeros
+ the supplied orbit norm is zero whenever a local value in that orbit is zero
+ the orbit norm is a unit
=> every Plucker value in that orbit is nonzero.
```

This is the finite landing surface supported by the actual-CM descent audit:
individual values do not descend on the nontrivial trace-GCD Frobenius
orbits, while orbit products/norms do.

For the trace-GCD route, the open arithmetic input is constructing a Kummer
payload attached to the actual Plucker coordinate
`Delta(t)=det(P V_t A)`, not merely to the matrix entries.

### TraceGcdBlockCycleGate

`TraceGcdBlockCycleGate.lean` records the finite implication for the current
right-211 block-cycle certificate surface:

```text
honest block norm = honest orbit product;
zero determinant value zeros its orbit product;
every block norm is nonzero;
therefore every trace-GCD determinant value is nonzero.
```

It also records the local-intersection/kernel form:

```text
block-cycle bad section forces a local bad tail-on-kernel vector;
no local bad vectors imply no block-cycle bad event.
```

The exact p24 verifier contract and orbit accounting are in
`p24/trace_gcd_block_cycle_certificate_spec.md`.  The open arithmetic input
is still the p-integral class-field/Fitting theorem constructing the actual
seven block-cycle norms and proving they are p-units.

The proof-facing version is recorded in
`p24/trace_gcd_local_unit_proof_target.md`: four full right trace blocks cut
`F_p(mu_157)` down to a 16-dimensional residual kernel, and the selected
16-coordinate tail map is nonsingular on that kernel; orbitwise this is a
unit zeroth-Fitting-ideal statement for the transported block-cycle failure
modules.

`TraceGcdLocalUnitGate.lean` joins those two interfaces.  It checks the p24
number facts

```text
4*35+16 = 156,
35+19 < 210-156+1,
16*(35-1) is even,
```

and proves that honest orbit Fitting-unit payloads, together with
zero-detection for the actual determinant sequence, imply the representative
trace-GCD row is good.

`TraceGcdOrdinaryFittingCriterionGate.lean` records the p-local ordinary
criterion that supplies those Fitting-unit payloads:

```text
zero local intersection
  or reduced block map isomorphism
  or unit zeroth Fitting ideal of the cokernel
=> Fitting determinant p-unit
=> no translated trace-GCD Schubert bad event.
```

It is the Lean companion to
`p24/trace_gcd_ordinary_fitting_disjointness_criterion.md`.  The open
arithmetic input is still constructing the actual phase-aware section and
proving the selected p24 local intersections are zero.

`TraceGcdOperatorRepresentativeGate.lean` packages the smallest trace-GCD
payload all the way to the mixed-rank handoff:

```text
operator norm p-unit
  + operator norm detects any zero in the actual Delta(t) sequence
=> selected representative determinant nonzero
=> representative row good
=> unit-2 propagation gives all six deletion rows
=> delete-one separation
=> right support >= 2
=> mixed rank certificate.
```

It also records the p24 counts:

```text
operator norm plus inverse = 2 field elements < sqrt(p);
66254 + 3107441 < sqrt(p).
```

The arithmetic input remains the construction of the honest p-integral
operator norm

```text
det(m_f on F[Y]/(Y^211 - 1))
```

and a proof that it is a p-unit at the selected ordinary prime.

The finite singular branch of the block-cycle identity is exercised by:

```text
p24/block_cycle_fitting_zero_detection_toy.py
```

That toy is not an arithmetic proof; it is a guardrail ensuring the
block-cycle/Fitting zero-detection interface behaves correctly on both
invertible and deliberately singular local blocks.

`TraceGcdSchurBridgeGate.lean` records the finite implication for the
sidecar-suggested Hermitian-Schur bridge:

```text
Schur zero-detection:
  trace-GCD orbit product zero forces full Gram product zero
  or kernel Gram product zero;

prefix Gram orbit products are units;
prefix Gram nonzero implies kernel Gram nonzero;
full Gram orbit products are units;

therefore every trace-GCD orbit product is nonzero,
and the selected trace-GCD row is good.
```

It also checks the p24 payload counts:

```text
alternate full/kernel Gram payload = 28 field elements,
natural prefix/full Gram payload = 28 field elements,
conservative prefix/full/kernel Gram payload = 42 field elements.
```

The actual-CM falsifier is:

```text
p24/orbitwise_schur_bridge_falsifier.py
```

The proof-facing split between the full Gram factor and the prefix Gram
factor is recorded in:

```text
p24/trace_gcd_prefix_full_gram_payload_refinement.md
```

The open arithmetic input is a Hermitian packet/autocorrelation p-unit theorem
for the actual p24 Gram products.

`PrefixGramSelfOrthogonalGate.lean` records the finite obstruction isolated by
the prefix/full Gram refinement:

```text
prefix Gram singular
  <=> there is a nonzero prefix vector orthogonal to every prefix vector;

absence of prefix self-orthogonal vectors
  plus radical transfer from kernel to prefix
  => absence of kernel self-orthogonal vectors.
```

The proof-facing target is in
`p24/trace_gcd_prefix_gram_self_orthogonal_obstruction.md`.  The arithmetic
Schur instance should use the metric-aware identity in
`p24/trace_gcd_metric_schur_refinement.md`, where the prefix Gram is
`A G^{-1} A^T` and the kernel Gram is `N^T G N`.  The finite-field guardrails
are:

```text
p24/prefix_gram_obstruction_toy.py
p24/metric_schur_identity_toy.py
```

`PrefixSubcodeDistanceGate.lean` records the equivalent support/distance
language for the same prefix obstruction, while
`PrefixGramErasureBridgeGate.lean` records the finite bridge from metric
prefix-Gram nondegeneracy to prefix erasure injectivity:

```text
metric prefix Gram nondegenerate
  => no nonzero prefix parameter vanishes on the prefix;

nonzero prefix parameter vanishes on the 140-prefix
  => associated nonzero-right trace word is supported on the 70-coordinate
     complement;

parameter-level nonzero-right distance >= 71
  => no such prefix obstruction;

or, with prime cyclic uncertainty:
time support <= 71 and frequency support <= 140
contradict threshold 212.
```

The file is deliberately parameter-level: a slogan like `C_S cap F_p^T = {0}`
needs injectivity of the trace-word map on the prefix span, or it must be read
as a statement about nonzero `lambda`, not just nonzero words.

### MSRDSupportGate

`MSRDSupportGate.lean` records the finite support-count implication behind the
MSRD/LRS import.  If every nonzero codeword has support weight at least
`210 - 156 + 1 = 55`, while the representative bad event forces support at
most `35 + 19 = 54`, then the bad event is impossible.  Lean checks the
numerical gap; the open arithmetic theorem is the block-equivalence between
the actual mixed CM trace-dual code and an LRS/MSRD code, or an equivalent
support-specific skew-polynomial p-unit determinant identity.

The same gate now records the metric caveat: if the support weight is only
coarse six-right-block support, then a distance-55 hypothesis would force every
word to be zero because `6 < 55`.  Thus the `35+19` argument is a scalar
coordinate/Hamming statement unless an explicit sum-rank expansion of total
rank length 210 is supplied.

### MatrixTreeFactorizationObstructionGate

`MatrixTreeFactorizationObstructionGate.lean` records the finite logic behind
the CRT-axis matrix-tree boundary.  If Cauchy-Binet coefficients factor as
ordinary edge weights,

```text
c(B) = C * product_edge_weights(B),
```

then any two pairs of bases with the same combined edge multiset must have
equal coefficient products.  The finite script
`axis_crt_matrix_tree_factorization_toy.py` supplies explicit small
finite-field witnesses where those products differ, so the ordinary
per-edge matrix-tree/Laplacian compression route is ruled out.  The open
trace-frame target remains the Plucker-weighted p-unit/Fitting theorem.

### SelectorDegreeLowerBoundGate

`SelectorDegreeLowerBoundGate.lean` records the finite skeleton of the
embedded selector degree lower bound.  If a rational selector fiber contains
an `H`-coset of size `n`, and all fibers have size at most the map degree,
then the selector degree is at least `n`.  Lean also checks the p24
inequalities showing that this lower bound does not rule out the live
third-trace certificate surface:

```text
3107441 < 10^12
2 + 157 + 211 + 3107441 < 10^12
2 + 2*157 + 314*211 + 3107441 < 10^12.
```

The geometric/divisor input remains external, as recorded in
`finite_field_selector_degree_theorem.md`.

### TowerSectionObstructionGate

`TowerSectionObstructionGate.lean` records the finite stabilizer implication
behind the embedded tower phase obstruction.  If every element of a parent
stabilizer `K` fixes the parent point, and a child selector is equivariant,
then every element of `K` fixes the selected child.  If the selected child's
stabilizer is `L`, a proper refinement witness in `K \ L` rules out such a
selector.

This is the Lean-checked reason that the phase-lifted tower producer must
supply relative child polynomials or relative class-character traces, not a
seedless canonical child choice.
