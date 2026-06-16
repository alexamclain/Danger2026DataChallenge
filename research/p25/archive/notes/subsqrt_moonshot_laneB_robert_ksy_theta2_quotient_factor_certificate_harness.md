# P25 Lane B: theta2 Quotient-Factor Certificate Harness

Updated: 2026-06-13 15:17 PDT

## Purpose

The factor-gauge normal form shows that the literal `base`, `K`, `D`, and `T`
coordinates are over-specified.  This harness accepts the quotient-level data:

```text
K = primitive generator of the size-25 right-mod-3 kernel
base, D, T in (C_75 / K) x C_169
```

and then lifts those classes to the existing factor-certificate verifier.

## Accepted Target

```text
base class = (1, 25)
D class    = (1, 3)
T class    = (2, 113)
K multiplier mod 25 = any primitive value
```

The default section lifts these to:

```text
base = (1, 25)
K    = (57 * k_multiplier mod 75, 0)
D    = (1, 3)
T    = (2, 113)
```

For `k_multiplier=1`, the derived KSY data are:

```text
H           = T / 2      = (1, 141)
center_base = base + H   = (2, 166)
half_shift  = -H         = (74, 28)
```

This is gauge-equivalent to the earlier literal representative and produces
the same bridge/theta2 object.

## Result

```text
target quotient data passes             = true
primitive K multiplier 2 passes          = true
nonprimitive K multiplier 5 fails        = true
wrong base quotient class fails          = true
wrong D quotient class fails             = true
wrong T quotient class fails             = true

factor support budget                    = 31
factor product support                    = 150
bridge contract reused                   = true
compact theta2 contracts reused          = true
period absorption reused                 = true
```

## Local Gate

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_quotient_factor_certificate_harness.py
```

Expected marker:

```text
robert_ksy_theta2_quotient_factor_certificate_harness_rows=1/1
```

## Candidate Mode

Positive target:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_quotient_factor_certificate_harness.py \
  --base-right-class 1 --base-c 25 \
  --d-right-class 1 --d-c 3 \
  --t-right-class 2 --t-c 113 \
  --k-multiplier 1
```

Expected marker:

```text
robert_ksy_theta2_quotient_factor_certificate_candidate_rows=1/1
```

## Interpretation

This is now the smallest concrete finite verifier intake for the KSY/theta
lane: three quotient classes plus a primitive `K` multiplier.  A theorem or
literature hit no longer needs to choose literal source-coordinate gauges.

The missing piece remains arithmetic: proving a challenge-legal producer for
this quotient factor/theta2 object.
