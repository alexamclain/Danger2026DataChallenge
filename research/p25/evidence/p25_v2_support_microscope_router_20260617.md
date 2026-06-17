# P25 v2 Support Microscope Router

Updated: 2026-06-17

Marker: `p25_v2_support_microscope_router_rows=1/1`

## Purpose

Synchronize the support-lane policy after the McCarthy square-axis endpoint
pass.

The older support-lane router demoted twisted-H90 and curved-corner, while the
new McCarthy endpoint pass promoted a concrete Lane-B support microscope. This
page puts both kinds of support work under one routing rule:

```text
support surface or microscope
  -> useful only when attached to a named theorem idea or exact endpoint
  -> not an independent first-pass front
```

## Pages Read

- `frontier.md`
- `concepts/transfer-matrix.md`
- `lanes/twisted-h90.md`
- `lanes/curved-corner.md`
- `lanes/exact-p.md`
- `evidence/p25_v2_support_lane_router_20260616.md`
- `evidence/p25_v2_support_lane_status_demotion_20260616.md`
- `evidence/p25_v2_mccarthy_endpoint_stability_router_20260617.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_support_microscope_router_gate.py
```

The gate returned `p25_v2_support_microscope_router_rows=1/1`.

## Routing Rows

```text
twisted_h90
  role     = period156_support_surface
  route    = period156_value_source_hook_then_source_snippet_intake
  decision = support_surface_not_frontdoor
  missing  = exact twisted/H90 source object with period-156 context and
             arithmetic source theorem

curved_corner
  role     = period156_support_surface
  route    = period156_value_source_hook_then_source_snippet_intake
  decision = support_surface_not_frontdoor
  missing  = exact unit-triangle curved K-traced payload with period-156
             context and arithmetic source theorem

lane_b_c_generic_microscopes
  role     = attached_support_microscope
  route    = only_when_tied_to_H0_conductor39_or_exactP_theorem_idea
  decision = not_standalone_moonshot
  falsifier = probe is not attached to a concrete theorem idea or produces
              only broad count/vocabulary data

mccarthy_square_axis_endpoint
  role     = exactp_endpoint_test_microscope
  route    = sparse_endpoint_theorem_or_invariant_cancellation_only
  decision = endpoint_test_not_frontdoor
  missing  = arithmetic theorem producing e_138, or nontrivial
             auxiliary-prime-invariant quotient cancellation

exact_p
  role     = heavy_upstream_route
  route    = exactp_minimal_hook_then_extraction_contract
  decision = heavy_route_not_first_pass_default
  missing  = compact C,D,K,orientation, equal-weight 75 atoms, accepted
             theta2 payload, or explicit reverse reconstruction theorem
```

## Counts

```text
evidence_markers_ok = 6/6
route_rows = 5
period156_support_surfaces = 2
support_microscopes = 2
heavy_routes = 1
frontdoor_support_rows = 0
current_source_closers = 0
p25_v2_support_microscope_router_rows=1/1
```

## Verdict

The support policy is now explicit:

```text
continue twisted-H90 / curved-corner
  only on exact source object + period-156 or scalar-fixed theorem data

continue generic Lane-B / Lane-C probes
  only when tied to H0, conductor 39, exact-P, or a named theorem idea

continue McCarthy square-axis
  only as sparse endpoint theorem intake or invariant-cancellation test

do not promote support surfaces or microscopes to first-pass front doors
```

This preserves useful finite artifacts without letting broad support
vocabulary consume the moonshot queue.
