# Lang Trace-GCD Spectral Scan Boundary

Date: 2026-06-05

This note audits the strongest spectral-collapse hope in the reduced
trace-GCD origin product.

## Question

The representative trace-GCD product reduces to:

```text
Delta_i(t) = det(P V_t A),       t mod right.
```

The pinned `(4,7)` row had a right sequence of length `7` but linear
complexity `3`, suggesting support on one Frobenius orbit.  For p24, the
analogue would be:

```text
right = 211
ord_211(p) = 35
Delta_i(t) supported on one degree-35 orbit.
```

That would turn the `211`-term product into a Gauss-period norm for one
degree-35 component.

## Scan Tool

I added:

```text
p24/lang_trace_gcd_spectral_scan.py
```

It scans small actual-CM trace-GCD origin rows, reduces by right component,
and reports the Berlekamp-Massey complexity of `Delta_i(t)` over two periods.

Reproduction of the known nontrivial row:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/lang_trace_gcd_spectral_scan.py \
  --only-D -13319 --only-q 13463 --q-start 13463 --q-stop 13464 \
  --only-m 28 --only-left 4 --only-right 7 \
  --include-linear --max-factor-degree 8 --max-extension-degree 8 \
  --min-left-orbit-len 2 --require-square-tail --require-prime-right \
  --min-tail-len 1 --max-rows 8
```

reported:

```text
omitted=0 tail=2 K=2 zeros=0 distinct=7 product=6352
  right_order=3 complexity=3 single_orbit=1

omitted=1 tail=2 K=2 zeros=0 distinct=7 product=6639
  right_order=3 complexity=3 single_orbit=1
```

A modest broader scan found more right-`7` nontrivial rows, all with
`complexity=3`, plus several degenerate `tail=0` rows.  A targeted right-`11`
search was stopped after it became a row-discovery CPU search rather than a
quick theorem filter.

## Exterior-Support Check

The important correction is that the right-`7` behavior is compatible with
plain exterior-power support.  For `right=7`, `orbit_len=3`, `tail=2`, the
distinct subset sums have size `3`.

For right `11`, exterior support fills the group immediately:

```text
PYTHONDONTWRITEBYTECODE=1 python3 \
  p24/lang_trace_gcd_exterior_support.py --right 11 --tail 2

right=11 orbit_len=10 tail=2
k=1 distinct_subset_sum_size=10
k=2 distinct_subset_sum_size=11
```

For p24:

```text
PYTHONDONTWRITEBYTECODE=1 python3 p24/lang_trace_gcd_exterior_support.py

right=211 orbit_len=35 tail=16
k=1 distinct_subset_sum_size=35
k=2 distinct_subset_sum_size=210
k=3 distinct_subset_sum_size=211
...
k=16 distinct_subset_sum_size=211
```

Thus a p24 degree-35 spectral collapse is not forced by the right action or
by Cauchy-Binet.  It would require special arithmetic cancellation in the
Pluecker coefficients:

```text
c_s =
  sum_{I subset O, |I|=16, sum(I)=s}
    det(P_I) det(A_I)
```

for all but one Frobenius orbit of exponents.

## Consequence

The current safe theorem target remains the direct right resultant:

```text
Res(Y^211 - 1, f_i(Y)) != 0 mod p,
```

or equivalently the `211` value/inverse certificate for the reduced
trace-GCD determinant sequence.

The stronger Gauss-period norm theorem is still possible, but the evidence is
weaker than the first right-`7` row suggested.  It should not be assumed unless
we find a genuine arithmetic reason for the Pluecker cancellations.
