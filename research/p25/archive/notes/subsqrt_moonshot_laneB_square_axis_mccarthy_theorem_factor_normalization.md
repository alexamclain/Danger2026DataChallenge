# p25 Lane B: McCarthy Theorem-Factor Normalization Scan

Updated: 2026-06-13 13:30 PDT

## Result

The easy theorem-side normalization escape hatch is killed.

After the auxiliary-prime probe showed that `R(138)^2029` lands in `mu_39`
only for the minimal auxiliary field, this scan tested whether the failure is
fixed by multiplying the quotient by simple factors already present in the
target-twist McCarthy formula.

Scanned factors:

```text
single factors, exponents +/-1,+/-2:
  denominator
  prefactor
  main_sum
  main_term
  lhs
  g(a0)
  g(-a0)
  g(a0)g(-a0)

small Gauss monomials, exponents -2..2:
  g(a0)^i g(-a0)^j g(0)^k

small theorem monomials, exponents -1..1:
  denominator^i prefactor^j g(a0)^k g(-a0)^l
```

Observed:

```text
raw quotient mu_39 hits across multipliers (1,4,7): (true, false, false)
single factors scanned = 32
single factors repairing all primes = 0
single factors repairing any prime = 0
Gauss monomials scanned = 124
Gauss monomials repairing all primes = 0
theorem monomials scanned = 80
theorem monomials repairing all primes = 0
```

The transformed difference itself remains stable:

```text
LHS(138) - main(138) = 2028
```

at all three auxiliary primes.

## Interpretation

The auxiliary-prime failure is not explained by forgetting one visible
denominator, prefactor, or Gauss-sum factor from the McCarthy theorem.  The
McCarthy exceptional delta remains a real theorem hook, but the powered
quotient still needs a nontrivial quotient-level cancellation, a natural
mod-extra-roots interpretation, or a direct endpoint identity.

## Local Gate

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_mccarthy_theorem_factor_normalization_scan.py
```

Observed:

```text
square_axis_mccarthy_theorem_factor_normalization_rows=1/1
```
