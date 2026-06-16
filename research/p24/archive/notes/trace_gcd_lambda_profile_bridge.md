# Trace-GCD Lambda Profile Bridge

Date: 2026-06-06

## Point

The dual-sparse route is now parameter-level.  The same `lambda` must be seen
in three equivalent finite coordinate systems:

```text
centered profile word:
  f_lambda(s) = Tr_{L/F_p}(lambda * G_s^0)

right Fourier periods:
  S_v = sum_s zeta_211^(v*s) G_s^0

Lang/Fitting coordinates:
  T_i = Lang-trivialized coordinates on each right Frobenius orbit.
```

For the p24 shape, `L = F_p(mu_157)`, and the nonzero right frequencies split
into six Frobenius orbits of length `35`.

## Finite Identities

The parameter bridge is:

```text
DFT_right(f_lambda)_v = Tr_{L R_v / R_v}(lambda * S_v).
```

On each right Frobenius orbit, with Lang Moore matrix `U_O`,

```text
(Tr_{L R_v / R_v}(lambda * S_v))_{v in O}
  = U_O * (Tr_{L/F_p}(lambda * T_i))_i.
```

Since `U_O` is invertible, zero conditions in the right-period vector and in
the Lang trace coordinates are equivalent for the same `lambda`.

The actual-CM audit is:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_lambda_profile_bridge_audit.py
```

Current output on the pinned row and the independent holdout:

```text
profile_dft_mismatches=0
lambda_fourier_trace_mismatches=0
lang_reconstruction_mismatches=0
lang_zero_equivalence_failures=0
```

This is a basis-level check in `lambda`, hence a linear identity check for all
`lambda` in the tested left field.

## Consequence For The Missing Theorem

The frequency-sparse side of the dual-sparse bridge is now honest:

```text
trace-GCD leading-erasure/Fitting failure
  => the same lambda has nonzero right-frequency support
     inside O4 + final19(O1), size 54.
```

The remaining unproved theorem is exactly:

```text
For the p24 selected ordinary CM point, if nonzero lambda causes the
representative trace-GCD leading-erasure/Fitting failure, then
f_lambda(s) is constant on the selected 157-term cyclic interval.
```

After cyclic differencing, that gives time support:

```text
211 - 157 = 54.
```

Together with the frequency support `35 + 19 = 54`, the Lean uncertainty gate
closes the contradiction:

```text
54 + 54 < 212.
```

## What This Rules Out

The bridge is not a rowspace identity and not a generic plateau-subspace
support statement.  The existing negative controls still apply:

```text
direct time-difference rowspace equality with Lang trace words is false;
the 54-dimensional plateau subspace touches all seven right factors;
ordinary cyclic-code/MDS shortcuts do not prove the selected p-unit.
```

So the next proof step must use the actual CM construction to prove plateau
vanishing for the bad `lambda`, not a general finite-code theorem.

## Rowspace Form

The bad-lambda-to-plateau bridge can be written as a rowspace containment.
Let:

```text
B_leading(lambda) = selected leading Lang/Fitting coordinates,
C_plateau(lambda) = (f_lambda(1)-f_lambda(0), ..., f_lambda(156)-f_lambda(0)).
```

Then:

```text
bad lambda => plateau
```

is exactly:

```text
ker(B_leading) subset ker(C_plateau)
```

or equivalently:

```text
rowspace(C_plateau) subset rowspace(B_leading).
```

The small-row audit is:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_lambda_plateau_rowspace_audit.py
```

Current output:

```text
rowspace_containment_failures=0
nonvacuous_containments=0
vacuous_full_leading_rank=10/10
```

So the tested actual-CM rows have no bad lambda at all.  They support the
leading p-unit, but they do not prove the rowspace bridge identity.  A
nonvacuous proof would need to show the rowspace containment before knowing
`B_leading` has full rank.

The broader centered-profile audit also found support-one actual-CM controls:

```text
centered_trace_one_support_tests=4
min_centered_trace_right_orbit_support=1
```

Thus the older strengthening "every nonzero lambda uses at least two right
orbits" is false in nearby geometries.  The p24 theorem must remain the
selected six-orbit/leading-erasure p-unit statement, or prove the rowspace
bridge for the actual selected ordinary p24 CM point.

## Determinant-Line Ratio Boundary

When both `B_leading` and `C_plateau` are square and full-rank, one can form:

```text
det(B_leading) / det(C_plateau).
```

The small audit is:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_lambda_plateau_det_ratio_audit.py
```

On the full-left-orbit holdout it reports:

```text
both_nonzero=2/2
rowspace_equal=2/2
distinct_nonzero_ratios=2
```

The two omitted-orbit ratios are different.  Thus there is no obvious
universal scalar comparison between the leading-erasure determinant and the
plateau determinant.  A proof may still compare determinant lines, but it must
use the actual arithmetic/Fitting section; it is not a fixed finite change of
basis visible from the small rows alone.

## Nonvacuous Search Status

A bounded search for a genuinely nonvacuous small actual-CM rowspace test is
recorded in:

```text
p24/trace_gcd_nonvacuous_rowspace_search_status.md
```

It found low-rank controls, but the clean failures were explained by
dimension loss after deleting a right orbit, while the enough-coordinate
rank-deficient row had noncoprime left/right orbit degrees.  Thus the current
p24-shaped small rows still only support the leading p-unit route vacuously;
they do not yet test `rowspace(C_plateau) subset rowspace(B_leading)` as an
independent theorem.
