# P25 v2 External H90 Literature Scout

Updated: 2026-06-16

## Purpose

Record a narrow external literature scout for the current first-pass theorem
shape. This is not a broad bibliography. It asks only whether newly surfaced
Hilbert-90, Siegel-unit, Kubert-Lang, or theta-function sources appear to
contain the exact p25 support-156 source-stage closer.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `sources/koo-shin-2010.md`
- `sources/kubert-lang.md`
- `sources/schertz-scholl.md`
- `evidence/p25_v2_self_contained_theorem_statement_20260616.md`
- `evidence/p25_v2_source_family_gap_matrix_20260616.md`
- `evidence/p25_v2_minimal_expert_ask_20260616.md`
- `evidence/p25_v2_current_expert_response_rubric_20260616.md`

## Search Surface

External queries were constrained to the live theorem shape:

```text
Hilbert 90 + Siegel functions + finite value/divisor theorem
Hilbert 90 + Koo/Shin + Siegel functions
period 156 + Siegel functions
Siegel-Robert / Kubert-Lang finite-field value language
```

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/archive/gates/p25_v2_external_h90_literature_scout_gate.py
```

The gate returned `p25_v2_external_h90_literature_scout_rows=1/1`.

## Screened Sources

```text
shin_2605_25291_h90_quotient_maps
  source   = https://arxiv.org/abs/2605.25291
  has      = Hilbert-90 quotient-map language for trace-zero rational maps
  missing  = Siegel/Yang/H0 level-507 support-156 row,
             Norm_156(Y_507), scalar-fixed finite row theorem
  decision = reject_different_h90_rational_map_setting

folsom_modular_units_selberg
  source   = https://afolsom.people.amherst.edu/Folsom-ModUnitsSel-MRL.pdf
  has      = Kubert-Lang modular-unit / Siegel-function vocabulary
  missing  = exact oriented p25 support-156 finite theorem
  decision = background_kubert_lang_modular_unit_vocabulary

kubert_lang_units_without_cm
  source   = https://www.numdam.org/item/CM_1980__41_1_127_0.pdf
  has      = Kubert-Lang units and distribution-relation context
  missing  = scalar-fixed finite value/divisor theorem for the p25 row
  decision = background_distribution_relations_not_row_value

anticyclotomic_theta_functions
  source   = https://annals.math.princeton.edu/wp-content/uploads/annals-v163-n3-p02.pdf
  has      = theta/Siegel/Hilbert-90 context in a CM anticyclotomic setting
  missing  = DANGER3 p25 finite non-CM row identity
  decision = background_cm_theta_siegel_context

class_invariants_cyclotomic_unit_groups
  source   = https://jtnb.centre-mersenne.org/item/10.5802/jtnb.628.pdf
  has      = modular-unit, Siegel-function, and class-invariant vocabulary
  missing  = p25 one-edge theorem or period-156 branch data
  decision = background_modular_unit_class_invariant_vocabulary
```

## Counts

```text
external_sources_screened = 5
superficially_relevant_sources = 5
exact_level507_rows = 0
norm156_y507_boundaries = 0
scalar_fixed_finite_theorems = 0
first_pass_closers = 0
current_submission_ready = 0
p25_v2_external_h90_literature_scout_rows=1/1
```

## Verdict

The external scout found no source-stage closer. The strongest new warning is
that Hilbert-90 vocabulary by itself is too broad: a result about quotient maps
or trace-zero rational maps is not evidence for the p25 Siegel/Yang row unless
it emits the exact support-156 level-507 product, the `Norm_156(Y_507)`
boundary, and scalar-fixed finite value/divisor data.

## Continue / Kill Recommendation

Continue asking the narrow first-pass theorem question from the self-contained
theorem statement. Kill broad external H90 quotient-map searches unless a hit
also names the exact p25 support-156 row, period-156 value branch, or
scalar-fixed finite divisor/additive identity.
