# Fixed-Frequency p24 Right Coboundary Obstruction Gate

Date: 2026-06-06

## Point

The product-coboundary route needs:

```text
R_chi = sigma(V) - epsilon_chi * V.
```

A tempting shortcut is to use the formal Frobenius covariance of the right
multiplicative resolvent.  This gate shows that shortcut has the sign wrong:
in the raw convention `chi_k(2)=zeta_7^k`, `Frob_p^780` acts on the right
coefficient vector with eigenvalue `zeta_7^k`, which is exactly the matching
product-coboundary twist `epsilon_k`.

Therefore the formal right character covariance places the right resolvent in
the obstruction eigenspace of `sigma - epsilon_k`; it does not construct the
potential.

## Consequence

The product-coboundary route is still a valid sufficient route, but the
missing input is sharper:

```text
extra CM/Lang internal-trace cancellation must remove the epsilon_k
obstruction component.
```

Equivalently, the proof cannot say:

```text
right-character covariance => right-resolvent coboundary.
```

It must prove a genuinely stronger internal packet identity.

The opposite twist would make the formal right resolvent a coboundary, but
that is the wrong product twist and does not feed the product-coboundary
Leibniz gate.

## Cyclotomic Internal Trace Boundary

The internal degree is:

```text
5549 = 31 * 179
```

and `Q=p^5460 mod n` has order `5549` modulo `n=3107441`.  A pure cyclotomic
trace over `<Q>` is a Gaussian period:

```text
sum_{i=0}^{5548} zeta_n^(a Q^i).
```

In the small split prime `q=37289293 = 12*n+1`, sampled nonzero `a` give
nonzero periods.  So cyclotomic orthogonality alone does not kill the internal
trace obstruction.

## Checked Gate

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_fixed_frequency_p24_right_coboundary_obstruction_gate.py
```

Key output:

```text
right_resolvent_covariance_failures=0
matching_coboundary_ranks=[180, 180, 180, 180, 180, 180]
matching_twist_trace_zeroes=0/6
matching_twist_coboundary_memberships=0/6
opposite_twist_trace_zeroes=6/6
opposite_twist_coboundary_memberships=6/6
internal_gaussian_period_nonzeroes=8/8
formal_right_character_covariance_has_matching_eigenvalue=1
formal_right_covariance_is_coboundary_obstruction_not_potential=1
cyclotomic_internal_trace_does_not_vanish_automatically=1
remaining_theorem_needs_cm_lang_internal_trace_cancellation=1
```

