# L1 Zero-Lemma Boundary

This note records why the new partial-moment scalar

```text
L1 = M0 + P2 + P157 + P211
```

does not reopen the finite-field zero-lemma proof route.

## Two Zero Counts

For the p24 split

```text
h = m*n
m = 66254
n = 3107441
ord_n(p) = 388430
```

there are two different vanishing regimes.

Exact harmful content means

```text
P_u(a) = 0 for every K-origin u.
```

The `H`-eigenrelation then propagates one character trace around every
relative orbit, giving

```text
m*n
```

CM zeros, or `m*n*ord_n(p)` after Frobenius packet propagation.

A selected scalar zero, such as

```text
L1(a) = 0
```

at one selected `K`-origin, only propagates around the relative `H` orbit.
It gives

```text
n
```

CM zeros, or `n*ord_n(p)` after Frobenius packet propagation.

The Frobenius multiplier appears on both sides of a divisor-count argument,
so it cancels from the zero-lemma inequality.

## Current p24 Numbers

The best balanced split correspondence still has optimistic X0 pole proxy

```text
delta = 311808
```

from the class element

```text
2 * 463 * 223^(-1).
```

The exact harmful-content zero lemma would need

```text
delta < m = 66254,
```

but

```text
delta/m = 4.706252.
```

The selected-scalar zero lemma would need

```text
delta < 1.
```

This is impossible for any nonconstant modular/correspondence realization,
even before using the actual p24 value `delta=311808`.

## Why the Four Projections Do Not Help

`L1` is built from four tower-native scalar pieces:

```text
M0, P2, P157, P211.
```

If all four pieces vanished, their product would vanish on the same `H` orbit.
Counting multiplicity would multiply both the zero count and the pole degree
by four.  The strict divisor window would still require average pole degree
below one.

The axis support size

```text
368 = 1 + 1 + 156 + 210
```

is a number of `K`-character frequencies, not a number of forced `K`
translates.  A selected `L1` zero does not force its full `K`-translation
orbit to vanish.

## Audit

I added:

```text
p24/l1_zero_lemma_window_audit.py
```

Run:

```text
PYTHONDONTWRITEBYTECODE=1 python3 p24/l1_zero_lemma_window_audit.py
```

Output:

```text
frobenius_scalar_zero_count=n*ord=1207023307630
harmful_content_zero_count=h*ord=79970122223718020
current_delta=311808
current_delta_over_m=4.706252

exact_harmful_content_current_correspondence:
  forced_units=66254
  pole_units=311808
  strict_window=0

selected_L1_scalar_current_correspondence:
  forced_units=1
  pole_units=311808
  strict_window=0

selected_L1_scalar_ideal_nonconstant_minimum:
  forced_units=1
  pole_units=1
  strict_window=0

four_projection_family_product_ideal_minimum:
  forced_units=4
  pole_units=4
  strict_window=0
```

## Consequence

`L1` remains a strong certificate target because it is tower-native and
rescues the known small `M0` failures, but the proof cannot be a finite-field
divisor-count proof.

The remaining theorem must prove selected-origin p-unitness directly, or give
an explicit finite-field identity that selects the desired CM root/component
without relying on zero-count surplus.
