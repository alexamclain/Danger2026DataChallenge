# P25 Lane B: Robert KSY Kubert-Lang Raw Exponent Saturation

Updated: 2026-06-13 17:08 PDT

## Purpose

The anti-invariant normalized-y intake gives a compact finite theorem target:

```text
C = (47,28), K = (57,0), D = (22,3), orientation
```

This gate asks whether the raw Kubert-Lang exponent-matrix congruences at
level `12675` select that target.

They do not.

## Result

The target raw source packet passes:

```text
support             = 150
coefficient counts  = (-1,75), (1,75)
sum mod 12          = 0
quadratic right     = 0 mod 12675
quadratic c         = 0 mod 12675
quadratic mixed     = 0 mod 12675
```

But so do these controls:

```text
missing K       support 6
collapsed K     support 6, coefficients +/-25
truncated D     support 100
wrong D         support 150
shifted center  support 150
```

This is not mysterious.  At raw level, each anti-invariant atom has the form
`z^a - z^-a`, so the exponent sum and quadratic sums cancel automatically.

## Interpretation

The elementary KL/Siegel exponent congruence screen is necessary hygiene but
not a selector for the raw anti-invariant route.

The first real finite selector is still:

```text
full K trace
symmetric length-three D segment
exact center C=(47,28)
orientation
theta2/resolvent acceptance
```

## Local Gate

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_raw_exponent_saturation_gate.py
```

Expected marker:

```text
robert_ksy_theta2_kubert_lang_raw_exponent_saturation_rows=1/1
```

## Consequence

Reject any theorem claim that only verifies raw exponent sums for an
anti-invariant product.  It must also satisfy the finite intake geometry and
feed the accepted theta2 certificate path.
