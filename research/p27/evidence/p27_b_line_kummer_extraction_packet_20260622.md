# P27 B-Line Kummer Extraction Packet

Date: 2026-06-22

## Claim

The B-line route has advanced from a bucket/telemetry idea to a precise
function-field extraction target:

```text
extract the Kummer/divisor class d3(B) on P1_B
then compare f3(B), f4(B), f5(B), ... for recurrence or coupling
```

This is the next concrete B-line test that could beat `sqrt(p)`: not by
filtering one more half-gate, but by finding a source, low-genus quotient, or
multi-gate class relation on `P1_B`.

## Artifacts

Packet generator:

```text
research/p27/archive/gates/p27_b_line_kummer_extraction_packet.py
```

Generated packet:

```text
research/p27/archive/probe_outputs/p27_b_line_kummer_extraction_packet_20260622.txt
```

Magma sanity fixture:

```text
research/p27/archive/fixtures/p27_b_line_sanity_q1607_magma.m
```

Local sanity equivalent:

```text
q1607 rows/degenerate/mismatches = 1604 / 3 / 0 / 0 / 0 / 0
```

This checks the B quotient, `A+2=B^2`, and the K/A branch equations over
`q=1607`.  The Magma fixture is an algebraic sanity check only; the full
normalization/genus extraction is still the open CAS task.

## Exact B-Line Quotient

On the residual source coordinate `X`:

```text
B = 8X^2/(X^2 - 1)^2
A + 2 = B^2
```

The packet records:

```text
B_relation = B*X^4 - 2B*X^2 + B - 8X^2
B_branch_resultant = 16384*B^3*(B + 2)^2
```

The K/A branch relation with `L=K^2` is:

```text
L = (B - 2)^4/(8B(B + 2)^2)         for Bplus
L = -(B + 2)^4/(8B(B - 2)^2)        for Bminus
```

This is why the B-line is a natural genus-0 quotient for the legal selected
tower.

## Source Cover To Normalize

The packet gives the d3 all-plus cover over `P1_Bline` with variables:

```text
X, W, T, beta, R, z, Y, eta, Bline
```

where `beta` is the first-half branch root and `Bline` is the quotient
coordinate.  The defining equations are:

```text
eta^2 = 1
W^2 = X^3 - X
T^2 = X(X^2 + 1)(X^2 + 2X - 1)
X*R^2 = criterion_num
Bline*(X^2 - 1)^2 = 8X^2
beta^2*U_den^2 = U_num^2 - 4U_den^2
4*z^2*H_num*(U_num + beta*U_den)
  = 2*U_den*A_den*(z^4 - 1)^2
Y^2*A_den = H_num
```

The auxiliary rational functions are emitted in the generated packet so the
CAS user does not need to reconstruct them from prose.

## Prior Kills

Already killed on the B line:

```text
B-atom products as d3/d4 predictors
rational-linear branch support of weight <=4 for d3(B)
one irreducible quadratic times <=2 rational linears for d3(B)
two irreducible quadratic branch factors for d3(B)
two irreducible quadratic branch factors for the legal B-domain
visible Belyi S3 orbit sampler on B
B-line prefix counts alone as a below-sqrt sampler
large GPU search from B buckets without an extracted class
```

So the B-line task is no longer "find a good bucket."  It is:

```text
compute the actual Kummer class, branch support, and genus
```

## CAS Task

Run over the p27-signature fields first:

```text
q = 1607, 1847, 2087
```

Required outputs:

```text
branch divisor degree for d3(B)
support field degrees
normalization genus over P1_B
visible involutions or quotients over B
comparison of f4/f3 and f5/f4 if d3 is tractable
```

Promotion bar:

```text
genus <= 1
or explicit sourceable walk
or recurrence/coupling among f3(B), f4(B), f5(B), ...
or a direct sampler that improves target/source_draw without fresh half-losses
```

Kill condition:

```text
high/generic branch degree
only previously killed split low-degree supports appear
f4/f5 are unrelated fresh Kummer classes
normalization is too high-genus to source or quotient
```

Update: the legal-domain split degree-4 screen is also negative:
[P27 B-Line Legal-Domain Two-Quadratic Support Screen](p27_b_line_legal_two_quadratic_support_20260622.md).
The core-to-legal B cut is not a product of two irreducible quadratic branch
factors in q1607/q1847/q2087.

Update: the visible Belyi orbit shortcut is negative:
[P27 B-Line Belyi-Orbit Screen](p27_b_line_belyi_orbit_20260622.md).
Every non-identity automorphism of the branch set `{0,-2,infinity}` sends core
B values outside the core bucket in q1607/q1847/q2087.

Update: one bounded GPU-sized visible family remains before this route fully
hands off to offline normalization:
[P27 B-Line Quartic GPU Test Card](p27_b_line_quartic_gpu_test_card_20260622.md).
Exact monic quartic support for `d3_on_legalB` or the combined gate4 prefix
would give a genus-1 double-cover source candidate.  The q1847/q2087 expected
random exact counts are tiny on the primary rows, so this is a real
math-structure GPU test, not a production search.

## Continue / Kill

```text
continue = run Magma/Sage normalization over P1_Bline in q1607/q1847/q2087
continue = bounded GPU exact quartic support screen for d3/gate4 on Bline
continue = if d3 is tractable, compare the B-line Kummer sequence f3,f4,f5
continue = use GPU only after a source/sampler or recurrence is named

kill = more unguided B-bucket scoring
kill = large GPU production from Bplus alone
kill = treating one-bit conditional lift as sqrt-beating
```

```text
p27_b_line_kummer_extraction_packet_rows=1/1
```
