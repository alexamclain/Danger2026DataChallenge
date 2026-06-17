# P25 v2 Exact-P Candidate Sweep

Updated: 2026-06-17

Marker: `p25_v2_exactp_candidate_sweep_rows=1/1`

## Purpose

Audit prior exact-P, KSY, Kubert-Lang, theta2, Sprang, finite-payload, and
reverse-unified artifacts after the exact-P heavy-route hook became precise.
The question is whether any older exact-P artifact already supplies the
accepted arithmetic source theorem. The answer remains no.

## Pages Read

- `frontier.md`
- `lanes/exact-p.md`
- `sources/koo-shin-yoon-1007-2307.md`
- `sources/kubert-lang.md`
- `sources/sprang.md`
- `evidence/p25_v2_exactp_minimal_hook_20260616.md`
- `evidence/p25_v2_exactp_orientation_branch_router_20260616.md`
- `evidence/p25_v2_exactp_finite_geometry_rigidity_20260616.md`
- `evidence/p25_v2_exactp_to_unified_target_spine_20260616.md`
- `evidence/p25_v2_reverse_exactp_information_loss_20260616.md`
- `evidence/p25_v2_exactp_closure_template_replay_boundary_20260616.md`
- `evidence/p25_v2_ksy_1007_2307_source_ingest_scan_20260616.md`
- `evidence/p25_v2_kubert_lang_selector_boundary_20260616.md`
- `evidence/p25_v2_kubert_lang_external_source_boundary_20260616.md`
- `evidence/p25_v2_theta2_period156_support_contract_20260616.md`
- `evidence/p25_v2_sprang_theta2_source_intake_20260616.md`
- `evidence/p25_v2_constructive_payload_source_scan_20260616.md`
- `evidence/p25_v2_value_payload_reality_ledger_20260616.md`
- `evidence/p25_v2_source_family_gap_matrix_20260616.md`
- `evidence/p25_v2_source_action_registry_20260616.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_exactp_candidate_sweep_gate.py
```

The gate returned `p25_v2_exactp_candidate_sweep_rows=1/1`.

## Sweep Rows

```text
ksy_normalized_y_surface
  prior_shape = normalized-y torsion/ray-class atom vocabulary on the KSY
                surface
  decision    = exactp_vocabulary_not_source_theorem
  missing     = exact equal-weight 75-atom selector/product theorem

finite_75_atom_payload
  prior_shape = disjoint four-cell supports, forced equal weights, and compact
                theta2 footprint
  decision    = rigid_finite_payload_not_arithmetic_producer
  missing     = challenge-legal arithmetic theorem selecting the payload

compact_cdk_orientation
  prior_shape = C=(47,28), D=(22,3), primitive K=(57,0), orientation
  decision    = accepted_hook_not_prior_theorem
  missing     = source theorem emitting one accepted raw branch with finite
                identity data

branchless_orientation_word
  prior_shape = C,D,K,orientation stated without one of the four raw branches
  decision    = repair_exactp_orientation_branch_missing
  missing     = forward/reverse branch and theta2/theta2-inverse output

kubert_lang_exponent_and_primitive_word
  prior_shape = KL congruence screen plus primitive word
                z^121*(1+z+z^2)*(1-z^263)
  decision    = finite_selector_boundary_not_source_closer
  missing     = theorem-legal mixed C3 x C169 selector or primitive-word
                identity

theta2_period156_support
  prior_shape = period-156 theta2/theta2-inverse divisor support and accepted
                finite interfaces
  decision    = support_payload_not_arithmetic_producer
  missing     = exact theta2/theta2-inverse divisor-additive source theorem

sprang_d2_support
  prior_shape = D=2 Poincare/Kronecker/theta machinery and distribution
                vocabulary
  decision    = support_source_not_theta2_closer
  missing     = sparse p25 theta2 payload, selector, bridge, and branch data

unified_target_theorem_as_exactp_recovery
  prior_shape = H0/conductor-39 support-156 theorem treated as reverse
                exact-P recovery
  decision    = repair_reverse_selector_structure_missing
  missing     = reverse reconstruction to C,D,K,orientation or 75 atoms is not
                proved

period156_value_side_bridge
  prior_shape = H0/Y507 value theorem or theta2 value without full exact-P
                selector
  decision    = value_route_may_feed_extraction_not_exactp_close
  missing     = exact-P selector or explicit reverse reconstruction

finite_packet_without_source
  prior_shape = local fixture, packet, product, or value payload only
  decision    = repair_arithmetic_source_missing
  missing     = finite payloads are targets and evidence, not source theorems
```

## Counts

```text
evidence_markers_ok = 15/15
newly_promoted_prior_candidates = 0
surviving_exactp_intake_families = 4
finite_payload_rigid = 1
exactp_to_unified_one_way = 1
current_exactp_source_theorems = 0
current_source_stage_closers = 0
current_submission_ready = 0
p25_v2_exactp_candidate_sweep_rows=1/1
```

The four surviving exact-P intake families are:

```text
compact C,D,K,orientation theorem with one accepted raw branch
exact equal-weight 75-atom normalized-y theorem
accepted theta2/theta2-inverse divisor-additive payload with period-156 bridge
explicit reverse reconstruction theorem from unified support-156 data
```

## Verdict

```text
positive_artifact = exact-P prior-art candidate sweep
continue_exactp = yes, but only through exact theorem hooks
new_candidate_from_prior_art = no
surviving_exactp_ask = arithmetic source theorem for compact C,D,K,orientation,
                       exact equal-weight 75 atoms, accepted theta2/theta2^-1
                       divisor-additive payload with period-156 bridge, or
                       explicit reverse reconstruction
discard_condition = answer only supplies normalized-y vocabulary, raw
                    Kubert-Lang exponent balance, generic modular-unit
                    generation, branchless orientation, finite payload without
                    source, ambient/value-only theta2 data, Sprang D=2
                    vocabulary, or unified-target theorem without reverse
                    selector data
```

This closes the exact-P "maybe already enough" family. Exact-P remains the
heavy moonshot, but the old artifacts are scaffolding and falsifiers rather
than the missing arithmetic producer.
