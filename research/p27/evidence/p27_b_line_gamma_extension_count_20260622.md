# P27 B-Line Gamma Extension Count

Date: 2026-06-22

## Claim

Extension-field point counts do not promote the B-line `gamma` class to a
source or GPU production filter.

The tested staged selector was:

```text
gamma^2 = U_next + 2
```

on the same eta-plus reduced B-line source chart used by the prime-field
point-count probe.  Across the tested fields, the gamma layer has the same
point count as the materialization layer:

```text
x6^2 - U_next*x6 + 1 = 0
```

So the extension-count evidence says that `gamma` is still coupled to the
ordinary materialization denominator.  It is not a cheaper direct source
stratum by itself.

## Probe

Probe:

```text
research/p27/archive/gates/p27_b_line_gamma_extension_count_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_b_line_gamma_extension_count_probe_20260622.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_b_line_gamma_extension_count_probe.py \
  --fields 607,7^3,7^4,7^5,23^2,23^3 \
  --fiber-limit 20 \
  | tee research/p27/archive/probe_outputs/p27_b_line_gamma_extension_count_probe_20260622.txt
```

Validation replay:

```text
GF(607) counts match the earlier prime-field reduced-cover point-count probe.
```

## Counts

The large-field summary is:

```text
field    reduced_U  gamma_pts  gamma/reduced_U  chi(+)/reduced_U
607      2084       2068       0.992322457      0.491362764
7^3      576        288        0.500000000      0.250000000
7^4      3368       3352       0.995249406      0.494061758
7^5      37760      39040      1.033898305      0.516949153
23^2     1288       1032       0.801242236      0.397515528
23^3     25536      26592      1.041353383      0.520676692
```

The two odd extension fields with meaningful larger counts have ordinary
near-half selector rates:

```text
GF(7^5):  chi(+)=19520, chi(-)=18240
GF(23^3): chi(+)=13296, chi(-)=12240
```

The smaller fields show local artifacts, not a stable p27 law:

```text
GF(7^3):  chi(+)=144, chi(-)=432
GF(23^2): chi(+)=512, chi(-)=768, chi(0)=8
```

In every tested field:

```text
selector_gamma_points = materialized_x6_points
```

up to the same zero-selector degeneracies already visible in the prime-field
point-count probe.

## Interpretation

Positive:

```text
The extension-field finite arithmetic is now instrumented.
The q607 replay agrees with the existing prime-field point-count probe.
The gamma/materialization coupling is explicit over extensions, not only in
the p27-signature prime guard fields.
```

Negative:

```text
No stable source-normalized lift appears.
The selector behaves like a fresh half-cover plus small-field artifacts.
The gamma layer does not separate from the materialized x6 denominator.
This does not justify GPU production or gamma bucket search.
```

## Continue / Kill

```text
continue = offline normalize the reduced legal B-line cover with gamma attached
continue = classify gamma as a Kummer/divisor class, not a bucket
continue = compare the f5/f4 class only after gamma is normalized
continue = use GPU for gamma only as bounded telemetry with raw denominator

kill = gamma^2=U+2 as a direct source sampler
kill = gamma bucket production
kill = interpreting GF(7^3) or GF(23^2) selector skew as a p27 recurrence
kill = more extension point counts without a new class/quotient question
```

## Linked Artifacts

- Reduced point count: [P27 B-Line Reduced-Cover Point Count](p27_b_line_reduced_cover_pointcount_20260622.md)
- Gamma handoff: [P27 B-Line Gamma Class Handoff](p27_b_line_gamma_class_handoff_20260622.md)
- V4 factorization: [P27 B-Line Gamma V4 Factorization](p27_b_line_gamma_v4_factorization_20260622.md)
- Phase sequence: [P27 B-Line Alpha/Beta Phase Sequence Screen](p27_b_line_alpha_beta_phase_sequence_20260622.md)

```text
p27_b_line_gamma_extension_count_rows=1/1
```
