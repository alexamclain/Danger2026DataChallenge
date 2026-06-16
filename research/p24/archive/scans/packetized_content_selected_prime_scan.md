# Packetized Content Selected-Prime Scan

This is the exact-content follow-up to the prime-relative-normality
counterexample.

The product/resultant theorem failed because one coordinate can vanish:

```text
J_u mod f_a = 0.
```

The actual harmful packet condition is stronger:

```text
gcd(f_a, J_0, J_1, ..., J_{m-1}) != 1,
```

equivalently every coordinate vanishes modulo the same packet factor.

I added:

```text
p24/packetized_content_selected_prime_scan.py
```

It is the multi-splitting-prime companion to
`packetized_relative_content_scan.py`.  For each selected splitting prime it
records:

```text
coord_zero_count          product/resultant shortcut failure;
content_gcd_degree        exact harmful packet failure;
energy_zero/norm_zero     ordinary scalar failure;
hermitian_zero/norm_zero  Hermitian scalar failure.
```

## Pinned Prime-`n` Product Counterexample

The row from `prime_relative_normality_counterexample.md` has prime recovery
length and a coordinate failure:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/packetized_content_selected_prime_scan.py \
  --only-D -956 --min-h 12 --max-h 20 \
  --max-prime-quotients 8 --max-composite-quotients 8 \
  --min-n 3 --max-n 12 --q-start 3307 --q-stop 3308 \
  --include-linear
```

Output:

```text
D=-956 q=3307 ell=5 h=15 m=5 n=3 n_prime=1 deg=1
coord_zero=1 content_gcd_degree=0
energy_zero=0 energy_norm_zero=0
hermitian_zero=0 hermitian_norm_zero=0
```

With all origins:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/packetized_content_selected_prime_scan.py \
  --only-D -956 --min-h 12 --max-h 20 \
  --max-prime-quotients 8 --max-composite-quotients 8 \
  --min-n 3 --max-n 12 --q-start 3307 --q-stop 3308 \
  --include-linear --scan-origins --max-origins 15 --summary-only
```

Output:

```text
packet_rows=45
unique_packet_rows_ignoring_origin=3
coord_zero_packets=15
content_failures=0
energy_zero_packets=0
energy_norm_zero_packets=0
hermitian_zero_packets=0
hermitian_norm_zero_packets=0
```

Thus the product failure is not an exact-content failure and not a Hermitian
scalar failure.

## Multi-Splitting Stress Window

Command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/packetized_content_selected_prime_scan.py \
  --max-cases 24 --min-h 12 --max-h 120 --max-abs-D 25000 \
  --max-prime-quotients 8 --max-composite-quotients 6 \
  --min-n 3 --max-n 120 --q-stop 250000 \
  --max-splitting-primes 5 --include-linear --summary-only
```

Output:

```text
packet_rows=481
prime_packet_rows=278
composite_packet_rows=203
coord_zero_packets=0
content_failures=0
energy_zero_packets=0
energy_norm_zero_packets=0
hermitian_zero_packets=0
hermitian_norm_zero_packets=0
```

This smaller scalar window did not include the `D=-956, q=3307` coordinate
failure, but the pinned run above confirms that the scalar/content checks
survive exactly where product nonvanishing fails.

The broader product/resultant selected-prime scan already tested exact content
on a larger window because it reports `content_zero_packets`:

```text
p24/relative_resultant_selected_prime_scan.md

packet_rows=3842
prime_packet_rows=1816
composite_packet_rows=2026
coord_zero_packets=5
content_zero_packets=0
```

## Consequence

The current hierarchy is now cleaner:

```text
product coordinate theorem:
  false even for prime n;

exact packet content:
  no failures in the selected-prime windows, including the product failure row;

Hermitian scalar:
  no failures in the scalar window or pinned product failure row;

p24 proof gap:
  still requires a selected-prime p-unit/content theorem, not just prime n.
```

This makes exact content and the Hermitian scalar the preferred theorem
targets.  The product resultant remains useful only as a p24-specific
sufficient certificate if one can prove it by arithmetic special to the p24
CM order and selected prime.

