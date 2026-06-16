# Fixed-Frequency p24 Matching Twist Bookkeeping Gate

Date: 2026-06-06

## Point

The product-coboundary theorem needs the matching twist:

```text
sigma(A)=alpha*A
B=sigma(V)-(epsilon/alpha)*V
```

For the p24 fixed-frequency packet terms under `sigma=Frob_p^780`, the twist
is now explicit rather than symbolic.

## p24 Convention

Use the raw right quotient character convention

```text
chi_k(2)=zeta_7^k.
```

Then:

```text
p^780 = 1 mod 157,
p^780 has right H-quotient shift 6 mod 7.
```

So the left covariance multiplier is trivial:

```text
alpha_a = 1.
```

For each nontrivial right quotient character:

```text
lambda_chi = chi(p^780) = zeta_7^(6k)
epsilon_chi = lambda_chi^(-1) = zeta_7^k.
```

Thus the concrete right-resolvent target is:

```text
R_{chi_k,-a} = sigma(V_{chi_k,a}) - zeta_7^k * V_{chi_k,a}
```

in the raw convention, up to the orientation/inverse convention chosen for the
right resolvent labels.

Some earlier toys normalize quotient labels so `p` itself has index `1`; in
that convention `p^780` has shift `3`, so the inverse eigenvalue exponents are
`4k`.  This is the same theorem with relabeled quotient characters.

## Checked Gate

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_fixed_frequency_p24_matching_twist_bookkeeping_gate.py
```

Key output:

```text
p24_rho_mod_157=1
rho_raw_h_quotient_shift=6
rho_normalized_h_quotient_shift=3
left_alpha_exponents=[0, 0, 0, 0, 0, 0]
raw_epsilon_exponents=[1, 2, 3, 4, 5, 6]
normalized_epsilon_exponents=[4, 1, 5, 2, 6, 3]
p780_fixes_left_157_frequency=1
left_covariance_alpha_is_trivial=1
raw_matching_epsilon_exponent_is_k=1
matching_right_resolvent_twist_is_now_explicit=1
```

