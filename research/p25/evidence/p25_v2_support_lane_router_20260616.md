# P25 v2 Support Lane Router

Updated: 2026-06-16

## Purpose

Prevent older support lanes from drifting back into independent moonshots.
Twisted-H90 and curved-corner remain useful labels for possible value/divisor
source snippets, but in the v2 wiki they are support surfaces routed through
the same period-156 value source hook. Exact-P remains the separate heavy
upstream route.

## Pages Read

- `frontier.md`
- `concepts/transfer-matrix.md`
- `lanes/exact-p.md`
- `lanes/twisted-h90.md`
- `lanes/curved-corner.md`
- `evidence/p25_v2_period156_value_source_hook_20260616.md`
- `evidence/p25_v2_theta2_period156_support_contract_20260616.md`
- `evidence/p25_v2_exactp_minimal_hook_20260616.md`
- `evidence/p25_v2_positive_theorem_clause_matcher_20260616.md`
- `evidence/p25_v2_current_expert_response_rubric_20260616.md`
- `evidence/p25_v2_source_snippet_intake_20260616.md`
- `evidence/p25_v2_frontdoor_count_sync_20260616.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/archive/gates/p25_v2_support_lane_router_gate.py
```

The gate returned `p25_v2_support_lane_router_rows=1/1`.

## Routing Rows

```text
twisted_h90
  role     = support value/divisor surface
  decision = support_lane_not_frontdoor
  route    = period156_value_source_hook_then_source_snippet_intake
  missing  = exact twisted/H90 source object plus period-156
             branch/root/telescoping and arithmetic source theorem

curved_corner
  role     = support value/divisor surface
  decision = support_lane_not_frontdoor
  route    = period156_value_source_hook_then_source_snippet_intake
  missing  = exact unit-triangle curved K-traced payload plus period-156
             branch/root/telescoping and arithmetic source theorem

exact_p
  role     = heavy upstream route
  decision = heavy_route_not_first_pass_default
  route    = exactp_minimal_hook_then_extraction_contract
  missing  = compact C,D,K,orientation packet, exact equal-weight 75 atoms,
             accepted theta2 payload, or explicit reverse reconstruction
             theorem
```

## Counts

```text
evidence_markers_ok = 7/7
support_lanes = 2
frontdoor_support_lanes = 0
heavy_routes = 1
current_source_closers = 0
p25_v2_support_lane_router_rows=1/1
```

## Verdict

```text
positive_artifact = support-lane routing guard
continue_first_pass = yes
intake_rule = twisted-H90 and curved-corner snippets must enter through the
              period-156 value source hook; exact-P snippets must enter
              through the exact-P minimal hook
discard_condition = support-lane lead only repeats broad H90, norm,
                    curved-product, or unit-triangle vocabulary
```
