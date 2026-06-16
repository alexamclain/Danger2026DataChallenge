# P25 Lane B: Robert KSY Kubert-Lang Exponent-Matrix Precheck

Updated: 2026-06-13 16:31 PDT

## Purpose

This gate tests the elementary Kubert-Lang/Siegel-unit exponent congruences
against the current p25 payloads.

For a Siegel-unit exponent matrix, the first necessary screen is:

```text
sum m(a) = 0 mod 12
sum m(a) a1^2 = 0 mod N
sum m(a) a2^2 = 0 mod N
sum m(a) a1*a2 = 0 mod N
```

This is not sufficient to prove a modular-unit producer.  It only says the
payload is not killed by the first congruence screen.

## Positive Congruence Results

### Six-cell source packet

Embed `C_3 x C_169` into `(Z/507)^2` by

```text
right_class -> 169 * right_class
c_log       -> 3 * c_log
```

The exact source packet passes:

```text
level               = 507
support             = 6
coefficient counts  = (-1,3), (1,3)
sum mod 12          = 0
quadratic right     = 0
quadratic c         = 0
quadratic mixed     = 0
```

### Theta2 / theta2 inverse footprint

Embed `C_75 x C_169` into `(Z/12675)^2` by

```text
right_log -> 169 * right_log
c_log     -> 75 * c_log
```

Both theta2 orientations pass:

```text
level               = 12675
support             = 300
coefficient counts  = (-4,75), (-1,75), (1,75), (4,75)
sum mod 12          = 0
quadratic right     = 0
quadratic c         = 0
quadratic mixed     = 0
```

## Controls

All fail the congruence screen:

```text
truncated D
wrong D
wrong T
positive-only packet
```

## Prime-power Projection

The `C_169` projection passes the prime-power congruence screen at level `169`,
but it loses the right classes and the nontrivial `T` edge.  It is therefore
finite-insufficient for p25.

```text
level 169 projection passes congruences = true
preserves right data                    = false
preserves T edge                        = false
accepted p25 finite payload             = false
```

## Local Gate

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_exponent_matrix_gate.py
```

Expected marker:

```text
robert_ksy_theta2_kubert_lang_exponent_matrix_rows=1/1
```

## Interpretation

The Kubert-Lang/Siegel route survives the first finite exponent-matrix screen.
The remaining debt is not the quadratic congruence; it is a theorem-legal
mixed-level lift or product that keeps the row-3 data, the `T=(2,113)` edge,
and the period-156 theta2 certificate.
