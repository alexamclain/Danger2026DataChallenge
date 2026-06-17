# P25 v2 Snippet / Expert Intake Sync

Updated: 2026-06-17

Marker: `p25_v2_snippet_expert_intake_sync_rows=1/1`

## Purpose

Synchronize the older detailed intake surfaces with the live source theorem
acceptance automaton. The source-snippet intake and expert-response rubric are
still useful broad routers, but they predate three current kernel updates:

```text
unique row powers = e in {3,5,13,39,75,169,507}
distribution/norm aggregate closure = repair_even_boundary_distribution_closure
matched aggregate route = normalize_matched_quotient_then_accept
```

This page records that both older surfaces now carry explicit sync notes and
defer source-stage theorem classification to the automaton.

## Pages Read

- `evidence/p25_v2_source_snippet_intake_20260616.md`
- `evidence/p25_v2_current_expert_response_rubric_20260616.md`
- `evidence/p25_v2_source_theorem_acceptance_automaton_20260617.md`
- `evidence/p25_v2_extended_unique_power_intake_20260617.md`
- `evidence/p25_v2_distribution_relation_closure_screen_20260617.md`
- `evidence/p25_v2_matched_quotient_closure_packet_20260617.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_snippet_expert_intake_sync_gate.py
```

The gate returned `p25_v2_snippet_expert_intake_sync_rows=1/1`.

## Sync Rows

```text
source_snippet_intake_sync
  decision = legacy_router_synced_to_current_automaton
  checks   = original marker present, 2026-06-17 sync note present,
             full unique-power set present, distribution repair row present,
             matched-quotient normalization present, automaton deferral present

current_expert_response_rubric_sync
  decision = legacy_router_synced_to_current_automaton
  checks   = original marker present, 2026-06-17 sync note present,
             full unique-power set present, distribution repair row present,
             matched-quotient normalization present, automaton deferral present
```

## Current Intake Rule

The current automaton remains the source-stage classifier:

```text
candidate_rows = 25
accepted_source_stage_rows = 9
normalize_then_accept_rows = 2
heavy_upstream_rows = 1
repair_rows = 11
reject_rows = 2
```

The important practical consequence is:

```text
R_m^75, R_m^169, R_m^507
  accepted only as exact row-labeled finite theorems with source provenance,
  boundary/period bridge, and scalar normalization

distribution/norm closure
  repair unless it supplies direct edge data, root/selector/scalar
  normalization, or an equivalent one-row theorem

aggregate plus matched quotient
  normalize only when exact R^v and exact R^(v - (sum v)e_m) are both source
  theorems and gcd(sum v,p-1)=1
```

## Counts

```text
evidence_markers_ok = 6/6
sync_rows_ok = 2/2
legacy_surfaces_synced = 2
current_source_stage_closers = 0
current_submission_ready = 0
current_automaton_candidate_rows = 25
current_automaton_normalize_then_accept_rows = 2
current_automaton_repair_rows = 11
full_unique_power_set_synced = 1
distribution_closure_repair_synced = 1
matched_quotient_normalization_synced = 1
p25_v2_snippet_expert_intake_sync_rows=1/1
```

## Verdict

Future source snippets and expert replies should be read through the current
automaton first. The older source-snippet intake and expert rubric remain
valid as broad context, but their older four-power phrasing is superseded by
the full unique-power set, and generic distribution/norm relation closure is a
named repair row rather than a source-stage closer.

Matched aggregate answers are now similarly explicit: they promote only when
the exact matched zero-lattice quotient theorem is supplied with invertible
coefficient sum; otherwise they remain aggregate or zero-lattice repair data.
