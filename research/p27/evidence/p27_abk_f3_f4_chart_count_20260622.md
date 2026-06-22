# P27 A/B/K F3/F4 Chart Count

Date: 2026-06-22

## Claim

The staged A/B/K f3/f4 chart now has a finite-field guard count.  The result
does not promote a GPU source.  It sharpens the CAS boundary:

```text
the all-chart f3/f4 model contains many extra B fibers;
the selected f3-plus-only B fibers reproduce the prior gamma-class handoff;
gamma remains a Kummer/divisor class to extract, not a visible source bucket
```

In particular, the selected f3-plus-only B counts match the old handoff row
counts exactly:

```text
q1607: 28 B fibers, gamma plus rate 76/112 = 0.678571...
q1847: 45 B fibers, gamma plus rate 76/180 = 0.422222...
q2087: 25 B fibers, gamma plus rate 72/100 = 0.720000...
```

Those rates are field-dependent class data, not a stable raw-source shrink.

## Probe

Probe:

```text
research/p27/archive/gates/p27_abk_f3_f4_chart_count_probe.py
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_abk_f3_f4_chart_count_probe_small_20260622.txt
research/p27/archive/probe_outputs/p27_abk_f3_f4_chart_count_probe_20260622.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_abk_f3_f4_chart_count_probe.py \
  --small-primes 607,1607,1847,2087 \
  --modes noR,compactD \
  --fiber-limit 18 \
  | tee research/p27/archive/probe_outputs/p27_abk_f3_f4_chart_count_probe_20260622.txt
```

The counted chart is:

```text
reduced U cover
H^2 = U + 2
F_A(U,V) = (V^2-4)^2 - 4U(V^2-4)(V+A) + 16(V+A)^2 = 0
gamma^2 = V + 2
```

The probe reports both:

```text
noR      = no compactD_R layer
compactD = compactD_R support included
```

The compactD mode is the best comparison with earlier reduced-cover point
counts; the noR mode is the offline-normalization staging chart.

## Guard-Field Results

In compactD mode, including the q607 smoke field and the p27-signature
promotion fields:

```text
field   legal_chart  reduced_U  f3_plus_U  HV_points  gamma_plus/HV
607     1044         2084       1044       4116       0.248785
1607    1600         3200       1696       7168       0.589286
1847    2048         4096       2464       11520      0.461111
2087    1824         3648       1712       6400       0.610000
```

The all-chart ratios are not stable and are polluted by mixed or empty B
fibers.  The selected-source cut is visible in the B-fiber classification:

```text
field   f3-plus-only B   f3-mixed B   f3-minus-only B
607     16               33           16
1607    28               50           22
1847    45               64           19
2087    25               57           32
```

On the selected f3-plus-only B fibers:

```text
field   selected HV  gamma+  gamma-  gamma+/HV
607     2048         0       2048    0.000000
1607    3584         2432    1152    0.678571
1847    5760         2432    3328    0.422222
2087    3200         2304    896     0.720000
```

The last three rows match the existing gamma-class handoff:

```text
q1607: 76 plus / 36 minus over 112 rows
q1847: 76 plus / 104 minus over 180 rows
q2087: 72 plus / 28 minus over 100 rows
```

This is a useful consistency check: the new all-chart count and the old
selected-row handoff are the same object after imposing the f3-plus-only
legal/core B cut.

## Interpretation

Positive:

```text
The staged f3/f4 chart is now executable as a finite-field count.
The compactD mode reproduces the reduced-U two-cover size in the guard fields.
The selected f3-plus-only B fibers match the previous gamma handoff exactly.
The noR/all-chart split tells offline CAS which components are staging artifacts.
```

Negative:

```text
All-chart gamma is mixed and field-dependent.
The f3-plus-only gamma split is also field-dependent, not a uniform source law.
No stable source-normalized lift or direct sampler appears from counts alone.
This does not justify a large GPU production run or gamma bucket search.
```

## CAS Consequence

Normalize with the selected-source legal/core cut visible:

```text
1. Normalize the noR reduced f3 base.
2. Separate f3-plus-only, f3-mixed, f3-minus-only, and empty B components.
3. Extract div(V+2) / the gamma Kummer class on the f3-plus-only component.
4. Compare with the f5/f4 class only after this selected component is explicit.
```

Do not interpret all-chart mixed fibers as legal-source ambiguity.  They are
chart/component bookkeeping for CAS, not GPU buckets.

Next-layer follow-up:
[P27 A/B/K F4/F5 Transition Count](p27_abk_f4_f5_transition_count_20260622.md).
On every guard-field B row with `f4=+1`, all four generic roots of
`F_A(V,W)=0` have `chi(W+2)` equal to the frozen `f5(B)` sign.  This shows the
gamma-transition shape repeats one layer deeper, but the available `f5` rows
are one-sided field tails, so it remains a CAS class-comparison target rather
than a GPU production source.

## Continue / Kill

```text
continue = offline normalize the selected f3-plus-only component
continue = use this count table as a regression fixture for CAS components
continue = compare gamma with f5/f4 only after component separation
continue = GPU only for named-class telemetry with raw-source denominators

kill = all-chart f3/f4 buckets as production source
kill = gamma sign bucket search from this count table
kill = treating field-dependent q1607/q1847/q2087 rates as a recurrence
kill = running GPU before a quotient/coboundary/source map is named
```

## Linked Artifacts

- [P27 A/B/K Symbolic Kummer CAS Brief](p27_abk_symbolic_kummer_cas_brief_20260622.md)
- [P27 B-Line Gamma Class Handoff](p27_b_line_gamma_class_handoff_20260622.md)
- [P27 B-Line Reduced-Domain Reconciliation](p27_b_line_reduced_domain_reconcile_20260622.md)
- [P27 B-Line Gamma V4 Factorization](p27_b_line_gamma_v4_factorization_20260622.md)

```text
p27_abk_f3_f4_chart_count_rows=1/1
```
