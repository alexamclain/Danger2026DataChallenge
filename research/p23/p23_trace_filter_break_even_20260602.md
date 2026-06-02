# p23 Trace-Residue Filter Break-Even

Date: 2026-06-02 PDT

Purpose: turn the exact p23 trace-lattice result into an operational cost
bound for any remaining odd trace-residue sidecar.

## Setup

If an exact early filter keeps a fraction `q` of the nonsplit stream and is
target-safe, then the raw-candidate cost changes from:

```text
baseline = C
filtered = F + q*C
```

where:

```text
C = current candidate cost
F = filter cost per candidate
q = fraction kept by the exact residue condition
```

The filter is production-positive only if:

```text
F < (1 - q) * C
```

This is the useful bound because the p23 trace-lattice audit showed exact odd
residue filters are independent at early diagnostic depths, but automatic at
the final depth.

## Helper

Added:

```text
scripts/p23_trace_filter_break_even.py
```

Run:

```bash
PYTHONUNBUFFERED=1 python3 scripts/p23_trace_filter_break_even.py \
  | tee runs/p23_trace_lattice_model_20260602/p23_trace_filter_break_even.log
```

Compile check:

```bash
python3 -m py_compile scripts/p23_trace_filter_break_even.py
```

Status:

```text
PASS
```

## Inputs

Measured/standing costs:

```text
active nonsplit worker rate ~= 0.108M/s
active cost per accepted candidate ~= 9.259 us

direct-y follow-on rate ~= 0.1175M/s
direct-y cost per accepted candidate ~= 8.511 us

measured exact ell=3 direct-y predicate ~= 72 us per nonsplit candidate
```

The exact p23 target traces give two residues modulo each tested odd prime:

```text
q(ell) = 2/ell
```

for `ell = 3,5,7,11,13,17,19`.

## Result

Break-even table:

```text
prefix                 q_keep       zero-cost  active_max_F  directy_max_F
ell=3                  0.666666667   1.500x     3.086 us      2.837 us
ell=3,5                0.266666667   3.750x     6.790 us      6.241 us
ell=3,5,7              0.076190476  13.125x     8.554 us      7.862 us
ell=3,5,7,11           0.013852814  72.188x     9.131 us      8.393 us
ell=3,5,7,11,13        0.002131202 469.219x     9.240 us      8.493 us
ell=3,5,7,11,13,17     0.000250730 3988.36x     9.257 us      8.509 us
ell=3,5,7,11,13,17,19  0.000026393 37889.4x     9.259 us      8.510 us
```

The key comparison:

```text
exact ell=3 measured cost ~= 72 us
ell=3 active break-even   ~= 3.09 us
ell=3 direct-y break-even ~= 2.84 us
```

So the exact ell=3 implementations are about:

```text
72 / 3.09 ~= 23x
```

above the break-even cost for a one-prime trace sidecar.

Even a combined exact `ell=3,5,7` sidecar would need to cost below about:

```text
8.55 us active
7.86 us direct-y
```

which is still far below the measured cost of ell=3 alone.

## Interpretation

This is a hard operational bound:

```text
An odd trace-residue sidecar can be mathematically stackable and still be
useless if it costs more than a few microseconds per candidate.
```

The p23 trace-lattice model says a target-safe early residue filter could, in
principle, reduce the stream dramatically. The measured exact algorithms say
we do not currently have such a filter at the needed cost.

## Decision

No production change.

```text
Keep the active y-filtered nonsplit X1(16) run.
If the active budget misses cleanly, launch the guarded direct-y nonsplit
follow-on.
Do not add ell=3 or other exact trace-residue filters to production unless
the predicate is reduced to low-single-digit microseconds.
```

Research classification:

```text
maybe:
  a genuinely closed-form root-squareclass/pullback predicate

ruled out:
  quotient-ring exponent/gcd ell=3 filters;
  generic SEA/Atkin trace filters;
  exact odd-residue sidecars whose first-prime cost is already tens of
  microseconds.
```
