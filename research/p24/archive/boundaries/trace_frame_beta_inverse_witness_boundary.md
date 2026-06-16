# Trace-Frame Beta Inverse-Witness Boundary

Date: 2026-06-05

This note tests a tempting certificate for the full beta-algebra Fitting unit.

## Question

If:

```text
delta_all in A_all = B[Y]/(Y^n - 1)
```

is a unit, one could certify it by carrying a literal inverse:

```text
u(Y) * delta_all(Y) = 1 mod (Y^n - 1).
```

For p24, this would be an inverse polynomial with:

```text
n = 3107441
```

coefficients in:

```text
B/E,       [B:E] = 5549.
```

So one literal inverse costs:

```text
n * 5549 = 17243190109 E-entries
94147817995140 Fp slots
94.14781799514 * sqrt(p).
```

This is already above the target scale before any duplication across
tensor-factor representatives.  Still, a small-row audit is useful: maybe the
inverse has sparse support or descends to a smaller subfield.

## Audit

I added:

```text
p24/trace_frame_beta_inverse_witness_audit.py
```

It computes the beta interpolant for `D_beta`, interpolates the pointwise
inverse sequence `1/D_beta`, and verifies:

```text
f(Y) * f_inv(Y) = 1 mod (Y^n - 1).
```

It reports:

```text
support:          nonzero coefficients of f;
inv_support:      nonzero coefficients of f_inv;
inv_E_coeffs:     inverse coefficients that lie in E;
inv_orbit_support coefficient-orbit support under E-Frobenius.
```

## Results

Pinned `D=-10919, m=12, n=13`:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_frame_beta_inverse_witness_audit.py \
  --only-D -10919 --min-h 1 --max-h 200 \
  --max-n 200 --max-m 40 --max-factor-degree 20 \
  --max-extension-degree 8 --max-tensor-factor-degree 12 \
  --max-top-count 4 --include-linear --only-m 12 \
  --target axis --target constant_plus_4 --target constant_plus_3
```

The degenerate full-axis rows have constant beta determinant values because
the tiny row spans the whole tensor factor:

```text
target=axis, kind=full:
  distinct=1 support=1 inv_support=1.
```

That is not the p24 regime, where:

```text
raw_rank = 368 << 5549 = [B:E].
```

The proper tail/projected rows are dense.  Examples:

```text
target=axis, subdegree=2, kind=tail:
  distinct=13 support=13 inv_support=7 inv_orbit_support=2/3.

target=constant_plus_4, subdegree=2, kind=tail:
  distinct=13 support=13 inv_support=13 inv_orbit_support=3/3.

target=constant_plus_3, subdegree=2, kind=full:
  distinct=13 support=12 inv_support=13 inv_orbit_support=3/3.
```

The compact bridge rows show the same pattern:

```text
D=-1559, q=2459, h=51, m=3, n=17:
  inv_support=17 in every full/tail row;
  inv_orbit_support=3/3 in every row.

D=-2207, q=2243, h=39, m=3, n=13:
  inv_support=13 in every full/tail row;
  inv_orbit_support=3/3 in every row.
```

All rows checked:

```text
2026-06-08 pinned rerun rows=12
inverse_identity=1.
```

The axis-tail inverse is smaller in this toy (`inv_support=7`) because the
full-axis row is dimension-forced (`raw_rank=6` equals the tensor-factor
degree).  The component rows, which better model a proper selected subspace,
still use every coefficient orbit and usually every beta coefficient.

## Consequence

The literal inverse/Bezout certificate is the wrong asymptotic object.  In
the nondegenerate compact rows, the inverse is dense in beta and uses every
coefficient orbit.  It also does not descend to `E[Y]`:

```text
inv_E_coeffs << n
```

in the dense rows.

This closes another finite-certificate shortcut:

```text
prove delta_all is a unit by carrying a sparse inverse in B[Y]/(Y^n - 1).
```

The surviving certificate surface is still the reduced-norm/Fitting theorem:

```text
Norm_{A_all/E}(delta_all)
  = D_0 * product_{Omega != 0} R_lead,Omega
```

or its degree-8 determinant-line descent.  A scalar norm value and inverse in
`E` is sub-sqrt; the literal inverse polynomial in `B[Y]/(Y^n-1)` is not.  The
inverse witness is useful only as a local algebra proof object after the
p-unit theorem is known.

2026-06-08 Lean bridge: `TraceFrameBetaResultantGate.lean` now records this
distinction as
`no_harmful_from_global_reduced_norm_inverse_payload`.  A scalar global norm
payload proves all beta trace frames good under the reduced-norm/product
zero-detection hypotheses; it does not require carrying the dense inverse
polynomial.
