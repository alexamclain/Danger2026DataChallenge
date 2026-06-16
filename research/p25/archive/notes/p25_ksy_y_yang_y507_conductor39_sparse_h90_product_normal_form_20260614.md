# P25 KSY-y: Sparse H90 Product Normal Form

Updated: 2026-06-14 11:15 PDT

## Purpose

The legal support-`156` Yang-lift potentials are now normalized as explicit
products.  This turns the value-side target into one canonical `78/78`
Yang-fiber product, up to the conductor-`39` doubling subgroup.

## Canonical Product

Let

```text
P0 = {7, 17, 23, 34, 37, 38}
N0 = {4, 8, 10, 11, 20, 25}
```

The canonical lifted sparse potential is:

```text
H0 = 6 * (
  sum_{a in P0, k=0..12} [a + 39k]
  -
  sum_{b in N0, k=0..12} [b + 39k]
)
```

Equivalently, as a product target:

```text
prod_{a in P0, k=0..12} E_{a+39k}^6
/
prod_{b in N0, k=0..12} E_{b+39k}^6
```

This has:

```text
positive lift count = 78
negative lift count = 78
support             = 156
coefficient counts  = (-6,78), (6,78)
boundary            = (1 - Frob_p)H0 = Norm_156(Y_507)
```

## Orbit

The conductor-`39` doubling subgroup is:

```text
<2> = (1, 2, 4, 8, 16, 32, 25, 11, 22, 5, 10, 20)
```

The canonical product has stabilizer:

```text
{1, 16, 22}
```

So the four legal sparse support-`156` potentials are exactly the four
translates represented by:

```text
1, 2, 4, 8
```

Rows:

```text
multiplier 1 -> legal_sparse_selector_0
multiplier 2 -> legal_sparse_selector_2
multiplier 4 -> legal_sparse_selector_3
multiplier 8 -> legal_sparse_selector_1
```

## Verdict

The value-side theorem target can now be phrased as:

```text
prove a finite-field value/divisor identity for the canonical 78-over-78
Yang-fiber product H0, or any <2>-translate of it
```

This is still not a DANGER3 certificate.  It is the smallest current legal
product normal form feeding the period-`156` Hilbert-90 route.

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_yang_y507_conductor39_sparse_h90_product_normal_form_gate.py
```

Marker:

```text
ksy_y_yang_y507_conductor39_sparse_h90_product_normal_form_rows=1/1
```
