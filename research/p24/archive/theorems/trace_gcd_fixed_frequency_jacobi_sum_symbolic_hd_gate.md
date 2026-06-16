# Symbolic Hasse-Davenport Gate

Date: 2026-06-07

## Point

The finite-field Jacobi anchor correction is not only an empirical finite
field pattern.  The product-formula identities follow from symbolic
character/Gauss-sum accounting.

This gate checks the residue conditions for the reduced packet:

```text
Jdagger(1,1)=1
Jdagger(A,B)=J(A,B) otherwise.
```

## Symbolic Row-Ratio Cancellation

For fixed right row `r`, write:

```text
A_k = chi^(u*t(r,k))
B_k = chi^(v*t(r,k)).
```

Since `u` is right-trivial, `B_k` and `A_kB_k` have the same right component.
Since `v` and `u+v` have nonzero C-components, each runs through the same
size-`c` C-coset as `k` varies.

At `k=0`, `A_0=1`, so:

```text
B_0 = A_0 B_0.
```

Removing the common `k=0` element leaves identical punctured C-cosets.  Thus
in:

```text
prod_{k != 0} G(A_k)G(B_k)/G(A_kB_k)
```

the `B_k` and `A_kB_k` Gauss factors cancel, leaving:

```text
prod_{k != 0} G(A_k),
```

which is independent of the right row `r` and of the right-mixed partner `v`.

## Symbolic Pair-Product Constants

For `k != 0`, admissibility makes `A`, `B`, and `AB` all nontrivial, so:

```text
J(A,B)J(A^-1,B^-1)=q.
```

On the C-zero fiber, `A=1`.  For `r != 0`, `B` is nontrivial and
`J(1,B)=-1`, giving pair-product `1`.  At `r=0`, the reduced anchor
`Jdagger(1,1)=1` also gives pair-product `1`.

## Coverage

The gate checks all admissible right-mixed pairs for:

```text
c = 5, 11, 13, 17, 19, 179.
```

For p24, `c=179`, and the pair count is:

```text
6*(179-1)*(179-2) = 189036.
```

Observed:

```text
symbolic_pair_count_rows=6/6
symbolic_pair_product_rows=6/6
symbolic_row_ratio_rows=6/6
symbolic_reduced_anchor_rows=6/6
symbolic_producer_rows=6/6
p24_symbolic_right_mixed_pairs=189036
```

No finite-field sums and no p24 class-set enumeration are used.

## Consequence

The p24 missing theorem is not the finite Jacobi/Hasse-Davenport algebra
anymore.  That algebra is isolated.

The gate now also checks the verifier-facing value identities directly for
the reduced Jacobi carry.  For every right-mixed admissible pair, including
all `189036` p24 pairs, the carry

```text
theta(t) = [u t] + [v t] - [(u+v)t]
```

satisfies:

```text
theta(r,0)=0,
theta(t)+theta(-t)=7*c off the C-zero fiber,
sum_c theta(r,c) is independent of r.
```

Thus a selected quotient packet identified with this reduced carry feeds the
value-side verifier gate without any further finite algebra.  The Lean file
`TraceGcdDualConditionsValueSideGate.lean` now records this as a
`ReducedJacobiCarryObligations` handoff.

The targeted source refresh gives the right name for this algebra:
Kubert-Lichtenbaum/Weil mixed-level Jacobi-sum Hecke characters and the
Langlands/Hasse-Davenport Gauss-sum identities.  That source validates the
shape of the reduced Jacobi packet, but it does not by itself identify the
p24 class-field orbit.

The imaginary-quadratic refinement of Brattstrom-Lichtenbaum gives the
natural next theorem shape: a mixed-level `theta` packet with integral
infinity type yields a Galois-equivariant Jacobi-sum Hecke character.  For
p24 the non-formal part is to choose such a packet so that, after projection
to the unramified `rho` quotient, it is exactly this reduced `C_7 x C_179`
packet.

The visible packet has the right conductor-lift infinity shadow.  Since the
p24 quadratic conductor is coprime to `7*179`, the conductor units split
evenly between the two CM embeddings.  For every admissible
`theta=[u]+[v]-[u+v]`, the visible unit sum is:

```text
phi(7*179)/2 = 534.
```

The p24 lift therefore has equal integral identity/conjugate coefficients:

```text
174015840695068591393327296
```

on both embeddings.  This makes the conductor lift compatible with the
Jacobi-sum Hecke-character criterion, but it also shows that the infinity type
does not select the rho quotient; selection has to come from the finite Artin
component.

The visible ray/Shimura unit component is not that finite Artin source.  Both
visible primes are inert in the p24 CM field, so the visible ray unit part
over the Hilbert class field has order:

```text
((7^2 - 1)(179^2 - 1))/2 = 768960.
```

This order is not divisible by `7`, by `179`, or by `7*179`.  Therefore the
post-`B/C` quotient is not a visible ray quotient.  It comes from the
unramified `n=3107441` class component, where `rho=p^780` has order
`7*31*179` and the `B/C` trace removes the `31` factor.

The gate records the explicit quotient coordinates:

```text
rho^e = (rho^179)^r * (rho^7)^c,
e = 179*r + 7*c mod 1253.
```

Equivalently, the `179` exponent step is the right `C_7` axis, the `7`
exponent step is the `C_179` axis, and the pairs `(r,c)` cover the full
post-`B/C` quotient.

The gate also separates quotient inflation from possible nontrivial
`B/C`-kernel twists.  For a reduced character exponent `a mod N`, where
`N=7*179`, the quotient pullback to the full `M=31*N` rho cycle uses exponent
`31*a`.  Then every kernel lift `T=t+jN` satisfies:

```text
(31*a*T mod M) = 31*(a*t mod N).
```

For the Jacobi carry this means:

```text
full raw carry on each lift = 31 * reduced raw carry.
```

The p24 check samples representative right-mixed packets over all `1253`
quotient points and all `31` kernel lifts:

```text
p24_bc_trace_inflation_sampled_point_checks=116529
p24_bc_trace_inflation_sampled_inflated_residue_identity=1
p24_bc_trace_inflation_sampled_inflated_carry_identity=1
p24_bc_trace_inflation_normalized_divisor_trace_scale=31
p24_bc_trace_inflation_multiplicative_norm_power=31
p24_bc_trace_inflation_bc_layer_introduces_new_character_support=0
```

The additive trace projection is exact across all full-cycle character
exponents:

```text
p24_bc_trace_character_projection_full_character_exponents=38843
p24_bc_trace_character_projection_surviving_quotient_exponents=1253
p24_bc_trace_character_projection_killed_kernel_twist_exponents=37590
p24_bc_trace_character_projection_survival_iff_exponent_divisible_by_31=1
p24_bc_trace_character_projection_trace_kills_nontrivial_kernel_twists=1
p24_bc_quotient_ratio_order_bound_survivor_pair_checks=1570009
p24_bc_quotient_ratio_order_bound_survivor_ratio_stays_kernel_trivial=1
p24_bc_quotient_ratio_order_bound_max_ratio_order=1253
p24_bc_quotient_ratio_order_bound_ratio_order_divides_post_bc_quotient=1
```

So for divisor/log packets, `Tr_{B/C}` automatically kills the nontrivial
`31`-kernel twists and projects to quotient characters.  The ratio of any two
surviving quotient packets still has order dividing `1253`, checked
exhaustively over all `1253^2` survivor pairs.  On that surviving quotient
part, trace/norm contributes only a harmless `31` scaling or `31`st power.
The remaining question is therefore not the killed kernel phase; it is whether
the surviving selected quotient packet is the reduced Jacobi/CM-Lang packet.

The plain cyclotomic Frobenius check is deliberately negative:

```text
p mod 7        = 1,  order 1
p mod 179      = 77, order 89
p mod 7*179    = 435, order 89
actual quotient after Tr_{B/C} has order 7*179 = 1253
```

So the reduced packet cannot be realized by simply taking ordinary
cyclotomic Frobenius on `mu_{7*179}`.  It has to be pulled back through the
CM/class-field Artin quotient where `rho=p^780` has the checked
post-`B/C` quotient `C_7 x C_179`.

The Anderson/Taniyama-group source removes one old objection but not the hard
one.  It defines Jacobi-sum Hecke characters over arbitrary number fields,
so the base field need not be abelian over `Q`.  However the parameter is
still made from cyclotomic symbols `[x] in Q/Z`.  Along the actual p24
class-field element `rho=p^780`, that cyclotomic shadow is:

```text
rho mod 7*179 on cyclotomic symbols = 666
order = 89
rho mod 7 = 1
rho mod 179 = 129, order 89
actual post-B/C class quotient order = 1253
```

Thus the theorem

```text
Anderson Jacobi character over a larger number field
  + visible cyclotomic parameter
  => selected p24 quotient packet
```

is false by finite order.  Anderson still supplies the right existence and
Frobenius/Gauss-sum language for `J_k(a)`, but the proof must add a genuine
CM-Artin/trace-GCD identification that pulls the mixed-level packet through
the unramified `rho` quotient.

The positive replacement is an unramified class-character twist, not a
visible cyclotomic action.  If `chi_full(rho)=zeta_M` for
`M=31*7*179`, then

```text
chi_q = chi_full^31
```

is trivial on the `B/C` kernel and has exact order `7*179` on the
post-trace quotient.  The gate checks:

```text
p24_unramified_twist_selector_quotient_twist_order=1253
p24_unramified_twist_selector_quotient_twist_trivial_on_bc_kernel=1
p24_unramified_twist_selector_quotient_twist_right_axis_order=7
p24_unramified_twist_selector_quotient_twist_c_axis_order=179
p24_unramified_twist_selector_quotient_character_exponents_are_exactly_trace_survivors=1
```

This is the finite selector we were missing after ruling out the cyclotomic
shortcut.  It is not yet the certificate: twisting by the unramified class
character supplies the correct quotient coordinates, but the arithmetic
producer still has to identify the selected trace-GCD/CM-Lang packet with the
Jacobi packet pulled through this twist.

There is also an important false strengthening.  The selector cannot be
treated as arbitrary extra multiplicative character noise on an already
selected packet.  In additive/log coordinates, a bare mixed linear quotient
character added after the fact breaks the value-side row balance:

```text
p24_linear_twist_guardrail_full_generator_row_balance_ok=0
p24_linear_twist_guardrail_full_generator_inversion_constant=0
p24_linear_twist_guardrail_full_generator_distinct_row_sums=7
p24_linear_twist_guardrail_pure_c_axis_preserves_value_identities=1
p24_linear_twist_guardrail_pure_right_axis_selected_defect_is_zero=1
```

So the correct theorem is not "multiply by any quotient character and keep
the verifier identities."  The unramified twist has to act as the Artin
coordinate pullback of the Jacobi packet before the selected-defect/value-side
identities are read.

The finite uniqueness part of that pullback is also now isolated.  The
post-`B/C` quotient is cyclic of order `1253` and generated by the image of
`rho`.  Therefore a finite-order unramified ratio character on this quotient
is determined by its value on `rho`.  The gate checks all `1253^2` pairs of
quotient characters:

```text
p24_artin_character_uniqueness_post_bc_quotient_order=1253
p24_artin_character_uniqueness_rho_image_generator_order=1253
p24_artin_character_uniqueness_post_bc_character_count=1253
p24_artin_character_uniqueness_character_pair_checks=1570009
p24_artin_character_uniqueness_same_value_on_rho_implies_same_character=1
```

So the coordinate-pullback theorem has a precise remaining arithmetic core:
prove the Hecke-character ratio between the selected trace-GCD packet and the
reduced Jacobi/CM-Lang packet has matching infinity type, matching finite
local type on the killed conductor/ray part, factors through the unramified
post-`B/C` quotient, and has the selected value on `rho`.

The selected value on `rho` can itself be split into independent axis checks.
In the quotient coordinates

```text
rho^e = (rho^179)^r * (rho^7)^c,
e = 179*r + 7*c mod 1253,
```

we have:

```text
1 = 2*179 + 128*7 mod 1253.
```

So:

```text
rho = (rho^179)^2 * (rho^7)^128.
```

The gate checks all `1253^2` character pairs:

```text
p24_axis_value_reconstruction_rho_from_right_axis_power=2
p24_axis_value_reconstruction_rho_from_c_axis_power=128
p24_axis_value_reconstruction_bezout_integer_sum=1254
p24_axis_value_reconstruction_bezout_reconstructs_rho_exponent=1
p24_axis_value_reconstruction_same_axis_values_iff_same_rho_value=1
p24_right_axis_selector_convention_rho_h_shift=6
p24_right_axis_selector_convention_post_bc_rho_right_coordinate=2
p24_right_axis_selector_convention_right_axis_h_shift_from_decomposition=3
p24_right_axis_selector_convention_c_axis_h_shift=0
p24_right_axis_selector_convention_rho_recomposed_h_shift=6
p24_right_axis_selector_convention_right_axis_selector_reduced_to_shift6_covariance=1
p24_c_axis_residual_character_right_fixed_residual_candidates=179
p24_c_axis_residual_character_residual_ratio_exponents_all_multiples_of_7=1
p24_c_axis_residual_character_residual_right_axis_values_count=1
p24_c_axis_residual_character_residual_c_axis_values_count=179
p24_c_axis_residual_character_residual_max_order=179
p24_c_axis_residual_character_c_axis_separates_characters_after_right_axis_fixed=1
p24_pure_c_axis_residual_value_side_invariance_residual_characters=179
p24_pure_c_axis_residual_value_side_invariance_invariant_value_side_hits=179
p24_pure_c_axis_residual_value_side_invariance_all_pure_c_residuals_preserve_value_side=1
p24_pure_c_axis_residual_value_side_invariance_pure_c179_residual_value_not_needed_for_hcoset_verifier=1
p24_verifier_equivalent_anchor_producer_surface_right_mixed_admissible_pairs=189036
p24_verifier_equivalent_anchor_producer_surface_r179_c_nontrivial_fourier_channels=1246
p24_verifier_equivalent_anchor_producer_surface_kernel_polynomial_degree=89
p24_verifier_equivalent_anchor_producer_surface_remaining_input_is_selected_cm_lang_r179_specialization=1
```

Therefore the verifier-facing axis obligation is weaker than exact
`ratioMatchesSelectorOnRho`.  The right-axis generator `rho^179` is the `+3`
shift in the old right-H quotient convention, because `rho` has right
coordinate `2`, the C-axis fixes the right-H quotient, and `2*3=6 mod 7`.
After that right-axis value is fixed, only `179` residual quotient characters
remain: exponents `1+7s`.  Dividing by the selected Artin coordinate leaves a
pure `C_179` character with exponent `7s`, and the C-axis separates those
`179` possibilities.  But every pure `C_179` residual preserves the three
value-side identities, so the exact residual value is not needed for the
1092-equation H-coset verifier.  It is only needed if one wants full packet
equality rather than verifier equivalence.

The remaining arithmetic producer is therefore concrete:

```text
punctured Hasse-Davenport rows
+ selected degenerate R_179 / kernel-polynomial anchor
+ selected-child subtraction compatibility
=> verifier-equivalent reduced Jacobi carry.
```

For p24 this surface is still tiny compared with `sqrt(p)`: `189036`
right-mixed admissible pairs, a `1246`-channel `C/E`-nontrivial anchor
residual, and a degree-`89` kernel polynomial anchor.

The killed visible/ray local part also has no room to carry either selector
axis.  Its order over the Hilbert class field is still:

```text
768960 = 2^6 * 3^3 * 5 * 89,
```

and the gate now records the stronger coprimality:

```text
p24_visible_shimura_ray_group_gcd_ray_order_right_axis=1
p24_visible_shimura_ray_group_gcd_ray_order_c_axis=1
p24_visible_shimura_ray_group_gcd_ray_order_post_bc_quotient=1
p24_visible_shimura_ray_group_candidate_ratio_order_bound=1253
p24_visible_shimura_ray_group_candidate_ratio_order_divides_post_bc_quotient=1
p24_visible_shimura_ray_group_gcd_ray_order_candidate_ratio_order_bound=1
p24_visible_shimura_ray_group_post_bc_order_character_restriction_to_visible_ray_forced_trivial=1
p24_visible_shimura_ray_group_visible_ray_has_no_hom_to_post_bc_axes=1
p24_visible_shimura_ray_group_local_finite_type_reduced_to_unramified_ratio_order=1
```

Thus the killed local/ray part has a sharper handoff than raw finite-local
equality.  If the packet ratio has order dividing the post-`B/C` quotient
`1253`, then its restriction to the visible ray group is forced trivial by
coprimality.  The selector axes cannot come from that local part; they must
factor through the unramified `n`-component.

The remaining arithmetic input is therefore:

```text
construct the selected trace-GCD packet after Tr_{B/C} as the p-integral
specialization/log/divisor of the reduced Jacobi/CM-Lang packet after the
CM-Artin pullback from the actual rho quotient.
```

Equivalently, find the CM/Lang unit whose single degenerate anchor is the
p24 analogue of `J(1,1)/(q-2)`.
