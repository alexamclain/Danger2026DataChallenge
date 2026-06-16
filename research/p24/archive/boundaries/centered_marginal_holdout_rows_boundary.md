# Centered Marginal Holdout Rows Boundary

Date: 2026-06-06

This note adds one cheap two-stage holdout beyond the original pinned
centered-marginal rows.

## Shape Shortlist

Added:

```text
p24/centered_marginal_shape_shortlist.py
```

This script uses only `qfbclassno` and quotient/component shapes.  It avoids
Hilbert class polynomial construction and splitting-prime searches, producing
small candidate lists for targeted follow-up.

Example shape-only scans:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/centered_marginal_shape_shortlist.py \
  --max-rows 24 --min-h 80 --max-h 600 --max-abs-D 120000 \
  --max-composite-quotients 80 --max-prime-quotients 30 \
  --min-n 8 --max-n 180 --max-m 220 --max-axis-dim 120 \
  --min-possible-left-orbit 4 --min-possible-right-orbits 2 \
  --max-possible-right-orbits 16

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/centered_marginal_shape_shortlist.py \
  --max-rows 24 --min-h 120 --max-h 1200 --max-abs-D 250000 \
  --max-composite-quotients 120 --max-prime-quotients 36 \
  --min-n 10 --max-n 260 --max-m 320 --max-axis-dim 180 \
  --min-possible-left-orbit 6 --min-possible-right-orbits 3 \
  --max-possible-right-orbits 24
```

The second scan finds many shapes of the form:

```text
D=-26759 h=231 m=21 n=11 components=[3,7]
left=7:Lmax6 right=7:Rcount3-3 axis_dim=9
```

Targeted heavy follow-up on that first row found:

```text
D=-26759 h=231 q=26903 m=21 n=11 components=[3,7]
left=7:L3 right=7:R3x2 axis_dim=9 packet_degree=10
```

The broad `polclass` candidate-index searches are still too slow if run
unfiltered; the shape shortlist is the right first-stage tool.

## Leading-Minor Holdout

Command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/centered_marginal_leading_minor_audit.py \
  --only-D -26759 --max-rows 4 --max-cases 1 --max-h 300 \
  --max-abs-D 30000 --max-composite-quotients 40 \
  --max-axis-dim 40 --max-m 40 --max-n 40 --q-stop 40000 \
  --max-splitting-primes 2 --min-factor-degree 1 \
  --max-factor-degree 12 --include-linear
```

Main row:

```text
D=-26759 q=26903 h=231 m=21 n=11 deg=10 comps=[3,7]
(3,7): rank2 leading_det=1817 windows5/5
(7,7): rank6 leading_det=15660 windows1/1
```

Aggregate:

```text
full_rank_applicable_pairs=9
leading_full_pairs=9
full_rank_but_leading_zero_pairs=0
```

This extends the leading-minor sanity check to a row with `packet_degree=10`
and a nontrivial `left=7,right=7` full-rank block.

## Origin Product And Full-Origin Power

For the symmetric pair `(7,7)`:

```text
alpha_zero_count=0
alpha_distinct_count=1
beta_mismatch_count=0
right_values=[15660,15660,15660,15660,15660,15660,15660]
right_product=9636
full_origin_exponent=n*m/right=33
raw_full_origin_power_match=1
normalized_full_origin_power_match=1
```

For the asymmetric pair `(3,7)`:

```text
alpha_values=[1817,26744,13803,14969,9974,17858,21510] repeated three times
alpha_zero_count=0
alpha_distinct_count=7
beta_mismatch_count=0
```

This supports the origin-covariance and full-origin power bridge on a new row.

## P-Adic Filtration Holdout

For `(7,7)`:

```text
power:                Pluecker 210/210,210/210; terms 5250
normal_x^1:           Pluecker 210/210,210/210; terms 5250
middle Frobenius:     Pluecker 210/210,210/210; terms 9294
Hermitian orthogonal: Pluecker 210/210,210/210; terms 210
window_det=15660, no initial degree sum equals window_det.
```

For `(3,7)`:

```text
power:                Pluecker 45/45,45/45; terms 765
normal_x^1:           Pluecker 45/45,45/45; terms 765
middle Frobenius:     Pluecker 45/45,45/45; terms 621
Hermitian orthogonal: Pluecker 45/45,45/45; terms 45
window_det=1817, no initial degree sum equals window_det.
```

This reinforces the previous boundary: Hermitian orthogonalization gives a
clean diagonal Pluecker dot product, but not a sparse or triangular one.

## Unit-Span Holdout

With right-binomial, constant, and small Heegner-fiber units:

Symmetric `(7,7)`:

```text
target_values=[15660,15660,15660,15660,15660,15660,15660]
first_containment_random_rate mod 2 = 0.02
first_containment_random_rate mod 13451 = 0.0
```

This looks special, but the determinant sequence is constant.  It is likely a
symmetric-row artifact, not a p24-like phase formula.

Asymmetric `(3,7)`:

```text
target_values=[1817,26744,13803,14969,9974,17858,21510]
mod 2:     first_containment_rank=7, random_rate=1.0
mod 13451: first_containment_rank=7, random_rate=1.0
```

The p24-like asymmetric row therefore matches the original conclusion: the
small Heegner/unit dictionary recognizes the target only after reaching full
phase-vector rank, i.e. by interpolation.

## Consequence

The new holdout strengthens, rather than changes, the route ranking:

```text
1. leading-minor and origin/full-origin identities survive on an unseen row;
2. natural p-adic filtration still does not appear;
3. elementary plus small-Heegner unit recognition still fails on the
   asymmetric phase-varying row;
4. symmetric constant-sequence positives should not be promoted to p24.
```

The remaining theorem is still the phase-aware centered Schubert/Fitting
orbit-product p-unit, or the equivalent full-origin centered Chow norm p-unit.
