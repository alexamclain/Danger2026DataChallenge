# Tensor Factor Top-Coefficient Block Split

This note records the current component-level form of the top-coefficient
certificate.

## Coefficient Maps

Let:

```text
B/C,        [B:C] = 31,
C/E,        [C:E] = 179,
B = C(theta),
```

and let `g` be the minimal polynomial of `theta` over `C`.

For `x in B`, define:

```text
Top_k(x) =
  the top k C-coefficients of g'(theta) * x
  in the C-basis 1, theta, ..., theta^30.
```

Then:

```text
Top_k(x) = 0
  iff Tr_{B/C}(theta^i x) = 0 for 0 <= i < k.
```

So `Top_3` is exactly the twisted trace-frame certificate.

## p24 Dimension Split

The accounting script is:

```text
p24/tensor_factor_top_coefficient_capacity.py
```

It reports:

```text
dim_E C = 179
dim(constant + 2 + 157) = 158
dim(211) = 210
dim(full axis) = 368
```

Therefore the dimensionally natural targets are:

```text
Top_1 injective on constant + 2 + 157,
Top_2 injective on the 211 block,
Top_3 injective on the full axis direct sum.
```

The last line is still the full theorem.  The first two are component
normality targets inside a much smaller coefficient space.

## Small Analogue

The dual-basis audit now includes component, pair, and prefix targets:

```text
p24/tensor_factor_dual_basis_window_audit.py
```

On the pinned `D=-10919, m=12` row with subdegree `3`, the audit reports:

```text
target=4                size=3   window=[3,3]
target=constant_plus_3  size=3   window=[3,3]
target=constant_plus_4  size=4   window=[3,4]
target=axis             size=6   window=[3,6]
```

This matches the capacity rule: one top coefficient gives rank at most `3`;
targets of size `4` or `6` need two windows.

The same `D=-10919` run over the nearby `m=3,4,12` quotient rows reported:

```text
rows=5
trace_window_rank_mismatch_targets=0
axis_rows_full_by_tested_window=5
```

and every displayed component/pair/prefix target filled exactly when the
window capacity reached its dimension.

A broader bounded run, still keeping only toy-sized tensor factors,

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/tensor_factor_dual_basis_window_audit.py \
  --max-rows 8 --max-cases 8 --max-h 220 --max-abs-D 50000 \
  --max-n 220 --max-m 48 --max-factor-degree 60 \
  --max-extension-degree 12 --max-tensor-factor-degree 24 --max-windows 4
```

reported:

```text
rows=8
trace_window_rank_mismatch_targets=0
axis_rows_full_by_tested_window=8
max_rank_profile_tests=128
max_rank_profile_failures=0
```

Thus, in the tested actual-CM tensor rows, the dual-basis top windows are not
just equivalent to twisted traces; each new top coefficient contributes the
full subfield rank until the target rank saturates.

## Current Theorem Target

For p24, prove:

```text
Top_1(V_constant + V_2 + V_157) has rank 158,
Top_2(V_211) has rank 210,
Top_3(V_axis) has rank 368.
```

Or equivalently, prove the first two component-normality statements and the
remaining cross-block directness in `C^3`.

This is the most proof-shaped version so far: it turns the one-factor
Moore determinant into a small number of relative leading-coefficient
conditions in the degree-31 extension `B/C`.

The full-axis certificate can be stated without choosing an arbitrary minor:
for every nonzero structured CRT-axis weight, the top three `C`-coefficients
of `g'(theta) * R(weight)` are not all zero.  Equivalently, the selected
axis subspace avoids the canonical codimension-`3` trace annihilator
`Ann(span_C{1, theta, theta^2})`.

The prefix-rank piece is sharpened in:

```text
p24/trace_frame_prefix_intersection_boundary.md
```

After component normality, `rank Top_2(W_axis)=358` is equivalent to:

```text
dim(Top_2(W_constant+W_2+W_157) cap Top_2(W_211)) = 10.
```

This names the forced cross-component intersection whose residual image is
then tested by the 10-coordinate Schubert tail.

## Degree-Bound Boundary

The next diagnostic is:

```text
p24/tensor_factor_relative_coefficient_profile.py
p24/tensor_factor_relative_coefficient_profile.md
```

It checks whether the adjusted elements `g'(theta)*R_s(theta)` have sparse or
triangular relative support.  Such support would enable a more direct
zero-lemma/degree-bound proof.  Full support would mean the top-coefficient
certificate is still a genuine rank theorem.

On the pinned `D=-10919, m=12` row the adjusted axis rows have full support in
every relative coefficient:

```text
subdegree=3: coeff_ranks=[3,3], support_sizes=[2,2,2,2,2,2]
subdegree=2: coeff_ranks=[2,2,2], support_sizes=[3,3,3,3,3,3]
```

Thus the naive triangular-support proof route is not visible in the small
analogue.

## Fourier Boundary

The frequency-side identity is recorded in:

```text
p24/tensor_factor_top_coefficient_fourier_audit.py
p24/tensor_factor_top_coefficient_fourier.md
```

It verifies:

```text
Top_k(R_s) = DFT_s(r |-> Top_k(J_r)).
```

On the pinned `D=-10919, m=12` row, the DFT identity has zero failures, but
every output coordinate has full frequency support.  Thus the theorem is a
clean vector-valued Fourier anti-annihilator statement, not a simple
coordinate-isolated Vandermonde factorization.

For a CRT component `c`, the component block is the DFT of the marginal sums:

```text
a mod c |-> sum_{r == a mod c} Top_k(J_r).
```

The sharper marginal-rank note is:

```text
p24/tensor_factor_crt_marginal_rank_audit.py
p24/tensor_factor_crt_marginal_rank.md
p24/tensor_factor_marginal_annihilator_theorem.md
```

It records the exact finite lemma: nontrivial component DFT rank equals the
affine rank of the CRT marginals, while constant-plus-component rank equals
their ordinary span rank.  Thus the p24 arithmetic input is:

```text
dim span(D0, Delta_2, Delta_157) = 158 in C,
dim Delta_211 = 210 in C^2,
dim span(D0, Delta_2, Delta_157, Delta_211) = 368 in C^3,
```

where `Delta_c` is the span of marginal differences
`M_a - M_0` for the relevant `Top_k` sequence.  The DFT/root-of-unity layer is
formal; the missing theorem is marginal affine-rank plus cross-component
directness, equivalently avoidance of the trace-annihilator by every nonzero
structured CRT-axis weight.
