# Packetized Relative-Content Scan

This note records a finite-field toy experiment for the exact p24 content
certificate:

```text
gcd(f_a, J_0, J_1, ..., J_{m-1}) = 1.
```

Unlike the earlier full-DFT scans, this experiment does not require the
relative roots of unity to lie in the base field.

## Method

For small CM cycles where the Hilbert class polynomial splits completely over
`F_q`, choose a quotient

```text
h = m*n,     n prime,
```

and form

```text
J_u(X) = sum_k j_{u+m*k} X^k,      0 <= u < m.
```

Then factor `Phi_n(X)` over `F_q`.  Each irreducible factor `f_a` is one
Frobenius packet of relative characters.  The exact packet certificate is:

```text
gcd(f_a, J_0, ..., J_{m-1}) = 1.
```

The script also computes the scalar energy packet

```text
C(X) = sum_d C_d X^d,
C_d = sum_i j_{i+m*d} j_i,
```

checks the Gram identity

```text
C(X) = sum_u J_u(X)J_u(X^-1)
```

in `F_q[X]/(X^n-1)`, and checks whether `C mod f_a` or its resultant norm
vanishes.

It also computes the carry-adjusted Hermitian scalar

```text
H(X) = sum_u X^c(u) J_u(X)J_{-u mod m}(X),
c(u) = (u + (-u mod m))/m.
```

This is the packet version of `sum |P_u(a)|^2` over complex embeddings, and
is another sufficient finite-field certificate when nonzero.

Implementation:

```text
p24/packetized_relative_content_scan.py
```

PARI is used for the cyclotomic factorization because SymPy's FLINT-backed
factor sorting can hang or error on some `nmod` factors.

## Calibration Run

The calibrated `D=-5000` row has

```text
h=30, m=6, n=5, q=1259, q=-1 mod 5.
```

Thus the CM roots lie in `F_q`, but the fifth roots of unity form two
quadratic Frobenius packets.  The scan reports two packet rows:

```text
factor_degree=2 content_gcd_degree=0 energy_zero=0 packet_norm_zero=0
factor_degree=2 content_gcd_degree=0 energy_zero=0 packet_norm_zero=0
```

This is the exact same finite-field packet shape as p24, only tiny.

## Summary Run

Command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/packetized_relative_content_scan.py \
  --max-cases 50 --min-h 12 --max-h 96 --max-abs-D 20000 \
  --max-quotients 3 --min-n 5 --q-stop 200000 --summary-only
```

Output:

```text
rows=50
packet_rows=126
nonlinear_packets=82
content_failures=0
energy_zero_packets=0
packet_norm_zero_packets=0
hermitian_zero_packets=0
hermitian_norm_zero_packets=0
```

The run also asserts the autocorrelation/Gram identity for every quotient row.

A low-order scan including the known small CM failure regime:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/packetized_relative_content_scan.py \
  --max-cases 40 --min-h 2 --max-h 30 --max-abs-D 2000 \
  --max-quotients 4 --min-n 2 --q-stop 50000 --summary-only
```

found:

```text
packet_rows=70
nonlinear_packets=36
content_failures=0
energy_zero_packets=2
packet_norm_zero_packets=2
hermitian_zero_packets=0
hermitian_norm_zero_packets=0
```

So the ordinary energy scalar can vanish in small natural CM packets even when
content is nonzero, while the Hermitian scalar survived this low-order scan.

## Interpretation

This supports the p24-specific arithmetic theorem target:

```text
the relative content vector is nonzero in every Frobenius packet.
```

It also supports the scalar energy sufficient certificate in the same packet
model.  It is not a proof: small ordinary CM data already has reduced
normality failures in unrelated low-order packets, so the theorem cannot be a
generic split-CM or cyclic-code fact.  The missing input remains a selected
prime p-adic/non-genus nonvanishing theorem for the p24 packet norm/content
ideal.
