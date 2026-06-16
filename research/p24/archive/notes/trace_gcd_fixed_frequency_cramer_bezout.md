# Fixed-Frequency Cramer/Bezout Certificate

Date: 2026-06-06

## Point

The cyclic syzygy target can be made more certificate-like.  Instead of
constructing coefficient sections by division after evaluating the seven fixed
frequencies, prove a Cramer identity inside

```text
R_7 = F_p[y] / (y^7 - 1).
```

Let

```text
P_2(y), P_3(y), P_5(y), P_6(y)
```

be the four fixed-frequency prefix vector sections and `T(y)` the tail
section.  Choose an intrinsic `4 x 4` prefix minor and call its determinant
`D(y)`.  The desired certificate surface is:

```text
D(y) T(y)
  = N_2(y) P_2(y)
  + N_3(y) P_3(y)
  + N_5(y) P_5(y)
  + N_6(y) P_6(y)
```

in `R_7 tensor L`, together with:

```text
D(y) in R_7^*.
```

The unit condition is equivalent to a Bezout identity:

```text
A(y) D(y) + B(y) (y^7 - 1) = 1.
```

Then `C_j(y)=A(y)N_j(y)` gives the earlier cyclic syzygy.

## Why This Is Sharper

Pointwise interpolation is automatic because `p = 1 mod 7`; it is not
arithmetic evidence.  The Cramer/Bezout form separates the two proof inputs:

```text
1. D(y) is a p-unit denominator, i.e. the fixed prefix Plucker gate;
2. the full vector identity holds before division.
```

This also prevents a projected-only proof from cheating.  A Cramer identity on
the pivot coordinates is tautological; the non-pivot coordinates are where the
tail-in-prefix content lives.

## Check

The finite gate is:

```text
p24/trace_gcd_fixed_frequency_cramer_bezout_toy.py
```

It checks:

```text
valid Cramer/Bezout package
  => cyclic relation section;

zero-divisor denominator
  => reject division even if pointwise relations partially exist;

corrupted non-pivot tail coordinate
  => pivot Cramer equations still hold but full vector identity fails.
```

## Current Arithmetic Target

Construct the intrinsic sections:

```text
D,N_2,N_3,N_5,N_6 in F_p[y]/(y^7-1)
```

from the CM/Lang fixed-frequency Hermitian packet.  The denominator `D` should
be one of the fixed-frequency prefix Plucker sections, and its Bezout inverse
should be proved by the same local p-unit theorem used for fixed ordinary
prefix rank.
