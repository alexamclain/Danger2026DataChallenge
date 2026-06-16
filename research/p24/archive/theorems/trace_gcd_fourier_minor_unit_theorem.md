# Trace-GCD Fourier-Head Minor Unit Theorem

Date: 2026-06-06

This note removes one ambiguity from the trace-GCD exterior expansion.  The
fixed Schubert/Fourier coefficients in the selected Lang-head projection are
p-units.  Therefore the missing theorem is not a support failure on the fixed
projection side; it is cancellation or p-unitness on the actual CM Plucker /
Fitting side.

## Setup

Fix a nonzero right Frobenius orbit

```text
O subset (Z/211Z)^*,     |O| = 35.
```

After adjoining a primitive `211`st root of unity `zeta`, the right
translation operator is diagonal on character lines:

```text
V_t e_u = zeta^(t u) e_u,        u in O.
```

The trace-GCD determinant for one orbit has the Cauchy-Binet expansion

```text
Delta_O(t)
  = sum_{U subset O, |U|=16}
      det(P_U) det(W_U) zeta^(t * sum_U u).
```

Here `W_U` is the CM Plucker coordinate of the transported 16-plane, while
`P_U` is fixed by the selected Lang-head projection.

## Theorem

For the selected first-16 Lang coordinates, every fixed coefficient

```text
det(P_U),        U subset O, |U|=16,
```

is a p-unit at `p = 10^24 + 7`.

Equivalently, all

```text
binom(35,16) = 4059928950
```

fixed Schubert/Fourier coefficients in one nonzero right orbit are nonzero
and have p-unit denominators.

## Proof

In the split character basis, the first-16 coordinate projection has rows

```text
1, zeta^u, zeta^(2u), ..., zeta^(15u).
```

Depending on the Fourier-inverse convention this matrix may be multiplied by
a global sign and a power of `211^{-1}`.  These are p-units at the selected
p24 prime and do not affect the zero/nonzero statement.

For a subset

```text
U = {u_1,...,u_16} subset O,
```

the corresponding minor is the Vandermonde determinant

```text
det(zeta^(r u_j))_{0 <= r <= 15, 1 <= j <= 16}
  = prod_{i<j} (zeta^(u_j) - zeta^(u_i)).
```

The exponents `u_j` are distinct modulo the prime `211`, so the roots
`zeta^(u_j)` are distinct.  Hence every factor is nonzero.

The Fourier inverse normalization contributes only a power of `211` in the
denominator.  Since

```text
gcd(211, 10^24 + 7) = 1,
```

that denominator is a p-unit.  Therefore every fixed minor is a p-unit.

## Audit

The p24 bookkeeping is reproducible with:

```text
PYTHONDONTWRITEBYTECODE=1 python3 \
  p24/fourier_head_minor_unit_audit.py
```

It reports:

```text
right=211
p_mod_right=114
ord_p_mod_right=35
orbit_length=35
tail=16
fixed_minor_count=binom(35,16)=4059928950
right_prime_to_p=1
distinct_orbit_exponents=1
denominator_p_unit=1
all_fixed_head_minors_nonzero_by_vandermonde=1
all_fixed_head_minors_p_units=1
distinct_subset_sum_support_size_k3=211
full_exponent_support_by_k3=1
```

## Consequence

The trace-GCD selected Schubert p-unit theorem is now more sharply localized.
For p24, the fixed projection side has full p-unit Plucker support, and the
exponent support is already all of `Z/211Z` by `k=3`.

Thus the remaining theorem is:

```text
prove p-adic noncancellation of the actual CM Plucker expansion,
or identify the orbit/global product with an honest class-field/Fitting/
Borcherds p-unit.
```

This strengthens the boundary in:

```text
p24/trace_gcd_orbit_exterior_schubert_expansion.md
p24/lang_trace_gcd_plucker_spectral_boundary.md
p24/trace_gcd_selected_schubert_punit_frontier.md
```

Coordinatewise nonzero CM Plucker entries would still be insufficient, as
shown by `p24/orbit_exterior_schubert_toy.py`; but any proof no longer has to
worry about fixed Fourier minors vanishing at the selected p24 prime.
