# P25 Lane B: Robert KSY Normalized-y Theorem Source Screen

Updated: 2026-06-13 16:25 PDT

## Purpose

This is a primary-source screen for the current theorem interface.  It does
not prove the missing identity; it ranks source families against the p25 finite
target:

```text
prod_A y(A)/y(A+T) = theta2^-1
prod_A y(A+T)/y(A) = theta2
```

with a true `K` trace, a short non-subgroup `D` segment, and the nontrivial
`T` edge.

## Continue

### Sprang / Kronecker D=2

Source:

```text
https://arxiv.org/pdf/1802.04996
```

Why it survives:

```text
D=2 is available at the Kronecker-section / elliptic-polylogarithm
differential level, unlike the ordinary Kato theta_D unit route.
```

P25 transfer:

```text
Best target for a D=2 differential or value-level theta2 identity,
especially if it can be paired with the period-156 telescoping context.
```

First debt:

```text
A dlog/Eisenstein-class formula alone is not enough. It must emit
theta2/theta2^-1 for the exact normalized-y product over K, D, and T.
```

### Kubert-Lang Siegel Exponent Matrix

Sources:

```text
https://link.springer.com/chapter/10.1007/978-1-4757-1741-9_2
https://link.springer.com/chapter/10.1007/978-1-4757-1741-9_4
```

Why it survives:

```text
Siegel-unit products are the natural modular-unit language for exact divisor
payloads.
```

P25 transfer:

```text
Continue only as an exponent-matrix search whose divisor is the exact six-cell
packet or exact 300-term theta2/theta2^-1 payload.
```

First debt:

```text
Generic modular-unit generation is too broad. The exponent matrix must satisfy
the p25 packet, T edge, and period-156 certificate constraints.
```

### Koo-Shin-Yoon Normalized wp-prime / y Route

Source:

```text
https://mathsci.kaist.ac.kr/bk21/morgue/research_report_pdf/09-20.pdf
```

Why it survives:

```text
The route uses normalized wp-prime / y-coordinate singular values and
Siegel-Ramachandra-style class-field invariants.
```

P25 transfer:

```text
This keeps the y/differential sign-breaking route alive because the current
finite product is built from normalized-y factors.
```

First debt:

```text
Class-field generation is not a payload. A candidate still must land on
y(A)/y(A+T), T=(2,113), and the period-156 theta2 certificate.
```

## Conditional

### Kubert-Lang Siegel-Robert Class-field Units

Source:

```text
https://link.springer.com/chapter/10.1007/978-1-4757-1741-9_11
```

Why it is conditional:

```text
The chapter explicitly works with powers of modular-function values to avoid
root ambiguities. That matches our value-level boundary.
```

P25 transfer:

```text
ambient 780 denominator: gcd(4^780 - 1, p - 1) = 11
support-period 156 denominator: gcd(4^156 - 1, p - 1) = 1
```

Continue only if:

```text
the theorem supplies period-156 fixedness/telescoping context or explicit
branch/root selection.
```

## Kill As Direct Shortcuts

### Ordinary Kato theta_D

Source:

```text
https://www.dpmms.cam.ac.uk/~ajs1005/preprints/euler.pdf
```

Reason:

```text
Scholl's Kato theta_D theorem assumes (6,D)=1. It is the right odd-D control,
but D=2 is outside the direct theorem.
```

### Literal Robert Subgroup Support

Source:

```text
https://www.dpmms.cam.ac.uk/~ajs1005/preprints/euler.pdf
```

Reason:

```text
Robert's finite-subgroup generalization uses subgroup divisors of order prime
to 6. The p25 D_segment is not subgroup support:

raw order(D)     = 12675
visible order(D) = 507
3D               = (66,9)
visible 3D       = (0,9)
```

## Local Gate

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_theorem_source_screen_gate.py
```

Expected marker:

```text
robert_ksy_theta2_theorem_source_screen_rows=1/1
```

## Next Probe

Try a Sprang/Kronecker `D=2` differential or value identity and force it
through the period-156 theta2 interface.  In parallel, search for a Kubert-Lang
Siegel exponent matrix whose divisor is the exact six-cell source packet or
the exact 300-term theta2 payload.
