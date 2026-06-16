# Trace-GCD Chow Plain-Divisor Boundary

Date: 2026-06-06

This note records a small actual-CM diagnostic for the easiest divisor
explanation of the trace-GCD Chow norm.

The current theorem target is the orbit Chow/Fitting determinant

```text
Delta(t) = det(P V_t A),
Pi_O = prod_{t in O} Delta(t).
```

A very useful shortcut would be:

```text
Delta_origin(i) = F(j_i)
```

or perhaps

```text
Delta_origin(i) = F(j_i, j_{i+1})
```

for a low-complexity rational function whose divisor is visibly supported on
CM/Heegner reductions.  That would give a plausible low-degree
Borcherds/modular-unit route.

## Audit

The bounded diagnostic is:

```text
p24/trace_gcd_chow_plain_divisor_scan.py
```

It uses the same actual-CM row as the origin-norm power audit and computes the
selected trace-GCD tail-on-kernel determinant over all CM origins.  It then
interpolates the values as a rational function of the plain `j` coordinate
and checks for a low-bidegree expression in the oriented edge
`(j_i,j_{i+1})`.

Command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_chow_plain_divisor_scan.py \
  --random-controls 1 \
  --max-edge-bidegree 4 \
  --max-heegner-abs-D 1000 \
  --max-heegner-h 20
```

Output summary:

```text
D=-13319
q=13463
h=140
m=28
n=5
pair=(4,7)
factor_degree=4
extension_degree=6

omitted=0
  value_rows=140
  zero_values=0
  distinct_values=7
  origin_value_period=7
  polynomial_degree=139
  rational_degree=70
  random_polynomial_degree_mean=139.000
  random_rational_degree_mean=70.000
  numerator_roots=[]
  denominator_roots=[]
  first_edge_polynomial_bidegree_leq_4=None
  first_edge_rational_bidegree_leq_4=None
```

## Interpretation

The determinant is not random in origin: it has only seven values and period
seven, matching the right-component structure already seen in

```text
p24/lang_trace_gcd_origin_norm_power_audit.py
```

But as a function of the plain CM root `j_i`, its interpolation degree is
exactly random-sized in this row:

```text
polynomial degree = 139 out of 140 samples,
rational degree = 70, same as the random control.
```

The oriented edge test also finds no expression of bidegree at most four.
Thus the visible period-seven structure is not explained by a low-degree
plain-`j` or one-edge formula.

This does **not** disprove a Borcherds/local-intersection proof.  It says that
such a proof must construct the phase-aware Chow/Fitting divisor itself.  The
surviving theorem remains:

```text
the pulled-back right-orbit Chow divisor has a p-integral class-field,
Borcherds, or Fitting section whose p24 selected CM value is a p-unit.
```

The result also sharpens the role of computation here: small actual-CM data
is useful for killing simple recognition hypotheses, but it is not a
substitute for the missing determinant-level p-unit theorem.
