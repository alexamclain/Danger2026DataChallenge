# P25 Lane B: KSY-y Theorem Legality Boundary

Updated: 2026-06-13 19:03 PDT

## Purpose

The KSY-y formula and period-context gates make the finite payload precise.
This note records the theorem-intake boundary: a claimed literature or theory
hit helps only if it emits one of the exact challenge-useful outputs below.

## Exact Contract

Index contract:

```text
C=(47,28), D=(22,3), K=(57,0), j=-1,0,1, k=0..24
A = C + jD + kK
orientation = y(A)/y(-A)
```

Formula contract:

```text
y(Q) = -g(2Q) / g(Q)^4

y(A)/y(-A) =
  g(2A)      coeff +1
  g(A)^-4    coeff -4
  g(-2A)^-1  coeff -1
  g(-A)^4    coeff +4
```

The four layers are disjoint `75`-point layers; the union is the `300`-term
theta2-inverse footprint with coefficient counts
`(-4,75), (-1,75), (1,75), (4,75)`.

Period/value contract:

```text
support period = 156
[2]^156 fixes the formula footprint
proper divisors of 156 fail
gcd(4^156 - 1, p - 1) = 1
ambient 780-period value route has 11 F_p branches
```

## Accepted Theorem Outputs

Accepted as complete certificate routes:

```text
1. Exact KSY-y divisor/additive identity.
   Output: the raw divisor/additive product for the exact C/D/K/orientation
   data above.  This routes through the theta2-inverse certificate path.

2. Exact KSY-y value identity with period-156 context.
   Output: the finite-field value product plus period-156 fixedness,
   telescoping, or equivalent branch/root data.  With that context the F_p
   root is unique.
```

Conditional, not complete by themselves:

```text
1. Exact value identity without period context.
2. Finite spine payload without a challenge-legal arithmetic source.
3. CM/Lang or class-field generation without a finite-field identity for this
   exact product.
```

Rejected as complete routes:

```text
1. Ambient 780-period value only.
2. Wrong C/D/K geometry or orientation.
3. Generic KSY ray-class generation from y-values.
4. Raw Kubert-Lang exponent balance without finite intake geometry.
```

## Local Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_theorem_legality_gate.py
```

Expected marker:

```text
robert_ksy_theta2_kubert_lang_ksy_y_theorem_legality_rows=1/1
```

## Interpretation

The moonshot is narrowly viable, not broadly viable.  The finite payload and
branch context are executable.  The missing object is a challenge-legal
arithmetic theorem for this exact product.

The first external question is:

```text
Can KSY/Siegel-Robert/Sprang/Kubert-Lang be stated to produce this exact C/D/K
product identity, or the value identity with period-156 context, without
relying on a forbidden CM shortcut?
```
