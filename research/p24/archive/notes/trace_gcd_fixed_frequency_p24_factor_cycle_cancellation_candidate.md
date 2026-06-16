# Fixed-Frequency p24 Factor-Cycle Cancellation Candidate

Date: 2026-06-06

## Point

The class-character expansion reduces the current order-7 target to packet
product sums

```text
sum_a T_{1,0,a} R_{chi,-a}.
```

Termwise right-combo vanishing is too strong, and inversion symmetry alone
does not cancel the packet.  The first positive p24-specific structure is the
70-way splitting of a relative packet after adjoining

```text
E = F_p(mu_m),     m = 2*157*211.
```

For p24:

```text
ord_m(p) = 5460
ord_n(p) = 388430
gcd(ord_m(p), ord_n(p)) = 70
```

so each `F_p` relative packet splits over `E` into 70 degree-5549 factors.

## The p780 Alignment

Let

```text
rho = p^780.
```

Then:

```text
rho fixes the left 157-character;
rho shifts the right H-quotient by 6 mod 7;
rho shifts the 70 E-factor labels by 10 mod 70.
```

The shift `+10` on `Z/70Z` has ten cycles of length 7.  In the scalar shadow,
if the E-factor packet contributions for a nontrivial order-7 character
satisfy the expected covariance along these cycles, each cycle has a
nontrivial geometric multiplier and its sum is zero.

In the actual tower this statement is semilinear: `p^780` has order `7` on
`E`, so covariance alone places the packet sum in a nontrivial Frobenius
eigenspace.  The zero follows only after proving the same total packet sum
descends to the `p^780`-fixed left field `L=F_p(mu_157)`.

This would prove the packet cancellation without requiring any individual
right-combo to vanish.

## Remaining Theorem

The finite implication is now clean:

```text
p780-covariant E-factor packet contributions plus descent to L
  => sum_a T_{1,0,a} R_{chi,-a} = 0
  => C P_H = 0
  => no fixed-frequency defect.
```

The missing arithmetic theorem is the first line: prove that the actual p24
class-character product contributions descend to the 70 E-factors, satisfy
this `p^780` covariance with the right order-7 character multiplier, and that
the total product sum is the descended `L`-valued fixed-frequency projection.

## Check

The finite gate is:

```text
p24/trace_gcd_fixed_frequency_p24_factor_cycle_cancellation_candidate.py
p24/trace_gcd_fixed_frequency_p24_semilinear_factor_cycle_gate.py
```

It verifies:

```text
tensor_factor_count_over_E=70
tensor_factor_degree_over_E=5549
rho_left157_fixed=1
rho_right_h_quotient_shift=6
rho_factor_step_mod_70=10
rho_factor_cycle_count=10
rho_factor_cycle_length=7
covariant_character_sums_zero=6/6
random_character_sums_nonzero=6/6
```
