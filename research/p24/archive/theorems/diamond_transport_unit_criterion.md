# Diamond Transport Unit Criterion

Date: 2026-06-06

## Point

The unit-2/diamond theorem has two logically separate parts:

```text
1. structural transport:
   the right-unit automorphism carries the p24 determinant-line object for
   O to the determinant-line object for 2O;

2. denominator hygiene:
   the resulting determinant-line comparison factor is a p-unit.
```

The hard construction is item 1.  Item 2 is now isolated as a finite
p-integral criterion.

## Criterion

Suppose the producer constructs p-integral source and target lattice
isomorphisms

```text
d_K,O : K_O -> K_2O
d_T,O : T_O -> T_2O
```

and the transported block maps commute:

```text
B_2O o d_K,O = d_T,O o B_O.
```

On determinant lines this gives

```text
Xi_2O = epsilon_O * Xi_O,
epsilon_O = det(d_T,O) * det(d_K,O)^(-1).
```

If `det(d_T,O)` and `det(d_K,O)` are p-units, then `epsilon_O` is a p-unit.

The finite abstraction is Lean-checked in:

```text
p24/lean/TraceGcdDiamondEquivarianceGate.lean
```

under:

```text
punit_transition_from_integral_det_transport
punit_arrow_from_commuting_integral_det_transport
p24_unit2_prime_to_right_level
p24_transport_denominators_prime_to_p
p24_unit2_six_steps_is_frobenius_rotation17
```

## p24 Denominator Audit

The executable audit is:

```text
p24/diamond_transport_unit_denominator_audit.py
```

It records that the obvious denominator sources are prime to

```text
p = 10^24 + 7:
```

```text
2, 7, 30, 35, 156, 157, 211, 5460, 66254, h.
```

This matches the local invariant audit:

```text
p24/trace_gcd_p24_local_invariants.py
```

## What Remains

This note does not prove diamond equivariance.  It says:

```text
if the determinant-line transport is constructed over the p-integral
full right product algebra, then its comparison factors are p-units.
```

Thus the remaining diamond proof is structural rather than valuation-theoretic:
construct the full product-algebra determinant line, show unit-2 carries
prefix kernels and tail windows to the corresponding transported objects, and
identify the determinant-line comparison.

The finite support part of that structural proof is checked separately in:

```text
p24/diamond_support_transport_audit.py
p24/full_product_determinant_transport_toy.py
```

For the representative row `delete O4, tail O1, prefix O2,O3,O5,O6`, the
unit-2 action cycles deletion and tail through all six nonzero right Frobenius
orbits, preserves four prefix blocks, and keeps the size-16 tail window
Frobenius-contiguous.  After six unit steps the tail is back in `O1` with
rotation start `17`, so the p-integral producer must allow internal Frobenius
rotation inside target factors.

The full-product determinant transport toy checks the exterior-power
consequence of the desired commuting square and the same six-step closure:
`B_2O d_K = d_T B_O` implies
`Xi_2O = det(d_T) det(d_K)^(-1) Xi_O`, with p-unit transition factors.

After that, the only arithmetic nonvanishing statements are still:

```text
Xi_O0 in O_p^*
Xi_O1 in O_p^*
```
