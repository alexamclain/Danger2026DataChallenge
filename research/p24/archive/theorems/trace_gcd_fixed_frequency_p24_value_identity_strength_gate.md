# p24 Value-Identity Strength Gate

Date: 2026-06-07

## Point

The three value-side identities are not equally related to the verifier.  The
verifier only needs the first identity:

```text
sum_c f(r,c) is independent of r.
```

The other two identities:

```text
f(r,0)=0,
f(r,c)+f(-r,-c) is constant for c != 0,
```

are structural Jacobi-carry conditions that nearly force the full admissible
span.  Once they hold, only three independent row-sum/global-balance equations
remain.

## Rank Split

For `C_7 x C_c`, with `q=(c-1)/2`, the ranks are:

```text
row-sum identity alone:              6
C-zero fiber identity:               7
inversion-complement identity:       7*q - 1
C-zero + inversion-complement:       7*q + 6
full value-side/admissible target:   7*q + 9
extra row-sum rank after structure:  3
```

For p24, `c=179`, `q=89`, so:

```text
C-zero + inversion-complement rank = 7*89 + 6 = 629
full value-side rank               = 7*89 + 9 = 632
solution dimension                 = 1253 - 632 = 621
```

## Consequence

The arithmetic theorem can be split into:

```text
1. structural symmetry:
   f(r,0)=0 and f(r,c)+f(-r,-c)=constant off the C-zero fiber;

2. three global balances:
   the remaining independent part of the row-sum identity.
```

This is sharper than treating all `632` equations uniformly.

It also explains how the admissible-Jacobi spectral fingerprint arises:
the structural symmetry supplies the conjugate-pair compatibility, and the
last three balances account for the terminal rank drop.

## Check

```text
PYTHONPYCACHEPREFIX=/private/tmp/codex-pycache PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH=p24 python3 \
  p24/trace_gcd_fixed_frequency_p24_value_identity_strength_gate.py
```

Observed:

```text
rank_matches=3/3
p24_zero_plus_inversion_rank=7*89+6=629
p24_full_value_rank=7*89+9=632
p24_row_sum_extra_after_zero_plus_inversion=3
p24_value_solution_dim=1253-632=621
```

No p24 class set or CM root enumeration is used.
