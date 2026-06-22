# P27 Trace/Norm Dplus H90 Quartic Model

Date: 2026-06-22

## Claim

The `Dplus` H90 cover over the elliptic quotient has a normalized cyclic
quartic model that depends on the orientation signs only through:

```text
eta = eh*ev
```

Thus the four fixed orientation components collapse to two quartic/Kummer
classes over:

```text
E_h90: w^2 = -(t^2+2t-1)(t^2-2t-1)
```

This is a meaningful simplification for the next CAS/theorem pass.  It is not
a production sampler: both `eta` quartics still have genus `17`.

## Probes

Symbolic gate:

```text
research/p27/archive/gates/p27_trace_norm_dplus_h90_quartic_model_probe.py
```

Symbolic output:

```text
research/p27/archive/probe_outputs/p27_trace_norm_dplus_h90_quartic_model_probe_20260622.txt
```

Magma fixture:

```text
research/p27/archive/fixtures/p27_trace_norm_dplus_h90_quartic_q607_magma.m
```

Magma output:

```text
research/p27/archive/probe_outputs/p27_trace_norm_dplus_h90_quartic_q607_magma_20260622.txt
research/p27/archive/probe_outputs/p27_trace_norm_dplus_h90_quartic_q607_magma_20260622.xml
```

## Model

Scale:

```text
rho = s / ((t+1)(t^2+2t-1))
```

Then:

```text
rho^4 - 2*U_eta*rho^2 + F*Sprime^2 = 0

U_eta = 2*t^2*(t-1)*(t^2+1)^2*(eta*w + t^2+2t-1)
F = t*(t^2+2t-1)*(t^2+1)
Sprime = (t-1)^3*(t+1)^2*(t^2+1)
eta = eh*ev
```

The symbolic verifier reports:

```text
u0_matches_U_eta = 1
norm_matches_F_Sprime_square = 1
quartic depends on eh,ev only through eta=eh*ev
p27_trace_norm_dplus_h90_quartic_model_probe_rows=1/1
```

## Magma Pricing

Online Magma over `q=607` reports:

```text
RESULT h90_quartic_base 1 2 608
RESULT h90_quartic_model 1 17 4 8
RESULT h90_quartic_model -1 17 4 8
```

Meaning:

```text
E_h90 has genus 1 and degree 2 over F_q(t)
eta=+1 quartic has genus 17 and degree 4 over E_h90
eta=-1 quartic has genus 17 and degree 4 over E_h90
```

Follow-up branch extraction:
[P27 Trace/Norm Dplus H90 Branch Class](p27_trace_norm_dplus_h90_branch_class_20260622.md).
The resolvent is not new: `U_eta^2 - F*Sprime^2 = F*W_eta^2`, so the first
quadratic layer is just the domain-spin cover `z^2=F`.  The hard class is
`rho^2=U_eta+z*W_eta` over that genus-5 cover, with Magma branch degree `16`.

## Interpretation

Positive:

```text
The four orientation components reduce to two eta classes.
The cyclic quartic equation is explicit and small enough for targeted CAS.
This is a cleaner branch/Kummer extraction target than the raw genus-17 cover.
The first quadratic resolvent is exactly identified as the domain-spin cover.
```

Negative:

```text
Both eta classes still have genus 17.
The second-layer branch divisor has degree 16.
No source map, recurrence, or d3 coupling is proved yet.
GPU should not promote this without additional structure.
```

## Next Test

For each `eta in {+1,-1}`, extract:

```text
branch divisor of rho^4 - 2*U_eta*rho^2 + F*Sprime^2 over E_h90
cyclic quartic/Kummer class
Prym or quotient decomposition
comparison with the next selected gate d3
```

Promotion requires:

```text
low-genus factor/source map,
recurrence to d3/d4,
or a sharply stated generic-branch obstruction.
```

## Continue / Kill

```text
continue = branch/Kummer extraction for eta=+1 and eta=-1
continue = compare A_eta=U_eta+z*W_eta with post-Dplus d3
continue = compare the two eta classes with post-Dplus d3
continue = use this normalized model for GPU/CAS handoffs

kill = treating four independent orientation components as separate frontiers
kill = looking for a new first quadratic resolvent
kill = treating the normalized quartic as a production source by itself
kill = low-weight eta-blind quotient-character scans
```

## Linked Artifacts

- H90 quotient: [P27 Trace/Norm Dplus H90 Quotient](p27_trace_norm_dplus_h90_quotient_20260622.md)
- Branch class: [P27 Trace/Norm Dplus H90 Branch Class](p27_trace_norm_dplus_h90_branch_class_20260622.md)
- Relative descent: [P27 Trace/Norm Dplus Relative Descent](p27_trace_norm_dplus_relative_descent_20260622.md)
- GPU handoff: [P27 GPU Dplus-Native Source Handoff](p27_gpu_dplus_native_source_handoff_20260622.md)

```text
p27_trace_norm_dplus_h90_quartic_model_rows=1/1
```
