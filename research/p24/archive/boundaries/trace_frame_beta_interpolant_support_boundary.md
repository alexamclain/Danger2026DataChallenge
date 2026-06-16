# Trace-Frame Beta Interpolant Support Boundary

Date: 2026-06-05

This note records a small support scan for the beta-shifted determinant
sequence:

```text
D_beta = Delta_lead(theta^(-beta)).
```

The unique cyclic interpolant

```text
f(Y) mod (Y^n - 1),        f(theta^(-beta)) = D_beta
```

is not the desired p24 certificate payload, but its support pattern is useful
for theorem search.  A uniformly sparse full-leading interpolant would suggest
a direct class-field identity; dense support would push the proof back to a
Fitting/norm p-unit theorem.

## Script

```text
p24/trace_frame_beta_interpolant_support_scan.py
```

This is a cheaper companion to:

```text
p24/trace_frame_beta_product_resultant_audit.py
```

It interpolates the determinant sequence and reports coefficient support,
Frobenius-orbit support, subfield support, and seed ranks, but it does not
construct the full cyclic resultant determinant.

## Pinned m=12 Row

Command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_frame_beta_interpolant_support_scan.py \
  --only-D -10919 --min-h 1 --max-h 200 --max-n 200 \
  --max-m 40 --max-factor-degree 20 --max-extension-degree 8 \
  --max-tensor-factor-degree 12 --max-top-count 4 \
  --include-linear --only-m 12 \
  --target constant_plus_4 --target constant_plus_3
```

The full leading rows had:

```text
coeff_orbits = 3
coeff_orbit_support = 2
support = 7 or 12 out of n=13
```

The residual-tail rows were often denser:

```text
coeff_orbit_support = 3
support = 13 out of n=13
```

For the same row with `target=axis`, the full leading determinant was
beta-constant:

```text
support = 1
coeff_orbit_support = 1
value_orbit_constants = 3
```

while the residual-tail determinant was dense:

```text
support = 13
coeff_orbit_support = 3.
```

This beta-constant case is dimension-saturated: the selected leading
projection covers the entire toy tensor factor (`raw_rank = target_dim`).
That is not the p24 geometry.

## Broader Compact Axis Sweep

Command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_frame_beta_interpolant_support_scan.py \
  --max-abs-D 50000 --min-h 24 --max-h 220 \
  --max-n 100 --max-m 30 --max-factor-degree 20 \
  --max-extension-degree 6 --max-tensor-factor-degree 12 \
  --min-tensor-factor-count 1 --max-top-count 4 \
  --max-cases 8 --include-linear --require-composite-m \
  --target axis
```

Most `m=6,n=5` dimension-saturated rows showed:

```text
full support = 1
tail support = 5.
```

But the `m=6,n=7` partial row showed the boundary:

```text
subdegree=2:
  full support = 7
  tail support = 7

subdegree=3:
  full support = 6
  tail support = 7
```

So full-leading support can be smaller than tail support, but it is not
uniformly sparse once the selected leading projection is genuinely partial.

## p24 Consequence

The p24 leading trace frame is partial:

```text
target_dim = 3 * 179 = 537
axis_dim = 368
relative_degree = 31
top_count = 3
```

Thus the dimension-saturated beta-constant toy does not transfer.  The scan
rules out a naive support-compressed interpolant theorem as the p24
certificate engine.

The surviving use of support structure is weaker:

```text
the full leading determinant-line has more semilinear structure than
basis-dependent residual-tail determinants.
```

That supports keeping `delta_all = det(T_lead,all)` as the canonical
Fitting/norm object, but the proof still has to show p-unitness of the
selected determinant-line norm rather than merely sparse support.
