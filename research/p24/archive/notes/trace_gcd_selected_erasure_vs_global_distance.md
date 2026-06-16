# Trace-GCD Selected Erasure vs Global Distance

Date: 2026-06-06

This note separates the support theorem actually needed for the trace-GCD
certificate from a stronger global MDS/distance theorem.

## Selected Erasure

For the metric prefix-Gram route, fix a four-orbit prefix:

```text
S subset (Z/211Z)^*,        |S| = 140,
T_nonzero = (Z/211Z)^* \ S, |T_nonzero| = 70.
```

The exact support theorem is:

```text
no nonzero lambda in U_S has nonzero-right trace word supported inside
T_nonzero.
```

Equivalently:

```text
the restriction of the trace-word map to the selected 140 prefix coordinates
is injective on U_S.
```

This is the same finite obstruction as:

```text
U_S cap U_S^perp = 0,
```

and the same metric prefix Gram p-unit:

```text
det(A_S G^{-1} A_S^T) != 0.
```

## Global Distance Is Stronger

A sufficient but stronger theorem is:

```text
every nonzero trace word from U_S has nonzero-right Hamming support >= 71.
```

Equivalently, the prefix subcode behaves like an `[210,140,71]` MDS code.
This would imply the selected erasure theorem, but it asks for all
140-coordinate erasures to be good, not only the selected prefix erasure.

The distinction matters because the direct trace-GCD/Fitting theorem is
support-specific.  Proving global distance may be harder than proving the
selected p-unit.

## Toy Boundary

The finite separation is exercised by:

```text
p24/selected_erasure_vs_global_distance_toy.py
```

A typical run:

```text
PYTHONDONTWRITEBYTECODE=1 python3 \
  p24/selected_erasure_vs_global_distance_toy.py \
  --q 5 --n 10 --k 6 --trials 1000
```

finds many matrices where the selected `k` columns have full rank but some
other `k`-subset is singular.  Thus:

```text
selected erasure != global MDS distance.
```

## Consequence

The live p24 theorem should be stated in the selected-erasure/Fitting language:

```text
metric prefix Gram p-unit
or
selected support erasure avoidance
or
tail-on-kernel/Fitting p-unit.
```

Full scalar distance, MDS, LRS/MSRD, and cyclic uncertainty remain useful only
if they come with an arithmetic theorem identifying the actual CM trace family
with a code that has those stronger properties.
