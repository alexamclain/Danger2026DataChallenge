# P27 K/S First-Half E-Prime Descent

Date: 2026-06-21

## Claim

The alpha quotient of the K/S first-half cover is obstructed over `F_p`, but
the quotient by the rational `(0,0)` translation is compatible with the
first-half branch class.

This is positive structure for the remaining E-prime route:

```text
E:  W^2 = X^3 - X
E': V^2 = U^3 + 4U
U = X - 1/X
V = W*(X^2+1)/X^2
```

The deck transformation is:

```text
X -> -1/X
W -> W/X^2
T -> +/- T/X^3
```

and the first-half `B` branch squareclass is preserved on the compactD
stratum in all tested p27-signature guard fields.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_ks_first_half_t0_descent_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_ks_first_half_t0_descent_probe_20260621.txt
```

Online Magma checksum:

```text
research/p27/archive/fixtures/p27_ks_first_half_t0_descent_q1607_magma.m
research/p27/archive/probe_outputs/p27_ks_first_half_t0_descent_q1607_magma_20260621.txt
research/p27/archive/probe_outputs/p27_ks_first_half_t0_descent_q1607_magma_20260621.html
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 research/p27/archive/gates/p27_ks_first_half_t0_descent_probe.py \
  | tee research/p27/archive/probe_outputs/p27_ks_first_half_t0_descent_probe_20260621.txt
```

Magma command:

```bash
curl -L -sS -A 'Mozilla/5.0' \
  --data-urlencode input@research/p27/archive/fixtures/p27_ks_first_half_t0_descent_q1607_magma.m \
  https://magma.maths.usyd.edu.au/calc/ \
  > research/p27/archive/probe_outputs/p27_ks_first_half_t0_descent_q1607_magma_20260621.html
```

## Symbolic Checks

The T-cover descends through the quotient:

```text
T2_transform_diff=0
```

where:

```text
T2(X) = X(X^2+1)(X^2+2X-1)
T2(-1/X) = T2(X)/X^6
```

The first-half branch factorization also checks exactly:

```text
branch_factorization_diff=0
```

with branch factor:

```text
32*T*X
  *(eta*T*W + X*(X-1)*(X+1)^2)
  *(2*eta*W*X + X^3 + X^2 - X - 1).
```

## Guard-Field Results

Python finite-field probe:

```text
q=1607:
  compactd_points=800
  t_lift_1_bbranch_ratio_chi_1=800
  t_lift_-1_bbranch_ratio_chi_1=800
  t_lift_1_compactd_chi_1=800
  t_lift_-1_compactd_chi_1=800

q=1847:
  compactd_points=972
  t_lift_1_bbranch_ratio_chi_1=972
  t_lift_-1_bbranch_ratio_chi_1=972
  t_lift_1_compactd_chi_1=972
  t_lift_-1_compactd_chi_1=972

q=2087:
  compactd_points=976
  t_lift_1_bbranch_ratio_chi_1=976
  t_lift_-1_bbranch_ratio_chi_1=976
  t_lift_1_compactd_chi_1=976
  t_lift_-1_compactd_chi_1=976
```

Online Magma q1607 checksum:

```text
BRANCH_FACTOR_DIFF_ZERO true
T2_TRANSFORM_ZERO true
COUNTS 800 800 1600 0 0 0
RESULT p27_ks_first_half_t0_descent_q1607 done
```

Here the count fields are:

```text
compact_points compact_reject same_plus same_minus bad_tcover bad_compact_image
```

So both T-lifts preserve compactD and the first-half B-branch squareclass on
every compactD point in the q1607 test.

## Interpretation

Positive:

```text
The E -> E' quotient is compatible with the exact first-half branch equations.
This explains why d3/d4 descent through the 2-isogenous quotient was not an accident.
The next extraction should happen on E': V^2=U^3+4U, not the raw genus-37 layer.
```

Negative:

```text
This is not a source by itself.
Line, two-line, low-pole random, visible branch-packet, and small affine-walk
screens on E' are already negative.
```

## Consequence

The concrete sqrt-beating test is now sharper:

```text
extract the actual d3 and d4 double covers over E'
compute their branch divisors / Kummer classes / genera
compare whether d4 is a fresh cover or a transform of d3
```

Promotion conditions:

```text
genus <= 1 source cover over E'
explicit sourceable recurrence for d_j
shared Kummer/Prym class controlling more than one selected x-square gate
```

Kill conditions:

```text
d3 and d4 are unrelated fresh high-genus double covers on E'
the only descent is the known constant-factor quotient
no low-genus factor appears after normalization
```

```text
p27_ks_first_half_eprime_descent_rows=1/1
```
