# P25 v2 Exact-P 75-Anchor Bridge Filter

Updated: 2026-06-17

Marker: `p25_v2_exactp_75_anchor_bridge_filter_rows=1/1`

## Purpose

Separate two superficially similar "75" claims:

```text
R_m^75 for one legal H0/conductor-39 row
exact equal-weight 75-atom normalized-y/theta2 product
```

The common-scalar filter says an exact row-labeled `R_m^75` value would
uniquely recover `R_m` because `gcd(75, p - 1) = 1`. That does not mean the
exact-P 75 atoms are automatically a first-pass row-power theorem. They live
in the exact-P normalized-y/theta2 atom basis and still need the exact
orientation and `75 -> 300 -> 12 -> 312 -> 156` bridge.

## Pages Read

- `frontier.md`
- `lanes/exact-p.md`
- `evidence/p25_v2_common_scalar_anchor_filter_20260617.md`
- `evidence/p25_v2_extended_unique_power_intake_20260617.md`
- `evidence/p25_v2_exactp_finite_geometry_rigidity_20260616.md`
- `evidence/p25_v2_exactp_minimal_hook_20260616.md`
- `evidence/p25_v2_exactp_to_unified_target_spine_20260616.md`
- `evidence/p25_v2_reverse_exactp_information_loss_20260616.md`
- `evidence/p25_v2_exactp_theta2_lookup_row_status_20260617.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_exactp_75_anchor_bridge_filter_gate.py
```

The gate returned `p25_v2_exactp_75_anchor_bridge_filter_rows=1/1`.

## Rows

```text
row_power_Rm75
  object_basis = H0/conductor-39 legal row value R_m
  scalar_test  = gcd(75, p-1) = 1
  accepted_if  = exact row-labeled finite theorem for R_m^75 plus boundary or
                 period bridge
  decision     = first_pass_anchor_after_inverse_exponent
  falsifier    = rowless 75-power, value up to scalar, or boundary-only
                 powered divisor

equal_weight_75_atom_exactp
  object_basis = exact-P normalized-y/theta2 atom basis
  scalar_test  = 75 atoms have disjoint 4-cell supports and forced equal
                 weights
  accepted_if  = challenge-legal exact 75-atom theorem with orientation and
                 75->300->12->312->156 bridge
  decision     = heavy_upstream_source_candidate_not_row_power_shortcut
  falsifier    = normalized-y vocabulary, finite fixture, nonuniform weights,
                 or atom count without source

compact_cdk_orientation
  object_basis = exact-P packet C,D,K plus one accepted orientation branch
  scalar_test  = orientation selects theta2 or theta2^-1 branch before bridge
  accepted_if  = arithmetic theorem emits compact packet and exact equal-weight
                 payload
  decision     = heavy_upstream_source_candidate_route_to_unified_then_extraction
  falsifier    = branchless orientation word, wrong center, wrong D, or
                 nonprimitive K

theta2_period156_payload
  object_basis = theta2/theta2-inverse divisor-additive payload
  scalar_test  = period-156 branch is unique in F_p after accepted bridge
  accepted_if  = exact theta2 payload with period-156 branch/root/telescoping
                 and bridge data
  decision     = heavy_upstream_or_value_bridge_candidate
  falsifier    = ambient-period-780 value, theta vocabulary, or Sprang D=2
                 support without sparse packet

unified_support156_to_exactp
  object_basis = H0/conductor-39 support-156 target
  scalar_test  = not a reverse exact-P selector
  accepted_if  = explicit reverse reconstruction theorem supplies
                 C,D,K/orientation or 75 atoms
  decision     = reject_reverse_without_extra_selector_structure
  falsifier    = unified value/divisor theorem alone or Y_507 bridge alone

atom_count_only
  object_basis = phrase containing 75 atoms or C_75 without exact payload
  scalar_test  = gcd(75,p-1) is irrelevant without row or bridge basis
  accepted_if  = never by count alone
  decision     = repair_exact_theorem_and_orientation_missing
  falsifier    = 75 vocabulary, ray-class generation, KL balance, or finite
                 packet without source
```

## Counts

```text
evidence_markers_ok = 7/7
bridge_rows = 6
first_pass_anchor_rows = 1
exactp_heavy_candidate_rows = 3
reverse_reject_rows = 1
repair_rows = 1
current_exactp_source_theorems = 0
current_row_power_75_theorems = 0
current_submission_ready = 0
p25_v2_exactp_75_anchor_bridge_filter_rows=1/1
```

## Verdict

The 75-count is useful but easy to over-credit:

```text
R_m^75 exact finite value theorem
  -> first-pass row anchor after inverse exponent

exact equal-weight 75-atom theorem
  -> exact-P heavy source-stage candidate only with orientation and bridge

75 vocabulary / atom count / C_75 context
  -> repair, not a theorem
```

So the common-scalar filter expands intake for future row-power theorems, but
it does not collapse exact-P into a cheap `R_m^75` shortcut. Exact-P remains
the stronger upstream moonshot: valuable, sharply specified, and still missing
an arithmetic source theorem.
