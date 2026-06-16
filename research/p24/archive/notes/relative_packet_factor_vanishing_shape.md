# Relative Packet-Factor Vanishing Shape

This note fixes a proof-hygiene point in the prime relative-normality target:
vanishing modulo one Frobenius packet factor is a cyclic-code condition, not
full primitive vanishing and not a hidden short recurrence.

## Exact Meaning

For

```text
h = m*n
J_u(X) = sum_k j_{u+m*k} X^k,
```

and a packet factor

```text
f_a | Phi_n,
```

the strong coordinate theorem fails when

```text
J_u mod f_a = 0.
```

Equivalently, the coefficient vector

```text
(j_u, j_{u+m}, ..., j_{u+m(n-1)})
```

lies in the cyclic code

```text
(f_a) / (X^n - 1).
```

This kills one Frobenius orbit of primitive characters.  It does **not** say
that the fiber is constant, that all primitive characters vanish, or that the
fiber has a proper period.  Only the stronger condition

```text
J_u mod Phi_n = 0
```

would kill every primitive character; for prime `n`, that would force the
length-`n` fiber to have only the trivial Fourier component.

The finite logic is checked in:

```text
p24/lean/PacketFactorGate.lean
```

It proves the implication hierarchy used here:

```text
coordinate/resultant nonvanishing for all coordinates
  => exact packet content nonzero
  => no harmful all-zero packet,
```

and records a tiny countermodel showing that one packet factor zero is weaker
than full primitive zero.

For p24 the relevant numbers are:

```text
n = 3107441
deg f_a = ord_n(p) = 388430
number of packet factors = 8
m = 66254
```

So one coordinate zero has random size about `p^(-388430)`, and the union
over all quotient coordinates and packets is still astronomically small.  But
as a deterministic condition it is just membership in a large cyclic code of
dimension

```text
n - deg f_a = 2719011.
```

That is why a pure cyclic-code or recurrence theorem cannot be enough.

## Diagnostic

I added:

```text
p24/relative_packet_factor_shape_scan.py
```

It records actual small-CM coordinate-zero hits and compares them to random
nonzero codewords in the same code.  It tracks:

```text
BM linear complexity,
distinct coefficient count,
zero coefficients,
trivial-character vanishing,
proper periods,
random codeword BM range.
```

Pinned `D=-1336` composite failure:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/relative_packet_factor_shape_scan.py \
  --only-D -1336 --min-h 12 --max-h 20 \
  --max-prime-quotients 8 --max-composite-quotients 8 \
  --min-n 3 --max-n 12 --q-start 1777 --q-stop 1778 \
  --include-linear --scan-origins --max-hits 12 --random-trials 40
```

Summary:

```text
zero_hits=12
prime_zero_hits=0
composite_zero_hits=12
hits_with_proper_period=0
hits_with_low_bm_le_half_n=0
hits_with_trivial_zero=0
```

The offending `n=6` fibers have:

```text
BM = 5 = n-1,
six distinct coefficients,
no proper period,
no trivial-character zero.
```

Random codewords in the same one-factor code have the same BM range.  Thus
the known CM failure is not an imprimitive repetition or low-recurrence
accident.

The two other known composite `n=4` failures behave the same way:

```text
D=-656,  q=173: zero_hits=16, proper_period_hits=0, low_BM_hits=0
D=-1028, q=293: zero_hits=16, proper_period_hits=0, low_BM_hits=0
```

Corrected bounded no-origin multi-splitting scan:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/relative_packet_factor_shape_scan.py \
  --max-cases 30 --min-h 12 --max-h 100 --max-abs-D 20000 \
  --max-prime-quotients 5 --max-composite-quotients 5 \
  --min-n 3 --max-n 100 --q-stop 200000 \
  --max-splitting-primes 3 --include-linear \
  --max-hits 12 --random-trials 20
```

found:

```text
zero_hits=0
prime_zero_hits=0
composite_zero_hits=0
```

on the same rows where the selected-prime resultant scan reports no
coordinate-zero packets.

## Consequence

This closes a tempting shortcut:

```text
packet-factor zero => low recurrence / proper period / imprimitive fiber
```

is false, even in actual CM failures.

The live proof target is therefore not a hidden low-complexity recurrence.
It remains an arithmetic p-unit/nonvanishing theorem:

```text
Res(Phi_3107441, J_u) is a p-unit for every u,
```

or the weaker exact-content theorem:

```text
gcd(f_a, J_0, ..., J_{m-1}) = 1
```

for each of the eight packet factors.

The probabilistic model is still useful calibration.  The fixed-prime theorem
needs an upgrade such as a phase-aware p-adic valuation formula for the
Hermitian packet norm or a selected-prime anti-concentration theorem for CM
relative packets.
