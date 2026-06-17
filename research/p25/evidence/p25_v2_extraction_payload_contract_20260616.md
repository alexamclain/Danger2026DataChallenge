# P25 v2 Extraction Payload Contract

Updated: 2026-06-16

## Purpose

Promote the constructive payload contract after a p25 source theorem hit.  The
source theorem target is now precise, but a theorem-stage win is still not a
DANGER3 certificate.  This page pins the ladder from source theorem to same-j
bridge, practical `X_1(16)` payload, halving/direct `x0`, and official
`vpp.py`.

This is not a source-stage theorem and not a certificate.  It is the downstream
acceptance contract for future theorem or expert-answer payloads.

## Pages Read

- `frontier.md`
- `lanes/practical-search.md`
- `evidence/p25_v2_post_theorem_extraction_router_20260616.md`
- `evidence/p25_v2_unified_submission_extraction_contract_20260616.md`
- `evidence/p25_v2_source_snippet_intake_20260616.md`
- `archive/notes/p25_ksy_y_h0_x18112_bridge_payload_contract_20260614.md`
- `archive/notes/p25_ksy_y_x1_16_montgomery_chart_contract_20260614.md`
- `archive/notes/p25_ksy_y_x1_16_halving_certificate_payload_20260614.md`

## Command

```bash
python3 research/p25/archive/gates/p25_v2_extraction_payload_contract_gate.py
```

The gate returned `p25_v2_extraction_payload_contract_rows=1/1`.

## Arithmetic Boundary

```text
p mod 8 = 5
sqrt_floor = 3162277660168
hasse_bound = 3162281216727
k = 42

8112 = 16 * 507
507^-1 mod 16 = 3
16^-1 mod 507 = 412
P16  = [1521]R
Q507 = [6592]R
1521 + 6592 = 1 mod 8112
ord(P16) = 16
ord(Q507) = 507

active mode = x16halvenonsplit
active start depth = 4
active halving links = 38
active x-chain points = 39

optional mode = x16halvenonsplitdgate
optional start depth = 5
optional halving links = 37
```

## Payload Rows

```text
source_theorem_no_framing
  decision = source_stage_win_danger3_framing_missing
  missing  = DANGER3 finite-identity / non-CM framing

framed_source_no_bridge
  decision = framed_source_same_j_bridge_missing
  missing  = same-j X_1(8112) bridge or equivalent fiber product

independent_p16_q507
  decision = reject_unglued_components
  falsifier = same j-invariant / same elliptic curve bridge missing

same_j_invariant_only
  decision = repair_same_j_invariant_only
  missing  = explicit same-curve P16/Q507 pair, order-8112 generator, or
             direct A,xP16

same_j_components_no_surface
  decision = same_j_components_order8112_or_x16_missing
  missing  = order-8112 generator, same-curve P16/Q507 pair, or direct X_1(16) payload

order8112_generator_only
  decision = order8112_bridge_x16_surface_missing
  missing  = X_1(16) y/model-root/A/xP16 surface or direct A,xP16

x16_y_only
  decision = x16_y_chart_missing_model_root
  missing  = model root x satisfying the X_1(16) quadratic

x16_y_model_root_surface
  decision = active_surface_reached_halving_missing
  missing  = 38-link halving chain from xP16 to x0 or direct x0

direct_A_xP16_surface
  decision = active_surface_reached_halving_missing
  missing  = 38-link halving chain from xP16 to x0 or direct x0

optional_dgate_surface
  decision = optional_depth5_surface_reached_halving_missing
  missing  = 37-link halving chain from x32 to x0 or direct x0

branch_word_without_values
  decision = reject_branch_word_without_values
  falsifier = actual square-root witnesses, x-chain, direct x0, or vpp.py missing

x_coordinate_chain
  decision = checkable_x_chain_vpp_missing
  missing  = official src/vpp.py verification

direct_A_x0
  decision = extraction_ready_vpp_missing
  missing  = official src/vpp.py verification

official_vpp_verified_triple
  decision = submission_ready
  missing  = none
```

## Counts

```text
bridge_stage_rows = 5
x16_surface_rows = 5
optional_dgate_rows = 1
extraction_ready_rows = 3
submission_ready_rows = 1
repair_rows = 11
reject_rows = 2
current_live_payload_rows = 0
```

## Verdict

Use this contract after source-snippet intake:

```text
source theorem
-> DANGER3 finite-identity / non-CM framing
-> same-j X_1(8112) bridge or order-8112 generator
-> practical X_1(16) y plus model root, or direct A,xP16
-> 38-link x-chain / active witness chain / direct x0
-> official vpp.py
```

Do not treat independent `P16` and `Q507` data as a bridge without same-j
gluing.  Do not treat a matching `j` value alone as a bridge without explicit
same-curve torsion data or a direct practical surface.  Do not require the
optional d-gate surface for the current production mode.  Do not accept a
branch word without concrete values.  Official `vpp.py` verification remains
the submission boundary.
