# P25 KSY-y Post-Bridge X1(16) Surface Intake

Updated: 2026-06-14 21:00 PDT

## Purpose

This intake starts after a same-`j` `X_1(8112)` bridge has been accepted.  It
decides whether the bridge has reached the practical `X_1(16)` Montgomery
surface used by the production search.

Active route:

```text
mode  = x16halvenonsplit
start = halve_chain_from_depth(A, xP16, depth=4, k=42)
need  = y plus model root x, or directly A,xP16
```

Optional route:

```text
mode  = x16halvenonsplitdgate
start = halve_chain_from_depth(A, x32, depth=5, k=42)
extra = z/sd first-half d-gate data
```

The optional d-gate is not required for the active production mode.

## Route Rows

```text
no_same_j_bridge:
  decision = conditional_same_j_bridge_missing
  missing  = accepted same-j X_1(8112) bridge
  next     = return to the post-policy X_1(8112) work order

same_j_no_p16:
  decision = conditional_same_curve_p16_missing
  missing  = same-curve 16-torsion component P16
  next     = project the X_1(8112) bridge to P16 or supply same-curve P16

abstract_p16:
  decision = abstract_p16_not_practical_chart
  missing  = X_1(16) y-chart parameter or direct A,xP16
  next     = specialize the bridge to the production Montgomery chart

x16_y_only:
  decision = y_chart_missing_model_root
  missing  = model root x satisfying the X_1(16) quadratic
  next     = derive x, then A and xP16

x16_y_and_model_root:
  decision = active_surface_reached_halving_missing
  missing  = halve chain from xP16 at depth 4 to x0
  next     = derive the halving chain or direct x0, then run official vpp.py

direct_A_xP16:
  decision = active_surface_reached_halving_missing
  missing  = halve chain from xP16 at depth 4 to x0
  next     = derive the halving chain or direct x0, then run official vpp.py

dgate_first_half_surface:
  decision = optional_depth5_surface_reached_halving_missing
  missing  = halve chain from x32 at depth 5 to x0
  next     = derive the halving chain or direct x0, then run official vpp.py

active_first_branch_chain_to_x0:
  decision = x0_extracted_official_vpp_missing
  missing  = official vpp.py verification
  next     = run official vpp.py and archive output

any_valid_chain_to_x0:
  decision = x0_extracted_not_active_path_vpp_missing
  missing  = official vpp.py verification; active-path provenance optional
  next     = run official vpp.py; retain chain provenance if available

direct_x0_without_chain:
  decision = direct_x0_official_vpp_missing
  missing  = official vpp.py verification
  next     = run official vpp.py on the concrete A,x0 payload

official_vpp_verified_boundary:
  decision = submission_ready
  missing  = none
  next     = archive official vpp.py output, command, environment, and certificate
```

The official-vpp row is a boundary shape only.  It is not current evidence.

## Counts

```text
row_count               = 11
current_evidence_rows   = 0
bridge_established_rows = 9
active_surface_rows     = 7
optional_dgate_rows     = 1
extraction_ready_rows   = 4
submission_ready_rows   = 1
rejected_rows           = 0
conditional_rows        = 2
```

## Dependencies

```text
ksy_y_x18112_bridge_claim_packet_fixture_export_rows=1/1
ksy_y_x1_16_montgomery_chart_contract_rows=1/1
ksy_y_x1_16_halving_chain_contract_rows=1/1
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_post_bridge_x16_surface_intake_gate.py
```

The gate also accepts copied packet JSON:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_post_bridge_x16_surface_intake_gate.py \
  --packet-json <packet.json>
```

Sample packet:

```text
research/p25/post_bridge_x16_surface_packet_samples/direct_A_xP16_surface.json
```

Expected:

```text
active_surface_reached_halving_missing
ksy_y_post_bridge_x16_surface_packet_candidate_rows=1/1
```

Marker:

```text
ksy_y_post_bridge_x16_surface_intake_rows=1/1
```

## Interpretation

After a same-`j` bridge, the next payload should be one of:

```text
y and model root x, hence A and xP16
direct A,xP16
```

That reaches the active `x16halvenonsplit` surface.  From there the remaining
work is a depth-`4` halving chain to `x0`, or a direct concrete `x0`, followed
by official `vpp.py`.
