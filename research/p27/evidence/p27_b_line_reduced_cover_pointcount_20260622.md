# P27 B-Line Reduced-Cover Point Count

Date: 2026-06-22

## Claim

The reduced B-line `U_next` cover is structurally clean but not yet a sampler.
Over the promotion guard fields, each legal chart point has two reduced
`U_next` roots, while the materialization and selector layers split by
`B`-fiber.

This sharpens the offline CAS ask:

```text
normalize the reduced U cover with the materialization x^2-U*x+1 and selector
gamma^2=U+2 layers attached
```

Do not treat the bare two-valued `U_next` cover as a below-sqrt source.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_b_line_reduced_cover_pointcount_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_b_line_reduced_cover_pointcount_probe_20260622.txt
```

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_b_line_reduced_cover_pointcount_probe.py \
  --small-primes 607,1607,1847,2087 \
  | tee research/p27/archive/probe_outputs/p27_b_line_reduced_cover_pointcount_probe_20260622.txt
```

## Result

The reduced `U_next` layer has stable size:

```text
q607:  reduced_U_points / legal_chart_points = 1.996168582
q1607: reduced_U_points / legal_chart_points = 2.000000000
q1847: reduced_U_points / legal_chart_points = 2.000000000
q2087: reduced_U_points / legal_chart_points = 2.000000000
```

The q607 deviation is a small degenerate fiber:

```text
q607: one B-fiber has legal_chart_points=20 and reduced_U_points=36;
      all other B-fibers have legal_chart_points=16 and reduced_U_points=32
```

For the promotion fields, every B-fiber has:

```text
legal_chart_points = 16
reduced_U_points   = 32
```

But materialization of `x6` through `x6^2 - U*x6 + 1 = 0` is not uniform:

```text
q1607 B-fibers:
  U_x6_fiber_pair_(32,0)  = 22
  U_x6_fiber_pair_(32,32) = 50
  U_x6_fiber_pair_(32,64) = 28

q1847 B-fibers:
  U_x6_fiber_pair_(32,0)  = 19
  U_x6_fiber_pair_(32,32) = 64
  U_x6_fiber_pair_(32,64) = 45

q2087 B-fibers:
  U_x6_fiber_pair_(32,0)  = 32
  U_x6_fiber_pair_(32,32) = 57
  U_x6_fiber_pair_(32,64) = 25
```

The selector layer `gamma^2=U+2` has the same fiber-size histogram in these
fields, but the plus/minus split varies:

```text
q1607 selector_pm_fiber_pair:
  (0,32)  = 22
  (16,16) = 50
  (32,0)  = 28

q1847 selector_pm_fiber_pair:
  (0,32)  = 19
  (16,16) = 64
  (32,0)  = 45

q2087 selector_pm_fiber_pair:
  (0,32)  = 32
  (16,16) = 57
  (32,0)  = 25
```

## Interpretation

Positive:

```text
The reduced cover is not a vague high-dimensional object anymore.
The U layer is a clean double cover over the legal chart.
The materialization/selector layers give concrete finite-field fiber profiles
for offline Magma/Sage normalization.
```

Negative:

```text
The bare U double cover is not the missing below-sqrt source.
The materialized/selector fibers still vary by B, with no direct uniform
sampler visible from point counts alone.
This does not promote GPU production.
```

Follow-up:
[P27 B-Line Reduced-Lift Classifier Screen](p27_b_line_reduced_lift_classifier_20260622.md)
tests whether the `0/mixed/full` B-fiber profile is the sum of two visible
B-line characters.  Named atoms, all rational-linear pairs, and all pairs of
monic irreducible quadratics are negative across q1607/q1847/q2087.

Domain reconciliation:
[P27 B-Line Reduced-Domain Reconciliation](p27_b_line_reduced_domain_reconcile_20260622.md)
shows that the mixed fibers are outside the frozen selected-source legal
B-domain.  On the legal fixture rows, `lift_units=2` exactly matches `d3 plus`
and `lift_units=0` exactly matches `d3 minus`.  Thus the point-count chart is
a larger CAS staging object; it must be cut down by the legal/core source
conditions before extracting the actual Kummer class.

## Continue / Kill

```text
continue = offline normalize the U cover plus x6-materialization/selector layers
continue = impose the selected-source legal/core cut before interpreting lift buckets
continue = extract branch divisor/classes for the B-fibers with 0/32/64 lifts
continue = compare the resulting f3 class against f4/f3 after normalization

kill = treating the bare U double cover as the whole d3 source
kill = treating mixed all-chart fibers as legal-source ambiguity
kill = two-visible-character classifier for the B-fiber lift profile
kill = GPU production before a named source map or recurrence is extracted
kill = online Magma for this extraction path
```

```text
p27_b_line_reduced_cover_pointcount_rows=1/1
```
