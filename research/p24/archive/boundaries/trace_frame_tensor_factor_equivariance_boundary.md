# Trace-Frame Tensor-Factor Equivariance Boundary

Date: 2026-06-05

This note tests the remaining compression question behind the selected-minor
Fitting theorem.

## Question

After adjoining:

```text
E = F_p(mu_m),
```

one H-packet splits into many scalar-extension tensor factors.  For p24:

```text
tensor_factor_count = gcd(ord_m(p), ord_n(p)) = 70.
```

The selected-minor theorem can always be stated as `70` degree-8 relative
norms, one per tensor factor.  A stronger, cleaner certificate would use one
degree-8 norm if tensor-factor Frobenius transports the fixed leading
determinant by p-unit changes of trivialization:

```text
Delta_lead(i') = unit(i,i') * sigma(Delta_lead(i)).
```

The zero/nonzero statement only needs `unit(i,i')` to be a p-unit.  Equality
of base norms in small rows is stronger evidence that the chosen normal
subfield basis and leading flag are behaving equivariantly.

## Audit

I added:

```text
p24/trace_frame_tensor_factor_equivariance_audit.py
```

It reuses the existing trace-frame CM row builder, but instead of comparing
origins it compares every scalar-extension factor above the same packet
factor.  For each factor it computes:

```text
raw rank;
fixed leading determinant;
base norm of that determinant;
deterministic pivot shape.
```

The important flags are:

```text
zero_status_uniform = all factors have the same zero/nonzero status;
norm_equal          = base determinant norms agree across factors;
pivot_shape_equal   = the fixed leading pivot rule is stable across factors.
```

## Pinned Rows

Full-axis `D=-10919, m=12, n=13`:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_frame_tensor_factor_equivariance_audit.py \
  --only-D -10919 --min-h 1 --max-h 200 --only-m 12 \
  --max-n 200 --max-factor-degree 20 --max-extension-degree 8 \
  --max-tensor-factor-degree 12 --max-top-count 4 \
  --target axis --max-rows 40 --include-linear
```

reported:

```text
subdegree=2: factors_covered=2/2 zero_count=0
             det_norm_distinct=1 pivot_shape_distinct=1
subdegree=3: factors_covered=2/2 zero_count=0
             det_norm_distinct=1 pivot_shape_distinct=1
```

The lower-rank projected targets on the same row:

```text
target=constant_plus_4
target=constant_plus_3
```

also reported:

```text
zero_status_uniform=1
norm_equal=1
pivot_shape_equal=1
```

Two additional compact rows referenced by the local-unit boundary give the
same result:

```text
D=-1559, q=2459, h=51, m=3, n=17:
  subdegree=2 and 4 both have norm_equal=1, pivot_shape_equal=1.

D=-2207, q=2243, h=39, m=3, n=13:
  subdegree=2 and 3 both have norm_equal=1, pivot_shape_equal=1.
```

## Interpretation

This supports the tensor-factor symmetry needed to reduce:

```text
70 degree-8 p-unit targets
```

to:

```text
one degree-8 p-unit target
```

provided the p24 determinant-line construction uses the same p-integral
normal-basis and leading-flag trivialization.

The audit does not prove the theorem.  The tested rows have only two split
tensor factors, and the equality is checked after reducing to compact
finite-field data.  The required p24 theorem is still:

```text
Tensor-factor determinant-line equivariance:
for every scalar-extension factor i and its Frobenius translate i',
Delta_lead(i') is a p-unit multiple of sigma(Delta_lead(i)).
```

The finite zero/nonzero implication from one representative norm plus this
transport theorem is Lean-gated in:

```text
p24/lean/TraceFrameTensorFactorEquivarianceGate.lean
```

Together with the full beta-algebra Fitting theorem:

```text
delta_all in (O_E[Y]/(Y^n - 1))^*,
```

this is the exact route from selected-minor local units to a single
degree-8 norm-compressed certificate.

## Boundary

The audit also explains what would falsify the one-norm compression:

```text
zero_status_uniform=0
```

would kill tensor-factor rank/vanishing symmetry for the fixed leading flag,
and:

```text
pivot_shape_equal=0
```

would warn that factorwise Gaussian pivots are being spliced rather than
descending from a fixed determinant-line section.  No such failure appeared
in the compact rows above.
