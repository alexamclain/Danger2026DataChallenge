# P25 Lane B: Robert KSY Kubert-Lang Raw K-Trace Reflection

Updated: 2026-06-13 17:00 PDT

## Purpose

The quotient reflection bridge proves `T=-2C` in `C_3 x C_169`.  The actual
KSY normalized-y product is raw: it lives in `C_75 x C_169` and includes the
forced 25-point `K` trace.

This gate checks that the quotient reflection lifts correctly to the raw source
product.

## Raw Law

With:

```text
base = (25,25)
D    = (22,3)
K    = (57,0)
T    = (38,113)
C    = base + D = (47,28)
```

we get:

```text
-2C       = (56,113)
T - (-2C) = (57,0) = K
```

So upstairs:

```text
T = -2C + K
```

Also:

```text
T/2      = (19,141)
-C       = (28,141)
T/2 + C  = (66,0) = 13K
```

The half-edge is therefore also correct only modulo the `K` trace.

## Trace Absorption

For centers

```text
A = C + jD + kK,  j in {-1,0,1}, k in {0,...,24}
```

we have:

```text
A + T = -C + jD + (k+1)K
```

while the inverse of the reflected numerator is:

```text
-(C - jD + k'K) = -C + jD - k'K
```

Choosing `k' = -k-1 mod 25` matches the denominators.  Thus the raw KSY
`T`-edge packet and the raw anti-invariant inversion-pair packet are identical
after the full `K` trace.

Measured payloads:

```text
center support                    = 75
raw source packet support          = 150
normalized-y theta2 footprint      = 300
kernel-shifted -2C representatives = 25/25 accepted
```

Controls reject:

```text
sparse K section
truncated D segment
T plus D
T plus C-axis step
T plus right-axis step
```

## Local Gate

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_raw_ktrace_reflection_gate.py
```

Expected marker:

```text
robert_ksy_theta2_kubert_lang_raw_ktrace_reflection_rows=1/1
```

## Interpretation

This moves the reflection bridge from quotient bookkeeping to the actual raw
KSY product.  A theorem source may target anti-invariant pair quotients over
the symmetric segment, but the arithmetic proof must still realize the full
`K` trace.  Without the trace, the raw reflection law fails.
