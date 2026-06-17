# P25 v2 External Finite-Normalization Scout

Updated: 2026-06-17

Marker: `p25_v2_external_finite_normalization_scout_rows=1/1`

## Purpose

Check the nearby external Siegel-unit/Kato-Siegel/modular-curve computation
sources against the exact finite-normalization clause in the live theorem ask.
The narrow question is whether any source already upgrades divisor,
distribution, generator, class-field, regulator, or model-computation language
to:

```text
one p25 legal support-156 row
+ Norm_156(Y_507) boundary or accepted period-156 bridge
+ scalar-fixed finite F_p value/additive/telescoping payload
+ arithmetic source theorem
```

It does not. The useful refinement is that Kato-Siegel normalization is real
at the canonical modular-unit level, but the inspected source still stops
before the p25 row specialization and finite `F_p` payload.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_live_theorem_ask_packet_20260617.md`
- `evidence/p25_v2_additive_normalization_contract_20260616.md`
- `evidence/p25_v2_kato_siegel_divisor_scout_20260617.md`
- `evidence/p25_v2_external_source_delta_20260617.md`
- `evidence/p25_v2_local_source_hook_coverage_audit_20260617.md`

## External Sources Checked

- [Notes on Kato-Siegel functions](https://swc-math.github.io/notes/files/01MazurPW.pdf)
- [Kubert-Lang, The Siegel Units Are Generators](https://link.springer.com/chapter/10.1007/978-1-4757-1741-9_4)
- [Kubert-Lang, Siegel-Robert Units in Arbitrary Class Fields](https://link.springer.com/chapter/10.1007/978-1-4757-1741-9_11)
- [Brunault, Regulators of Siegel Units and Applications](https://perso.ens-lyon.fr/francois.brunault/recherche/reg_siegel.pdf)
- [Daniels, Siegel functions, modular curves, and Serre's uniformity problem](https://hdaniels.people.amherst.edu/Uniformity.pdf)

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_external_finite_normalization_scout_gate.py
```

The gate returned `p25_v2_external_finite_normalization_scout_rows=1/1`.

## Source Rows

```text
kato_siegel_canonical_thetaD
  useful = canonical theta_D divisor and isogeny/base-change normalization
  missing = p25 support-156 row selector, Norm_156(Y_507) row boundary,
            and finite F_p payload
  decision = support_canonical_divisor_not_p25_row_payload

kubert_lang_siegel_unit_generators
  useful = generator, q-expansion, and root-of-q-product framework for modular units
  missing = selected p25 row theorem plus scalar-fixed finite value/additive normalizer
  decision = support_generators_not_finite_normalizer

siegel_robert_class_field_units
  useful = values of modular functions defining units in class fields
  missing = non-CM DANGER3 finite identity or p25 finite row theorem over F_p
  decision = support_class_field_units_not_challenge_row

brunault_siegel_unit_regulators
  useful = explicit logarithmic/regulator formulas for Siegel units
  missing = row-selected finite F_p value, additive telescoping payload,
            or period-156 branch bridge
  decision = support_regulator_not_finite_fp_payload

daniels_modular_curve_models
  useful = worked use of Siegel functions and modular units to compute
           modular-curve models and j-maps
  missing = p25 X1(8112)/X1(16) extraction payload or source theorem for one
            support-156 row
  decision = support_model_computation_not_p25_theorem
```

## Counts

```text
evidence_markers_ok = 5/5
source_urls_ok = 5/5
source_rows = 5
support_rows = 5
finite_normalization_closers = 0
current_source_stage_closers = 0
current_submission_ready = 0
p25_v2_external_finite_normalization_scout_rows=1/1
```

## Verdict

This external pass does not change H0, conductor 39, exact-P, or submission
status. It tightens the next source/expert question:

```text
Can one of these canonical Siegel/Kato-Siegel/modular-unit constructions be
specialized all the way to one p25 legal support-156 row with Norm_156(Y_507)
boundary and an explicit finite F_p value/additive/telescoping normalization?
```

Until that specialization and finite payload are supplied, these sources are
support or repair rows rather than source-stage closers.
