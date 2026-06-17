# P25 v2 Additive Normalizer Source Scan

Updated: 2026-06-16

## Purpose

Apply the additive-normalization contract to the local primary source extracts.
The target was deliberately narrow: look for a source-stage closer that fixes
the otherwise invisible `F_p^*` scalar by finite additive, value, basepoint,
branch/root, or telescoping data for one legal support-156 row.

## Pages Read

- `frontier.md`
- `sources/koo-shin-2010.md`
- `sources/koo-shin-yoon-1007-2307.md`
- `sources/koo-shin-ii-1007-2318.md`
- `evidence/p25_v2_additive_normalization_contract_20260616.md`
- `evidence/p25_v2_source_snippet_intake_20260616.md`
- `evidence/p25_v2_current_expert_response_rubric_20260616.md`

## Command

```bash
python3 research/p25/archive/gates/p25_v2_additive_normalizer_source_scan_gate.py
```

The gate returned `p25_v2_additive_normalizer_source_scan_rows=1/1`.

## Source Rows

```text
koo_shin_2010_mathz
  helper_hits = Theorem 5.2, Theorem 6.2, root of unity,
                up to a root of unity, unique normalized generators,
                distribution relation
  strong_normalizer_hits = none
  decision = helper_source_not_additive_normalizer
  missing  = no basepoint/telescoping/period-156/Hilbert-90/Y507
             scalar-fixing finite theorem in extract

ksy_1007_2307_normalized_y
  helper_hits = normalize, normalization, wp', ray class, Siegel
  strong_normalizer_hits = none
  decision = exactp_vocabulary_not_additive_normalizer
  missing  = normalized-y vocabulary appears, but no accepted
             additive-normalization closer terms appear

koo_shin_ii_1007_2318
  helper_hits = ray class, Siegel, normal basis, Galois
  strong_normalizer_hits = none
  decision = background_source_not_additive_normalizer
  missing  = ray-class/Siegel context only; no accepted
             additive-normalization closer terms appear
```

## Strong Terms Screened

```text
basepoint
base point
telescop*
additive identity
divisor identity
finite field / finite-field
Hilbert-90 / Hilbert 90
period-156 / period 156
Norm_156
Y_507 / Y507
scalar-fixing
fixing the F_p
```

The local extracts do contain unrelated finite-field notation such as `Fpm`;
that was not treated as a positive hit because it does not name the p25
period-156/H90/Y507 scalar-fixing normalizer.

## Counts

```text
source_stage_closers = 0
helper_rows = 3
killed_as_additive_normalizer = 3
```

## Verdict

```text
positive_artifact = bounded local source scan against the additive-normalizer
                    contract
continue_first_pass = yes, but not through these extracts as written
intake_rule = local Koo-Shin/KSY extracts remain helper/vocabulary/context
              unless a new source snippet supplies explicit scalar-fixing
              additive/value/basepoint/telescoping data for one legal row
discard_condition = source lead only repeats current helper vocabulary
```
