# Trace-GCD Crossed Coinvariant Norm Target

Date: 2026-06-06

## Point

The fixed orbit can now be expressed as one square coinvariant determinant:

```text
Phi_full : R^4 + C_tail -> E/(tau_R - 1)E.
```

For a nonzero right Frobenius orbit this should not be collapsed to an
ordinary base-field polynomial.  The honest analogue is the crossed norm of
the transported square coinvariant maps.

Let

```text
O = {t0, p*t0, ..., p^34*t0} subset Z/211Z.
```

For each `t in O`, define the transported full coinvariant map

```text
Phi_t : R^4 + C_t -> E/(tau_R - 1)E,
Phi_t((y_j), z) =
  [sum_{j in B_t} y_j*S_j(t) + z*S_tail(t)].
```

Each `Phi_t` is square of dimension `156`.  The nonzero p-unit target is

```text
Xi_O = Nrd_O(Phi_t) = product_{t in O} det(Phi_t)
```

with determinant-line p-unit conventions.  Equivalently, `Xi_O` is the
determinant of the semilinear block-cycle/Fitting operator built from the
transported square coinvariant maps.

## Why This Is Better Than A List

The previous safe target was

```text
Norm_O(Res_p-lin(P_Kt,T_t)).
```

That is still correct, but it hides the arithmetic object behind transported
kernel bases.  The crossed coinvariant norm says instead:

```text
construct Phi_t in the 157/211 class-field phase algebra,
then prove the crossed reduced norm of Phi_t is a p-unit.
```

This is the nonzero-orbit analogue of the fixed square coinvariant target in:

```text
p24/trace_gcd_full_coinvariant_tail_target.md
```

It is still the same four-field verifier payload:

```text
Xi_O0, Xi_O0^{-1}, Xi_O1, Xi_O1^{-1}.
```

No new compression is claimed.  The new value is proof-facing: the p24
producer can target one reduced norm in the semilinear orbit algebra rather
than 35 unrelated kernel-basis determinants.

## Bad Event Detection

Finite algebra gives:

```text
det(block_cycle(Phi_t : t in O))
  = (-1)^(156*(35-1)) * product_{t in O} det(Phi_t)
  = product_{t in O} det(Phi_t).
```

The sign is positive for p24.  Therefore

```text
Xi_O in O_p^*
  => every Phi_t is an isomorphism modulo p
  => every transported trace-GCD resultant in O is a p-unit
  => no local bad tail-on-kernel event occurs in that orbit.
```

The same diamond/unit-2 determinant-line theorem then transports this one
nonzero representative orbit around the six nonzero right orbits.

This norm target is also the correct response to the cyclic class-tower
selector obstruction.  A parent quotient root has a child torsor above it, so
the theorem should not depend on a canonical child label.  The reduced norm is
allowed: changing admissible local choices only changes the determinant-line
representative by p-unit scale.  The finite choice-invariance handoff is:

```text
p24/crossed_norm_torsor_invariance.md
p24/lean/TraceGcdCrossedCoinvariantNormGate.lean
```

## Current Missing Theorem

For the actual p24 mixed periods and selected ordinary prime above
`p = 10^24 + 7`, prove:

```text
Nrd_O(Phi_t) in O_p^*
```

for one nonzero right Frobenius orbit `O`, and prove the unit-2
determinant-line transport factors are p-units.

In coboundary language, a local singularity at `t` is a nontrivial relation

```text
sum_j y_j*S_j(t) + z*S_tail(t) = tau_R(W)-W,
```

with `(y_j,z) != 0`.  The crossed norm theorem rules out such a relation
simultaneously over the Frobenius orbit by proving that the semilinear
Fitting determinant is a p-unit.

## Toy

The finite package is checked by:

```text
p24/trace_gcd_crossed_coinvariant_norm_toy.py
```

The toy builds tiny finite-extension square coinvariant maps, packages them
into a block-cycle crossed norm, and includes a forced singular local
coinvariant map.  It checks that the crossed norm detects exactly those local
singularities.

## Actual-CM Square-Map Audit

The same identity is now checked one level closer to the p24 producer by:

```text
p24/trace_gcd_actual_cm_square_coinvariant_block_cycle_audit.py
```

On the two actual-CM rows used by the two-resultant holdout, the audit builds
the full square coinvariant matrices `Phi_t` for every right-origin class,
groups them by right Frobenius orbit, and verifies:

```text
det(block_cycle(Phi_t : t in O))
  = (-1)^(d*(|O|-1)) * product_{t in O} det(Phi_t)
```

with `d` equal to the local square-map dimension.  The current bounded output
is:

```text
p24_target=skew_reduced_norm_of_transported_square_coinvariant_maps
p24_square_dim=156
p24_nonzero_orbit_len=35
p24_block_cycle_sign_positive=1
block_cycle_matches=12/12
block_cycle_full_rank_detection_matches=12/12
full_rank_orbits=12/12
square_coinvariant_block_cycle_is_skew_reduced_norm=1
nonzero_side_can_target_transported_square_coinvariant_maps=1
p24_still_needs_punit_theorem_for_the_actual_skew_norm=1
```

This does not prove the p24 p-unit theorem.  It does prove that the nonzero
side can be targeted as the skew reduced norm of the transported square
coinvariant maps, without retreating to separately chosen local kernel bases.
