# Hermitian Selected-Prime Zero Scan

This note records the bounded experiment suggested by the p-adic unit sidecar:
rotate small split CM cycles through all selected embedded roots and test
whether packet scalar zeros are isolated selected-prime events, full-orbit
events, or absent.

The script is:

```text
p24/hermitian_selected_prime_zero_scan.py
```

For a complete CM cycle and quotient `h=m*n`, it computes the packet scalar
polynomial modulo each Frobenius factor of `Phi_n`.  Rotating the cycle models
choosing a different prime above the same split rational prime.

## Hermitian scan

Run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/hermitian_selected_prime_zero_scan.py \
  --scalar hermitian --max-cases 40 --min-h 12 --max-h 90 \
  --max-abs-D 20000 --max-quotients 4 --min-n 5 \
  --q-stop 250000 --summary-only
```

Output:

```text
rows=40
packet_rows=74
selected_embedding_tests=1456
selected_embedding_zeros=0
origin0_zero_packets=0
packet_rows_with_any_selected_zero=0
packet_rows_with_full_orbit_zero=0
packet_rows_with_isolated_or_partial_zeros=0
selected_vs_packet_norm_mismatches=0
```

Low-order control on the same script:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/hermitian_selected_prime_zero_scan.py \
  --scalar hermitian --max-cases 40 --min-h 2 --max-h 30 \
  --max-abs-D 3000 --max-quotients 5 --min-n 2 \
  --q-stop 80000 --include-linear --summary-only
```

Output:

```text
rows=40
packet_rows=70
selected_embedding_tests=735
selected_embedding_zeros=0
packet_rows_with_any_selected_zero=0
selected_vs_packet_norm_mismatches=0
```

No Hermitian selected-prime zeros appeared.

## Ordinary energy control

Run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/hermitian_selected_prime_zero_scan.py \
  --scalar ordinary --max-cases 40 --min-h 2 --max-h 30 \
  --max-abs-D 3000 --max-quotients 5 --min-n 2 \
  --q-stop 80000 --include-linear --summary-only
```

Output:

```text
rows=40
packet_rows=70
selected_embedding_tests=735
selected_embedding_zeros=16
origin0_zero_packets=2
packet_rows_with_any_selected_zero=2
packet_rows_with_full_orbit_zero=2
packet_rows_with_isolated_or_partial_zeros=0
selected_vs_packet_norm_mismatches=0
```

The two ordinary-energy zero packets were full-orbit zeros:

```text
D=-304, q=101, h=6,  m=2, n=3, factor_degree=2, zero_count=6
D=-423, q=439, h=10, m=2, n=5, factor_degree=2, zero_count=10
```

Thus the selected-prime rotation scan is capable of detecting scalar
cancellation.  In these toy failures, ordinary energy vanishes for every
selected origin in the class orbit, while Hermitian energy remains nonzero.

## Interpretation

The finite identity

```text
selected scalar zero  <=>  packet norm zero
```

held in all tested rows:

```text
selected_vs_packet_norm_mismatches=0
```

The experiment does not prove the p24 Hermitian p-unit theorem.  It does
sharpen the evidence:

```text
ordinary energy can fail structurally by full-orbit cancellation;
Hermitian energy did not fail even after rotating selected primes;
no isolated selected-prime Hermitian zeros were found in the bounded window.
```

So the Hermitian packet p-unit statement remains the best scalar theorem
target, and the ordinary-energy route is again demoted to a weaker control.
