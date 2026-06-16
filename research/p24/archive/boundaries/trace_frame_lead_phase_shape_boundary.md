# Trace-Frame Leading Phase-Shape Boundary

Date: 2026-06-05

This note tests the next simplest phase-aware explanation for the
single-leading p-unit target:

```text
Xi_lead in K_m Q(zeta_n)^<p>.
```

After the plain-`j` divisor scan failed, the natural follow-up was:

```text
Maybe Norm(Xi_lead) is a low-bidegree function of an oriented edge
(j_i, j_{i+s}).
```

The small moving trace-frame rows say no, at least for the first edge windows
where a simple correspondence proof would be visible.

## Tool

The diagnostic is:

```text
p24/trace_frame_lead_phase_shape_scan.py
```

It computes the leading determinant norm sequence and searches for:

```text
value_i = F(j_i, j_{i+s})
value_i = P(j_i, j_{i+s}) / Q(j_i, j_{i+s})
```

with bounded bidegree.  Random controls preserve the observed origin period,
so a fit caused merely by the `13`-period repetition is not mistaken for a
theorem.

## Representative Moving Row

The main p24-shaped toy row is:

```text
D=-10919, q=11243, h=156, m=4, n=39
factor_degree=12
tensor_factor_degree=6
raw_rank=4 < 6
origin_value_period=13
origin_value_orbit_size=12
distinct_norm_values=13
```

Run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_frame_lead_phase_shape_scan.py \
  --D -10919 --q 11243 --ell 2 --m 4 \
  --factor-index 0 --subdegree 2 --step 1 \
  --max-bidegree 6 --random-trials 6
```

Output:

```text
poly_bidegree=none
rat_bidegree=none
poly_random_hits=0/6
rat_random_hits=0/6
```

The smaller bidegree-4 window also had no fit for:

```text
m=4, step=1
m=4, step=13
m=3, step=1.
```

## Interpretation

The determinant norm definitely has phase structure:

```text
origin_value_period=13
origin_value_orbit_size=12=factor_degree.
```

But this structure is not captured by a low-bidegree function of a single
oriented edge.  Together with:

```text
p24/trace_frame_lead_divisor_support_boundary.md
```

this closes the two easiest visible modular-function explanations:

```text
plain selected j divisor;
single oriented-edge low-bidegree relation.
```

The live proof target therefore remains more algebraic:

```text
prove the determinant-line packet norm Xi_lead is a p-unit
through a crossed-product beta norm, class-field determinant-line identity,
or a Borcherds/modular-unit construction whose principal part explicitly
retains the non-genus packet phase.
```

## Consequence For p24

The single-leading route is still the cleanest denominator-free certificate
surface:

```text
Norm_{K_m Q(zeta_n)^<p> / K_m}(Xi_lead) mod p != 0.
```

This scan only rules out a simple edge-coordinate shortcut.  It supports the
view that any proof beating sqrt scaling must exploit the full packet/crossed
product structure rather than a small rational parametrization of the CM
cycle.
