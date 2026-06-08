# p24 Dual Conditions Value-Side Gate

Date: 2026-06-07

## Point

The four dual Fourier families are the clean verifier-facing target, but an
arithmetic proof of the selected weighted packet is more likely to see
value-side identities.

For a packet function:

```text
f : C_7 x C_179 -> K
```

the four Fourier families with:

```text
lambda_179 = -1/89
```

are equivalent to three value-side conditions.

## Three Value-Side Conditions

### 1. C-Row Sums Are Independent Of Right Coordinate

For every `r in C_7`:

```text
sum_c f(r,c)
```

is independent of `r`.

This is the value-side form of:

```text
F(a,0)=0, a=1,...,6.
```

### 2. C-Zero Fiber Vanishes

For every `r in C_7`:

```text
f(r,0)=0.
```

This packages the three global pair-balance equations together with the
right-trivial normalization.

### 3. Inversion-Complement Is Constant Off The C-Zero Fiber

There is a single constant `kappa` such that for all `c != 0`:

```text
f(r,c) + f(-r,-c) = kappa.
```

This is the value-side form of the conjugate-skew equations and the
right-trivial pair-sum normalization.

For an admissible C-axis Jacobi carry, this constant is the product degree
`N=7*c` in the integral model.

## Consequence

The selected-packet theorem can now be targeted without Fourier language:

```text
After Tr_{B/C}, the selected weighted packet f on C_7 x C_179 has
equal C-row sums, vanishes on the C-zero fiber, and has constant
inversion-complement off that fiber.
```

That is equivalent to the `632` Fourier equations and therefore to membership
in the rank-`621` admissible span.

The Lean companion records the formal handoff from these three identities to
the existing verifier pipeline:

```text
p24/lean/TraceGcdDualConditionsValueSideGate.lean
```

This is likely the best packet-facing version of the missing theorem.  It
separates three arithmetic inputs:

```text
1. row-sum descent / C/E-centering;
2. section-aware C-zero fiber vanishing;
3. anti-Hermitian or product-formula complement law.
```

## Check

```text
PYTHONPYCACHEPREFIX=/private/tmp/codex-pycache PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH=p24 python3 \
  p24/trace_gcd_fixed_frequency_p24_dual_conditions_value_side_gate.py

lean p24/lean/TraceGcdDualConditionsValueSideGate.lean
```

Observed:

```text
value_dual_equivalence_random_checks=3/3
value_dual_rank_matches=3/3
admissible_carries_satisfy_value_conditions=3/3
random_controls_reject_both=3/3
```

No p24 class set or CM root enumeration is used.
