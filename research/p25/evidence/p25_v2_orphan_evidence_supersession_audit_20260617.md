# P25 v2 Orphan Evidence Supersession Audit

Updated: 2026-06-17

Marker: `p25_v2_orphan_evidence_supersession_audit_rows=1/1`

## Purpose

Audit the `p25_v2` evidence notes that are intentionally outside the cockpit
gate. These notes are not missing live work; they are historical or
intermediate source screens consumed by later canonical artifacts.

This prevents two bad moves:

```text
1. treating an old source scan as an unreviewed live hook;
2. promoting superseded exact-P or source-ingest notes back into the cockpit.
```

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `lanes/exact-p.md`
- `sources/koo-shin-2010.md`
- `sources/koo-shin-yoon-1007-2307.md`
- `sources/koo-shin-ii-1007-2318.md`
- `evidence/p25_v2_exactp_theorem_interface_contract_20260616.md`
- `evidence/p25_v2_h0_conductor39_canonical_frontier_pass_20260616.md`
- `evidence/p25_v2_koo_shin_ii_first_pass_source_scan_20260616.md`
- `evidence/p25_v2_ksy_1007_2307_source_ingest_scan_20260616.md`
- downstream references named in the gate

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_orphan_evidence_supersession_audit_gate.py
```

The gate returned `p25_v2_orphan_evidence_supersession_audit_rows=1/1`.

## Supersession Rows

```text
exactp_theorem_interface_contract
  decision = superseded_by_exactp_minimal_hook_lookup_and_spine
  status   = heavy_upstream_interface_not_standalone_cockpit_row

h0_conductor39_canonical_frontier_pass
  decision = superseded_by_h0_conductor39_interface_and_koo_shin_falsifiers
  status   = historical_local_source_scan_not_current_closer

koo_shin_ii_first_pass_source_scan
  decision = superseded_by_source_family_gap_and_constructive_payload_scan
  status   = background_context_not_front_door_source

ksy_1007_2307_source_ingest_scan
  decision = superseded_by_exactp_candidate_sweep_kl_scan_and_source_gap
  status   = exactp_vocabulary_not_arithmetic_producer
```

## Counts

```text
orphan_evidence_rows = 4
rows_ok = 4/4
downstream_refs_checked = 15
live_source_stage_closers = 0
cockpit_promotion_needed = 0
broad_reread_unlocked = 0
p25_v2_orphan_evidence_supersession_audit_rows=1/1
```

## Verdict

The apparent `p25_v2` cockpit orphans are accounted for. They remain useful
provenance for Koo-Shin/KSY/Koo-Shin II/exact-P reasoning, but their live
content has already been absorbed into the current theorem kernel, source
family gap matrix, exact-P lookup rows, and canonical source dossiers.

No source-stage closer, exact-P producer, or new broad reread obligation is
hidden in these four notes.
