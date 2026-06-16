# Trace-Frame Leading Divisor-Support Boundary

Date: 2026-06-05

This note records a small falsification test for the easiest modular-unit
proof of the single-leading p-unit target:

```text
Xi_lead in K_m Q(zeta_n)^<p>.
```

The tested hope was:

```text
Norm(Xi_lead) is already a simple Heegner/cuspidal-supported divisor
as a rational function of the selected j-coordinate.
```

The answer in the small trace-frame rows is no.  The determinant norm does
show the expected Frobenius packet periodicity, but its plain-`j` divisor is
generic or unsupported by small Heegner roots.

## Tool

The diagnostic is:

```text
p24/trace_frame_lead_divisor_support_scan.py
```

For a small CM cycle it:

```text
1. computes the fixed leading trace-frame determinant norm for each origin;
2. interpolates the norm as a rational function of the selected j-value;
3. factors numerator/denominator over F_q by root search;
4. compares numerator roots with the target CM roots and small Heegner roots;
5. reports the additive origin period of the determinant norm sequence.
```

This is not a test of every phase-aware Borcherds product.  It only tests
whether the already-constructed `Xi_lead` scalar has an easy plain-`j`
divisor explanation.

## Dimension-Forced Control

On the pinned full-axis row:

```text
D=-10919, q=11243, h=156, m=12, n=13,
factor_degree=12, tensor_factor_degree=6, raw_rank=6.
```

The determinant acts on the full tensor factor, and its norm is constant
across origins:

```text
distinct_norm_values=1
rational_degree=0
zero_norm_values=0.
```

This is not p24-shaped, because in p24:

```text
raw_rank = 368 << tensor_factor_degree = 5549.
```

## Moving Lower-Rank Rows

The p24-shaped lower-rank analogues from the same CM row move with origin.

Run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_frame_lead_divisor_support_scan.py \
  --D -10919 --q 11243 --ell 2 --m 4 \
  --factor-index 0 --subdegree 2 \
  --max-heegner-abs-D 1000 --max-heegner-h 20
```

Output:

```text
h=156, m=4, n=39
factor_degree=12
tensor_factor_degree=6
raw_rank=4
value_rows=156
zero_norm_values=0
distinct_norm_values=13
origin_value_period=13
origin_value_orbit_size=12
rational_degree=78
numerator_roots=[]
denominator_roots=[]
```

Run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_frame_lead_divisor_support_scan.py \
  --D -10919 --q 11243 --ell 2 --m 3 \
  --factor-index 0 --subdegree 2 \
  --max-heegner-abs-D 1000 --max-heegner-h 20
```

Output:

```text
h=156, m=3, n=52
factor_degree=12
tensor_factor_degree=6
raw_rank=3
value_rows=156
zero_norm_values=0
distinct_norm_values=13
origin_value_period=13
origin_value_orbit_size=12
rational_degree=78
numerator_roots=[668,1175]
denominator_roots=[10074,10481]
numerator_roots_in_target_cm=[]
small_heegner_hits=0/2.
```

A second packet factor in the `m=4` row gives the same shape:

```text
factor_index=1, subdegree=2:
zero_norm_values=0
distinct_norm_values=13
origin_value_period=13
origin_value_orbit_size=12
rational_degree=78
numerator_roots=[3695,8213]
numerator_roots_in_target_cm=[]
small_heegner_hits=0/2.
```

## Interpretation

The period is meaningful:

```text
origin_value_orbit_size = 12 = factor_degree.
```

So the determinant norm is constant on the finite-field Frobenius packet
orbits.  This is exactly what the decomposition-field packet-norm story
predicts, and it supports using `Xi_lead` as a packet-norm object.

But the rational degree:

```text
rational_degree = 78 = h/2
```

and the lack of target-CM or small-Heegner numerator support say that
`Xi_lead` is not a simple low-degree function of `j`.  The easy modular-unit
route is therefore unlikely:

```text
plain j divisor with small Heegner/cuspidal support => Xi_lead p-unit.
```

The viable route must retain phase information: an oriented-edge coordinate,
a crossed-product beta norm, a determinant-line class-field construction, or
a Borcherds product whose principal part sees the non-genus packet phase.

## Consequence For p24

For p24 the single-leading target remains the cleanest denominator-free
surface:

```text
Norm_{K_m Q(zeta_n)^<p> / K_m}(Xi_lead) mod p != 0.
```

This scan supports the packet-norm/descent architecture, but it closes the
naive plain-`j` divisor proof.  The next proof attempt should be explicitly
phase-aware rather than a search for a low-degree rational function of `j`.
