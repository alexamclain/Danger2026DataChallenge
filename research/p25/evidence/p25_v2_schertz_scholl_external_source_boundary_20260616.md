# P25 v2 Schertz/Shin/Scholl External Source Boundary

Updated: 2026-06-16

## Purpose

Record the narrow value of the external Schertz/Shin/Scholl value-side sources
for the p25 moonshot. The sources are real anchors for ray-class generation,
Siegel-Ramachandra invariants, and Kato-Siegel/theta distribution language, but
the p25 ask is more specific: an exact period-156 finite value/divisor theorem
or accepted theta2 payload with the `Norm_156(Y_507)` bridge and branch/root or
additive normalization.

This page is a boundary, not a source-stage close.

## Sources Read

- Schertz, "Construction of Ray class fields by elliptic units":
  `https://eudml.org/doc/248002`
- Shin, "Generation of class fields by Siegel-Ramachandra invariants":
  `https://arxiv.org/abs/1009.2253`
- Scholl, "An introduction to Kato's Euler systems":
  `https://www.dpmms.cam.ac.uk/~ajs1005/preprints/euler.pdf`

## Pages Read

- `sources/schertz-scholl.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `lanes/exact-p.md`
- `evidence/p25_v2_period156_value_source_hook_20260616.md`
- `evidence/p25_v2_h0_y507_period156_compatibility_20260616.md`
- `evidence/p25_v2_theta2_period156_support_contract_20260616.md`
- `evidence/p25_v2_sprang_theta2_source_intake_20260616.md`
- `evidence/p25_v2_constructive_payload_source_scan_20260616.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_schertz_scholl_external_source_boundary_gate.py
```

The gate returned `p25_v2_schertz_scholl_external_source_boundary_rows=1/1`.

## Boundary Rows

```text
schertz_1997_ray_class_elliptic_units
  decision = ray_class_generator_anchor_not_period156_hook
  use      = primary source anchor for ray-class fields, elliptic units, and
             Klein-form generator language
  missing  = exact p25 support-156 edge value, H0/Y507 boundary, or theta2
             payload

shin_1009_2253_siegel_ramachandra
  decision = siegel_ramachandra_generator_not_p25_value_hook
  use      = primary source anchor for Siegel-Ramachandra generator language
  missing  = arithmetic finite value theorem for one oriented support-156 row

scholl_euler_kato_siegel
  decision = kato_siegel_norm_relations_not_d2_p25_hook
  use      = source-note anchor for Kato-Siegel/theta and norm-relation
             vocabulary
  missing  = direct D=2 period-156 theta2/divisor payload with branch or
             additive normalization

future_period156_value_or_theta2_hit
  decision = accepted_if_period156_source_theorem_present
  accepted = exact H0/Y507 period-156 value theorem, scalar-fixed
             divisor/additive theorem, or accepted theta2/theta2-inverse
             payload with bridge data
  missing  = DANGER3 framing and extraction after theorem hit
```

## Counts

```text
general_value_unit_framework_rows = 4
period156_payload_rows = 1
h0_y507_bridge_rows = 1
repair_rows = 3
accepted_future_hook_rows = 1
current_period156_value_theorems = 0
current_source_stage_closers = 0
```

## Verdict

```text
positive_artifact = external Schertz/Shin/Scholl source boundary
continue_value_side = yes, but only through exact period-156 hook language
accepted_future_hook = arithmetic source theorem for canonical H0/Y507
                       period-156 value, scalar-fixed finite divisor/additive
                       identity, or accepted theta2/theta2-inverse payload
                       with branch/root/telescoping or additive normalization
discard_condition = source lead only cites ray-class generation, primitive
                    generator language, ambient value-unit formulas, generic
                    norm relations, or direct Scholl D=2 import
```

Schertz, Shin, and Scholl remain useful orientation sources for what kind of
theorem might exist. They do not currently supply the theorem needed for p25.
