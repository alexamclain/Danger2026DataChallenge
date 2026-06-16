# Tensor Factor Trace Annihilator Theorem

This is the dual-basis form of the twisted trace-frame target.

## Linear Algebra

Let:

```text
B/C,        [B:C] = 31,
B = C(theta),
```

and use the trace pairing:

```text
<x,y> = Tr_{B/C}(xy).
```

Because `B/C` is finite separable, this pairing is perfect.  The length-3
trace frame

```text
x |-> (
  Tr_{B/C}(x),
  Tr_{B/C}(theta x),
  Tr_{B/C}(theta^2 x)
)
```

is exactly pairing against:

```text
span_C{1, theta, theta^2}.
```

Therefore its kernel is:

```text
Ann_3 = span_C{1, theta, theta^2}^perp
      = { x in B : Tr_{B/C}(theta^i x)=0 for i=0,1,2 }.
```

This is a `C`-subspace of dimension:

```text
31 - 3 = 28,
```

or dimension:

```text
28 * 179 = 5012
```

over `E`.

## p24 Theorem Target

Let `W_axis(B)` be the `368`-dimensional `E`-span of the selected
K-character resolvents in one tensor factor.  The twisted trace-frame
certificate is equivalent to:

```text
W_axis(B) ∩ Ann_3 = {0}.
```

This is sharper than saying "a 368 by 537 matrix has full rank": the target
is an avoidance theorem against a canonical trace-annihilator subspace.

Equivalently, the exterior product

```text
∧_{s in S_axis} T_3(R_s)
```

is nonzero in `Exterior_E^368(C^3)`.  This is the coordinate-free finite
certificate; individual minors are Plucker coordinates after choosing an
`E`-basis of `C^3`.

## Dual-Basis Form

If `g(Y)` is the minimal polynomial of `theta` over `C`, then the dual basis
to:

```text
1, theta, ..., theta^30
```

is expressible using:

```text
g(Y) / (Y - theta)
```

and `g'(theta)`.  Thus `Ann_3` can also be described by coefficient-window
equations.

This may be the route to a smaller explicit finite-field identity: multiply
an axis resolvent by `g'(theta)`, expand over the `C`-basis
`1,theta,...,theta^30`, and require the top three relative coefficients to
vanish.  Equivalently:

```text
x in Ann_3
  iff the theta^30, theta^29, theta^28 coefficients of g'(theta)*x are 0.
```

So the p24 theorem can be stated as:

```text
the map taking an axis combination to those top three C-coefficients of
g'(theta)*x is injective.
```

The small-row audit for this dual-basis window is:

```text
p24/tensor_factor_dual_basis_window_audit.py
```

The component-capacity split is recorded in:

```text
p24/tensor_factor_top_coefficient_capacity.py
p24/tensor_factor_top_coefficient_block_split.md
```

Pinned evidence:

```text
PYTHONPATH=p24 python3 p24/tensor_factor_dual_basis_window_audit.py \
  --only-D -10919 --min-h 1 --max-h 200 \
  --max-n 200 --max-m 40 --max-factor-degree 20 \
  --max-extension-degree 8 --max-tensor-factor-degree 12 --max-rows 8
```

reported:

```text
rows=5
trace_window_rank_mismatch_targets=0
axis_rows_full_by_tested_window=5
```

After adding component/pair/prefix targets, the same run also shows the
capacity rule: a target reaches full rank when the number of top coefficients
times the intermediate degree reaches its dimension.

In the pinned `m=12` row, the axis ranks match exactly:

```text
subdegree 2: trace=[2,4,6], window=[2,4,6]
subdegree 3: trace=[3,6],   window=[3,6]
```

A broader bounded toy-CM run reported:

```text
rows=8
trace_window_rank_mismatch_targets=0
axis_rows_full_by_tested_window=8
max_rank_profile_tests=128
max_rank_profile_failures=0
```

This supports the deterministic coefficient-window formulation: every tested
top-window rank matches the twisted trace-frame rank, and no tested target
failed the expected "add one full subfield rank until saturation" profile.

## Formal Gate

The abstract implication is Lean-checked in:

```text
p24/lean/TraceFrameAnnihilatorGate.lean
```

It does not prove the arithmetic theorem.  It verifies that:

```text
trace-frame kernel lies in Ann_3
axis image avoids Ann_3
  => axis evaluation is injective.
```

Combined with the existing scalar-extension and tensor-factor gates, this is
a valid route back to the original p24 packet axis certificate.

## Kernel-Shape Boundary

The forced-kernel audit:

```text
p24/trace_frame_annihilator_kernel_audit.py
p24/trace_frame_annihilator_kernel_boundary.md
```

shows that component nonvanishing is not enough.  In the pinned
`D=-10919, m=12` row, using one fewer trace-frame block gives:

```text
single_block_kernel_dims=[constant:0,4:0,3:0]
pair_kernel_dims=[4+3:1]
```

Thus every smooth-axis component is separately injective, while a
dimension-forced cross-block kernel still exists.  The p24 arithmetic theorem
must prove direct-sum/Schubert transversality of the full axis image against
`Ann_3`, not merely p-unitness of individual component images.
