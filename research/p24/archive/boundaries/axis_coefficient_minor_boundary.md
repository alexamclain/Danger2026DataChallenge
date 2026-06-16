# Axis Coefficient-Minor Boundary

This note records a tempting alternative to the Hermitian axis Gram
determinant.

## Candidate

For each packet factor `f_a`, write the axis images in the power basis of

```text
A_a = F_p[X]/(f_a).
```

If the first `dim(W_axis)` coordinate columns of these images have full rank,
then the coordinate projection

```text
W_axis -> A_a -> F_p^dim(W_axis)
```

is injective, hence the full axis map is injective.  In Lean this is the
new generic gate:

```text
p24/lean/AxisInjectivityGate.lean
theorem injective_from_projected_eval
```

For p24 this would replace the Hermitian `368 x 368` trace-Gram determinant
by a `368 x 368` coordinate minor in each packet.

## Data

I added:

```text
p24/axis_coefficient_minor_audit.py
```

Small non-origin scan:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/axis_coefficient_minor_audit.py \
  --max-cases 12 --min-h 12 --max-h 160 --max-abs-D 50000 \
  --max-prime-quotients 8 --max-composite-quotients 8 \
  --min-n 3 --max-n 160 --q-stop 500000 \
  --max-splitting-primes 2 --max-axis-dim 65 \
  --include-linear --summary-only
```

reported:

```text
rows=30
full_axis_rows=30
leading_full_rows=30
full_axis_leading_failure_rows=0
max_pivot_max=2
```

Composite scan:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/axis_coefficient_minor_audit.py \
  --max-cases 20 --min-h 12 --max-h 220 --max-abs-D 120000 \
  --max-prime-quotients 12 --max-composite-quotients 16 \
  --min-n 3 --max-n 220 --q-stop 900000 \
  --max-splitting-primes 2 --max-axis-dim 90 \
  --include-linear --require-composite-m
```

reported `18/18` full leading minors, with the displayed rows all having
pivots exactly:

```text
0,1,2,3
```

for `m=6`, axis dimension `4`.

Targeted all-origin scans on the first genuinely multidimensional CRT rows
also stayed nonzero:

```text
D=-8711,  h=132, m=12=4*3, n=11: rows=264, leading_full_rows=264
D=-10919, h=156, m=12=4*3, n=13: rows=312, leading_full_rows=312
```

For `D=-8711`, the small determinant tracker saw:

```text
leading_det_values_seen=264
distinct_leading_det_values=44
zero_leading_det_values=0
```

The first 20 origins for `q=8747` already had 20 distinct nonzero determinant
values.

Broader composite all-origin run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/axis_coefficient_minor_audit.py \
  --max-cases 16 --min-h 12 --max-h 180 --max-abs-D 70000 \
  --max-prime-quotients 10 --max-composite-quotients 10 \
  --min-n 3 --max-n 180 --q-stop 700000 \
  --max-splitting-primes 2 --max-axis-dim 75 \
  --include-linear --scan-origins --require-composite-m --summary-only
```

reported:

```text
rows=444
full_axis_rows=444
leading_full_rows=444
full_axis_leading_failure_rows=0
max_pivot_max=3
leading_det_values_seen=444
distinct_leading_det_values=52
zero_leading_det_values=0
```

## Boundary

This route is not currently a replacement for the Hermitian p-unit theorem.

First, these are coordinates after reduction modulo the packet factor `f_a`.
For p24 the reduction from degree `n-1` to degree `388430-1` folds high
coefficients into the displayed coordinate window.  So the leading coordinate
minor is not just a short prefix of raw CM fiber sums; constructing it still
requires packet-level embedded class data.

Second, unlike the Hermitian determinant, the leading coordinate minor is not
origin-invariant.  The determinant can stay nonzero across origins while
taking many different values.  That makes it a plausible selected-coordinate
certificate but a less natural class-field norm target.

The origin action is separated in:

```text
p24/axis_minor_origin_action_audit.py
p24/axis_minor_origin_action_boundary.md
```

Pure `alpha` origin shifts are only unimodular axis-basis changes.  Pure
`beta` shifts multiply the axis subspace by `X^(-beta)` before leading
projection, so the invariant-looking version of this route is a cyclic
consecutive-Pluecker condition for all relevant monomial shifts.

The useful conclusion is narrower:

```text
coordinate-minor nonzero => axis injectivity
```

is now Lean-gated and empirically strong in small data.

I also checked the Cauchy-Binet bridge to the Hermitian determinant in:

```text
p24/plucker_trace_form_audit.py
p24/plucker_trace_form_boundary.md
```

For the first extra-dimensional row `D=-8711`, `factor_degree=10`,
`axis_dim=6`, all `210` Pluecker coordinates are nonzero and `5040`
off-diagonal trace-form terms contribute.  So the leading minor is not
currently a proof of the Hermitian p-unit theorem.

The best invariant arithmetic theorem remains

```text
p does not divide Norm_{M^+/Q}(Delta_axis).
```
