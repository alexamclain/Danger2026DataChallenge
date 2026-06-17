# P25 v2 Exact-P Orientation Branch Router

Updated: 2026-06-16

## Purpose

Promote the exact-P orientation word into an explicit branch classifier. The
minimal exact-P hook asks for `C,D,K,orientation`; this page says which four
raw branches are accepted, which theta2 payload each branch emits, and how
value-only branch claims are routed.

This is not an arithmetic producer theorem. It is a finite intake router for a
future exact-P theorem or source snippet.

## Pages Read

- `frontier.md`
- `lanes/exact-p.md`
- `evidence/p25_v2_exactp_minimal_hook_20260616.md`
- `evidence/p25_v2_exactp_theorem_interface_contract_20260616.md`
- `evidence/p25_v2_theta2_period156_support_contract_20260616.md`
- `evidence/p25_v2_period156_value_branch_contract_20260616.md`
- `evidence/p25_v2_source_snippet_intake_20260616.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_exactp_orientation_branch_router_gate.py
```

The gate returned `p25_v2_exactp_orientation_branch_router_rows=1/1`.

## Accepted Branches

```text
center_forward_route
  center = (47, 28)
  D = (22, 3)
  Kmult = 1
  reverse = 0
  emits = theta2_inverse
  recovered_sign = -1

center_reverse_route
  center = (47, 28)
  D = (22, 3)
  Kmult = 1
  reverse = 1
  emits = theta2
  recovered_sign = 1

inverse_center_forward_route
  center = (28, 141)
  D = (22, 3)
  Kmult = 1
  reverse = 0
  emits = theta2
  recovered_sign = 1

inverse_center_reverse_route
  center = (28, 141)
  D = (22, 3)
  Kmult = 1
  reverse = 1
  emits = theta2_inverse
  recovered_sign = -1
```

All four branches route through the divisor/additive theta2 certificate path.

## Intake Routes

```text
one_of_four_oriented_branches_with_divisor_additive_payload
  decision = exactp_source_stage_win_route_to_extraction
  missing  = downstream DANGER3 framing and extraction

one_of_four_oriented_branches_with_period156_value_context
  decision = exactp_source_stage_win_route_to_extraction
  missing  = downstream DANGER3 framing and extraction

branchless_C_D_K_orientation_word
  decision = repair_exactp_orientation_branch_missing
  missing  = one of the four raw center/reverse branches and theta2/theta2^-1
             output

theta2_value_without_period156_context
  decision = repair_period156_branch_selection_missing
  missing  = period-156 theta2 fixedness, branch, root, or telescoping data

ambient780_value_only
  decision = repair_period156_branch_selection_missing
  missing  = ambient route has mu_11 ambiguity in F_p^*

wrong_center_wrong_d_or_nonprimitive_k
  decision = reject_wrong_exactp_payload
  falsifier = raw orientation router rejects wrong center, wrong D, and
              nonprimitive K
```

## Counts

```text
evidence_markers_ok = 5/5
accepted_orientation_branches = 4
theta2_inverse_routes = 2
theta2_routes = 2
support_period = 156
support_period_value_root_unique_fp = 1
ambient_value_branch_count_fp = 11
rejected_controls = 3
current_exactp_source_theorems = 0
current_submission_ready = 0
p25_v2_exactp_orientation_branch_router_rows=1/1
```

## Verdict

```text
positive_artifact = exact-P orientation branch intake router
continue_exactp = yes
accepted_branch_hit = one of four raw center/reverse branches plus divisor/
                      additive theta2 payload, or value payload with
                      period-156 context
discard_condition = branchless orientation word, ambient-period value only,
                    wrong center, wrong D, or nonprimitive K
```

Exact-P remains open, but future expert or source replies should no longer use
`orientation` as an opaque word. The theorem must identify one of the four
raw branches above, or provide an accepted theta2/theta2-inverse payload with
the equivalent branch information.
