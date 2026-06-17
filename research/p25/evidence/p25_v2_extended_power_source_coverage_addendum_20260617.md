# P25 v2 Extended Power Source Coverage Addendum

Updated: 2026-06-17

Marker: `p25_v2_extended_power_source_coverage_addendum_rows=1/1`

## Purpose

Close a small classification gap created by the expanded unique-power intake.
The current kernel accepts exact row-labeled values of `R_m^75`, `R_m^169`,
and `R_m^507` because all three powers are invertible modulo `p - 1`. This
does not reopen a broad local source search and does not identify exact-P
75 atoms with an `R_m^75` row-power theorem.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `lanes/exact-p.md`
- `evidence/p25_v2_extended_unique_power_intake_20260617.md`
- `evidence/p25_v2_local_source_hook_coverage_audit_20260617.md`
- `evidence/p25_v2_current_theorem_kernel_20260617.md`
- `evidence/p25_v2_drew_kernel_review_packet_20260617.md`
- `evidence/p25_v2_exactp_75_anchor_bridge_filter_20260617.md`
- `evidence/p25_v2_exactp_spine_payload_separation_20260617.md`
- `evidence/p25_v2_kl_source_split_local_scan_20260617.md`
- `evidence/p25_v2_exactp_theta2_lookup_row_status_20260617.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_extended_power_source_coverage_addendum_gate.py
```

The gate returned `p25_v2_extended_power_source_coverage_addendum_rows=1/1`.

## Addendum Rows

```text
extended_row_power_intake
  object_basis = one labeled legal row R_m with e in {75,169,507}
  accepted_if  = arithmetic source theorem gives exact finite F_p value for
                 R_m^e plus the boundary or accepted period bridge
  decision     = intake_only_if_exact_row_labeled_theorem_arrives
  falsifier    = rowless power value, boundary-only powered divisor, or value
                 up to scalar

exactp_75_atom_not_row_power
  object_basis = exact-P normalized-y/theta2 atoms
  accepted_if  = challenge-legal exact-P theorem emits compact packet,
                 orientation, and 75->300->12->312->156 bridge
  decision     = heavy_upstream_not_first_pass_row_power_shortcut
  falsifier    = 75 vocabulary, atom count, or finite fixture without
                 arithmetic source theorem

c169_507_context_not_power_hook
  object_basis = KL/Sprang/Koo-Shin source vocabulary mentioning 169 or 507
  accepted_if  = row-labeled R_m^169/R_m^507 theorem, or accepted exact-P/KL/
                 theta2 payload
  decision     = support_or_repair_until_exact_hook
  falsifier    = C_169, level-507, Y_507, or primitive-word vocabulary without
                 exact payload

no_local_reread_unlocked
  object_basis = local Koo-Shin/KSY/Koo-Shin II/Sprang extracts
  accepted_if  = new snippet names one of the exact accepted hooks
  decision     = external_theorem_new_snippet_or_proof_attempt_only
  falsifier    = broad reread request driven only by expanded unique-power list
```

## Counts

```text
evidence_markers_ok = 8/8
extended_exact_row_power_hooks = 3
addendum_rows = 4
broad_local_reread_unlocked = 0
current_extended_power_source_theorems = 0
current_exactp_source_theorems = 0
current_source_stage_closers = 0
current_submission_ready = 0
p25_v2_extended_power_source_coverage_addendum_rows=1/1
```

## Verdict

The expanded row-power intake is a useful guardrail for future expert answers:
an exact row-labeled `R_m^75`, `R_m^169`, or `R_m^507` theorem would recover
the row and route through the normal source-stage spine.

It does not change the source-search plan:

```text
do not reopen broad local source search for 75/169/507 vocabulary;
do not identify exact-P 75 atoms with row-power R_m^75;
do continue only on an exact row-labeled theorem, accepted exact-P packet,
new source snippet, external theorem, or fresh proof attempt.
```
