# Tensor Factor Block Directness

This note refines the one-factor tensor theorem into component blocks.

## Setup

Inside one tensor factor

```text
B_i / E,       E = F_p(mu_m),
```

the axis K-character frequency set is the disjoint union

```text
S_axis = {0} ∪ S_2 ∪ S_157 ∪ S_211.
```

For p24 the block sizes are:

```text
constant: 1
2-axis:   1
157-axis: 156
211-axis: 210
total:    368
```

The factor degree is:

```text
[B_i:E] = 5549,
```

so every component block and every pair with the constant block is
dimensionally possible.

## Audit

I added:

```text
p24/k_character_tensor_factor_block_scan.py
```

It factors `f` over `E=F_q(mu_m)`, selects one irreducible tensor factor, and
checks:

```text
1. internal rank of each component block;
2. directness of constant + each one component block;
3. full directness of all axis blocks.
```

Pinned dimension-possible row:

```text
D=-10919, q=11243, h=156, m=12, n=13
deg(f)=12, [E:F_q]=2, factor_degree=6, axis_dim=6

block_ranks=[
  ('constant', 1, 1),
  ('4',        3, 3),
  ('3',        2, 2)
]
block_fail=0
pair_fail=0
full_fail=0
```

Pinned dimension-bound row:

```text
D=-8711, q=8747, h=132, m=12, n=11
deg(f)=10, [E:F_q]=2, factor_degree=5, axis_dim=6

block_ranks=[
  ('constant', 1, 1),
  ('4',        3, 3),
  ('3',        2, 2)
]
block_fail=0
pair_fail=0
full_fail=1
```

Here only the full axis rank fails, and only because `factor_degree=5 <
axis_dim=6`.

Broader small window:

```text
rows=20
one_factor_dimension_possible_rows=2
block_internal_failure_rows=17
block_internal_unforced_failure_rows=0
pair_directness_failure_rows=18
pair_directness_unforced_failure_rows=0
full_directness_failure_rows=18
dimension_possible_block_failure_rows=0
dimension_possible_pair_failure_rows=0
dimension_possible_full_failure_rows=0
```

Thus every observed block or pair failure was dimension-forced.  No
dimension-possible component-normality, pair-directness, or full-directness
failure appeared.

## Theorem Shape

The p24 one-factor determinant can now be stated as the following direct-sum
theorem inside any tensor factor `B_i`:

```text
E·R_0 ⊕ span_E{R_s : s in S_2}
      ⊕ span_E{R_s : s in S_157}
      ⊕ span_E{R_s : s in S_211}
```

is a direct sum, with each component block internally full rank.

This is the tensor-factor version of the earlier axis module direct-sum gate.
The existing Lean file

```text
p24/lean/AxisModuleDirectSumGate.lean
```

checks the finite implication from component kernels plus directness to axis
injectivity.  The arithmetic work remains proving the selected-prime
directness in the degree-5549 tensor factor.

## Boundary

This still does not factor the determinant into independent component
determinants: cross-component directness is a genuine extra condition.  The
useful improvement is that the theorem is now a structured class-field tower
statement over the smooth layers `2`, `157`, and `211`, not a generic
368-vector rank assertion.

There is also no internal K-eigenspace shortcut inside one tensor factor.  The
boundary is recorded in:

```text
p24/tensor_factor_k_action_boundary.md
```

In the row `D=-8711`, six nonzero axis character resolvents with distinct
K-labels live in a degree-5 tensor factor and have total rank `5`.  If the
K-action were an internal `E`-linear diagonal action on that factor, distinct
eigenvalues would force rank `6`.  Thus the component directness theorem is a
real p-unit/rank statement, not a formal eigenspace consequence.
