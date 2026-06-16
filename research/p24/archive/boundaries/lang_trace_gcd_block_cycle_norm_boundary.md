# Lang Trace-GCD Block-Cycle Norm Boundary

Date: 2026-06-05

## Point

The crossed-product orbit norm can be lifted from scalar determinant weights
to the actual tail-on-kernel matrices.

For each right translate:

```text
Delta(t) = det(M_t),
M_t = tail-on-kernel trace-GCD matrix.
```

For a Frobenius orbit:

```text
O = {t_0, q*t_0, ..., q^(r-1)*t_0},
```

form the block cyclic operator:

```text
B_O e_i = M_{q^i t_0} e_{i+1}.
```

If each `M_t` is `k x k`, then:

```text
det(B_O) = (-1)^(k*(r-1)) prod_{t in O} det(M_t).
```

For p24:

```text
k = 16,
r = 35 on nonzero right orbits,
(-1)^(k*(r-1)) = +1.
```

So each nonzero orbit norm is the determinant of a `560 x 560`
block-cycle/Fitting operator.

## Audit

Added:

```text
p24/lang_trace_gcd_block_cycle_norm_audit.py
p24/lean/TraceGcdBlockCycleGate.lean
```

Pinned command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/lang_trace_gcd_block_cycle_norm_audit.py \
  --only-D -13319 --only-q 13463 --q-start 13463 --q-stop 13464 \
  --only-m 28 --only-left 4 --only-right 7 \
  --include-linear --max-factor-degree 8 --max-extension-degree 8 \
  --min-left-orbit-len 2 --require-square-tail \
  --max-origin-shifts 140
```

Small actual-CM row:

```text
D=-13319, q=13463, h=140, m=28, n=5, right=7
block_size=2
Frobenius orbits: [0], [1,2,4], [3,6,5]
```

For both omitted rows:

```text
right_class_det_mismatches=0
block_cycle_match=1 on every orbit
block_cycle_full_rank_iff_no_local_singular=1 on every orbit
block_cycle_nonzero=1 on every orbit
failures=0
```

Representative nontrivial orbit products:

```text
omitted=0:
  orbit [1,2,4]: block_cycle_det=2515
  orbit [3,6,5]: block_cycle_det=603

omitted=1:
  orbit [1,2,4]: block_cycle_det=9495
  orbit [3,6,5]: block_cycle_det=6085
```

These match the scalar crossed-product norms and the previously recorded
orbit products.

## Consequence

This is a sharper arithmetic producer target than seven unrelated scalars:

```text
Construct seven p-integral block-cycle/Fitting operators B_O for the actual
p24 trace-GCD tail maps, and prove det(B_O) is a p-unit.
```

It still has the same finite payload:

```text
det(B_O), det(B_O)^(-1), for seven orbits = 14 field elements.
```

But the theorem now talks about a concrete module map:

```text
direct sum of 35 transported prefix kernels
  -> direct sum of 35 tail windows
```

for each nonzero orbit.  That is closer to a class-field/Fitting/local
intersection proof than a bare scalar product.

Equivalently, the local-intersection target is:

```text
there is no nonzero bad section in the direct sum of transported prefix
kernels whose block-cycle tail image is zero.
```

The Lean gate:

```text
p24/lean/TraceGcdBlockCycleGate.lean
```

now records the finite implication that a block-cycle bad section can be
reduced to a local bad tail-on-kernel vector, so ruling out all local bad
vectors rules out the orbit block bad event.

A separate small finite-control toy exercises the singular branch of the same
identity:

```text
p24/block_cycle_fitting_zero_detection_toy.py
```

It generates random block cycles with deliberate singular local blocks and
checks:

```text
det(block_cycle) = (-1)^(k*(r-1)) * product_i det(M_i),
any local det zero => block-cycle det zero,
block cycle full rank iff every local block is full rank.
```

The same determinant is now compared to the split-interpolant/right-resultant
norm on the pinned actual-CM row in:

```text
p24/trace_gcd_actual_cm_norm_triangle_audit.py
```

It verifies, for both omitted rows:

```text
prod_{t in O} det(M_t)
  = signed det(block-cycle(M_t : t in O))
  = Norm_O(f_trace)
```

with zero failures.  It also reports
`naive_base_polynomial_possible=0`, so this is evidence for the
crossed-product/Fitting producer object rather than for an ordinary
`F_q[Y]` polynomial shortcut.

The determinant-line invariance check is:

```text
p24/block_cycle_determinant_line_invariance_toy.py
p24/lean/DeterminantLineUnitScaleGate.lean
```

It applies independent source and target basis changes around the whole orbit:

```text
M_i' = T_{i+1}^{-1} M_i S_i.
```

The block-cycle determinant scales by

```text
prod_i det(S_i) / prod_i det(T_i),
```

hence by a p-unit for p-integral basis changes.  The toy checks both
invertible and deliberately singular controls and reports:

```text
scale_failures=0
zero_mismatches=0
basis_changes_scale_block_cycle_by_units=1
```

This is why the safe producer object is the block-cycle/Fitting
determinant-line norm.  The smaller monodromy matrix remains conditional on
extra source-target identifications; determinant-line p-unitness does not.

## Monodromy Caveat

The companion audit:

```text
p24/lang_trace_gcd_monodromy_basis_boundary.md
```

checks the tempting compression:

```text
det(B_O) = det(M_{r-1} ... M_0).
```

This is true after choosing bases, but it is not yet an intrinsic p24
producer object.  The pinned row has `prefix_len=0`, so it does not test the
coherent transported-kernel-basis issue; a bounded search found no useful
nonzero-prefix calibration row.  Therefore the safe target remains the
block-cycle/Fitting operator unless a separate coherent-basis descent theorem
is proved.

## What It Does Not Prove

The block-cycle identity is finite linear algebra.  It does not prove
p-unitness for p24.

It does rule out a weak producer theorem that supplies only arbitrary nonzero
scalars.  The producer must construct the actual block-cycle operator or an
equivalent determinant-line object and compare its determinant to the supplied
norm scalar.
