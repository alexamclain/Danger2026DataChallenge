# p24 Compressed Search Readiness

Date: 2026-06-07

This note answers the operational question: can we start testing inside the
current compressed search surface for `p=10^24+7`?

## Result

Yes, but only conditionally. If a selected p-integral CM/Lang subgroup kernel
polynomial realizing the whole `179`-subgroup residual is supplied, the
remaining check is small and deterministic. Without that object, there is no
honest compressed root search to run; the only large computation available is
the old randomized Pomerance search, which is a lottery and not the asymptotic
proof.

I added:

```text
p24/trace_gcd_p24_compressed_search_readiness.py
```

Run:

```text
PYTHONPYCACHEPREFIX=/private/tmp/codex-pycache PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=p24 python3 p24/trace_gcd_p24_compressed_search_readiness.py
```

It reports:

```text
p_mod_8=7
danger_k=40
strict_trace_representatives=[-1178414874616, -78903246840, 1020608380936]
selected_trace=-1178414874616
selected_order_two_adic_depth=41
selected_order_odd_part=454747350887
x16_p23_sampler_available_for_p24=0

p24_symbolic_right_mixed_pairs=189036
p24_admissible_jacobi_rank=621
p24_broad_jacobi_rank=625
p24_broad_minus_admissible_rank=4

p24_diamond_orbit_size=178
p24_oriented_one_point_diamond_choices=178
p24_x_coordinate_generator_pairs=89
p24_kernel_polynomial_generator_orbits=1
p24_c_divides_selected_group_order=0
p24_c_frobenius_discriminant_legendre=-1
p24_c_final_curve_rational_isogeny_available=0
p24_diamond_norm_matches_cyclotomic_residual=1
p24_residual_fourier_channels=1246

p24_kummer_selected_e_values=[1]
p24_h_coset_equations=1092
p24_compressed_independent_equations=48
p24_low_moment_first_layer_constraints=4
p24_low_moment_second_layer_constraints=26
p24_low_moment_pairing_constraints=30

conditional_punit_payload_field_elements=4
selected_chain_slots=3107811
generic_sqrt_scale_trials=1000000000000
conclusion=compressed_search_surface_ready_but_producer_missing
```

## Consequence

The current deterministic search space is not `sqrt(p)` and not `1092`
samples. It is:

```text
2 anchor signs,
1 forced Kummer exponent e=1,
1 subgroup kernel polynomial after generator choices collapse and after the
  selected auxiliary fiber/section is already paired,
then the 48 / 1092 finite verifier surface.
```

There is now one useful pre-producer testing lane:

```text
low-moment selector hypothesis:
  first p24 odd layer:  4 random-like F_p moments
  second p24 odd layer: 26 random-like F_p moments
  total:                30 moment constraints
```

The actual-CM selector sweep supports the collision model on small embedded
CM towers: default run `19/19` rows isolate within the tested degree bound,
and a wider run gives `65/65` rows isolated within degree `6`.  This is
evidence for a theorem target, not a certificate.  The missing step is still
an intrinsic construction of those selected moments plus a CM anti-collision
proof.

The sharper dictionary is sparse-relation avoidance: after canceling overlap,
two same-size subsets with equal first `k` moments give a disjoint signed
relation on the moment curve `x -> (x,...,x^k)`.  Newton identities already
forbid reduced collision size `<= k`, so the p24 proof only has to rule out
sizes `5..157` in the first layer and `27..211` in the second layer.

The construction target is also sharper now: the child power sums are
relative traces `Tr(Y^d)` of powers of the fine quotient-period element.
Thus p24 needs either `30` selected relative-trace values on the selected path
or `8172` coefficients if the moment functions are kept as parent-field
elements.

Refinement: two of the `30` selected values are automatic first moments
`P_1=sum(children)=parent`, already carried by the selected parent chain.
The genuinely new higher-moment target is `28` selected values.  The full
anti-collision verifier still uses the two `P_1` constraints: higher-only
entropy is not enough for random-unique selection at p24 scale.

Equivalently, by Newton identities, the producer may target `28` new
truncated child-polynomial coefficients:

```text
first layer:  e_2..e_4
second layer: e_2..e_26
```

The `178` count is the size of the residual product, not a generator-candidate
count after passing to `K_H`.  The missing datum is not CPU volume. It is the
selected p-integral CM/Lang subgroup kernel polynomial. Once that is named,
the test is immediate.

Generator collapse does not supply section pairing.  The first p24 odd layer
has `binomial(314,157)` possible unordered degree-157 children; even a single
trace/sum constraint leaves random-scale ambiguity about `10^69`.  The
producer still needs relative class-character traces, an embedded relative
morphism, or an equivalent phase-aware CM/Lang identity.

Important guardrail: this `K_H` is not an `F_p`-rational final-curve
`179`-isogeny object for the selected p24 trace.  Here `179` does not divide
`#E(F_p)`, and `t^2-4p` is a nonsquare modulo `179`, so the final curve has no
`F_p`-rational `179`-isogeny.  The kernel target must live in the auxiliary
CM/Lang or cyclotomic layer.

The old p23 `X1(16)` nonsplit sampler is not a good p24 fallback because this
`p` has `p mod 8 = 7`, while that sampler path requires `p mod 8 = 5`. A
generic 2-Sylow search still runs, but a 10,000-trial smoke test found no hit
and only confirms it is a sqrt-scale lottery, not the theorem route.
