# Hermitian Mixed Resolvent Pairing Formula

This note connects the trace-intersection periods back to K-character
resolvents.

## Formula

For one H-packet, let

```text
F_r(X) = sum_k j_{n*r + m*k} X^k.
```

The Hermitian packet kernel is

```text
K(r,s)=Tr_packet(F_r(X)F_s(X^-1)).
```

For CRT components `c,d | m`, define K-character resolvents:

```text
A_u = sum_r zeta_c^(u*r) F_r,
B_v = sum_s zeta_d^(v*s) F_s.
```

Then the mixed Fourier entry is the bilinear Hermitian-resolvent pairing:

```text
H_{c,d}(u,v)
  = sum_{r,s} zeta_c^(u*r) zeta_d^(v*s) K(r,s)
  = <A_u,B_v>.
```

The pairing is "Hermitian" in the packet variable, because `K(r,s)` already
contains the inverse H-character conjugation.  The K-character scalar
extension is the bilinear coefficient layer used by the double DFT.

## p24 Periods

For p24, the six periods in the trace-intersection theorem are:

```text
S_j = H_{157,211}(1,v_j) = <A_1,B_{v_j}>,
```

where `v_j` runs over the six Frobenius orbit representatives modulo `211`.

Thus the current transversality theorem:

```text
L ∩ span_R{S_j}^perp = {0}
```

is a statement about six mixed Hermitian pairings between one left
`157`-character resolvent and the six right `211`-orbit resolvents.

## Audit

Added:

```text
p24/hermitian_mixed_resolvent_pairing_audit.py
```

Pinned rows:

```text
D=-10919:
  rows=2
  tests=8
  entry_mismatches=0
  rank_mismatch_tests=0
  all_seed_periods_nonzero_tests=8

D=-8711:
  rows=2
  tests=8
  entry_mismatches=0
  rank_mismatch_tests=0
  all_seed_periods_nonzero_tests=8
```

A broader summary window was intentionally stopped after it became slower than
its theorem-shaping value.  The identity itself is algebraic; the audit checks
that the implemented DFT, kernel, and resolvent-pairing conventions agree on
actual CM rows.

## Current Proof Surface

The mixed Schur theorem can now be phrased as:

```text
The six pairings <A_1,B_{v_j}> define an R-subspace W whose E/R trace
orthogonal complement is transverse to L=F_p(mu_157).
```

This is the class-field-period object a proof should attack.
