# P27 B-Line Frobenius Plateau Audit

Date: 2026-06-22

## Claim

The B-line all-plus plateaus are not proper-subfield or short-Frobenius-orbit
samplers.

In every tested extension field, the legal B set, every all-plus survival set,
and every first-stop set consists entirely of full-degree Frobenius orbits.
This includes `GF(7^6)`, where proper subfields of degrees `1`, `2`, and `3`
were available.

So the local plateaus are real finite-field phenomena, but they do not give a
direct subfield sampler or obvious source shrink for p27.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_b_line_frobenius_plateau_probe.py
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_b_line_frobenius_plateau_probe_q23_3_q103_2_gate10_20260622.txt
research/p27/archive/probe_outputs/p27_b_line_frobenius_plateau_probe_q7_5_q7_6_gate10_20260622.txt
```

## Commands

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_frobenius_plateau_probe.py \
  --fields 23:3,103:2 \
  --max-gate 10 \
  | tee research/p27/archive/probe_outputs/p27_b_line_frobenius_plateau_probe_q23_3_q103_2_gate10_20260622.txt

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_frobenius_plateau_probe.py \
  --fields 7:5,7:6 \
  --max-gate 10 \
  | tee research/p27/archive/probe_outputs/p27_b_line_frobenius_plateau_probe_q7_5_q7_6_gate10_20260622.txt
```

## Results

Summary:

```text
field      legal_B  last nonzero prefix  plateau/stop structure
GF(7^5)        590  d5                   all tested sets degree 5
GF(7^6)       3576  d6                   all tested sets degree 6
GF(23^3)       399  d8                   all tested sets degree 3
GF(103^2)      288  d5                   all tested sets degree 2
```

Detailed survival sets:

```text
GF(7^5):
  legal_B = 590, all min_subfield_degree_5 / orbit_5
  d3+ = 315, all min_subfield_degree_5 / orbit_5
  d4+ = 140, all min_subfield_degree_5 / orbit_5
  d5+ = 140, all min_subfield_degree_5 / orbit_5
  d6+ = 0

GF(7^6):
  legal_B = 3576, all min_subfield_degree_6 / orbit_6
  d3+ = 1896, all min_subfield_degree_6 / orbit_6
  d4+ = 1128, all min_subfield_degree_6 / orbit_6
  d5+ = 600, all min_subfield_degree_6 / orbit_6
  d6+ = 360, all min_subfield_degree_6 / orbit_6
  d7+ = 0

GF(23^3):
  legal_B = 399, all min_subfield_degree_3 / orbit_3
  d3+ = 216, all min_subfield_degree_3 / orbit_3
  d4+ = 120, all min_subfield_degree_3 / orbit_3
  d5+ = 84, all min_subfield_degree_3 / orbit_3
  d6+ = 84, all min_subfield_degree_3 / orbit_3
  d7+ = 84, all min_subfield_degree_3 / orbit_3
  d8+ = 84, all min_subfield_degree_3 / orbit_3
  d9+ = 0

GF(103^2):
  legal_B = 288, all min_subfield_degree_2 / orbit_2
  d3+ = 160, all min_subfield_degree_2 / orbit_2
  d4+ = 96, all min_subfield_degree_2 / orbit_2
  d5+ = 48, all min_subfield_degree_2 / orbit_2
  d6+ = 0
```

The first-stop sets have the same full-orbit behavior.  For example in
`GF(7^6)`:

```text
gate3_minus = 1680, all degree 6
gate4_minus = 768, all degree 6
gate5_minus = 528, all degree 6
gate6_minus = 240, all degree 6
gate7_minus = 360, all degree 6
```

## Interpretation

Positive:

```text
The plateau sets are Frobenius-stable algebraic sets, not random logging
artifacts.
They are good data for an eventual Kummer-class/Frobenius explanation.
```

Negative:

```text
No tested plateau is a proper-subfield source.
No tested plateau has short Frobenius orbits.
The moving hard-stop gates are not explained by an obvious subfield sampler.
```

Thus the B-line route remains:

```text
extract f3(B), f4(B), ... in the Kummer group
then explain the local plateaus by class/Frobenius action
```

not:

```text
sample a proper subfield
sample a short Frobenius orbit bucket
launch a large B-prefix GPU production run
```

Follow-up:
[P27 B-Line Trace/Norm Plateau Audit](p27_b_line_trace_norm_plateau_audit_20260622.md)
tests the next named Frobenius invariants.  Trace+norm is exact only in
relative quadratic extensions, where it records a conjugate pair.  Prime-degree
fields remain mixed.  This is useful quotient bookkeeping, not a transferable
sampler.

## Continue / Kill

```text
continue = B-line Kummer sequence extraction
continue = compare extracted classes with local Frobenius stop gates
continue = use these extension sets as regression fixtures for CAS
continue = use trace+norm-to-half only as even-extension regression data

kill = proper-subfield explanation for the tested B-line plateaus
kill = short-Frobenius-orbit sampler for the tested B-line plateaus
kill = trace/norm bucket sampler as a p27 production lane
kill = GPU production from plateau counts without extracted classes
```

```text
p27_b_line_frobenius_plateau_audit_rows=1/1
```
