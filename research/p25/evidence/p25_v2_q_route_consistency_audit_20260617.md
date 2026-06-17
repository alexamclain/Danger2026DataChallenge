# P25 v2 Q-Route Consistency Audit

Updated: 2026-06-17

Marker: `p25_v2_q_route_consistency_audit_rows=1/1`

## Purpose

Lock the conductor-39 `Q` support route against over-promotion. The Q-route
evidence stack is useful, but scattered: `Q/Q^3` support, `Q^6` boundary
repair, Q diagonal/split normalization, Q-square bounded payload, extraction
boundary, local-source scan, and Q/Yang lookup status each live in separate
screens.

This audit checks that all of those screens agree on the same boundary:
`Q` data is support/normalization unless it pays selector debt, supplies an
oriented split/root, gives a Q-square value plus extraction map, or directly
proves one legal edge theorem.

## Pages Read

- `frontier.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_conductor39_norm_one_quotient_route_20260616.md`
- `evidence/p25_v2_q_route_selector_debt_20260616.md`
- `evidence/p25_v2_q_diagonal_normalization_20260616.md`
- `evidence/p25_v2_q_split_quartic_selector_20260616.md`
- `evidence/p25_v2_q_square_payload_router_20260616.md`
- `evidence/p25_v2_q_square_extraction_boundary_20260616.md`
- `evidence/p25_v2_q_route_source_hook_scan_20260616.md`
- `evidence/p25_v2_q_route_candidate_sweep_20260617.md`
- `evidence/p25_v2_q_yang_lookup_row_status_20260617.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_q_route_consistency_audit_gate.py
```

The gate returned `p25_v2_q_route_consistency_audit_rows=1/1`.

## Checked Boundary

```text
Q or Q^3 finite theorem data:
  support_only_until_selector_paid

Q^6 / Hilbert-90 boundary only:
  repair_additive_or_value_normalization_missing

Q diagonal plus correct pure quartic split:
  repair until oriented root/sign or direct edge theorem is supplied

Exact scalar-fixed Q-square finite value:
  bounded_two_root_payload_not_source_close
  extraction map still required

Direct one-edge theorem:
  routes back to priority-1 source-stage intake
```

## Counts

```text
evidence_markers_ok = 9/9
candidate_consistent = 1
lookup_consistent = 1
square_consistent = 1
evidence_text_consistent = 1
canonical_pages_ok = 1
surviving_q_intake_families = 4
current_q_source_hooks = 0
current_source_stage_closers = 0
current_extraction_ready = 0
current_submission_ready = 0
p25_v2_q_route_consistency_audit_rows=1/1
```

## Verdict

The `Q` route remains live, but only as a support/normalization route. A future
answer should be promoted only if it supplies one of:

```text
Q or Q^3 finite theorem data with selector debt paid;
Q diagonal plus correct pure quartic split plus oriented root/sign;
exact scalar-fixed Q-square value plus extraction map;
direct one-edge scalar-fixed finite theorem.
```

Everything else stays support, repair, or reject. Current Q source hooks,
source-stage closers, extraction-ready rows, and submission-ready rows remain
zero.
