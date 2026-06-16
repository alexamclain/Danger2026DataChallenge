# Moment Lambda Packaging Boundary

This note refines the two-moment exact-content target.

For a packet factor `f | Phi_n`, define

```text
M0 = sum_u J_u mod f,
M1 = sum_u u J_u mod f.
```

If the content vector is nonzero and `{M0,M1}` is not the zero pair, then

```text
L_lambda = M0 + lambda*M1
```

can vanish for at most one `lambda in F_q`.  Thus after proving the two-moment
certificate, a single-resultant certificate can be obtained by choosing
`lambda` outside a finite bad set.  For p24 there are only eight nontrivial
relative packets, so there are at most eight bad base-field lambdas once the
two-moment theorem is known.

I added:

```text
p24/moment_lambda_bad_values_scan.py
p24/lean/MomentLambdaGate.lean
```

It computes the forbidden base-field lambda when it exists and records small
signed lambdas that fail in bounded CM rows.

The Lean file checks the finite implication:

```text
{M0,M1} nonzero in every packet
  => exact packet content;

chosen lambda avoids every packet's forbidden value
  => M0 + lambda*M1 nonzero in every packet
  => exact packet content.
```

## Pinned Product Counterexample

The prime-`n` product failure row still has no `{M0,M1}` failure:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/moment_lambda_bad_values_scan.py \
  --only-D -956 --min-h 12 --max-h 20 \
  --max-prime-quotients 8 --max-composite-quotients 8 \
  --min-n 3 --max-n 12 --q-start 3307 --q-stop 3308 \
  --include-linear --section contiguous --lambda-bound 16
```

Output:

```text
packet_rows=3
content_failures=0
m0_failures=0
pair_failures=0
rows_with_base_field_bad_lambda=2
rows_with_small_lambda_hit=0
```

The complement section gives the same no-pair-failure result.  With all
origins and a wider lambda window:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/moment_lambda_bad_values_scan.py \
  --only-D -956 --min-h 12 --max-h 20 \
  --max-prime-quotients 8 --max-composite-quotients 8 \
  --min-n 3 --max-n 12 --q-start 3307 --q-stop 3308 \
  --include-linear --section complement \
  --lambda-bound 32 --scan-origins --max-origins 15 --summary-only
```

Output:

```text
packet_rows=45
content_failures=0
m0_failures=0
pair_failures=0
rows_with_base_field_bad_lambda=30
rows_with_small_lambda_hit=3
small_hits_by_lambda={-9: 3}
```

Thus even where product coordinates fail, the two-moment certificate survives;
but a particular fixed lambda can still be bad after changing the selected
origin.

## Selected-Prime Windows

Complement section:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/moment_lambda_bad_values_scan.py \
  --max-cases 40 --min-h 12 --max-h 140 --max-abs-D 40000 \
  --max-prime-quotients 8 --max-composite-quotients 8 \
  --min-n 3 --max-n 140 --q-stop 400000 \
  --max-splitting-primes 3 --include-linear \
  --section complement --lambda-bound 16 --summary-only
```

Output:

```text
packet_rows=337
content_failures=0
m0_failures=0
pair_failures=0
rows_with_base_field_bad_lambda=150
rows_with_small_lambda_hit=11
small_hits_by_lambda={-16:3, -15:1, -13:2, -11:1, 3:1, 6:1, 12:1, 13:1}
```

Contiguous section:

```text
packet_rows=475
content_failures=0
m0_failures=1
pair_failures=0
rows_with_base_field_bad_lambda=218
rows_with_small_lambda_hit=14
small_hits_by_lambda={-13:1, -11:1, -7:1, -6:2, 0:1, 4:1, 6:1, 7:1, 9:2, 10:1, 14:1, 16:1}
```

So the finite-field hierarchy is:

```text
M0 alone:
  can fail at random rate;

M0 + lambda*M1 for a fixed lambda:
  can fail for unlucky lambda/packet pairs;

{M0,M1}:
  no failures observed in these windows;

exact content:
  no failures observed.
```

## p24 Interpretation

The strongest packaging target remains:

```text
gcd(Phi_3107441, M0, M1) = 1 mod p.
```

If this is proved, then one can choose a small `lambda` by testing at most
nine candidates against the eight p24 packets, or prove directly that a chosen
lambda such as `1` is not in the finite bad set.

This is still not the missing arithmetic theorem.  It only reduces the
finite-field certificate surface from all `66254` coordinate fibers to two
transverse quotient moments, or to one scalar after a finite lambda choice.
Constructing and proving the p-unitness of those moments remains the embedded
class-field/selected-prime problem.
