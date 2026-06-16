# Relative Product Too Strong Scan

This note records a small-CM correction to the stronger product/norm
certificate target.

## Background

For a relative character `a`, write

```text
P_u(a) = sum_k zeta_n^(a*k) j_{u+m*k}.
```

The exact harmful event is

```text
P_u(a) = 0 for every u.
```

A stronger sufficient certificate is the relative product

```text
prod_u P_u(a) != 0.
```

If the product is nonzero then no individual fiber vanishes, so harmful
vanishing is impossible.  But this certificate is stronger than needed.

## Larger natural scan

I ran:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/natural_relative_resolvent_scan.py \
  --max-cases 160 --min-h 12 --max-h 120 --max-abs-D 40000 \
  --max-quotients 6 --q-stop 400000 --summary-only
```

Output:

```text
rows=160
quotient_rows=520
relative_characters_tested=2150
relative_fibers_tested=7337
harmful_a_total=0
individual_zero_fiber_total=1
expected_random_zero_fibers=2.908526
quotient_rows_with_all_individual_fibers_nonzero=519
all_equivalences_verified=1
```

The unique individual-zero row was:

```text
D=-1336
q=1777
ell=5
h=12
m=2
n=6
harmful_a_count=0
individual_zero_fiber_count=1
min_nonzero_fibers=1
```

So a natural CM relative fiber can vanish individually even though the harmful
all-fiber event does not occur.

For that row, the zero occurs at `a=1`:

```text
relative_fibers=[1400, 0]
ordinary_pairing=1746
hermitian=1746
```

The Hermitian scalar is nonzero, so the preferred scalar still certifies this
packet even though the product certificate fails.

## Consequence

This does not hurt the exact relative-content target:

```text
gcd(f_a, J_0, ..., J_{m-1}) = 1.
```

It does rule out using individual-fiber product nonvanishing as a universal
CM theorem.  For p24 it might still hold accidentally or under extra
hypotheses, but it is now clearly the wrong general statement to try to prove.

The preferred scalar target remains the Hermitian packet p-unit, because the
packetized scan has found no Hermitian packet zeros even in regimes where
ordinary/product-like scalar certificates can fail.

## Prime-Recovery Refinement

The counterexample above has composite recovery length:

```text
n = 6.
```

The third p24 target has prime recovery length:

```text
n = 3107441.
```

The refined product theorem is therefore recorded separately in:

```text
p24/prime_relative_normality_candidate.md
```

The diagnostic

```text
p24/relative_normality_prime_composite_scan.py
```

tests primitive relative packets and separates prime from composite `n`.
In a bounded mixed run with linear packets included it found:

```text
prime_packet_rows=301
composite_packet_rows=350
prime_coord_zero_packets=0
composite_coord_zero_packets=2
prime_hermitian_zero_packets=0
composite_hermitian_zero_packets=0
```

This was evidence for the prime-order relative normality version, but it was
later superseded by a wider selected-prime scan:

```text
p24/prime_relative_normality_counterexample.md

D=-956 q=3307 h=15 m=5 n=3 deg=1
coord_zero=1 content_zero=0 hermitian_zero=0
```

Thus the broad prime-order product theorem is also false.  It remains a
p24-specific sufficient target only.

With selected-origin rotation enabled, a moderate mixed run found:

```text
prime_packet_rows=153
composite_packet_rows=160
prime_packets_with_some_origin_coord_zero=0
composite_packets_with_some_origin_coord_zero=1
selected_origin_tests=5861
selected_origin_coord_zeros=16
expected_prime_origin_coord_zeros_random=6.055355
expected_composite_origin_coord_zeros_random=4.777915
```

This bounded selected-prime rotation test should now be read as historical
small-window evidence only; it did not sample the later prime-`n`
counterexample row.

Correction: later algebra shows that origin rotations are not independent for
coordinate/resultant vanishing.  See:

```text
p24/relative_origin_shift_invariance.md
```

The origin-rotation run remains a consistency check, explaining why the
composite coordinate failure persists across origins.  The random expectation
that multiplies by origin count should not be treated as independent evidence.

The companion inspector

```text
p24/relative_zero_structure_inspector.py
```

shows that the observed composite coordinate-zero fibers are not simply
proper-period pullbacks.  The failures are primitive linear root-of-unity
cancellations in the finite field.  Therefore the prime-order proof cannot be
just "prime `n` has no proper divisor"; it must prove a genuine selected-prime
anti-cancellation or p-unit statement for the relative normality resultant.
