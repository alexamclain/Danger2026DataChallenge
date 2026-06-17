# P25 v2 Priority-1 Packet Fixture Contract

Updated: 2026-06-17

Marker: `p25_v2_priority1_packet_fixture_contract_rows=1/1`

## Purpose

Promote the archived priority-1 source-answer fixtures into the current v2
intake contract without reviving the old lane ordering. These fixtures are
useful because they make future theorem snippets and expert answers
machine-checkable before lane promotion.

This is not a theorem and not a new source scan. It is a packet contract for
classifying hypothetical source answers.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `lanes/twisted-h90.md`
- `lanes/curved-corner.md`
- `evidence/p25_v2_self_contained_theorem_statement_20260616.md`
- `evidence/p25_v2_source_snippet_intake_20260616.md`
- `evidence/p25_v2_priority1_divisor_additive_work_order_20260617.md`
- `evidence/p25_v2_priority1_source_lookup_capsule_20260617.md`
- `evidence/p25_v2_live_theorem_ask_packet_20260617.md`
- `evidence/p25_v2_current_theorem_kernel_20260617.md`
- `evidence/p25_v2_support_lane_status_demotion_20260616.md`
- `archive/fixtures/priority1_divisor_additive_packet_fixtures/*.json`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_priority1_packet_fixture_contract_gate.py
```

The gate returned `p25_v2_priority1_packet_fixture_contract_rows=1/1`.

## V2 Reclassification

The archived fixtures split as follows under the current first-class run:

```text
h0_divisor_close.json
  decision = current_first_pass_positive_packet
  meaning  = an H0 source answer with exact row, H90 boundary, arithmetic
             source theorem, and finite divisor/additive payload would enter
             source-stage normalization.

conductor39_divisor_close.json
  decision = current_first_pass_positive_packet
  meaning  = a mixed U_chi/W answer preserving the tensor, Yang lift, H90
             descent, arithmetic source theorem, and finite divisor/additive
             payload would enter source-stage normalization.

twisted_divisor_close.json
curved_corner_divisor_close.json
  decision = support_packet_requires_source_snippet
  meaning  = still useful if a snippet already carries the exact source object
             and period-156 context, but not a reopened first-pass front door.

h0_missing_boundary.json
  decision = repair_h0_boundary_missing

twisted_missing_period.json
curved_missing_period.json
  decision = repair_period156_context_missing

projection_reject.json
  decision = reject_projection_or_axis_only
```

## Consequence

Future source or expert answers can be tested as packets before any lane page
changes. A current first-pass positive packet must look like one of the two
front-door rows:

```text
H0:
  exact legal H0 row/product
  Hilbert-90 boundary
  arithmetic source theorem
  finite scalar-fixed divisor/additive payload

conductor 39:
  mixed U_chi/W object
  chi_3 tensor chi_13 structure preserved
  Yang distribution/lift to the level-507 object
  Frobenius or Hilbert-90 descent
  arithmetic source theorem
  finite scalar-fixed divisor/additive payload
```

The packet contract is also bound to the four legal row identities already
published by the self-contained theorem statement and source-snippet intake:

```text
m=1  sha256=eb5a86ae58b16b7e10706ac166d1f548aaccdfc677181a253119b6876e470d1e
m=2  sha256=97517200105db6e1f44e04e76977407615a88c8b4ca782fefec6cb2821e0a0e9
m=4  sha256=28b3e03228d428ac6474ff92eaefb1a9a7dfbfda8af2318812d5bca68e8958d6
m=8  sha256=ace1a01fa59701567225b8f781ffda2fe308aac41662f80439ace7a6cda7bf87
```

Thus a future H0 or conductor-39 packet must identify one row by `m`, edge, or
stable hash before it can change lane status.

Twisted-H90 and curved-corner packets remain support surfaces: they are worth
continuing only when a concrete snippet already includes the exact source
object and period-156 context.

## Counts

```text
evidence_markers_ok = 7/7
legal_row_hashes_ok = 4/4
fixture_rows = 8
legal_row_hashes_bound = 4
current_first_pass_positive_packets = 2
support_only_positive_packets = 2
repair_packets = 3
reject_packets = 1
current_priority1_source_theorems = 0
current_source_stage_closers = 0
current_submission_ready = 0
p25_v2_priority1_packet_fixture_contract_rows=1/1
```

## Verdict

Keep the fixture set as the mechanical source-answer intake for priority-1
work. Promote only H0 or conductor-39 packets that satisfy all finite theorem,
boundary, and scalar-fixing clauses. Route twisted-H90 and curved-corner
packets as support unless the source snippet itself already carries the exact
period-156 object.
