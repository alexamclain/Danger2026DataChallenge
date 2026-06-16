# Hermitian Isotropy Probability Audit

This note records the exact random-model scale for the preferred Hermitian
energy packet certificate.

## Finite-Field Model

One p24 Hermitian packet lives over

```text
F_{Q^2},      Q = p^194215,
```

with involution `x -> x^Q`.  The content vector has length

```text
m = 66254.
```

The Hermitian scalar is modeled by

```text
H(v) = sum_i v_i v_i^Q in F_Q.
```

For a nondegenerate Hermitian form on `F_{Q^2}^m`, the exact number of zero
vectors is

```text
Q^(2m-1) + (-1)^m (Q-1) Q^(m-1).
```

Thus for large `m`, a random vector has Hermitian energy zero with probability
about

```text
Q^-1 = p^-194215.
```

## p24 Scale

The script

```text
p24/hermitian_isotropy_probability_audit.py
```

reports:

```text
real_packet_degree=194215
packet_count=8
log_Q=1.073272e7
log10_zero_probability≈-4.661160e6
log10_union_bound_8_packets≈-4.661159e6
```

So the random model predicts a Hermitian packet failure probability around

```text
10^-4661160
```

per packet, and the eight-packet union bound barely changes the exponent.

## Validation

The script validates the zero-count formula by brute force over a tiny
quadratic extension:

```text
Q=3 m=1 formula=1   brute=1
Q=3 m=2 formula=33  brute=33
Q=3 m=3 formula=225 brute=225
```

## Interpretation

This is not a certificate.  It says the Hermitian scalar is statistically
very strong but still a quadric membership condition, not exact content
nonzero.  The p24 proof still needs a selected-prime p-adic unit theorem or
an explicit finite-field identity for the chosen CM packet.
