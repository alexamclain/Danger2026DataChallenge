# P27 Trace/Norm Dplus U6 Row-Bit H90 Solubility Boundary

Date: 2026-06-22

## Claim

The Dplus `U6` row bit has an exact tested H90 local-solubility boundary.

Across the small regression fields and the p27-signature guard fields

```text
71, 167, 199, 263, 607, 1607, 1847, 2087
```

the active `t`-fibers obey:

```text
Ktrace square or zero  => row-bit fiber is uniform;
Ktrace nonsquare       => row-bit fiber is mixed, always 4 plus / 4 minus.
```

Here

```text
Ktrace = -(t^2 + 2*t - 1)*(t^2 - 2*t - 1)
E_h90: w^2 = Ktrace
row bit = chi(U6 + 2) = chi(x6)
```

This strengthens the point-fiber observation.  It still does not give a source
sampler, because the uniform plus/minus sign on the H90-soluble side remains
non-visible in the tested coordinate atoms.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_trace_norm_dplus_u6_rowbit_h90_solubility_boundary_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_trace_norm_dplus_u6_rowbit_h90_solubility_boundary_probe_20260622.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_trace_norm_dplus_u6_rowbit_h90_solubility_boundary_probe.py \
  --fields 71,167,199,263,607,1607,1847,2087 \
  --include-bare \
  | tee research/p27/archive/probe_outputs/p27_trace_norm_dplus_u6_rowbit_h90_solubility_boundary_probe_20260622.txt
```

## Materialized Tower Result

With the selected materialization filters enabled:

```text
active t-fibers        = 688
boundary failures      = 0
Ktrace square fibers   = 448, all uniform
Ktrace nonsquare       = 240, all mixed
mixed fiber shape      = 240 fibers of 4 plus / 4 minus
```

Aggregate excerpt:

```text
aggregate:
  active_t = 688
  boundary_failures = 0
  ktrace_plus = 448
  ktrace_minus = 240
  ktrace_plus_uniform_minus = 208
  ktrace_plus_uniform_plus = 240
  ktrace_minus_mixed = 240
  mixed_plus_4_minus_4 = 240
```

## Bare Tower Result

Without the materialization filters:

```text
active t-fibers        = 914
boundary failures      = 0
Ktrace square fibers   = 464, all uniform
Ktrace zero fibers     = 2, all uniform
Ktrace nonsquare       = 448, all mixed
mixed fiber shape      = 448 fibers of 4 plus / 4 minus
```

Aggregate excerpt:

```text
aggregate:
  active_t = 914
  boundary_failures = 0
  ktrace_plus = 464
  ktrace_zero = 2
  ktrace_minus = 448
  ktrace_plus_uniform_minus = 208
  ktrace_plus_uniform_plus = 256
  ktrace_zero_uniform_minus = 2
  ktrace_minus_mixed = 448
  mixed_plus_4_minus_4 = 448
```

## Interpretation

Positive:

```text
The H90 quotient is not merely correlated with the row bit.
It is the tested local-solubility boundary for whether the t-fiber is uniform
or split.
The boundary survives p27-signature fields and does not depend on the
materialization filters.
```

Negative:

```text
This still does not name the plus/minus row-bit sign on H90-soluble fibers.
The visible E_h90/Z/Aeta character screen found no exact product through
weight 4.
The q607 function-field lift remains irreducible over the bare H90 elliptic
base.
```

## Consequence

The next theorem/CAS question should be sharpened to:

```text
prove the H90 local-solubility boundary for the Dplus U6 row bit;
then identify the non-visible class on the H90-soluble side that separates
uniform plus from uniform minus.
```

If that class is sourceable or recurrent through later gates, it is a
sqrt-beating candidate.  If it is a fresh independent half-cover or only a
local solubility artifact, the Dplus row-bit lane remains structural telemetry
rather than a production search-space shrink.

## Continue / Kill

```text
continue = prove/explain the Ktrace solubility boundary
continue = extract the non-visible plus/minus class on H90-soluble fibers
continue = include Ktrace, row bit, A, and later gates in fused/native Dplus telemetry

kill = treating mixed fibers as a materialization-filter artifact
kill = treating H90 as only a weak correlation
kill = GPU visible-character buckets from E_h90/Z/Aeta atoms
```

```text
p27_trace_norm_dplus_u6_rowbit_h90_solubility_boundary_rows=1/1
```
