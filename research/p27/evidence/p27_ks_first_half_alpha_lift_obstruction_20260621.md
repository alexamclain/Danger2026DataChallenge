# P27 K/S First-Half Alpha-Lift Obstruction

Date: 2026-06-21

## Claim

The K/S first-half cover has a clean branch factorization, but the most
obvious alpha quotient shortcut is obstructed over the p27 base field.

For the eta-fixed first-half equation

```text
B^2 * U_den^2 = U_num^2 - 4*U_den^2,
```

the non-square branch part factors as:

```text
32*T*X
  *(eta*T*W + X*(X-1)*(X+1)^2)
  *(2*eta*W*X + X^3 + X^2 - X - 1).
```

For `eta=+1`, the `T -> -T` alpha deck changes the first new branch factor by
the ratio

```text
(-T*W + X*(X-1)*(X+1)^2)
/
( T*W + X*(X-1)*(X+1)^2).
```

On the intermediate curve

```text
W^2 = X^3 - X
T^2 = X(X^2+1)(X^2+2X-1),
```

this ratio is exactly:

```text
-((-T*W + X*(X-1)*(X+1)^2)/(2*X*W))^2.
```

So the same-eta alpha lift requires adjoining `sqrt(-1)`.  Since p27 is
`3 mod 4`, this is not an `F_p`-rational lift.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_ks_first_half_branch_alpha_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_ks_first_half_branch_alpha_probe_20260621.txt
```

Independent online Magma checksum:

```text
research/p27/archive/fixtures/p27_ks_first_half_alpha_ratio_q1607_magma.m
research/p27/archive/probe_outputs/p27_ks_first_half_alpha_ratio_q1607_magma_20260621.txt
research/p27/archive/probe_outputs/p27_ks_first_half_alpha_ratio_q1607_magma_20260621.html
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 research/p27/archive/gates/p27_ks_first_half_branch_alpha_probe.py \
  | tee research/p27/archive/probe_outputs/p27_ks_first_half_branch_alpha_probe_20260621.txt
```

Magma command:

```bash
curl -L -sS -A 'Mozilla/5.0' \
  --data-urlencode input@research/p27/archive/fixtures/p27_ks_first_half_alpha_ratio_q1607_magma.m \
  https://magma.maths.usyd.edu.au/calc/ \
  > research/p27/archive/probe_outputs/p27_ks_first_half_alpha_ratio_q1607_magma_20260621.html
```

## Results

Symbolic checks:

```text
symbolic_factorization_diff=0
same_eta_ratio_identity_diff=0
```

Guard-field checks on p27-signature fields:

```text
q=1607:
  compactd_points=800
  same_eta_ratio_chi_-1=800
  eta_flip_ratio_chi_-1=400
  eta_flip_ratio_chi_1=400

q=1847:
  compactd_points=972
  same_eta_ratio_chi_-1=972
  eta_flip_ratio_chi_-1=512
  eta_flip_ratio_chi_1=460

q=2087:
  compactd_points=976
  same_eta_ratio_chi_-1=976
  eta_flip_ratio_chi_-1=456
  eta_flip_ratio_chi_1=520
```

Online Magma q1607 checksum:

```text
FACTOR_DIFF_ZERO true
RATIO_IDEAL_MEMBER true
COUNTS 800 800 0 800 0 400 400 0
RESULT p27_ks_first_half_alpha_ratio_q1607 done
```

Interpretation of the finite checks:

```text
same eta: always nonsquare, exactly as the -square identity predicts
eta flip: mixed square/nonsquare, so no simple eta-swapping alpha rescue
```

## Interpretation

Positive:

```text
The first-half B-cover is no longer an opaque large equation.
Its branch class has a compact named factorization.
The obstruction to alpha lifting is exact, not statistical.
```

Negative:

```text
The natural alpha/order-4 quotient does not lift over F_p for p27.
The lift exists only after a quadratic constant extension adjoining sqrt(-1).
The eta-swapped variant is mixed on p27-signature guard fields.
```

This demotes the K/S first-half quotient route as a direct `F_p` search-space
sampler.  A geometric quotient over `F_{p^2}` might still be diagnostic, but it
would need an additional descent mechanism before it could beat sqrt over the
actual p27 base field.

## Consequence

The live K/S route is now narrower:

```text
continue = use the branch factorization in offline normalization
continue = test whether any F_{p^2} alpha quotient descends to an F_p sampler
continue = compare the named B-branch class with actual d3/d4 covers

kill = direct F_p alpha quotient of the first-half B-cover
kill = eta-swap alpha lift as a quotient shortcut
kill = visible branch-factor products as d3/d4 selectors
```

The next sqrt-beating candidate should not be "quotient the genus-37 curve by
alpha" generically.  It should be one of:

```text
1. An explicit F_p descent of the sqrt(-1)-twisted geometric quotient.
2. A separate low-genus quotient of the actual d3/d4 E-level double covers.
3. A trace/norm or Kummer identity that couples many selected x-square gates.
```

```text
p27_ks_first_half_alpha_lift_obstruction_rows=1/1
```
