# Prime Relative-Normality Counterexample

This note records the first small CM counterexample to the broad
prime-recovery product theorem.

## Candidate That Failed

The tempting strengthening was:

```text
If n is prime, then every selected nontrivial relative character packet has
P_u(a) != 0 for every coordinate u.
```

Equivalently, for a prime recovery length `n`,

```text
Res(Phi_n, J_u) != 0
```

for all quotient coordinates `u`, at every selected splitting prime.  This
would be a strong product certificate for p24, because p24 has
`n=3107441` prime.

## Multi-Splitting Stress Scan

The first broad scans tested only the first convenient splitting prime per CM
row and found no prime-`n` coordinate failures.  I then used the
multi-splitting selected-prime scan:

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

Thus prime `n` alone does not prevent selected-coordinate vanishing.  The
failure is a product-certificate failure only: exact content still survives.
The selected-prime content/Hermitian follow-up is recorded in:

```text
p24/packetized_content_selected_prime_scan.md
```

## Pinned Row

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

The zero coordinate is not an imprimitive proper-period artifact.  The
inspector reports:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/relative_zero_structure_inspector.py \
  --D -956 --q-start 3307 --q-stop 3308 --min-n 3 --max-n 12
```

Key row:

```text
m=5 n=3 n_prime=1 deg=1 roots=[57] shift=0 u=2
proper_periods=[] coeffs=[615,1471,658]
```

The same length-3 fiber reappears under origin shifts, as expected from the
origin-shift symmetry.

## Consequence

The broad theorem

```text
prime recovery length => all coordinate resultants nonzero
```

is false.  For p24, `Res(Phi_3107441,J_u) != 0` for all `u` may still hold as
a p24-specific selected-prime statement, but it cannot be justified by
prime-ness of `n` or by a general CM relative-normality theorem of this form.

The current live targets are therefore:

```text
exact content:
  gcd(f_a,J_0,...,J_{m-1}) = 1 for each of the eight p24 packets;

Hermitian scalar:
  the phase-aware Hermitian packet scalar is a p-unit;

p24-specific product:
  all coordinate resultants are nonzero for this one discriminant/prime,
  with an arithmetic proof stronger than prime n.
```

The pinned row itself supports the first two surviving targets:

```text
content_gcd_degree=0
energy_zero=0
energy_norm_zero=0
hermitian_zero=0
hermitian_norm_zero=0
```
