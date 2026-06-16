# Internal C/E Character Filter Gate

This gate sharpens the newest p24 internal-trace target.

The Gaussian-functional form was:

```text
Tr_{C/E}(Tr_{B/C}(R_obstruction)) = 0
```

or, after choosing a relative `n`-th root of unity,

```text
sum_k c_k eta_{a k} = 0.
```

The new finite-algebra formulation is:

```text
the B/C-traced obstruction has zero trivial C/E character component.
```

Equivalently, after setting

```text
Y_C = Tr_{B/C}(R_obstruction),
```

the theorem is

```text
Pi_C,triv(Y_C) = 0.
```

This is still exactly the same codimension-one target, but it is now phrased
as an internal character-support statement rather than an opaque weighted
Gaussian-period pairing.

## p24 Bookkeeping

The script records:

```text
rho = p^780 mod n
ord_n(rho) = 38843 = 7 * 5549
rho^7 = p^5460 mod n
ord_n(rho^7) = 5549 = 179 * 31
ord_n((rho^7)^179) = 31       # B/C trace subgroup
ord_n((rho^7)^31) = 179       # C/E character direction
```

The order-7 quotient twist is therefore not the internal cancellation source:
after seven raw steps the scalar quotient twist has disappeared.  Random
order-7 covariant packets have nonzero internal trace in the toy model.

## Positive Theorem Shape

The useful sufficient theorem is not the stronger

```text
Tr_{B/C}(R_obstruction) = 0.
```

The gate constructs packets with:

```text
Tr_{C/E}(Tr_{B/C}(...)) = 0
Tr_{B/C}(...) != 0
```

by placing the `B/C` trace in a nontrivial `C/E` character space.  This is the
minimal p24-shaped target already identified by the stage-target gate.

## Harness Markers

```text
order7_quotient_twist_dies_after_internal_generator=1
random_order7_covariant_packets_do_not_have_internal_trace_zero=1
nested_internal_trace_zero_is_zero_trivial_C_character_component=1
nontrivial_C_character_support_is_sufficient_and_not_B_over_C_zero=1
remaining_theorem_is_no_trivial_C_character_in_B_over_C_obstruction=1
conclusion=reported_trace_gcd_fixed_frequency_p24_internal_character_filter_gate
```
