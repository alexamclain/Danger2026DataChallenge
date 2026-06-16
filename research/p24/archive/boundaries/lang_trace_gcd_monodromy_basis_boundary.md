# Lang Trace-GCD Monodromy Basis Boundary

Date: 2026-06-05

## Temptation

The block-cycle norm for a Frobenius orbit uses square tail-on-kernel matrices:

```text
Delta(t) = det(M_t).
```

For an orbit `O = {t_0, q*t_0, ..., q^(r-1)*t_0}`, the block-cycle
determinant satisfies:

```text
det(block_cycle(M_t : t in O))
  = (-1)^(k*(r-1)) * prod_{t in O} det(M_t).
```

Since determinants multiply, one can also write:

```text
prod_{t in O} det(M_t) = det(M_{r-1} ... M_0)
```

as a raw matrix identity whenever all `M_t` are represented by `k x k`
matrices over the same field.

This is tempting because for p24 it would replace a `560 x 560` block-cycle
determinant by a `16 x 16` monodromy determinant.

## Audit

Added:

```text
p24/lang_trace_gcd_monodromy_basis_audit.py
```

Pinned command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/lang_trace_gcd_monodromy_basis_audit.py \
  --only-D -13319 --only-q 13463 --q-start 13463 --q-stop 13464 \
  --only-m 28 --only-left 4 --only-right 7 \
  --include-linear --max-factor-degree 8 --max-extension-degree 8 \
  --min-left-orbit-len 2 --require-square-tail \
  --max-origin-shifts 140
```

The determinant algebra holds:

```text
monodromy_det_match=1 on every orbit.
```

But the pinned row is degenerate for the real p24 question:

```text
prefix_lengths_by_t=[0,0,0,0,0,0,0]
tail_lengths_by_t=[2,2,2,2,2,2,2]
kernel_free_cols_by_t=[(0,1),...,(0,1)]
```

So the kernel is the whole left space.  There is no nontrivial transported
prefix-kernel basis to compare.

A bounded search for a nonzero-prefix square-tail calibration row:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 timeout 45 python3 \
  p24/lang_trace_gcd_monodromy_basis_audit.py \
  --max-cases 8 --q-stop 180000 --max-abs-D 40000 \
  --max-h 360 --max-m 120 \
  --include-linear --max-factor-degree 10 --max-extension-degree 10 \
  --min-left-orbit-len 4 --require-square-tail \
  --max-origin-shifts 160
```

ended with:

```text
no eligible monodromy row found
```

without useful nonzero-prefix evidence.

The same conclusion held in a slightly broader 2026-06-06 actual-CM pass:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 timeout 45 python3 \
  p24/lang_trace_gcd_monodromy_basis_audit.py \
  --max-cases 8 --q-stop 250000 --max-abs-D 70000 \
  --max-h 500 --max-m 160 \
  --include-linear --max-factor-degree 8 --max-extension-degree 10 \
  --min-left-orbit-len 4 --min-right-orbits 3 \
  --require-square-tail --max-origin-shifts 120
```

returned:

```text
no eligible monodromy row found
```

Parallel checks with `lang_trace_gcd_kernel_audit.py` and
`lang_trace_gcd_spectral_scan.py` in the same window returned `rows=0`.
Shape-only candidates with the right prefix/tail dimensions did appear, but
failed the full Hilbert splitting / full-cycle / packet audit.  Thus the
absence of a faithful small p24 analogue is now a calibration boundary, not
just a missing command.

## Consequence

The `k x k` monodromy determinant is not currently a safe producer target.
It is a determinant equality after choosing bases separately for the
translated kernels.  For p24, those kernels come from the four full prefix
blocks and have dimension `16`; a monodromy product would need an additional
theorem:

```text
the transported prefix kernels around each right Frobenius orbit have
coherent p-integral bases, compatible with the tail coordinate maps.
```

Without that theorem, the raw product:

```text
M_{r-1} ... M_0
```

is basis-dependent and should not replace the block-cycle/Fitting operator.

## Current Status

Safe producer target:

```text
seven block-cycle/Fitting determinants, one for each right Frobenius orbit.
```

Possible stronger target:

```text
seven 16 x 16 monodromy determinants, but only after proving coherent
kernel-basis descent.
```

The current evidence supports the first target.  The second remains a
conditional refinement, not an established certificate surface.
