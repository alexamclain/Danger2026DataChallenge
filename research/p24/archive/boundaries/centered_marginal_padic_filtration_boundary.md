# Centered Marginal P-Adic Filtration Boundary

Date: 2026-06-06

This note records the structured-basis test for the remaining p-adic
dominance idea in the centered route.

## Candidate Theorem Shape

The exterior identity is:

```text
Delta_C = det(A B R^t)
        = <L_1 wedge ... wedge L_r,
           R_1 wedge ... wedge R_r>_{wedge B}.
```

A p-adic dominance proof would need a p-integral packet basis and a filtration
such that:

```text
1. one exterior Cauchy-Binet term is a selected-prime unit;
2. every other term has strictly positive selected p-valuation;
3. therefore Delta_C is a p-unit without enumerating the class set.
```

The useful finite-field shadow of such a theorem is not merely "there is a
term order with a leading monomial"; generic dense polynomials have that.
The shadow should be visible in a structured arithmetic basis, for example a
power basis, Frobenius normal basis, middle-Frobenius eigenspace basis, or a
Hermitian self-dual/orthogonal basis.

## Audit

Added:

```text
p24/centered_marginal_padic_filtration_audit.py
```

The audit recomputes the same centered Cauchy-Binet determinant after
structured basis changes and reports:

```text
left/right Pluecker support;
nonzero Cauchy-Binet terms;
diagonal versus off-diagonal terms;
whether the natural degree initial layer is the whole determinant modulo q.
```

Pinned rows:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/centered_marginal_padic_filtration_audit.py \
  --only-D -6719 --only-left 3 --only-right 7 \
  --max-cases 1 --max-h 200 --max-abs-D 12000 \
  --max-composite-quotients 20 --max-m 60 --max-n 80 \
  --q-stop 200000 --max-splitting-primes 2 \
  --max-factor-degree 12 --include-linear

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/centered_marginal_padic_filtration_audit.py \
  --only-D -13319 --only-left 4 --only-right 7 \
  --max-cases 1 --max-h 200 --max-abs-D 14000 \
  --max-composite-quotients 20 --max-m 60 --max-n 80 \
  --q-stop 200000 --max-splitting-primes 2 \
  --max-factor-degree 12 --include-linear

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/centered_marginal_padic_filtration_audit.py \
  --only-D -10919 --only-left 4 --only-right 4 \
  --max-cases 1 --max-h 200 --max-abs-D 12000 \
  --max-composite-quotients 20 --max-m 60 --max-n 80 \
  --q-stop 200000 --max-splitting-primes 2 \
  --max-factor-degree 12 --include-linear
```

## Results

For `D=-6719`, `q=6863`, `factor_degree=4`, `pair=(3,7)`:

```text
power:                  Pluecker 6/6,6/6; terms 30; higher degree terms 29
normal_x^1:             Pluecker 6/6,6/6; terms 30; higher degree terms 29
middle Frobenius eigen: Pluecker 6/6,6/6; terms 10; higher degree terms 9
Hermitian orthogonal:   Pluecker 6/6,6/6; terms 6;  higher degree terms 5
window_det=4733, but no initial degree sum equals window_det.
```

For `D=-13319`, `q=13463`, `factor_degree=4`, `pair=(4,7)`:

```text
power:                  Pluecker 4/4,4/4; terms 16; higher degree terms 15
normal_x^1:             Pluecker 4/4,4/4; terms 16; higher degree terms 15
middle Frobenius eigen: Pluecker 4/4,4/4; terms 6;  higher degree terms 5
Hermitian orthogonal:   Pluecker 4/4,4/4; terms 4;  higher degree terms 3
window_det=554, but no initial degree sum equals window_det.
```

For the hard nondegenerate row `D=-10919`, `q=11243`,
`factor_degree=12`, `pair=(4,4)`:

```text
power:                  Pluecker 220/220,220/220; terms 6160; higher degree terms 6159
normal_x^1:             Pluecker 220/220,220/220; terms 6160; higher degree terms 6159
middle Frobenius eigen: Pluecker 220/220,220/220; terms 8536; higher degree terms 8535
Hermitian orthogonal:   Pluecker 220/220,220/220; terms 220;  higher degree terms 219
window_det=6470, but no initial degree sum equals window_det.
```

For the asymmetric degree-`12` row `D=-10919`, `q=11243`,
`factor_degree=12`, `pair=(3,4)`:

```text
power:                  Pluecker 66/66,66/66; terms 1386; higher degree terms 1385
normal_x^1:             Pluecker 66/66,66/66; terms 1386; higher degree terms 1385
middle Frobenius eigen: Pluecker 66/66,66/66; terms 1134; higher degree terms 1133
Hermitian orthogonal:   Pluecker 66/66,66/66; terms 66;   higher degree terms 65
window_det=10037, but no initial degree sum equals window_det.
```

For the holdout row `D=-26759`, `q=26903`, `factor_degree=10`:

```text
pair=(7,7):
  power/normal Pluecker 210/210,210/210;
  Hermitian orthogonal terms 210;
  window_det=15660, no initial degree sum equals window_det.

pair=(3,7):
  power/normal Pluecker 45/45,45/45;
  Hermitian orthogonal terms 45;
  window_det=1817, no initial degree sum equals window_det.
```

The degree-`2` row `D=-10919`, `pair=(3,13)` is degenerate in the expected
way: there is only one Pluecker coordinate and one term.

## Consequence

The naive p-adic filtration route is not visible in the small actual-CM
reductions.  Power, normal, and middle-Frobenius bases do not collapse the
Pluecker supports, and the natural degree initial term is not the determinant
modulo `q`; higher Cauchy-Binet layers are nonzero.

The one useful simplification is the Hermitian orthogonal basis.  It replaces:

```text
sum_{S,T} det(A_S) det(B_{S,T}) det(R_T)
```

by the diagonal exterior dot product:

```text
sum_S u_S v_S
```

where `u_S` and `v_S` are Pluecker coordinates in a Hermitian-orthogonal
packet basis.  This is cleaner than the dense two-sided expansion, but in the
hard symmetric row all `220` Pluecker coordinates on both sides are nonzero,
and in the asymmetric degree-`12` row all `66` matched coordinates are
nonzero.  Thus it still needs a selected-prime p-unit/noncancellation theorem.

## Updated Best Form

The p-adic-filtration theorem is still possible only in a stronger form:

```text
construct an explicit p-integral Hermitian orthogonal or self-dual normal
basis, then prove the resulting Pluecker dot product has a unique p-adic unit
initial contribution at the selected ordinary prime.
```

The finite handoff for that exact possible theorem is recorded in:

```text
p24/lean/CenteredHermitianPluckerGate.lean
```

Without that new local basis theorem, computation supports the existing
conclusion: the centered route should target the phase-aware
Schubert/Fitting or full-origin Chow p-unit, not a natural-coordinate
triangularization.
