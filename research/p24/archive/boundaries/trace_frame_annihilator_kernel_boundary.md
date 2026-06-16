# Trace-Frame Annihilator Kernel Boundary

Date: 2026-06-05

This note records the sharpened zero obstruction after the beta/tensor bridge.

## Zero Obstruction

In one p24 tensor factor:

```text
B/E,        [B:E]=5549
C/E,        [C:E]=179
B/C,        [B:C]=31
```

the trace-frame theorem is:

```text
W_axis(B) cap Ann_3 = {0},
Ann_3 = span_C{1,theta,theta^2}^perp.
```

Equivalently, for a nonzero axis-supported K-character combination `x`, the
failure condition is:

```text
top three relative coefficients of g'(theta)*x vanish.
```

So a hypothetical p24 failure is not merely a zero of one component
resolvent.  It is a cross-axis low-relative-degree congruence:

```text
exists 0 != w in W_axis:
  g'(theta) * sum_s w_s R_s has relative degree <= 27 over C.
```

## Kernel-Shape Audit

I added:

```text
p24/trace_frame_annihilator_kernel_audit.py
```

It intentionally uses too few top trace-frame blocks in small rows so that a
kernel is forced by dimension, then asks whether the kernel is supported in a
single smooth-axis block or only appears through cross-block cancellation.

Pinned command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_frame_annihilator_kernel_audit.py \
  --only-D -10919 --min-h 1 --max-h 200 \
  --max-n 200 --max-m 40 --max-factor-degree 20 \
  --max-extension-degree 8 --max-tensor-factor-degree 12 \
  --max-top-count 3 --include-linear --only-m 12 --max-cases 1
```

Key row:

```text
D=-10919, q=11243, h=156, m=12, n=13
subdeg=2, top=2
axis_dim=6, target_dim=4, rank=4, kernel_dim=2
single_block_kernel_dims=[constant:0,4:0,3:0]
pair_kernel_dims=[4+3:1]
basis_support_min=5, basis_support_max=5
basis_block_touch_hist=[3:2]
```

Thus every individual smooth block is injective, but a cross-block kernel is
still dimension-forced.  Component p-unitness alone would not prove the
trace-frame theorem.

The compact rows found by the beta/tensor bridge audit show the same
qualitative pattern:

```text
D=-1559, q=2459, h=51, m=3, n=17
  single_block_kernel_dims=[constant:0,3:0]
  pair_kernel_dims=[constant+3:1]
  basis_support_min=3, basis_support_max=3

D=-2207, q=2243, h=39, m=3, n=13
  single_block_kernel_dims=[constant:0,3:0]
  pair_kernel_dims=[constant+3:1]
  basis_support_min=3, basis_support_max=3
```

These are dimension-forced failures, not p24 failures.  Their value is that
they rule out a too-weak theorem shape.

## Consequence

The p24 p-unit theorem should not be phrased only as:

```text
each smooth-axis component has nonzero trace-frame image.
```

The correct theorem is a direct-sum/Schubert transversality statement:

```text
the four axis images
  constant, 2-axis, 157-axis, 211-axis
are in direct position relative to the top-three trace-frame flag.
```

Equivalently:

```text
the leading Plucker coordinate delta_lead is a p-unit,
```

or, in the beta/tensor bridge language:

```text
the crossed-product reduced norm of this Schubert coordinate is a p-unit
in each scalar-extension factor.
```

This is now a sharper boundary for proof attempts:

```text
component nonvanishing: necessary but too weak;
pair/direct-sum p-unit: plausible and matches the observed obstruction;
ordinary norm/sparse beta/one-block annihilator shortcuts: closed.
```

## Next Lemma Shape

A useful arithmetic lemma would be:

```text
If an axis combination lies in Ann_3, then the corresponding mixed
CM divisor has a nontrivial relation among at least two smooth-axis
components.
```

To finish p24, that relation must be shown impossible at the selected prime,
for example by a phase-aware class-field p-unit, Borcherds/Schofer divisor, or
explicit split-cycle identity.  The small kernel audit says the lemma must
see cross-axis directness; it cannot only certify component support.

The same obstruction is now measured directly in:

```text
p24/trace_frame_low_degree_congruence_boundary.md
p24/trace_frame_low_degree_congruence_audit.py
```

There, forced low-relative-degree congruences in the pinned and compact
bridge rows are cross-axis and have full low-tail support.  This further
rules out sparse-tail or one-component explanations.
