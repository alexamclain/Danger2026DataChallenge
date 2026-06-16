# P25 Lane B: KSY Normalized-y Siegel Formula

Updated: 2026-06-13 18:44 PDT

## Purpose

This instantiates the Koo-Shin-Yoon normalized-y source as an exact p25 finite
payload, rather than a generic ray-class-field generator.

The formula is:

```text
y(Q) = -g(2Q) / g(Q)^4
```

For the accepted anti-invariant product over the `75` atoms
`A=C+jD+kK`, this becomes:

```text
y(A)/y(-A) = g(2A) * g(A)^-4 * g(-2A)^-1 * g(-A)^4
```

with:

```text
C = (47,28)
D = (22,3)
K = (57,0)
j in {-1,0,1}
k mod 25
```

## Result

The four Siegel layers are disjoint:

```text
g(2A)      coeff +1   support 75
g(A)^-4    coeff -4   support 75
g(-2A)^-1  coeff -1   support 75
g(-A)^4    coeff +4   support 75
```

Union:

```text
support = 300
coefficient counts = (-4,75), (-1,75), (1,75), (4,75)
```

This footprint exactly matches the accepted anti-invariant theta2-inverse
payload, passes the elementary KL exponent screen, and routes as:

```text
raw divisor/additive output -> theta2 inverse -> certificate path
raw value output            -> needs period-156 theta2 context
```

Generic KSY ray-class generation or a single y-value remains insufficient.

## Local Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_siegel_formula_gate.py
```

Expected marker:

```text
robert_ksy_theta2_kubert_lang_ksy_y_siegel_formula_rows=1/1
```

## Interpretation

The KSY lane is no longer just "maybe y-values help."  It now has a concrete
four-layer Siegel payload.  The remaining proof debt is challenge-legal
arithmetic production of this exact product, or period-156 context if the
theorem emits finite-field values.
