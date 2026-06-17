# P25 v2 Kernel Consistency Audit

Updated: 2026-06-17

Marker: `p25_v2_kernel_consistency_audit_rows=1/1`

## Purpose

Lock the current theorem-kernel surfaces against drift. The live p25 intake
now accepts exact row-labeled powers with
`e in {3,5,13,39,75,169,507}`; this audit checks that the current theorem
kernel, Drew packet, source-stage normalization spine, repair-debt matrix,
extended unique-power intake, live theorem ask packet, source-theorem
automaton, matched-quotient packet/source-feasibility screen, period-156
supersession, and canonical lane pages all agree.

This is not a new theorem route. It is a guardrail so future expert/source
answers are classified against one consistent kernel.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_current_theorem_kernel_20260617.md`
- `evidence/p25_v2_drew_kernel_review_packet_20260617.md`
- `evidence/p25_v2_source_stage_normalization_spine_20260617.md`
- `evidence/p25_v2_repair_debt_closure_matrix_20260617.md`
- `evidence/p25_v2_extended_unique_power_intake_20260617.md`
- `evidence/p25_v2_live_theorem_ask_packet_20260617.md`
- `evidence/p25_v2_affine_row_normal_form_20260617.md`
- `evidence/p25_v2_matched_quotient_closure_packet_20260617.md`
- `evidence/p25_v2_matched_quotient_source_feasibility_20260617.md`
- `evidence/p25_v2_period156_feasibility_supersession_20260617.md`
- `evidence/p25_v2_source_theorem_acceptance_automaton_20260617.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_kernel_consistency_audit_gate.py
```

The gate returned `p25_v2_kernel_consistency_audit_rows=1/1`.

## Checked Invariants

```text
unique_powers = (3, 5, 13, 39, 75, 169, 507)

3^-1   = 6666666666666666666666675
5^-1   = 4000000000000000000000005
13^-1  = 7692307692307692307692317
39^-1  = 5897435897435897435897443
75^-1  = 266666666666666666666667
169^-1 = 5207100591715976331360953
507^-1 = 5069033530571992110453655
```

The audit verifies:

```text
current theorem kernel powers = Drew packet powers
source-stage spine powers = extended unique-power intake powers
repair-debt matrix marks all seven as gcd(e,p-1)=1
canonical frontier/H0/conductor-39 pages name the same set
wrong stale inverse exponents are absent from current evidence pages
current theorem kernel and Drew packet each have two support rows
source theorem acceptance automaton has 25 rows and 2 normalize routes
matched aggregate packet has accept/zero-lattice-missing/nonunit-sum rows
live theorem ask has exactly three action rows and broad reread closed
matched-quotient source feasibility keeps standard aggregates in root debt
period-156 feasibility is superseded by the row-bridge packet
current_source_stage_closers = 0
current_submission_ready = 0
```

## Counts

```text
evidence_markers_ok = 11/11
powers_consistent = 1
inverses_consistent = 1
repair_consistent = 1
evidence_pages_ok = 1
canonical_pages_ok = 1
row_counts_consistent = 1
automaton_consistent = 1
live_action_consistent = 1
matched_source_feasibility_consistent = 1
period156_supersession_consistent = 1
current_source_stage_closers = 0
current_submission_ready = 0
p25_v2_kernel_consistency_audit_rows=1/1
```

## Verdict

The first-pass theorem front door is now synchronized:

```text
one scalar-fixed legal row;
one exact row-labeled power R_m^e with e in {3,5,13,39,75,169,507};
or one support-period-156 value with legal-row bridge.
```

The extended `75/169/507` powers are intake guardrails for exact row-labeled
finite value theorems, not separate broad search lanes. Q/Yang and
matched-quotient aggregate packets are support-normalization routes until
their selector/quotient debts are paid exactly; standard pair/diagonal/all-four
aggregates still carry root debt. Period-156 value work is also at a stop sign:
the row-bridge packet already covers the accepted shapes and repair rows, so
another broad feasibility layer is not progress. Current source-stage closers
and submission-ready rows remain zero.
