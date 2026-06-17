# P25 v2 Yang Lift / Descent Boundary Contract

Updated: 2026-06-16

## Purpose

Make the conductor-39 source-theorem ladder explicit.  Identifying the mixed
source word, lifting it to level `507`, giving the Hilbert-90 boundary, and
proving a finite value/divisor theorem are separate requirements.  A source
snippet that stops at one of the first three is useful context, but it is not a
source-stage close.

This is a classifier, not the missing theorem.

## Pages Read

- `frontier.md`
- `lanes/conductor39.md`
- `lanes/h0.md`
- `evidence/p25_v2_conductor39_yang_h90_interface_contract_20260616.md`
- `evidence/p25_v2_unified_group_ring_payload_20260616.md`
- `evidence/p25_v2_unified_source_theorem_gap_20260616.md`
- `evidence/p25_v2_source_snippet_intake_20260616.md`
- `evidence/p25_v2_current_expert_response_rubric_20260616.md`

## Command

```bash
python3 research/p25/archive/gates/p25_v2_yang_lift_descent_boundary_contract_gate.py
```

The gate returned `p25_v2_yang_lift_descent_boundary_contract_rows=1/1`.

## Target Contract

```text
level = 507
conductor = 39
lift_length = 13
legal source support = 12
legal lift support = 156
legal product shape = 78 positive / 78 negative Yang-fiber factors
required boundary = Norm_156(Y_507)
```

The accepted source-stage theorem must reach one of the legal support-156
Yang/Hilbert-90 rows and then add finite value/divisor content.

## Decisions

```text
mixed_unit_without_yang_lift
  decision = repair_yang_lift_missing
  missing  = level-507 Yang lift to the support-156 product

mixed_yang_without_h90_descent
  decision = repair_h90_descent_boundary_missing
  missing  = Hilbert-90 descent with boundary Norm_156(Y_507)

yang_h90_source_without_finite_theorem
  decision = repair_value_divisor_theorem_missing
  missing  = finite value/divisor theorem for the selected support-156 row

yang_h90_with_finite_divisor_theorem
  decision = source_stage_win_route_to_extraction_contract
  missing  = DANGER3 framing, same-j bridge, X_1(16), halving/x0, vpp.py

yang_h90_with_period156_value_theorem
  decision = source_stage_win_route_to_extraction_contract
  missing  = DANGER3 framing, same-j bridge, X_1(16), halving/x0, vpp.py

projection_or_suborbit_lift
  decision = reject_yang_lift_boundary_or_target_mismatch
  falsifier = legal mixed conductor-39 target with Norm_156(Y_507) boundary

wrong_boundary_lift
  decision = reject_yang_lift_boundary_or_target_mismatch
  falsifier = legal mixed conductor-39 target with Norm_156(Y_507) boundary
```

## Counts

```text
source_closing_rows = 2
repair_rows = 3
reject_rows = 2
current_source_stage_closers = 0
```

## Verdict

The conductor-39 source lane now has this promotion ladder:

```text
mixed U_chi/W source word
-> level-507 Yang lift
-> Hilbert-90 descent with Norm_156(Y_507) boundary
-> finite divisor/additive theorem or period-156 value theorem
-> source-stage win, then extraction contract
```

Anything stopping before the finite theorem is repair.  Projection, suborbit,
altered-lift, or wrong-boundary variants are rejected as current-target
presentations.
