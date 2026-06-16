# Lang Trace-GCD Sequence Complexity

Date: 2026-06-05

This note tests the reduced right-translation determinant sequence from the
origin-covariance theorem:

```text
Delta_i(t),   t mod right.
```

If this sequence has low linear complexity, the origin product may be smaller
than the raw right-cycle length.

## Tool

Added:

```text
p24/lang_trace_gcd_sequence_complexity.py
```

It reuses the actual-CM trace-gcd origin audit, extracts the beta-invariant
right sequence, and reports:

```text
zero count,
product mod q,
Berlekamp-Massey complexity on two periods,
connection polynomial,
whether the connection divides X^right - 1.
```

## Pinned Nontrivial Row

Command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/lang_trace_gcd_sequence_complexity.py \
  --only-D -13319 --only-q 13463 --q-start 13463 --q-stop 13464 \
  --only-m 28 --only-left 4 --only-right 7 \
  --include-linear --max-factor-degree 8 --max-extension-degree 8 \
  --min-left-orbit-len 2 --require-square-tail
```

Output summary:

```text
D=-13319, q=13463, h=140, m=28, n=5, pair=(4,7)
right_lengths=[3,3]
```

For `omitted=0`:

```text
right_sequence_length=7
right_sequence_zero_count=0
right_sequence_distinct_count=7
right_sequence_product_mod_q=6352
right_sequence_linear_complexity_two_periods=3
right_sequence_connection=[1, 6790, 6789, 13462]
right_sequence_connection_divides_xn_minus_1=1
right_sequence_frobenius_compatibility_mismatches=6
```

The connection polynomial is:

```text
x^3 - 6673*x^2 - 6674*x - 1.
```

For `omitted=1`:

```text
right_sequence_length=7
right_sequence_zero_count=0
right_sequence_distinct_count=7
right_sequence_product_mod_q=6639
right_sequence_linear_complexity_two_periods=3
right_sequence_connection=[1, 6674, 6673, 13462]
right_sequence_connection_divides_xn_minus_1=1
right_sequence_frobenius_compatibility_mismatches=6
```

The connection polynomial is:

```text
x^3 + 6674*x^2 + 6673*x - 1.
```

Thus each determinant sequence is supported on a single degree-3 Frobenius
factor of `X^7-1`, and the two omitted blocks land on conjugate degree-3
factors.  The raw value sequence is not Frobenius-invariant, so the
interpolant should be treated as a splitting-field object whose orbit products
are base-field valued, not as a base-coefficient polynomial.

## Degenerate Control

Command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/lang_trace_gcd_sequence_complexity.py \
  --only-D -10919 --only-q 11243 --q-start 11243 --q-stop 11244 \
  --only-m 12 --only-left 4 --only-right 4 \
  --include-linear --max-factor-degree 20 --max-extension-degree 8 \
  --min-left-orbit-len 2 --require-square-tail
```

reported a constant sequence:

```text
right_sequence_length=4
right_sequence_zero_count=0
right_sequence_distinct_count=1
right_sequence_linear_complexity_two_periods=1
connection=x-1.
```

## p24 Consequence

For p24, the right component is `211` and:

```text
ord_211(p)=35.
```

The raw origin product has `211` factors, but the small nontrivial row suggests
the determinant sequence may be supported on one degree-35 Frobenius factor of
`X^211-1`.

The sharpened theorem candidate is:

```text
Delta_i(t) has right spectral support in one Frobenius orbit O_i
of size 35,
and prod_{t mod 211} Delta_i(t) != 0 mod p.
```

Equivalently, there should be an element `A_i` in the degree-35 right factor
such that:

```text
Delta_i(t) = Tr_{F_{p^35}/F_p}(A_i * zeta_211^t)
```

up to a nonzero scalar/unit convention.  The p-unit theorem then becomes a
Gauss-period norm/product nonvanishing statement for one degree-35 component,
not an arbitrary 211-term determinant sequence.

This is not yet a proof.  It is the first evidence that the 211-product target
itself may have a fixed-degree spectral collapse compatible with the right
Frobenius orbit structure.

## Exterior-Support Caveat

Added:

```text
p24/lang_trace_gcd_exterior_support.py
```

For the small pinned row:

```text
PYTHONDONTWRITEBYTECODE=1 python3 \
  p24/lang_trace_gcd_exterior_support.py --p 13463 --right 7 --tail 2
```

reported:

```text
orbit_len=3
k=2 repeated_sum_size=6 distinct_subset_sum_size=3
```

So the degree-3 recurrence in the `2 x 2` toy determinant is compatible with
the exterior square of a degree-3 right orbit.  It is useful, but it is not by
itself evidence of a new p24 collapse.

For p24:

```text
PYTHONDONTWRITEBYTECODE=1 python3 p24/lang_trace_gcd_exterior_support.py
```

reported:

```text
right=211
orbit_len=35
tail=16
k=1 distinct_subset_sum_size=35
k=2 distinct_subset_sum_size=210
k=3 distinct_subset_sum_size=211
...
k=16 distinct_subset_sum_size=211
```

Thus a generic `16 x 16` exterior coordinate under the right action has full
right spectral support.  If the p24 trace-gcd determinant sequence collapses
to one degree-35 factor, that collapse must come from the special prefix
kernel / trace-gcd geometry, not from representation theory alone.

## Pluecker Spectral Identity

The precise Pluecker/Fourier identity for this determinant sequence is
recorded in:

```text
p24/lang_trace_gcd_plucker_spectral_boundary.md
p24/lang_trace_gcd_plucker_spectral_toy.py
p24/lang_trace_gcd_spectral_scan_boundary.md
p24/lang_trace_gcd_spectral_scan.py
```

It states:

```text
Delta(t)
  = sum_{I subset O, |I|=k}
      det(P_I) det(A_I) zeta^(t * sum(I)).
```

Thus the sequence support is controlled by subset sums of the right Frobenius
orbit weighted by the two Pluecker vectors attached to the coordinate window
and the transported tail image.
