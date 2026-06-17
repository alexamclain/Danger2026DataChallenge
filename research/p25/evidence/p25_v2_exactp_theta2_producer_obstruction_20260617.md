# P25 v2 Exact-P / Theta2 Producer Obstruction

Updated: 2026-06-17

Marker: `p25_v2_exactp_theta2_producer_obstruction_rows=1/1`

## Purpose

Package the exact-P/theta2 heavy route as a small producer matrix. The finite
packet, KL primitive word, theta2 period certificate, and support ladder are
now rigid enough to be useful, but they still do not produce a source-stage
theorem. This page says exactly what would count as a producer, and what
remains support or repair.

## Pages Read

- `frontier.md`
- `lanes/exact-p.md`
- `evidence/p25_v2_exactp_theta2_lookup_row_status_20260617.md`
- `evidence/p25_v2_theta2_period156_support_contract_20260616.md`
- `evidence/p25_v2_exactp_orientation_branch_router_20260616.md`
- `evidence/p25_v2_sprang_theta2_source_intake_20260616.md`
- `evidence/p25_v2_sprang_distribution_instantiation_falsifier_20260616.md`
- `evidence/p25_v2_kl_primitive_word_source_split_20260617.md`
- `evidence/p25_v2_kl_source_split_local_scan_20260617.md`
- `evidence/p25_v2_kl_cyclotomic_norm_route_audit_20260617.md`
- `evidence/p25_v2_exactp_spine_payload_separation_20260617.md`
- `evidence/p25_v2_source_action_registry_20260616.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_exactp_theta2_producer_obstruction_gate.py
```

The gate returned `p25_v2_exactp_theta2_producer_obstruction_rows=1/1`.

## Producer Rows

```text
compact_cdk_orientation_branch
  accepted_if = arithmetic theorem emits C,D,K plus one accepted raw branch
                and the theta2/theta2-inverse divisor-additive payload
  still_missing = source theorem for one accepted branch
  decision = positive_exactp_producer_if_source_theorem_exists

equal_weight_75_atom_theorem
  accepted_if = challenge-legal theorem emits the exact equal-weight 75-atom
                normalized-y product with orientation and bridge
  still_missing = arithmetic source theorem selecting the fixed atoms
  decision = positive_exactp_producer_if_source_theorem_exists

theta2_divisor_additive_payload
  accepted_if = exact theta2 or theta2-inverse divisor/additive data includes
                period-156 branch/root/telescoping and the bridge
  still_missing = theta2 arithmetic producer, not only finite support
  decision = positive_theta2_producer_if_source_theorem_exists

kl_primitive_word_or_h90_chain
  accepted_if = theorem-legal oriented word z^121*(1+z+z^2)*(1-z^263), or the
                three-term H90 chain with boundary step and K-trace
  still_missing = arithmetic source theorem plus raw K-trace/theta2 bridge
  decision = positive_kl_producer_if_source_theorem_exists

sprang_sparse_specialization
  accepted_if = Sprang/Kronecker specialization selects base, K_trace,
                D_segment, T edge, theta2 direction, and p25 branch
  still_missing = collapse from full distribution to sparse p25 packet
  decision = positive_sprang_producer_if_source_theorem_exists

explicit_reverse_reconstruction
  accepted_if = theorem reconstructs C,D,K/orientation, the 75 atoms, or an
                accepted theta2 payload from a unified support-156 theorem
  still_missing = reverse selector theorem
  decision = positive_reverse_route_if_explicit_selector_theorem_exists
```

## Obstruction Rows

```text
finite_payload_without_source
  overclaim = rigid finite support or local fixture already proves exact-P
  falsifier = finite payloads are targets; no arithmetic producer theorem is present
  decision = repair_arithmetic_source_missing

generic_kl_or_modular_unit_source
  overclaim = KL generator, cyclotomic-unit, or Robert-unit context emits the p25 selector
  falsifier = no exact oriented primitive word, mixed selector, or theta2 payload theorem
  decision = support_not_source_closer

sprang_distribution_as_sparse_packet
  overclaim = full Sprang distribution relation is the p25 sparse theta2 packet
  falsifier = full kernel/torsion trace lacks the base*K_trace*D_segment*(1-T) selector
  decision = repair_sparse_specialization_missing

value_only_theta_claim
  overclaim = theta2 or period value without branch data is enough
  falsifier = ambient-period-780 value claims keep the F_p mu_11 ambiguity
  decision = repair_period156_branch_missing

source_chain_without_k_trace
  overclaim = three-term H90 or cyclotomic compression alone closes KL
  falsifier = raw K-trace, orientation, and theta2 bridge are still absent
  decision = repair_k_trace_theta2_context_missing

unified_target_as_exactp_recovery
  overclaim = H0/conductor-39 support-156 theorem automatically recovers exact-P
  falsifier = C,D,K/orientation and atom selector data are lost in the forward bridge
  decision = repair_reverse_selector_theorem_missing
```

## Counts

```text
evidence_markers_ok = 10/10
producer_rows = 6
obstruction_rows = 6
current_exactp_source_theorems = 0
current_theta2_arithmetic_producers = 0
current_kl_source_theorems = 0
current_sprang_sparse_specializations = 0
current_reverse_reconstruction_theorems = 0
current_source_stage_closers = 0
current_submission_ready = 0
p25_v2_exactp_theta2_producer_obstruction_rows=1/1
```

## Verdict

Exact-P/theta2 remains viable only as a theorem-producing upstream route. The
moonshot ask is now precise:

```text
produce one of the six positive rows above, with arithmetic source theorem
status and the p25 orientation/bridge data attached.
```

Everything else in the current exact-P/theta2 stack is support: finite packet
rigidity, source vocabulary, KL generator/cyclotomic-unit context, Sprang
distribution machinery, theta value language, or the unified target without
reverse selector data. These can repair or normalize a future theorem, but
they are not a current source-stage closer.
