# Tensor Factor Relative Coefficient Profile

This note records a boundary test for proving the top-coefficient theorem by a
simple degree or triangular-support argument.

The audit script is:

```text
p24/tensor_factor_relative_coefficient_profile.py
```

It computes, for small tensor rows, the relative `C`-coefficients of:

```text
g'(theta) * R_s(theta)
```

in the basis:

```text
1, theta, ..., theta^(relative_degree-1).
```

If the adjusted axis elements were supported only in a few relative degrees,
or had a triangular component support pattern, the p24 theorem might reduce to
a plain degree-bound argument.  If they have full support, the theorem remains
a genuine rank/directness statement about the leading coefficient maps.

## Current Status

The small-row profile should be checked before claiming a zero-lemma proof of
the top-coefficient certificate.  In the `D=-10919` row, use:

```text
PYTHONPATH=p24 python3 p24/tensor_factor_relative_coefficient_profile.py \
  --only-D -10919 --min-h 1 --max-h 200 --only-m 12 \
  --max-n 200 --max-factor-degree 20 --max-extension-degree 8 \
  --max-tensor-factor-degree 12
```

The expected useful distinction is:

```text
sparse/triangular support  => possible degree-bound proof route,
full support               => no naive degree-bound proof.
```

Pinned output:

```text
D=-10919, m=12, subdegree=3, relative_degree=2
target=axis coeff_ranks=[3,3]
support_sizes=[2,2,2,2,2,2]
full_support_rows=6/6
```

and for subdegree `2`, relative degree `3`:

```text
target=axis coeff_ranks=[2,2,2]
support_sizes=[3,3,3,3,3,3]
full_support_rows=6/6
```

So the adjusted toy rows have full relative support.  This rules out the
simple triangular-support proof shape in the small analogue.  The leading
coefficient theorem remains a genuine rank/directness statement.
