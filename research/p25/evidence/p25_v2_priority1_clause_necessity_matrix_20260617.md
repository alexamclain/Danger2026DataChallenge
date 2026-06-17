# P25 v2 Priority-1 Clause Necessity Matrix

Updated: 2026-06-17

Marker: `p25_v2_priority1_clause_necessity_matrix_rows=1/1`

## Purpose

Strengthen the priority-1 packet contract by proving that each required H0
and conductor-39 packet clause is necessary. The packet fixture contract gives
positive and near-miss examples; this matrix mutates the two positive
front-door fixtures one clause at a time and verifies that no damaged packet
still classifies as a current first-pass positive.

This is not a theorem and not a source scan. It is a false-positive guard for
future source snippets and expert answers.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_priority1_packet_fixture_contract_20260617.md`
- `evidence/p25_v2_current_theorem_kernel_20260617.md`
- `evidence/p25_v2_source_stage_normalization_spine_20260617.md`
- `evidence/p25_v2_self_contained_theorem_statement_20260616.md`
- `archive/fixtures/priority1_divisor_additive_packet_fixtures/h0_divisor_close.json`
- `archive/fixtures/priority1_divisor_additive_packet_fixtures/conductor39_divisor_close.json`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_priority1_clause_necessity_matrix_gate.py
```

The gate returned `p25_v2_priority1_clause_necessity_matrix_rows=1/1`.

## Mutated Clauses

The H0 positive packet fails if any of these are removed or changed:

```text
theorem body verified
divisor/additive output kind
arithmetic source theorem
finite/divisor payload
legal multiplier m in {1,2,4,8}
exact residue sets
Hilbert-90 boundary
```

The conductor-39 positive packet fails if any of these are removed or changed:

```text
theorem body verified
divisor/additive output kind
arithmetic source theorem
finite/divisor payload
source object U_chi
emitted conductor-39 object
mixed chi_3 tensor chi_13 structure
Yang/Yu legal unit
Yang distribution/lift to level 507
Frobenius or Hilbert-90 descent
not projection/axis-only
```

## Counts

```text
evidence_markers_ok = 4/4
mutation_rows = 18
h0_clause_rows = 7
conductor39_clause_rows = 11
repair_rows = 17
reject_rows = 1
false_positive_packets = 0
current_priority1_source_theorems = 0
current_source_stage_closers = 0
current_submission_ready = 0
p25_v2_priority1_clause_necessity_matrix_rows=1/1
```

## Verdict

The first-pass packet contract is now stricter: every H0 and conductor-39
positive clause is individually necessary. Future source answers that omit one
of these clauses should be repaired or rejected before any H0, conductor-39,
or frontier status changes.
