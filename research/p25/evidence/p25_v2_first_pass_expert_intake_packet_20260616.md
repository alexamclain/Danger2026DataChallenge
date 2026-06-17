# P25 v2 First-Pass Expert Intake Packet

Updated: 2026-06-16

## Purpose

Make the current H0/conductor-39 expert/source feedback loop mechanical. This
page is the compact intake packet to use when Drew, a source snippet, or a
future lane pass proposes a theorem shape. It does not claim the theorem
exists; it says what clauses must be present before an answer can be promoted.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_self_contained_theorem_statement_20260616.md`
- `evidence/p25_v2_unified_theorem_review_packet_20260616.md`
- `evidence/p25_v2_minimal_expert_ask_20260616.md`
- `evidence/p25_v2_positive_theorem_clause_matcher_20260616.md`
- `evidence/p25_v2_source_stage_normalization_spine_20260617.md`
- `evidence/p25_v2_source_graph_normal_form_20260616.md`
- `evidence/p25_v2_additive_normalization_contract_20260616.md`
- `evidence/p25_v2_constructive_value_payload_contract_20260616.md`
- `evidence/p25_v2_source_action_registry_20260616.md`
- `evidence/p25_v2_power_normalized_theorem_intake_20260616.md`
- `evidence/p25_v2_extended_unique_power_intake_20260617.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/archive/gates/p25_v2_first_pass_expert_intake_packet_gate.py
```

The gate returned `p25_v2_first_pass_expert_intake_packet_rows=1/1`.

## Intake Rows

```text
scalar_fixed_edge_divisor_additive
  promote if =
    one exact oriented row R_m, m in {1,2,4,8}
    arithmetic source theorem
    Hilbert-90 boundary Norm_156(Y_507)
    scalar-fixed finite divisor/additive identity
    finite datum fixing F_p^* scalar: additive value, basepoint, branch/root,
      telescoping product, or equivalent deterministic finite evaluation
  then =
    source-stage candidate; route to DANGER3 framing and extraction

quartic_character_finite_theorem
  promote if =
    exact W / Norm_156(Y_507) boundary
    exact row-antisymmetric C4_1 phase
    mixed tensor row sign
    oriented row data or matching boundary-sign convention
    arithmetic source theorem
    scalar-fixed finite divisor/additive theorem for the selected row
  then =
    equivalent first-pass source-stage candidate

period156_h0_or_y507_value_theorem
  promote if =
    canonical H0 value or Y_507 value
    compatibility bridge to one legal support-156 row
    arithmetic source theorem
    support-period-156 branch/root/telescoping context
    no ambient-period-780 mu_11 ambiguity
  then =
    source-stage candidate; route to DANGER3 framing and extraction

power_normalized_row_value_theorem
  promote if =
    one exact oriented row R_m, m in {1,2,4,8}
    arithmetic source theorem
    exact finite F_p value for R_m^e with e in {3,5,13,39,75,169,507}
    inverse exponent recovery modulo p - 1
    Norm_156(Y_507) boundary or accepted period-156 bridge
  then =
    recover R_m by the listed inverse exponent and route through
    source-snippet intake as a source-stage candidate

row_labeled_orbit_theorem
  promote if =
    theorem gives scalar-fixed divisor/additive or period-156 value identities
    for all four rows with labels m, edge, or stable hash
  then =
    choose any labeled row and route through the positive clause matcher

exactp_upstream_or_theta2_bridge
  promote if =
    exact 75-atom or accepted theta2/theta2-inverse payload
    one accepted orientation branch
    arithmetic source theorem
    bridge 75 -> 300 -> 12 -> 312 -> 156
  then =
    heavier upstream source-stage candidate; not the first-pass default
```

The first five rows are the H0/conductor-39 first-pass front door. The exact-P
row is deliberately separated as a heavier upstream route.

The source-stage normalization spine is now the common reducer for all accepted
first-pass presentations. A direct edge, quartic selector, row-labeled orbit,
reciprocal-minus-boundary presentation, bijective power value, or
support-period-156 value is accepted only when it uniquely recovers one
scalar-fixed legal support-156 row.

## Required Object Identity

An answer must identify one row by multiplier, edge, or stable hash:

```text
m=1  edge=7H -> 4H  sha256=eb5a86ae58b16b7e10706ac166d1f548aaccdfc677181a253119b6876e470d1e
m=2  edge=7H -> H   sha256=97517200105db6e1f44e04e76977407615a88c8b4ca782fefec6cb2821e0a0e9
m=4  edge=2H -> H   sha256=28b3e03228d428ac6474ff92eaefb1a9a7dfbfda8af2318812d5bca68e8958d6
m=8  edge=2H -> 4H  sha256=ace1a01fa59701567225b8f781ffda2fe308aac41662f80439ace7a6cda7bf87
```

Equivalent H0/H0-translate language and mixed conductor-39 `U_chi/W` language
are acceptable only when they land on one of these rows or a row-labeled
theorem containing one of them.

## Repair Or Reject Rows

```text
source_legality_only
  decision = repair_finite_theorem_missing

boundary_only
  decision = repair_identity_for_one_edge_missing

unspecified_fp_scalar
  decision = repair_additive_or_value_normalization_missing

period780_or_mu11_only
  decision = repair_period156_value_selection_missing

degree6_value_without_fp_descent
  decision = repair_fp_descent_missing

aggregate_or_row_square_only
  decision = repair_oriented_edge_selection_missing

projector_values_without_fourth_root
  decision = repair_mu4_root_selection_missing

two_edge_pair_without_oriented_square_root
  decision = repair_sign_or_root_missing

exact_quartic_selector_without_finite_theorem
  decision = repair_value_divisor_theorem_missing

coarse_quartic_phase_or_magnitude_only
  decision = repair_quartic_edge_selection_missing

ambiguous_power_value_without_selector
  decision = repair_power_root_selection_missing

finite_payload_without_source
  decision = repair_arithmetic_source_theorem_missing

generic_cm_or_class_field_generation
  decision = repair_danger3_finite_framing_missing

coset_selector_or_Q_source_only
  decision = repair_finite_value_divisor_theorem_missing

Q_diagonal_value_only
  decision = support_diagonal_aggregate_selector_missing

Q_plus_row_quotient_without_root
  decision = repair_oriented_square_root_missing

Q6_boundary_only
  decision = repair_additive_or_value_normalization_missing

pure_character_degree6_norm
  decision = reject_pure_character_degree6_norm_cancels
```

## Packet Use

For any future expert answer or source snippet:

```text
1. Normalize the object to one row, a row-labeled orbit theorem, or a heavier
   exact-P/theta2 bridge.
2. Check arithmetic source theorem provenance.
3. Check boundary: Norm_156(Y_507) for the oriented row, or the matching sign
   for a reciprocal presentation.
4. Check scalar/branch normalization: additive value, basepoint,
   branch/root, telescoping product, or period-156 value context.
5. Normalize through the source-stage spine to one scalar-fixed legal
   support-156 row.
6. If all first-pass clauses are present, route to DANGER3 framing and
   same-j/X_1(16)/halving extraction. Otherwise classify as repair/reject.
```

## Counts

```text
source_markers_ok = 11/11
row_hashes_ok = 4/4
intake_rows_ok = 6/6
first_pass_frontdoor_routes = 5
support_or_heavy_routes = 3
repair_or_reject_rows = 18
current_source_theorems = 0
submission_ready_rows = 0
p25_v2_first_pass_expert_intake_packet_rows=1/1
```

## Verdict

The current expert/source loop is narrow enough to be binary. A useful answer
either supplies all clauses for one first-pass intake row, supplies the heavier
exact-P/theta2 upstream theorem, or gives a sharp falsifier for the exact row
identity plus scalar-fixed theorem shape. Broad source rereads, selector-only
answers, and boundary-only answers should be killed or repaired immediately.
