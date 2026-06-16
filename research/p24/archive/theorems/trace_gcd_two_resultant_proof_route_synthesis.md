# Trace-GCD Two-Resultant Proof Route Synthesis

Date: 2026-06-06

## Current Best Route

The strongest remaining p24 route is no longer a seven-independent-orbit
statement.  It is the following two-resultant theorem plus transport:

```text
Xi_0 in O_p^*
Xi_1 in O_p^*
diamond/unit transport preserves p-unitness around the six nonzero orbits
```

where

```text
Xi_0 = Res_p-lin(P_{K_0}, T_0)
Xi_1 = Norm_O1(Res_p-lin(P_{K_t}, T_t)).
```

The verifier surface is then the conditional four-field-element payload:

```text
Xi_0, Xi_0^{-1}, Xi_1, Xi_1^{-1}.
```

This is the first p24 certificate surface in this work that is both
sub-sqrt by construction and backed by finite gates rather than by an
enumerated class list.

The fixed-frequency `1092` scalar equations are a separate verifier
interface, not this payload count.  They are `156` left coordinates times
`7` right H-cosets after a tower-native theorem supplies compressed coset
sums.  They should not be read as samples, class elements, or Fitting orbit
payload entries.

The current direct proof checklist and machine-readable constants are:

```text
p24/trace_gcd_semilinear_fitting_nonintersection_attack.md
p24/trace_gcd_two_resultant_theorem_manifest.py
```

## New Holdout Evidence

Added:

```text
p24/trace_gcd_two_resultant_holdout_audit.py
p24/trace_gcd_actual_cm_square_coinvariant_block_cycle_audit.py
```

It tests two actual-CM rows:

```text
pinned:  D=-13319, q=13463, m=28, pair=(4,7)
holdout: D=-26759, q=26903, m=21, pair=(3,7)
```

Both have right Frobenius orbits:

```text
{0}, {1,2,4}, {3,6,5}
```

and a quotient-cycle unit:

```text
unit=3
```

The audit output was:

```text
selected_two_punit_groups=4/4
all_nonzero_groups=4/4
punit_transport_edges=8/8
literal_equal_nonzero_edges=0/8
split_norm_matches=12/12
naive_base_polynomial_groups=0/4
```

The square coinvariant block-cycle audit uses the same two rows and checks the
nonzero producer identity in the full square-map language.  Its bounded
summary is:

```text
block_cycle_matches=12/12
block_cycle_full_rank_detection_matches=12/12
full_rank_orbits=12/12
square_coinvariant_block_cycle_is_skew_reduced_norm=1
nonzero_side_can_target_transported_square_coinvariant_maps=1
```

Interpretation:

1. fixed-orbit p-unit plus one nonzero crossed-norm p-unit is the right
   compressed observable on actual-CM rows;
2. p-unit transport is the correct unit-action statement;
3. literal equality of printed orbit norms is false even on small data;
4. the nonzero crossed norm can be targeted as the skew reduced norm of
   transported square coinvariant maps;
5. ordinary base-field polynomial/resultant descent is also false on these
   rows, so the p24 theorem really is semilinear/crossed-product.

## Proof Routes Still Alive

### Direct Semilinear Fitting Route

Construct a p-integral determinant line for the tail-on-kernel maps:

```text
K_t = kernel(prefix_t)
T_t : K_t -> tail_t^vee
```

Then prove:

```text
det(T_0|K_0) in O_p^*
Norm_O1(det(T_t|K_t)) in O_p^*.
```

This is now the preferred route because it maps directly to the verifier and
to the actual-CM holdout evidence.

The p24 class-field tower is structurally friendly but not automatically
solved.  The target class group is cyclic of squarefree order

```text
2 * 157 * 211 * 3107441,
```

so the tower layers are unique cyclic subquotients.  However the genus
quotient only accounts for the order-2 layer.  Any proof of the `157/211`
phase cancellation must use embedded non-genus CM/Lang data, not just
quadratic/genus characters.

The finite selector obstruction is now isolated in:

```text
p24/cyclic_class_tower_selector_obstruction.md
p24/cyclic_class_tower_selector_obstruction.py
p24/lean/CyclicTowerSectionObstructionGate.lean
```

It proves the reason the trace-GCD route should stay in determinant/norm
language: a parent quotient root has a child torsor above it, not a canonical
child.  The p-unit route avoids choosing a child, but still needs the
embedded determinant section.

The corresponding positive invariant is the crossed norm itself:

```text
p24/crossed_norm_torsor_invariance.md
p24/lean/TraceGcdCrossedCoinvariantNormGate.lean
```

Once the producer proves all admissible local choices change the norm only by
p-unit determinant-line scale, p-unitness of one representative norm is
choice-independent.

For the fixed orbit, the same determinant can now be targeted without
choosing a prefix-kernel basis.  Let `C_tail` be the selected 16-dimensional
tail-coordinate subspace in the right field.  The fixed p-unit is equivalent
to the square Hilbert-90 coinvariant determinant

```text
Phi_full : R^4 + C_tail -> E/(tau_R - 1)E,
Phi_full((y_j),z) = [sum_{j in {2,3,5,6}} y_j*S_j + z*S_1].
```

For p24 both sides have dimension `4*35+16=156`.  This is not a new
compression layer; it is a cleaner producer target for `Xi_0`.  It folds the
prefix rank and quotient-tail injectivity into one class-field
nonintersection:

```text
sum_j y_j*S_j + z*S_1 = tau_R(W)-W
  => y_j=0 and z=0.
```

The note and finite checks are:

```text
p24/trace_gcd_full_coinvariant_tail_target.md
p24/trace_gcd_full_coinvariant_tail_toy.py
p24/trace_gcd_full_gaussian_rs_tail_target.md
p24/trace_gcd_rs_tail_semilinear_core_theorem.md
p24/trace_gcd_rs_tail_semilinear_core_toy.py
p24/trace_gcd_rs_tail_fixed_adjoint_toy.py
p24/trace_gcd_rs_tail_syndrome_moore_schur_toy.py
p24/trace_gcd_actual_cm_rs_tail_semilinear_core_audit.py
p24/trace_gcd_full_gaussian_rs_tail_toy.py
p24/trace_gcd_actual_cm_gaussian_rs_tail_audit.py
p24/lean/TraceGcdFullCoinvariantTailGate.lean
```

The Gaussian/RS-tail form is currently the sharpest explicit fixed-orbit
producer statement: after scalar extension to `K=F_p(mu_35)`, the four full
right blocks diagonalize and the selected 16-tail becomes a degree-`<16`
Reed-Solomon subspace across the 35 right frequencies.  Thus the fixed
nonintersection can be attacked as a semilinear RS-tail kernel-transversality
theorem, not as a clean `F_p[C_35]` Smith problem.

The newest fixed theorem surface descends that four-component
kernel-transversality to a single Hilbert-90 fixed-relation map:

```text
Psi_RS : F_p^28 + K^28 + F_p^16 -> L,
28 + 4*28 + 16 = 156.
```

Proving `det(Psi_RS)` is a p-unit is equivalent to the square coinvariant
fixed determinant, and is currently the most explicit finite-field identity
to attack for `Xi_O0`.

The trace-adjoint version is equally explicit:

```text
L -> F_p^28 + K^28 + F_p^16,
lambda |-> syndrome(lambda).
```

Surjectivity of this syndrome map is equivalent to `det(Psi_RS)` being a
p-unit.  This is the current Moore/resultant-facing version of the fixed
orbit theorem, because it turns the fixed determinant into full coordinate
span for trace and relative-trace evaluations.

The newest split of this theorem is:

```text
Delta_156(C_RS) != 0
```

or equivalently

```text
Delta_140(C_prefix) != 0
and
Delta_16(P_prefix(W_0),...,P_prefix(W_15)) != 0.
```

Small exact controls now separate a prefix failure from a tail-quotient
failure.  The available actual-CM prefix-plus-tail negative rows fail the
prefix rank first, so they do not yet provide a positive p24-like calibration
of the quotient-tail determinant.

The selected `140+16` object uses `156` of the `210` natural fixed-source
columns.  The five selected blocks have dimensions `35,35,35,35,16`; the
support-profile gate tests all `31` nonempty block subsets for directness.  A
hidden LRS/MSRD proof cannot be read off from the selected square alone: once
the five selected block spans are direct, p-unit row and block changes leave
little visible moduli.  The natural-coordinate visible GRS signature is
explicitly rejected by the toy falsifier, so the remaining coding-theory route
needs either an explicit class-field p-unit block equivalence or a full
`210`-column Plucker/cross-ratio invariant involving the unused `54` columns.

A concrete full-object modulus is now isolated: after the selected `156`
columns are a basis, the omitted `54` columns define a `156 x 54`
Plucker-ratio chart.  Visible scalar GRS/MDS codes give a scaled Cauchy chart,
so the entrywise inverse has rank at most `2`; random full-source charts do
not.  For p24 this would be an `8424`-entry invariant.  A useful theorem would
have to prove the actual CM chart has a block/skew Cauchy form or use the same
chart to derive the selected p-unit directly.

The block/skew version should be stated as a Sylvester displacement identity:
after choosing the selected basis, prove

```text
A C - C B = R S
```

with small rank for `R S`, where `A` and `B` are not fitted parameters but
transported CM/Lang operators.  This is the non-scalar replacement for the
entrywise-inverse rank `<= 2` Cauchy signature.

The finite handoff is: from `X=[S O]`, `C=S^{-1}O`, and an arithmetic operator
boundary

```text
T S = S A + E_s,      T O = O B + E_o,
```

derive

```text
A C - C B = S^{-1}(E_o - E_s C).
```

Thus the actual theorem can target a low-rank boundary for the full `210`
columns rather than individual Plucker chart entries.  Operators fitted after
seeing `C` are explicitly rejected by the handoff control.

For the RS-tail split, the first explicit `A,B,T` candidate is the common
cyclic/Lang shift on the six right blocks.  In the p24 selection, four full
blocks are selected, one full block is omitted, and only the `16/19` split tail
block crosses the selected/omitted boundary.  Therefore the expected Sylvester
residue is not merely small but rank `2`, from the two tail cut edges.  Proving
the fixed p-unit can now be aimed at constructing this operator boundary
integrally for the actual CM columns and coupling it to the selected-basis
determinant.

The smaller actual-CM rows currently available do not test this nontrivial
chart: tail-only basis rows make the inverse-rank condition automatic, while
the prefix-plus-tail rows fail before the selected block is a basis.  The
boundary audit records this as a calibration gap, not as a failure of the
full-chart theorem candidate.

For the nonzero representative orbit, the matching producer target is the
crossed norm of the transported square coinvariant maps:

```text
Xi_O1 = Nrd_O(Phi_t),    t in O.
```

This is the same nonzero p-unit as
`Norm_O(Res_p-lin(P_Kt,T_t))`, but in a class-field coinvariant form.  The
finite block-cycle check and gate are:

```text
p24/trace_gcd_crossed_coinvariant_norm_target.md
p24/trace_gcd_crossed_coinvariant_norm_toy.py
p24/trace_gcd_actual_cm_square_coinvariant_block_cycle_audit.py
p24/lean/TraceGcdCrossedCoinvariantNormGate.lean
```

### Exterior/Plucker Norm Route

Package the nonzero orbit as an exterior norm:

```text
Norm_O(ell_tail(wedge^16 K_t))
```

This is equivalent to the Fitting determinant once the CM Plucker line is
identified.  The obstruction is still proving the actual CM Plucker line is
not on the selected Schubert divisor; fixed Fourier-head minors alone do not
prove this.

### Phase-Aware Borcherds/Fitting Divisor Route

Construct a modular or Borcherds product whose divisor is the pulled-back
trace-GCD Schubert/Fitting divisor for:

```text
O0 and one nonzero O1.
```

Then evaluate its CM norm and prove the selected prime is absent.  This route
could prove the same two p-unit inputs but has more arithmetic overhead.

## False Shortcuts Removed

The following statements are not compatible with the data and should not be
used as theorem targets:

```text
all nonzero orbit products are literally equal;
the right-unit action fixes printed determinant scalars;
the nonzero-orbit norm is an ordinary F_p[Y] resultant;
small right-binomial or Heegner-unit dictionaries explain the phase vector;
principal Frobenius on the Hilbert class set forces ordinary cyclotomic descent.
```

The theorem has to live in the determinant-line/crossed-product setting.

## Next Missing Theorem

The remaining arithmetic theorem can be stated cleanly:

```text
For p = 10^24 + 7 and the embedded 157/211 trace-GCD construction,
the p-integral semilinear Fitting section satisfies

  Xi_0 = Res_p-lin(P_{K_0}, T_0) in O_p^*
  Xi_1 = Norm_O1(Res_p-lin(P_{K_t}, T_t)) in O_p^*

and multiplication by 2 on the right cyclotomic factor transports the
determinant line around the six nonzero Frobenius orbits by p-unit factors.
```

The finite implications of this theorem are already represented in:

```text
p24/lean/TraceGcdLinearizedResultantNormGate.lean
p24/lean/TraceGcdDiamondEquivarianceGate.lean
p24/lean/TraceGcdTwoOrbitCompressionGate.lean
p24/trace_gcd_orbit_norm_certificate_verifier.py --unit2-schema
```

Thus further work should attack those two p-unit nonvanishing statements
directly, not add more compression layers.
