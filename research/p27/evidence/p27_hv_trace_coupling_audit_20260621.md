# P27 H/V Trace Coupling Audit

Date: 2026-06-21

## Claim

The simplest trace, anti-trace, and norm evaluations of the `H`/`V`
half-norm sections do not produce a non-tautological `T_line` selector.

This is a useful falsifier: the current Hilbert-90 boundary is real, but the
selector is not just `chi(Tr(H))`, `chi(Tr(V))`, `chi(Tr(HV))`, or the
corresponding anti-trace/norm under the quotient involution.

## Setup

Use the component arguments:

```text
H = 4 C B + 8 t z
V = 8 y C t^2 + 4 y z w
z^2 = F
w^2 = K
sigma(t) = -1/t
sigma(w) = w/t^2
```

Named sections tested:

```text
H
V
HV
pref_HV = (t - 1) H V
BC_HV = B C H V
T_arg = (t - 1) B C H V
```

For each section `U`, the gate tests:

```text
chi(U)
chi(sigma(U))
chi(U + sigma(U))
chi(U - sigma(U))
chi(U * sigma(U))
```

with the standard normalizations `raw`, `b`, `a`, `ab`, and `p26line`.

## Gate

Added:

```bash
python3 -m py_compile research/p27/archive/gates/p27_hv_trace_coupling_gate.py
```

Run:

```bash
python3 research/p27/archive/gates/p27_hv_trace_coupling_gate.py \
  --tids 0:64 \
  --chunks 0,1 \
  --draws-per-thread 256 \
  --top 30 \
  | tee research/p27/archive/probe_outputs/p27_hv_trace_coupling_64tid_2chunk_256draw_20260621.txt
```

Held-out:

```bash
python3 <inline heldout script> \
  | tee research/p27/archive/probe_outputs/p27_hv_trace_coupling_heldout_20260621.txt
```

## Result

Sample:

```text
raw_draws = 32768
nonsplit_y = 16432
k_points = 32864
rows = 16096
sigma_not_same_quotient = 0
```

Sanity check:

```text
T_arg:raw with p26line normalization is exact for T_line.
```

This is tautological, since:

```text
T_arg = (t - 1) B C H V
chi(T_arg) = pref * h * vq = T
```

Non-tautological trace/norm candidates:

```text
No candidate was exact.
The best non-taut in-sample candidates were only about 1.03x.
Several of those were not line-consistent, so they are not valid selectors.
```

Held-out checks for the main non-taut candidates:

```text
HV:sigma p26line:
  seed=121 lift=1.028712898
  seed=122 lift=1.025077296
  seed=123 lift=1.004970955
  seed=124 lift=1.008368973

H:norm a / V:norm raw:
  seed=121 lift=1.026483417
  seed=122 lift=1.008606868
  seed=123 lift=1.018284186
  seed=124 lift=1.006549579

HV:trace ab:
  seed=121 lift=1.029608424
  seed=122 lift=1.007062055
  seed=123 lift=1.006226974
  seed=124 lift=1.017566929
```

These are not promoted as filters.  At best they are tiny telemetry signals to
include in a GPU line-stratum report.

## Interpretation

Positive:

```text
The trace/anti-trace gate confirms the exact T_arg recombination and the
sigma quotient wiring.
```

Negative:

```text
No simple trace, anti-trace, or norm of H, V, HV, pref_HV, or BC_HV gives the
missing selector.
Tiny percent-level lifts are too small and unstable to justify a production
strategy.
```

## Continue / Kill

```text
continue = use the Hilbert-90 boundary as the expert/literature ask
continue = GPU line telemetry may report HV:sigma and H/V norm strata as
           optional counters, but not as production filters
continue = test only named theta/additive/Kummer formulas that exploit the
           same-boundary quotient

kill = simple Tr/anti-Tr/Norm explanations for T_line
kill = promoting any trace-coupling lift without a much stronger same-stream
       GPU survivor-per-second measurement
```

## Linked Artifacts

- Gate: `research/p27/archive/gates/p27_hv_trace_coupling_gate.py`
- Output: `research/p27/archive/probe_outputs/p27_hv_trace_coupling_64tid_2chunk_256draw_20260621.txt`
- Held-out output: `research/p27/archive/probe_outputs/p27_hv_trace_coupling_heldout_20260621.txt`
- Related: [P27 Component Involution Boundary](p27_component_involution_boundary_20260621.md)

```text
p27_hv_trace_coupling_audit_rows=1/1
```
