# Centered Marginal Rank Stress Audit

This note records the first actual-CM rows that stress the centered
base-field marginal theorem beyond left orbit length `2`.

## Candidate Index

Added:

```text
p24/centered_marginal_candidate_index.py
```

It first scans class numbers with `qfbclassno`, quotient shapes `h=m*n`, CRT
components, and Frobenius orbit lengths before building heavy CM packet data.
The first useful candidates included:

```text
D=-13319 h=140 q=13463 m=28 n=5 components=[4,7]
left=7:L3 right=4:R2

D=-6719 h=105 q=6863 m=21 n=5 components=[3,7]
left=7:L6 right=7:R6
```

Broader candidate searches with `n>=8` were stopped at the Hilbert-polynomial
splitting stage once they became slower than their theorem-shaping value.  The
right workflow is now two-stage:

```text
1. use qfbclassno/divisor shapes to shortlist D,h,m,n;
2. run polclass/splitting only on a very small hand-picked shortlist.
```

The first stage is now executable as:

```text
p24/centered_marginal_shape_shortlist.py
```

It found the later holdout shape `D=-26759, h=231, m=21, n=11`,
`components=[3,7]`; targeted splitting then produced `q=26903` with packet
degree `10`.  The holdout audits are summarized in:

```text
p24/centered_marginal_holdout_rows_boundary.md
```

## Full Left-Orbit Stress Row

For `D=-6719`, the nontrivial left characters modulo `7` form one orbit of
length `6`, so this row exercises the same base-field rank equivalence used
for p24:

```text
centered_base_rank_applicable_tests=4
centered_base_profile_rank_mismatches=0
max_left_orbit_len=6
```

The key rows are:

```text
(7,3)[1]: L=6, transformed_rank=2, base_rank=2, full=0
(7,7)[1]: L=6, transformed_rank=4, base_rank=4, full=0
```

The failure is explained by packet degree:

```text
n=5, hermitian packet degree=4 < left orbit length=6.
```

Thus this is not a counterexample to the p24 theorem, where the packet degree
`388430` is far larger than `156`.  It is a useful sanity check: the base-rank
form sees the obvious dimension obstruction.

The new Delsarte delete-one diagnostic reports:

```text
delete_one_full_left_span_tests=0
max_delete_one_min_transformed_rank=0
```

This is expected here because the stressed right components have only one
right Frobenius orbit; deleting it removes all right information.

## Normal-Coordinate Boundary

The same `D=-6719` row also kills a too-weak normal-coordinate proof:

```text
centered_profile_max_single_normal_rank=6
centered_profile_stability_defect=2
full=0
```

So individual centered-profile values can be normal over `F_q` while their
span is not Frobenius-stable and does not fill the left field.  A normal-frame
proof must first prove stability of the whole profile span, not merely find a
normal coordinate.

## Positive Small Stress Row

For `D=-13319`, the row with `left=7` has left orbit length `3` and packet
degree `4`; all tested mixed profiles are full:

```text
max_left_orbit_len=3
max_centered_right_profile_rank=3
centered_profile_rank_mismatches=0
centered_profile_stability_defect=0
full_left_span_tests=8
delete_one_full_left_span_tests=5
delete_one_annihilator_degree_mismatches=0
delete_one_annihilator_vanish_failures=0
delete_one_zero_residual_norms=0
delete_one_full_field_annihilator_all_tests=5
delete_one_leading_full_tests=5
delete_one_leading_annihilator_degree_mismatches=0
delete_one_leading_annihilator_vanish_failures=0
delete_one_leading_zero_residual_norms=0
delete_one_leading_full_field_annihilator_all_tests=5
delete_one_prefix_full_block_full_all_tests=8
delete_one_prefix_tail_full_all_tests=5
delete_one_prefix_full_block_zero_residual_norms=0
delete_one_prefix_full_block_norm_products_missing=0
delete_one_prefix_tail_zero_residual_norms=0
delete_one_prefix_tail_norm_products_missing=0
centered_trace_support_checked_tests=2
centered_trace_zero_support_tests=0
centered_trace_one_support_tests=0
min_centered_trace_right_orbit_support=2
```

This gives a small nontrivial actual-CM check of the centered-profile and
subspace-polynomial equivalences beyond left degree `2`.  The checked
trace-support cases also match the stronger Delsarte/delete-one support
candidate: no nonzero left twist was supported on zero or one right orbit.

The full delete-one cases show leading pivot prefixes:

```text
(7,7): deletepivotprefixes [[0,1,2], [0,1,2]]
(4,7): deletepivotprefixes [[0,1], [0,1]]
```

Origin shifts `1,2,3,4` preserve the aggregate delete-one counts, and the
checked shifted verbose row preserves these leading prefixes in the full
delete-one cases.  This suggests a deterministic p24 certificate candidate:
for each deleted right orbit, use the first `156` Lang/trace-dual coordinates
from the remaining five orbits as the Moore minor.

The prefix split diagnostics also behave as expected in this small row:
whenever the leading delete-one prefix is full, the full-block prefix and tail
augmentation are both full.  For p24 the analogous split is `140+16`.
The quotient-tail residual products are nonzero and base-field-valued in the
checked row, giving the small-row analogue of the p24 `16 x 16` quotient
p-unit.
The full-block residual products are also nonzero/base-field-valued, so the
small-row leading determinant is already split into the two intended factors.

## Consequence

The p24 base-field theorem should include an explicit dimension hypothesis:

```text
packet_degree >= left_degree.
```

For p24 this is overwhelmingly satisfied:

```text
388430 >= 156.
```

The remaining nontrivial theorem is still:

```text
rank_Fp centered_marginal_{157,211} = 156.
```

But the stress rows clarify three boundaries:

```text
1. full rank can fail for dimension reasons in small packets;
2. normal coordinates alone do not prove full span without Frobenius stability.
3. delete-one support requires at least two right Frobenius orbits, so the
   one-orbit boundary rows are controls rather than p24 analogues.
```
