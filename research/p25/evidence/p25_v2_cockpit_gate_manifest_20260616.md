# P25 v2 Cockpit Gate Manifest

Updated: 2026-06-16

Marker: `p25_v2_cockpit_gate_manifest_rows=1/1`

## Purpose

Audit the trust boundary around the lightweight cockpit. The cockpit should
not replay every theorem gate during production-search-first work, but every
cockpit evidence marker should still point to a real archived gate, and the
few heavy recomputation gates should be explicitly documented.

## Pages Read

- `AGENTS.md`
- `archive/gates/p25_v2_wiki_cockpit_lightweight_check_gate.py`
- `archive/gates/p25_v2_exactp_to_unified_target_spine_gate.py`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_cockpit_gate_manifest_gate.py
```

The gate returned `p25_v2_cockpit_gate_manifest_rows=1/1`.

## Findings

```text
cockpit_marker_count >= 92
missing_gate_files = 0
heavy_gate_count = 2
heavy_gates_documented = yes
exactp_spine_harness_path_present = yes
exactp_spine_sys_path_present = yes
```

The exact-P-to-unified spine gate had previously needed an explicit
`archive/harness` import path to run directly from repo root. That path is now
present, and the gate has been direct-run successfully in both the private
cockpit and public mirror.

## Verdict

The cockpit marker layer is backed by concrete archived gates rather than
orphan evidence pages. Heavy recomputation remains documented instead of being
pulled into the default lightweight cockpit run.
