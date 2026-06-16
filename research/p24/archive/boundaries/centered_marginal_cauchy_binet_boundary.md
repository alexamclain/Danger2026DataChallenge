# Centered Marginal Cauchy-Binet Boundary

Date: 2026-06-05

This note checks whether the leading centered-marginal minor
`Delta_C_leading` factors through separate left and right coefficient minors.

## Exterior Pairing Formula

For CRT components `c,d`, let

```text
L_a = sum_{r == a mod c} F_r - sum_{r == 0 mod c} F_r,
R_b = sum_{s == b mod d} F_s - sum_{s == 0 mod d} F_s.
```

In a packet power basis, write the coefficient matrices of
`L_1,...,L_{c-1}` and the first `c-1` right differences
`R_1,...,R_{c-1}` as:

```text
A, R in F_q^((c-1) x packet_degree).
```

Let `B` be the Hermitian trace-form matrix in that power basis.  The leading
centered marginal window is:

```text
C_lead = A * B * R^t.
```

Therefore:

```text
Delta_C_leading = det(C_lead)
                = <L_1 wedge ... wedge L_{c-1},
                   R_1 wedge ... wedge R_{c-1}>_{wedge B}.
```

Equivalently, Cauchy-Binet expands:

```text
Delta_C_leading =
  sum_{|S|=|T|=c-1} det(A_S) det(B_{S,T}) det(R_T).
```

This is a useful exact identity: the p24 arithmetic theorem can be phrased as
nonorthogonality of two explicit decomposable exterior class-field vectors
under the induced Hermitian trace form.

## Audit

Added:

```text
p24/centered_marginal_cauchy_binet_audit.py
```

Degenerate case with no extra packet coordinates:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/centered_marginal_cauchy_binet_audit.py \
  --only-D -10919 --only-left 3 --only-right 13 \
  --max-cases 1 --max-h 200 --max-abs-D 12000 \
  --max-composite-quotients 20 --max-m 60 --max-n 80 \
  --q-stop 200000 --max-splitting-primes 2 \
  --max-factor-degree 12 --include-linear
```

reported one Cauchy-Binet term:

```text
factor_degree=2
window_dim=2
nonzero_terms=1
off_diagonal_terms=0
leading_term=window_det=10044.
```

Nondegenerate extra-coordinate cases are dense:

```text
D=-6719, q=6863, m=21, n=5, factor_degree=4, pair=(3,7):
  window_dim=2
  left_pluecker_nonzero=6/6
  right_pluecker_nonzero=6/6
  nonzero_terms=30
  off_diagonal_terms=24
  leading_term=4382
  window_det=4733.

D=-13319, q=13463, m=28, n=5, factor_degree=4, pair=(4,7):
  window_dim=3
  left_pluecker_nonzero=4/4
  right_pluecker_nonzero=4/4
  nonzero_terms=16
  off_diagonal_terms=12
  leading_term=10420
  window_det=554.

D=-10919, q=11243, m=12, n=13, factor_degree=12, pair=(4,4):
  window_dim=3
  left_pluecker_nonzero=220/220
  right_pluecker_nonzero=220/220
  nonzero_terms=6160
  off_diagonal_terms=5940
  leading_term=7493
  window_det=6470.
```

## Consequence

The leading difference minor is a valid finite rank certificate, but the
small actual-CM data does not support a simple factorization:

```text
Delta_C_leading != leading_left_minor * unit * leading_right_minor.
```

Once the packet degree exceeds the window dimension, the induced exterior
trace pairing is genuinely dense.  A proof should therefore target either:

```text
1. an arithmetic p-unit theorem for the whole exterior pairing;
2. a p-adic dominance/filtration theorem preventing cancellation in the dense
   Cauchy-Binet sum;
3. a different basis or class-field normalization where this exterior pairing
   becomes triangular.
```

The first option is currently the honest theorem shape.  The third remains
possible, but it would need a new normalizing identity; the natural packet
power basis does not expose it.
