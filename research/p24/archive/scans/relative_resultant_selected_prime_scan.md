# Relative Resultant Selected-Prime Scan

This note records direct bounded scans for the prime relative-normality
candidate.  The first window was encouraging, but a later wider
multi-splitting window found a prime-`n` coordinate failure.  The broad
prime-relative-normality theorem is therefore false.

## Target

For `h=m*n`, a relative fiber is

```text
J_u(X) = sum_k j_{u+m*k} X^k.
```

For p24,

```text
n = 3107441
```

is prime, so every nontrivial relative character is primitive.  The stronger
coordinate theorem is:

```text
Res(Phi_n, J_u) != 0 mod p      for all 0 <= u < m.
```

This implies the exact packet-content theorem but is stronger than necessary.

The scan in

```text
p24/relative_resultant_selected_prime_scan.py
```

tests the selected-prime shape by checking whether any `J_u mod f` vanishes
for packet factors `f | Phi_n`, across multiple splitting primes.

Origin rotations are deterministic symmetries for this coordinate-zero
condition; see:

```text
p24/relative_origin_shift_invariance.md
```

They are useful consistency checks but should not be counted as independent
selected-prime tests.

## Multi-Splitting Window

Command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/relative_resultant_selected_prime_scan.py \
  --max-cases 30 --min-h 12 --max-h 100 --max-abs-D 20000 \
  --max-prime-quotients 5 --max-composite-quotients 5 \
  --min-n 3 --max-n 100 --q-stop 200000 \
  --max-splitting-primes 3 --include-linear --summary-only
```

Output:

```text
packet_rows=361
prime_packet_rows=204
composite_packet_rows=157
coord_zero_packets=0
prime_coord_zero_packets=0
composite_coord_zero_packets=0
content_zero_packets=0
expected_prime_coord_zero_packets_random=0.517802
expected_composite_coord_zero_packets_random=0.274960
```

This first zero count was cleaner than the naive random coordinate-zero model.
It was evidence only, and the broader scan below breaks the broad theorem.

## Wider Prime Counterexample

Command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/relative_resultant_selected_prime_scan.py \
  --max-cases 90 --min-h 12 --max-h 180 --max-abs-D 60000 \
  --max-prime-quotients 12 --max-composite-quotients 8 \
  --min-n 3 --max-n 180 --q-stop 700000 \
  --max-splitting-primes 10 --include-linear --summary-only
```

Output:

```text
packet_rows=3842
prime_packet_rows=1816
composite_packet_rows=2026
coord_zero_packets=5
prime_coord_zero_packets=1
composite_coord_zero_packets=4
content_zero_packets=0
expected_prime_coord_zero_packets_random=2.355173
expected_composite_coord_zero_packets_random=2.071820

prime_failure_samples:
  D=-956 q=3307 h=15 m=5 n=3 deg=1 origin=0 coord_zero=1
```

Pinned reproduction:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/relative_normality_prime_composite_scan.py \
  --only-D -956 --min-h 12 --max-h 20 \
  --max-prime-quotients 8 --max-composite-quotients 8 \
  --min-n 3 --max-n 12 --q-start 3307 --q-stop 3308 \
  --include-linear
```

Output:

```text
D=-956 q=3307 ell=5 h=15 m=5 n=3 n_prime=1 deg=1
coord_zero=1 content_zero=0 hermitian_zero=0
```

The inspector shows the vanished length-3 fiber has no proper period:

```text
p24/relative_zero_structure_inspector.py --D -956 \
  --q-start 3307 --q-stop 3308 --min-n 3 --max-n 12

m=5 n=3 n_prime=1 deg=1 roots=[57] shift=0 u=2
proper_periods=[] coeffs=[615,1471,658]
```

The full writeup is:

```text
p24/prime_relative_normality_counterexample.md
```

## Composite Control

The pinned product-failure row still fails:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/relative_resultant_selected_prime_scan.py \
  --only-D -1336 --min-h 12 --max-h 20 \
  --max-prime-quotients 8 --max-composite-quotients 8 \
  --min-n 3 --max-n 12 --q-start 1777 --q-stop 1778 \
  --include-linear --scan-origins --max-origins 12
```

Output summary:

```text
packet_rows=72
unique_packet_rows_ignoring_origin=6
prime_packet_rows=24
composite_packet_rows=48
coord_zero_packets=12
unique_coord_zero_packets_ignoring_origin=1
distinguished_zero_packets=6
prime_coord_zero_packets=0
composite_coord_zero_packets=12
content_zero_packets=0
```

All failures are the known composite `n=6` coordinate-zero packet repeated by
origin rotation.  The distinguished `u=0` coordinate is zero on half of the
origins, reflecting that origin shifts permute the two quotient coordinates.
Exact content remains nonzero.

The companion shape diagnostic

```text
p24/relative_packet_factor_shape_scan.py
```

shows that these composite coordinate-zero packets are not low-complexity
fibers.  For the pinned `D=-1336` row, all twelve origin-rotated hits have

```text
BM = n-1,
proper_periods = [],
trivial_zero = 0,
six distinct coefficients.
```

The `D=-656` and `D=-1028` composite `n=4` hits have the same shape:
near-full BM, no proper period, and no trivial zero.  Thus composite
failures are genuine one-factor cyclic-code vanishings, not imprimitive
sequence repetitions.

## Interpretation

The hierarchy now looks like:

```text
exact content:
  no failures observed;

prime relative resultants:
  false as a broad theorem, with a prime n=3 coordinate-zero row;

composite relative resultants:
  false in natural small CM rows;

ordinary/Hermitian scalar:
  useful sufficient certificates, with Hermitian empirically strongest.
```

For p24, the prime recovery length still leaves the relative-resultant
statement as a valid sufficient target:

```text
prove selected-prime p-unitness of Res(Phi_3107441, J_u)
for all 66254 quotient coordinates.
```

It remains stronger than needed and still lacks a p-adic proof.  The new
counterexample means such a proof would have to use p24-specific arithmetic,
not prime-ness of the recovery length alone.
