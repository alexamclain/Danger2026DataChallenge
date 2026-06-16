# Hermitian Principal-Dominance Theorem

This note records the strongest characteristic-zero statement for the
preferred Hermitian scalar.

## Statement

For the third p24 target, choose the CM origin so that `j_0` is the principal
singular modulus, and write

```text
h = m*n,
m = 66254,
n = 3107441.
```

For every nontrivial relative character `a`, the fiber

```text
P_0(a) = sum_k zeta_n^(a*k) j_{m*k}
```

contains `j_0` with coefficient `1`.  The principal reduced form is the unique
form with denominator `a_form=1`; every other conjugate has `a_form >= 2`.
Using the standard bound

```text
||j(tau)| - exp(pi*sqrt(|Delta|)/a_form)| <= 2079,
```

the principal term dominates all other terms in `P_0(a)`.  Therefore

```text
P_0(a) != 0
```

in characteristic zero, and the Hermitian scalar

```text
H_a = sum_u |P_u(a)|^2
```

is strictly positive.

## p24 Numeric Margin

The audit

```text
p24/hermitian_principal_dominance_audit.py
```

reports:

```text
log_principal_lower=5.076699e12
log_one_other_upper=2.538350e12
log_fiber_other_sum_upper=2.538350e12
p0_dominance_margin=2.538350e12
log_abs_P0_lower=5.076699e12
log_Hermitian_embedding_lower=1.015340e13
lower_over_log_p=1.837319e11
```

So the complex nonvanishing is not delicate: the principal term dominates the
entire rest of the relative fiber by an exponential margin.

## Boundary

This does not prove the DANGER certificate.  The verifier needs `H_a` to be
nonzero after reduction at a selected split prime above

```text
p = 10^24 + 7.
```

The same audit reports that the positive value itself has log size about

```text
1.015340e13 = 1.837319e11 * log(p),
```

so archimedean dominance is far too large to imply p-adic unit status.

The theorem is still useful because it sharpens the target:

```text
the p24 Hermitian packet is a huge positive algebraic number in characteristic
zero; the only missing issue is divisibility by the selected split prime.
```

Thus the remaining proof must be a selected-prime p-adic unit theorem, a
congruence argument, or an explicit finite-field certificate.  Complex
positivity/dominance alone cannot finish it.
