# P25 v2 Live Theorem Ask Packet

Updated: 2026-06-17

Marker: `p25_v2_live_theorem_ask_packet_rows=1/1`

## Purpose

Turn the classified source lookup rows into the next action surface. This is
the packet to use for a Drew question, a narrow literature pass, or a proof
attempt after the priority-1, period-156, Q/Yang, normalizer, and exact-P
lookup rows were pinned.

This page is not another source scan. It says what a useful answer must
contain and where it routes next.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `lanes/exact-p.md`
- `evidence/p25_v2_source_action_registry_20260616.md`
- `evidence/p25_v2_first_pass_expert_intake_packet_20260616.md`
- `evidence/p25_v2_priority1_source_lookup_capsule_20260617.md`
- `evidence/p25_v2_period156_lookup_row_status_20260617.md`
- `evidence/p25_v2_q_yang_lookup_row_status_20260617.md`
- `evidence/p25_v2_normalizer_lookup_row_status_20260617.md`
- `evidence/p25_v2_exactp_theta2_lookup_row_status_20260617.md`
- `evidence/p25_v2_source_stage_normalization_spine_20260617.md`
- `evidence/p25_v2_matched_quotient_closure_packet_20260617.md`
- `evidence/p25_v2_source_theorem_acceptance_automaton_20260617.md`
- `evidence/p25_v2_source_snippet_intake_20260616.md`
- `evidence/p25_v2_current_expert_response_rubric_20260616.md`
- `evidence/p25_v2_post_theorem_extraction_router_20260616.md`
- `evidence/p25_v2_unified_submission_extraction_contract_20260616.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_live_theorem_ask_packet_gate.py
```

The gate returned `p25_v2_live_theorem_ask_packet_rows=1/1`.

## Live Ask Rows

```text
first_pass_row_theorem
  status          = live_primary
  required_object = one oriented legal support-156 row R_m, m in {1,2,4,8},
                    with Norm_156(Y_507) boundary
  positive_hook   = scalar-fixed finite divisor/additive theorem, or uniquely
                    invertible finite power-value theorem, or aggregate theorem
                    plus exact matched zero-lattice quotient, from an
                    arithmetic source
  first_falsifier = legality-only, boundary-only, selector-only, aggregate
                    without matched quotient, Q-only without selector debt, or
                    unspecified F_p^* scalar
  next_action     = ask Drew/source/proof attempt for the finite theorem;
                    route positives to source-stage normalization then the
                    extraction router

period156_h0_y507_value
  status          = live_support_value
  required_object = canonical H0 or Y_507 support-period-156 value with
                    legal-row bridge
  positive_hook   = finite value theorem with branch/root/telescoping or
                    additive normalization, avoiding ambient-period-780
                    ambiguity
  first_falsifier = class-field generation, ambient-period-780 value, mu_11
                    quotient, degree-6 value without F_p descent, or value up
                    to scalar
  next_action     = use only when a source snippet already names H0/Y_507
                    period-156 data; otherwise keep as support

exactp_theta2_heavy
  status          = live_heavy
  required_object = compact C,D,K,orientation packet, equal-weight 75 atoms,
                    or accepted theta2/theta2-inverse payload
  positive_hook   = arithmetic theorem emitting the exact packet, primitive
                    KL word or mixed selector, Sprang sparse specialization,
                    or reverse reconstruction
  first_falsifier = normalized-y vocabulary, raw KL exponent balance, generic
                    modular-unit generation, theta language without
                    period-156 branch, or unified-target-only theorem
  next_action     = keep as second-pass moonshot unless the source/proof
                    already carries one accepted exact-P hook
```

## How To Use This Packet

For an expert question, lead with the first row:

```text
Do you know a finite divisor/additive theorem, or an exact uniquely
root-invertible finite value theorem, for one of the four legal support-156
H0/conductor-39 rows R_m with boundary Norm_156(Y_507)?
```

Then ask for the missing clauses explicitly:

```text
row label/orientation
arithmetic source theorem
Norm_156(Y_507) boundary or accepted reciprocal sign
scalar/branch/value normalization over F_p
evaluable finite payload or theorem body
```

If the answer is value-side rather than divisor/additive, route it through the
period-156 row before updating H0 or conductor 39. If the answer is exact-P,
route it through the exact-P/theta2 heavy row and do not treat a unified
support-156 theorem as exact-P recovery unless it also supplies the exact-P
selector data.

## Stop Conditions

```text
kill_as_broad_reread
  any request for "p25-relevant modular units" without one of the three rows

repair_as_source_legality_only
  Koo-Shin Theorem 6.2, source certification, class-field generation, or
  modular-unit generation without a finite p25 theorem

repair_as_boundary_only
  Norm_156(Y_507), Hilbert-90 boundary, Q^6 boundary, or divisor class without
  scalar-fixed finite value/additive normalization

repair_as_selector_only
  row labels, C4 phase, projector values, Q split, or KL exponent balance
  without the arithmetic theorem and finite payload

route_to_extraction
  only after a source-stage theorem normalizes to one scalar-fixed legal row
  or after an accepted exact-P/theta2 theorem supplies its bridge
```

## Counts

```text
evidence_markers_ok = 14/14
live_theorem_asks = 3
broad_reread_allowed_rows = 0
current_source_stage_closers = 0
current_submission_ready = 0
p25_v2_live_theorem_ask_packet_rows=1/1
```

## Verdict

The plan is now fully artifact-driven on the theory side. The next meaningful
mathematical output is not another lane survey; it is either:

```text
1. a source-stage theorem for one scalar-fixed legal support-156 row,
2. a period-156 H0/Y_507 value theorem with branch/normalization and row bridge,
3. an exact-P/theta2 upstream theorem carrying the accepted packet, or
4. a sharp falsifier proving one of those theorem shapes cannot exist.
```

Everything else stays support, repair, or archive provenance.
