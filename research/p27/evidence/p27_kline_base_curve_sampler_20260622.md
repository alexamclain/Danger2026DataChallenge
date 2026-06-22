# P27 K/A Base-Curve Sampler Probe

Date: 2026-06-22

## Claim

The explicit K/A base curve is real but not yet a practical source sampler.
Over the promotion fields it has exactly `q` affine `(K,A)` points, while the
actually realized label-2/compactD legal source is only a small sparse subset:

```text
q1607: realized d2 K/A = 49 / 1607
q1847: realized d2 K/A = 63 / 1847
q2087: realized d2 K/A = 57 / 2087
```

All realized legal points lie on the base curve, but the base curve contains
many non-legal points.  Simple squareclass atom products do not identify the
legal subset.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_kline_base_curve_sampler_probe.py
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_kline_base_curve_sampler_probe_q607_smoke_20260622.txt
research/p27/archive/probe_outputs/p27_kline_base_curve_sampler_probe_q1607_q1847_q2087_20260622.txt
research/p27/archive/probe_outputs/p27_ka_base_curve_q607_magma_20260622.txt
```

Commands:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_kline_base_curve_sampler_probe.py \
  --small-primes 607 \
  --max-weight 4 \
  --top 8 \
  | tee research/p27/archive/probe_outputs/p27_kline_base_curve_sampler_probe_q607_smoke_20260622.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_kline_base_curve_sampler_probe.py \
  --small-primes 1607,1847,2087 \
  --max-weight 4 \
  --top 10 \
  | tee research/p27/archive/probe_outputs/p27_kline_base_curve_sampler_probe_q1607_q1847_q2087_20260622.txt
```

## Tested Base Curve

The enumerated base curve is:

```text
64(A-2)^2(A+2)L^2 + 64(A+2)(A+14)(3A+10)L - (A-2)^4 = 0,
L = K^2.
```

The probe solves the quadratic in `L`, takes square roots `K^2=L`, and compares
the resulting `(K,A)` points with the actual legal label-2/compactD candidates.

Online Magma follow-up:
[P27 K/A Base-Curve Magma Validation](p27_ka_base_curve_magma_validation_20260622.md).
Over q607, Magma independently confirms:

```text
base_KA = 607
B-chart KA = 604
base points outside nondegenerate B chart = 3
B-chart points outside base = 0
B-chart rooted rows = 1208
equation/discriminant mismatches = 0
```

This confirms that the K/A base model and B rationalization are clean; the
remaining obstruction is the additional legal/d3 cover over the base.

## Counts

Smoke:

```text
q607:
  base_KA = 607
  realized_d2_KA = 32
  realized_d2_in_base = 32
  realized_d2_missing_from_base = 0
  realized_d3plus_KA = 16
  realized_d3plus_in_base = 16
```

Promotion fields:

```text
q1607:
  base_KA = 1607
  realized_d2_KA = 49
  realized_d2_in_base = 49
  realized_d2_missing_from_base = 0
  realized_d3plus_KA = 28
  realized_d3plus_in_base = 28

q1847:
  base_KA = 1847
  realized_d2_KA = 63
  realized_d2_in_base = 63
  realized_d2_missing_from_base = 0
  realized_d3plus_KA = 45
  realized_d3plus_in_base = 45

q2087:
  base_KA = 2087
  realized_d2_KA = 57
  realized_d2_in_base = 57
  realized_d2_missing_from_base = 0
  realized_d3plus_KA = 25
  realized_d3plus_in_base = 25
```

The realized `d2` fractions are:

```text
q1607: 49 / 1607 = 0.03049
q1847: 63 / 1847 = 0.03411
q2087: 57 / 2087 = 0.02731
```

The realized `d3-plus` fractions are even smaller:

```text
q1607: 28 / 1607 = 0.01742
q1847: 45 / 1847 = 0.02436
q2087: 25 / 2087 = 0.01198
```

## Atom Screen

The probe tested squareclass products of these atoms up to weight `4`:

```text
K
K+1
K-1
K^2+4
A+2
A-2
A+6
A+14
3A+10
A^2+60A+132
```

No atom product came close to identifying the legal subset.  The best scores
are just the majority classifier caused by the target subset being sparse.

Examples:

```text
q1607 d2:
  target_rows = 49 / 1604 scored rows
  best nontrivial score ~= 0.537

q1847 d2:
  target_rows = 63 / 1844 scored rows
  best nontrivial score ~= 0.534

q2087 d2:
  target_rows = 57 / 2084 scored rows
  best nontrivial score ~= 0.534
```

The same negative pattern holds for the `d3-plus` subset.

## Interpretation

Positive:

```text
The K/A equation is exactly the right base containment: every realized legal
K/A point in the guard fields lies on the base curve.
The base curve is extremely clean: base_KA = q in every tested field.
```

Negative for sqrt beating:

```text
Sampling the base curve would still produce mostly non-legal points.
The legal subset is not an obvious low-weight squareclass stratum of the base
curve.
This does not provide a direct legal-pullback sampler into the recurrence
domain.
```

So the base curve is a good coordinate system for CAS normalization, but not a
standalone source.  The next mathematical object remains the additional legal
cover over this base curve, especially the d3 reverse-root cover over
`P1_Sroot`.

## Continue / Kill

```text
continue = normalize the legal subset/cover over the explicit K/A base curve
continue = use Sroot as the cleaner coordinate for branch/genus extraction
continue = search for a theorem-specified legal cover or gate-coupling law

kill = direct GPU sampling of the K/A base curve
kill = simple squareclass atom products as the legal-subset selector
kill = treating base_KA=q as a source-normalized win
kill = treating B-chart degeneracies as a hidden source shrink
```

```text
p27_kline_base_curve_sampler_rows=1/1
```
