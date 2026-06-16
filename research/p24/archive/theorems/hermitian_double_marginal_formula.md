# Hermitian Double-Marginal Formula

This note records the exact CRT marginal form of the Hermitian axis Gram
blocks.

## Kernel

For one H-packet factor, let

```text
K(r,s) = <F_r,F_s>
       = Tr_packet(F_r(X) * F_s(X^-1)).
```

Here `F_r` are the complement fibers and the Hermitian involution is
`X -> X^-1`.

For CRT components `c,d | m`, define the double marginal table

```text
M_{c,d}(a,b)
  = sum_{r == a mod c, s == b mod d} K(r,s).
```

Then the block between trace-zero component bases

```text
U_c,a = sum_{r == a mod c} F_r - sum_{r == 0 mod c} F_r,
U_d,b = sum_{s == b mod d} F_s - sum_{s == 0 mod d} F_s
```

is exactly the centered table:

```text
<U_c,a, U_d,b>
  = M_{c,d}(a,b) - M_{c,d}(a,0)
    - M_{c,d}(0,b) + M_{c,d}(0,0)
```

for `a,b != 0`.

The constant-component block is the centered single marginal:

```text
<sum_r F_r, U_c,a>
  = sum_{r, s == a mod c} K(r,s)
    - sum_{r, s == 0 mod c} K(r,s).
```

Thus every entry of the Hermitian axis Gram matrix is a centered CRT marginal
of the inverse-character autocorrelation kernel.

## Audit

Added:

```text
p24/hermitian_double_marginal_audit.py
```

Pinned `(4,3)` rows:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/hermitian_double_marginal_audit.py \
  --only-D -10919 --max-rows 20 --max-cases 1 --max-h 200 \
  --max-abs-D 12000 --max-composite-quotients 20 \
  --max-axis-dim 40 --max-m 60 --max-n 80 \
  --q-stop 500000 --max-splitting-primes 5 --include-linear

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/hermitian_double_marginal_audit.py \
  --only-D -8711 --max-rows 20 --max-cases 1 --max-h 200 \
  --max-abs-D 10000 --max-composite-quotients 20 \
  --max-axis-dim 40 --max-m 60 --max-n 60 \
  --q-stop 400000 --max-splitting-primes 5 --include-linear
```

Both report zero identity failures.  For example:

```text
D=-10919, q=11243:
  constant_fail=0
  pair_ranks=(4,4):3/3:fail0,
             (4,3):2/2:fail0,
             (3,4):2/2:fail0,
             (3,3):2/2:fail0

D=-8711, q=8747:
  constant_fail=0
  pair_ranks=(4,4):3/3:fail0,
             (4,3):2/2:fail0,
             (3,4):2/2:fail0,
             (3,3):2/2:fail0
```

Broader bounded window:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/hermitian_double_marginal_audit.py \
  --max-rows 30 --max-cases 16 --min-h 12 --max-h 220 \
  --max-abs-D 80000 --max-prime-quotients 10 \
  --max-composite-quotients 20 --min-n 3 --max-n 220 \
  --q-stop 600000 --max-splitting-primes 2 \
  --max-axis-dim 75 --max-m 120 --include-linear --summary-only
```

reported:

```text
rows=14
constant_component_identity_failures=0
pair_identity_failures=0
pair_rank_mismatch_count=0
max_centered_pair_rank=2
```

## p24 Interpretation

For p24, the Hermitian Schur correction can now be phrased as a p-unit theorem
for one centered marginal-kernel matrix whose blocks are:

```text
constant with 2,157,211 single marginals;
2 x 157 centered double marginals;
2 x 211 centered double marginals;
157 x 211 centered double marginals;
diagonal centered marginals for 2,157,211.
```

The largest genuinely mixed table is:

```text
157 x 211
```

centered to a `156 x 210` cross block.  This is still large enough to be a
real coupled object, but it is no longer opaque: it is a marginal of the
single packet autocorrelation kernel `K(r,s)`.

## Current Theorem Shape

The Hermitian proof target can be refined to:

```text
1. prove diagonal centered marginal blocks are p-units;
2. prove the centered double-marginal Schur correction is a p-unit;
3. multiply over the eight p24 H-packets to get the degree-8 norm p-unit.
```

This is not a solution yet.  It is the next exact finite-field identity
surface for the missing theorem.
