# P27 B-Line No-R Fixed-B Norm Relation

Date: 2026-06-22

## Claim

On the common square-`B` support, `hidden_mixed_fixedB` carries the same
`gamma` sign as `beta_U_fixedB` in every tested quadratic field.

This is a useful relation, but in the demotion direction: hidden_mixed looks
like a related secondary model of the same first sign on the materialized
square-`B` side, not an independent second source.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_b_line_noR_fixedB_norm_relation_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_b_line_noR_fixedB_norm_relation_probe_20260622.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_noR_fixedB_norm_relation_probe.py \
  --fields 23^2,71^2,103^2,167^2,199^2,263^2,311^2 \
  | tee research/p27/archive/probe_outputs/p27_b_line_noR_fixedB_norm_relation_probe_20260622.txt
```

## Result

For every common active square-`B` row:

```text
gamma_hidden = gamma_beta
gamma_beta * gamma_hidden = +1
```

Counts:

```text
field   common B   product gamma_beta*gamma_hidden
23^2    2          +1 on 2/2
71^2    8          +1 on 8/8
103^2   12         +1 on 12/12
167^2   20         +1 on 20/20
199^2   24         +1 on 24/24
263^2   32         +1 on 32/32
311^2   38         +1 on 38/38
```

Regression checks:

```text
beta_U_fixedB_gamma_norm_mismatch = 0
hidden_mixed_fixedB_gamma_norm_mismatch = 0
beta_mixed_B = 0
hidden_mixed_B = 0
nonbase_norm = 0
```

The norm-value sets are not the same.  Their overlaps are often zero or small:

```text
199^2: norm_overlap_0 = 20, norm_overlap_4 = 4
263^2: norm_overlap_0 = 21, norm_overlap_2 = 4, norm_overlap_4 = 7
311^2: norm_overlap_0 = 33, norm_overlap_2 = 1, norm_overlap_4 = 3, norm_overlap_6 = 1
```

So the sign relation is cleaner than equality of norm-value fibers.

## Interpretation

Positive:

```text
hidden_mixed_fixedB is not random relative to beta_U_fixedB.
On materialized square-B rows it shares the same selected gamma sign.
```

Negative:

```text
hidden_mixed_fixedB does not add an independent first sign on square-B rows.
The hidden_mixed next-gate probe still shows no f4 continuation sampler.
The norm-value fibers differ, so this is not just identical norm support.
```

## Consequence

Keep `beta_U_fixedB` as the primary f3/materialization class.  Treat
`hidden_mixed_fixedB` as secondary component/Prym data sharing the square-`B`
`gamma` sign, plus nonsquare-`B` boundary data from the next-gate probe.

No GPU production mode follows from hidden_mixed.  CAS should preserve
`gamma_hidden = gamma_beta` on square-`B` rows as a regression and ask whether
the two classes share a quotient/Prym factor, not whether hidden_mixed is a
separate first-sign source.

## Continue / Kill

```text
continue = enforce gamma_hidden = gamma_beta on square-B rows as a regression
continue = ask CAS for the quotient/Prym relation explaining the shared sign
continue = keep hidden_mixed nonsquare-B rows as boundary/component data

kill = hidden_mixed as an independent first-sign source on square-B rows
kill = hidden_mixed as a GPU production sampler without a named direct source
kill = blind hidden_mixed norm-fiber overlap scans
```

```text
p27_b_line_noR_fixedB_norm_relation_rows=1/1
```
