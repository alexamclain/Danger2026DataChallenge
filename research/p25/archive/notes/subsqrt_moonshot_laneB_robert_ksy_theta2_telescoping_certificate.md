# P25 Lane B: theta2 Telescoping Certificate Skeleton

Updated: 2026-06-13 14:55 PDT

## Purpose

The support-period resolvent gives a `46800`-term expanded finite filter for
recovering the bridge from `theta2`.  For a compact KSY/theta hit, the verifier
does not need to expand that filter first.  It can certify the two identities

```text
theta2 = (4 - [2]) * bridge
[2]^156 bridge = bridge
```

and then the resolvent numerator telescopes to `(4^156 - 1) * bridge`.

## Result

```text
compact recipe center_base        = (44, 166)
compact recipe half_shift         = (56, 28)
support period                    = 156
route center support              = 75
bridge support                    = 150
theta2 support                    = 300

theta2 = 4*bridge - [2]bridge     = true
[2]^156 bridge = bridge           = true
[2]^156 theta2 = theta2           = true
proper divisors of 156 fix theta2 = false

denominator bit length            = 312
gcd(4^156 - 1, p25 - 1)           = 1
compact linear cell check budget  = 975
expanded resolvent term budget    = 46800
budget improvement factor         = 48
```

The touched doubling-orbit skeleton is small:

```text
touched doubling orbits           = 27
ambient orbit lengths             = 15 orbits of length 156, 12 of length 780
bridge points per orbit           = 15 orbits with 2 points, 12 with 10
theta2 points per orbit           = 15 orbits with 4 points, 12 with 20
global [2]^156 is identity        = false
support [2]^156 is identity       = true
```

## Local Gate

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_telescoping_certificate_gate.py
```

Expected marker:

```text
robert_ksy_theta2_telescoping_certificate_rows=1/1
```

## Interpretation

This is the best current compact checkpoint for the KSY/theta moonshot.  If a
theorem or hand derivation emits the compact KSY theta2 object, the finite
bridge recovery can be checked by a telescoping certificate before falling back
to the full `46800`-term resolvent expansion.

This is not yet an arithmetic theta2 producer.  It is a verifier/certificate
skeleton: it amortizes the p24-derived bridge structure and turns the p25
finite deconvolution into two compact identities plus a period check.
