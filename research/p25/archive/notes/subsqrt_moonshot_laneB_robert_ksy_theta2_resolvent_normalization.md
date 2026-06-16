# P25 Lane B: theta2 Resolvent Normalization Gate

Updated: 2026-06-13 14:32 PDT

## Purpose

The theta2 resolvent gives the exact integer identity

```text
resolvent_numerator = (4^780 - 1) * bridge
```

This gate separates two different meanings of "divide by `4^780 - 1`":

- additive/divisor or linear coefficient normalization;
- multiplicative finite-field unit root extraction.

## Result

Additive/divisor normalization is finite and clean:

```text
denominator bit length              = 1560
denominator nonzero mod p25         = true
denominator nonzero mod 126751      = true
denominator nonzero mod 2029        = true
integer exact division recovers     = bridge
additive scaling mod p25 recovers   = bridge
additive scaling mod 126751 recovers= bridge
additive scaling mod 2029 recovers  = bridge
weighted exponent bit budget        = 182520000
weighted bit budget below sqrt(p)   = true
```

Multiplicative-unit normalization is not automatic:

```text
gcd(4^780 - 1, p25 - 1)     = 11
gcd(4^780 - 1, p25 + 1)     = 3
gcd(4^780 - 1, 126751 - 1)  = 12675
gcd(4^780 - 1, 2029 - 1)    = 507
```

So exponentiating by an inverse of `4^780 - 1` is not available on the relevant
multiplicative unit groups.

## Local Gate

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_resolvent_normalization_gate.py
```

Expected marker:

```text
robert_ksy_theta2_resolvent_normalization_rows=1/1
```

## Interpretation

The live KSY/theta2 target is now precise:

1. If the theorem emits a divisor/additive coefficient object, the resolvent
   normalization is legitimate and sub-sqrt.
2. If the theorem emits only multiplicative finite-field unit values, it must
   also supply a root/branch selection for the `4^780 - 1` denominator.

This is progress: the finite deconvolution is real, but the arithmetic
producer must land in the right category.
