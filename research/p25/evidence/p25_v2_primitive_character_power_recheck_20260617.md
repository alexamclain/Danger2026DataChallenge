# P25 v2 Primitive Character Power Recheck

Updated: 2026-06-17

Marker: `p25_v2_primitive_character_power_recheck_rows=1/1`

## Purpose

Recheck the older conductor-39 primitive-character relation under the newer
power-normalized theorem intake. The tempting shortcut is:

```text
U_chi = -chi_39
V_bal = U_chi^3
W     = U_chi^6
```

Because the cube map is bijective on `F_p^*`, this could look like a new
power-normalized close. It is not one by itself.

## Pages Read

- `frontier.md`
- `lanes/conductor39.md`
- `archive/notes/p25_ksy_y_yang_y507_conductor39_primitive_character_unit_20260614.md`
- `evidence/p25_v2_power_normalized_theorem_intake_20260616.md`
- `evidence/p25_v2_power_output_kind_router_20260616.md`
- `evidence/p25_v2_first_pass_expert_intake_packet_20260616.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_primitive_character_power_recheck_gate.py
```

The gate returned `p25_v2_primitive_character_power_recheck_rows=1/1`.

## Recheck Rows

```text
primitive_unit_relation
  input    = U_chi=-chi_39 with V_bal=U_chi^3 and W=U_chi^6 in exponent notation
  decision = support_identity_not_power_value_theorem
  missing  = old artifact explicitly says primitive normalization is not a
             finite-field value/divisor theorem

v_bal_cube_relation
  input    = V_bal=U_chi^3 source-word relation
  decision = repair_exact_Fp_value_for_one_legal_row_missing
  missing  = cube map is bijective, but only after an exact F_p value for a row
             power exists

w_sixth_relation
  input    = W=U_chi^6 source-word relation
  decision = repair_sign_and_current_boundary_missing
  missing  = sixth roots have kernel 2 and scaled-boundary data is not the
             current row boundary

future_primitive_value_theorem
  input    = exact arithmetic theorem giving an F_p value for U_chi^3, R_m^3,
             or another uniquely invertible row power
  decision = route_only_if_it_names_one_legal_row_and_boundary_bridge
  missing  = must attach the exact value to one of m={1,2,4,8} or a row-labeled
             theorem with Norm_156(Y_507) boundary
```

## Counts

```text
evidence_markers_ok = 4/4
cube_map_bijective = 1
sixth_root_ambiguous = 1
old_relation_is_exponent_word = 1
current_source_stage_closers = 0
current_submission_ready = 0
p25_v2_primitive_character_power_recheck_rows=1/1
```

## Verdict

```text
positive_artifact = primitive-character power shortcut falsifier
continue_first_pass = yes
falsifier = V_bal=U_chi^3 is an exponent-word/source-unit relation, not an
            exact finite F_p row-power value theorem
surviving_route = an expert/source answer may still use U_chi or V_bal only if
                  it supplies an exact finite value theorem, one legal row or
                  row-labeled theorem, and the Norm_156(Y_507) boundary/period
                  bridge
discard_condition = source answer gives only primitive-unit legality,
                    V_bal=U_chi^3, W=U_chi^6, or powered H90 boundary without
                    finite value/additive normalization
```
