# Fixed-Frequency Class-Character Expansion

Date: 2026-06-06

## Point

The multiplicative-resolvent target can be expanded in the relative
class-character basis.  For one relative packet, write

```text
T_{u,v,a}
  = sum_i zeta_157^(u i) zeta_211^(v i) lambda_a^(floor(i/m)) j_i,
```

where `u` is the left `157` additive character, `v` is the right `211`
additive character, and `a` is a relative `n=3107441` packet character.

Then the mixed Hermitian period has the product form

```text
H(1,v) = <A_1,B_v>
       = sum_{a in packet} T_{1,0,a} T_{0,v,-a}.
```

Therefore for a nontrivial order-7 right multiplicative quotient character
`chi`,

```text
sum_v chi(v) H(1,v)
  = sum_{a in packet} T_{1,0,a}
      * (sum_v chi(v) T_{0,v,-a}).
```

This is exactly the new order-7 theorem target after the nonzero Gauss-sum
factor is removed.

## Consequence

The p24 theorem is not simply "one class-character resolvent vanishes".
Generically every factor in the packet product sum can be nonzero while the
total multiplicative projection is nonzero.  A proof has to supply one of two
stronger arithmetic inputs:

```text
1. packet cancellation:
   sum_a T_{1,0,a} * R_{chi,-a} = 0;

2. stronger right-combo vanishing:
   R_{chi,-a} = sum_v chi(v)T_{0,v,-a} = 0
   for every relative packet character a.
```

The second input is sufficient but probably too strong unless a new
relative-character theorem gives it naturally.  The first is the exact
determinant/packet-level cancellation p24 appears to need.

The pinned actual-CM analogue `D=-13319, q=13463, m=28=4*7, n=5` has all
primitive relative right-combos nonzero for its nontrivial right quotient
character.  Thus termwise right-combo vanishing is not generic CM-packet
structure; it would need a genuinely p24-specific reason.

The first p24-specific cancellation candidate is factor-cycle cancellation
after scalar extension to `E=F_p(mu_m)`: each relative packet splits into 70
degree-5549 factors, and `p^780` fixes the left `157` character while cycling
the right order-7 quotient and the 70 factors as ten 7-cycles.  The refined
semilinear gate shows that covariance alone gives a nontrivial Frobenius
eigenvector, not necessarily zero.  The p24 proof needs covariance plus
descent of the total packet sum to the `p^780`-fixed left field.

## Check

The finite model is:

```text
p24/trace_gcd_fixed_frequency_class_character_expansion_toy.py
p24/trace_gcd_fixed_frequency_actual_cm_right_combo_boundary.py
p24/trace_gcd_fixed_frequency_p24_factor_cycle_cancellation_candidate.py
p24/trace_gcd_fixed_frequency_p24_semilinear_factor_cycle_gate.py
```

It verifies over a small split cyclic model:

```text
sum_v chi(v)<A_u,B_v>
  = sum_a T_{u,0,a} * sum_v chi(v)T_{0,v,-a};

random models have all left packet traces, all right multiplicative packet
combos, and all product terms nonzero, and the target projection is nonzero;

a right-neutral toy model kills the right multiplicative packet combos
termwise, which is sufficient but much stronger than the p24 statement.

a pinned actual-CM analogue has all right multiplicative packet combos
nonzero, so the termwise theorem is not generic CM structure.
```

## Updated Proof Surface

The next p24 theorem attempt should target the actual packet product sum:

```text
for every nontrivial order-7 chi,
sum_{a in packet} T_{1,0,a} R_{chi,-a} = 0.
```

This aligns the fixed-frequency order-7 problem with the existing embedded
relative phase/Kummer lane: the missing object is still non-genus relative
class-character data, but the required output is a named packet cancellation,
not a selected child polynomial and not a coordinatewise nonvanishing theorem.
