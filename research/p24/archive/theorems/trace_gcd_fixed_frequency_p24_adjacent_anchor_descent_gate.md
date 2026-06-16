# p24 Adjacent-Trace Anchor Descent Gate

Date: 2026-06-07

## Point

The covariance-telescope route has a single remaining descent object:

```text
T_0 = Tr_{Q(zeta_n)/Q(zeta_n)^<p>}(P_0(zeta_n)).
```

Once the pointwise CM/Lang Frobenius functoriality gives

```text
T_{i+6} = rho(T_i),
```

and adjacent differences telescope,

```text
sum_i T_i = 0,
```

the only extra input needed is

```text
rho(T_0) = T_0.
```

This is one field-valued anchor descent statement.  In an order-7 rho quotient
it is equivalent to the six nontrivial projector identities

```text
Pi_k(T_0) = 0,  k = 1,...,6,
Pi_k = (1/7) sum_{j=0}^6 omega^(-k*j) rho^j.
```

So the current branch does not ask to check the raw `1092` H-coset equations.
It asks to prove a single embedded CM/Lang descent theorem for `T_0`.

## Guardrails

The executable finite gate checks the semisimple order-7 projector algebra and
two leaks:

```text
covariance + telescope without anchor descent can be nonzero;
covariance + anchor descent without telescope can be nonzero.
```

Thus the remaining theorem is not a counting shortcut.  The proof needs the
actual selected adjacent-trace packet to land in the rho-fixed subfield.

## Checked Gate

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_fixed_frequency_p24_adjacent_anchor_descent_gate.py
```

Key markers:

```text
projector_idempotent_failures=0
projector_sum_failures=0
rho_projector_eigen_failures=0
anchor_descended_iff_nontrivial_rho_projectors_zero_failures=0
covariance_orbit_failures=0
covariance_plus_telescope_without_anchor_leaks=64/64
covariance_plus_anchor_without_telescope_leaks=42/42
fixed_anchor_telescope_forces_zero=43/43
p24_raw_hcoset_equations=1092
p24_compressed_right_difference_equations=48
p24_single_adjacent_anchor_projectors=6
single_anchor_descent_is_rho_fixedness_of_T0=1
single_anchor_projectors_are_the_remaining_descent_target=1
```

## Updated Proof Target

The remaining theorem for this branch can now be stated without ambiguity:

```text
For the embedded trace-GCD adjacent difference packet P_0 produced by the
CM/Lang construction, prove that

  T_0 = Tr_{Q(zeta_n)/Q(zeta_n)^<p>}(P_0(zeta_n))

is fixed by rho=p^780.
```

Equivalently, all six nontrivial rho-projectors of `T_0` vanish.  Proving this
plus the pointwise Frobenius functoriality of the `P_i` proves the `48`
compressed right-difference equations, which imply the raw `1092` H-coset
surface by the earlier gates.
