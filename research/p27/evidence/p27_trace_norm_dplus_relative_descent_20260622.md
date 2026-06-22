# P27 Trace/Norm Dplus Relative Descent

Date: 2026-06-22

## Claim

The `Dplus` quotient symmetry is real, but it is not a standalone rational
squareclass on the conic quotient.  It is a relative Kummer/Hilbert-90 class
over the domain-spin cover.

This sharpens the previous quotient note:

```text
finite-field fiber constancy = true after z exists
free conic source a^2+g^2=4 = not enough
actual object = relative class over z^2 = F
```

The exact symbolic identity is:

```text
u = -core = u0 + u1*z
F = t*(t^2+2t-1)*(t^2+1) = z^2
Norm_z(u) = F * square
```

So `z -> -z` preserves the observed `Dplus` character on rows where the
domain-spin root `z` is already rational, but the norm still carries the
domain-spin squareclass `F`.  This kills the naive search for a standalone
`R(m)` on the conic parameter line.

## Probe

Gate:

```text
research/p27/archive/gates/p27_trace_norm_dplus_relative_descent_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_trace_norm_dplus_relative_descent_probe_20260622.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_trace_norm_dplus_relative_descent_probe.py \
  | tee research/p27/archive/probe_outputs/p27_trace_norm_dplus_relative_descent_probe_20260622.txt
```

## Identity

Use:

```text
B = t^2 + 1
C = t^2 + 2t - 1
R = t^2 - 2t - 1
F = t*C*B = z^2
w^2 = -C*R
u = -core
```

Writing `u = u0 + u1*z` gives:

```text
u0 =
2*t^2*(t - 1)*(t + 1)^2*(t^2 + 1)^2*(t^2 + 2*t - 1)^2
  *(eh*ev*w + t^2 + 2*t - 1)

u1 =
(t - 1)*(t + 1)^2*(t^2 + 1)*(t^2 + 2*t - 1)^2
  *(4*eh*t^3 + ev*t^2*w + ev*w)
```

After reducing by `w^2=-C*R`:

```text
Norm_z(u)
= t*(t - 1)^6*(t + 1)^8*(t^2 + 1)^3*(t^2 + 2*t - 1)^5
```

Equivalently:

```text
Norm_z(u) = F * S^2
S = (t - 1)^3*(t + 1)^4*(t^2 + 1)*(t^2 + 2*t - 1)^2
```

The symbolic verifier reports:

```text
exact = 1
p27_trace_norm_dplus_relative_descent_probe_rows=1/1
```

## Interpretation

Positive:

```text
The quotient-symmetry fiber constancy is explained exactly.
The hard class is now a named relative Kummer/Hilbert-90 problem.
The known domain-spin gate is the boundary term, not disposable bookkeeping.
```

Negative:

```text
Dplus is not a free rational character on a^2+g^2=4.
The failed low-weight a/g/m character screen was testing the wrong level.
Sampling the conic quotient alone cannot impose Dplus.
```

## Next Test

The next mathematical test is a relative Hilbert-90 extraction:

```text
Given u = u0 + u1*z and Norm_z(u) = F*S^2 = z^2*S^2,
find an explicit coboundary or Kummer representative for u on z^2=F,
then test whether that representative:
  1. has a low-genus source map,
  2. couples to the next selected gate d3, or
  3. has a branch divisor large/generic enough to kill this Dplus source route.
```

The first CAS packet should use the domain-spin cover, not the bare conic:

```text
z^2 = t*(t^2+2t-1)*(t^2+1)
w^2 = -(t^2+2t-1)*(t^2-2t-1)
u = u0 + u1*z
Norm_z(u) = z^2*S^2
```

## Continue / Kill

```text
continue = relative Hilbert-90/Kummer extraction using u0,u1,S
continue = quotient coordinates a=t-1/t, g=w/t only together with the
           domain-spin cover
continue = GPU only after the relative source map or d3 coupling is named

kill = standalone R(m) search on the conic parameter line
kill = treating the conic quotient as a direct Dplus sampler
kill = low-weight a/g/m character buckets as the Dplus class
```

## Linked Artifacts

- Quotient symmetry: [P27 Trace/Norm Dplus Quotient Symmetry](p27_trace_norm_dplus_quotient_symmetry_20260622.md)
- Dplus cover: [P27 Trace/Norm D_plus Cover](p27_trace_norm_dplus_cover_20260621.md)
- Source-orientation pricing: [P27 Trace/Norm Source-Orientation Cover](p27_trace_norm_source_orientation_cover_20260621.md)
- GPU handoff: [P27 GPU Dplus-Native Source Handoff](p27_gpu_dplus_native_source_handoff_20260622.md)

```text
p27_trace_norm_dplus_relative_descent_rows=1/1
```
