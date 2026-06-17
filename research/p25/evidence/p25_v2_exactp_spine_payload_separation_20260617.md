# P25 v2 Exact-P Spine Payload Separation

Updated: 2026-06-17

Marker: `p25_v2_exactp_spine_payload_separation_rows=1/1`

## Purpose

Record the finite-support separation behind the exact-P moonshot:

```text
75 fixed atoms -> 300 theta2 terms -> 12 Y_507 terms -> 312 period-norm cells
-> 156 Hilbert-90 support
```

This is the constructive bridge from exact-P into the unified
H0/conductor-39 target. It is not a proof that exact-P is a plain `R_m^75`
row-power theorem, and it is not reversible from a unified support-156 theorem
without extra selector data.

## Pages Read

- `frontier.md`
- `lanes/exact-p.md`
- `evidence/p25_v2_exactp_to_unified_target_spine_20260616.md`
- `evidence/p25_v2_exactp_75_anchor_bridge_filter_20260617.md`
- `evidence/p25_v2_basis_sensitive_anchor_sieve_20260617.md`
- `evidence/p25_v2_exactp_finite_geometry_rigidity_20260616.md`
- `evidence/p25_v2_reverse_exactp_information_loss_20260616.md`
- `evidence/p25_v2_theta2_period156_support_contract_20260616.md`

## Commands

The heavy spine replay completed successfully:

```bash
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=research/p25/archive/gates:research/p25/archive/harness \
python3 research/p25/archive/gates/p25_v2_exactp_to_unified_target_spine_gate.py
```

It returned `p25_v2_exactp_to_unified_target_spine_rows=1/1` and the support
profile:

```text
atom_count = 75
theta2_payload_support = 300
quotient_y507_support = 12
period_norm_support = 312
unified_h90_support = 156
unified_lift = +78 / -78
exactp_implies_unified_target = 1
unified_target_implies_exactp = 0
```

The lightweight separation gate:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_exactp_spine_payload_separation_gate.py
```

returned `p25_v2_exactp_spine_payload_separation_rows=1/1`.

## Separation Rows

```text
fixed_75_atoms
  support = 75 fixed normalized-y atoms, each with disjoint four-cell support
  decision = exactp_payload_not_75_candidate_search
  falsifier = treating atoms as independent tries or generic atom vocabulary

theta2_to_y507_bridge
  support = 75 atoms expand to 300 theta2 terms and descend to 12 Y_507 terms
  decision = bridge_support_not_source_theorem
  falsifier = theta2 vocabulary or Y_507 support without source theorem and branch data

period_norm_to_h90
  support = 12 Y_507 terms period-norm to 312 cells and a 156-support H90 product
  decision = unified_support156_target_after_bridge
  falsifier = calling the 156-support H90 product the plain 75-atom exact-P product

h90_product_not_plain_75
  support = unified H90 lift is 78 positive over 78 negative factors
  decision = reject_plain_75_atom_identification
  falsifier = H90 support equals atom count, or positive/negative side equals atom count

exactp_75_not_row_power_75
  support = exact-P atoms live in normalized-y/theta2 basis, not in row-value R_m basis
  decision = reject_row_power_shortcut_without_row_labeled_Rm75_theorem
  falsifier = using gcd(75,p-1)=1 on atom count instead of row-labeled R_m^75

forward_not_reverse
  support = compact exact-P theorem feeds unified target; unified theorem alone loses C,D,K/orientation
  decision = exactp_stronger_upstream_one_way_bridge
  falsifier = claiming unified support-156 theorem reconstructs exact-P without selector data
```

## Counts

```text
evidence_markers_ok = 6/6
separation_rows = 6
support_ladder_ok = 1
bridge_rows = 3
current_exactp_source_theorems = 0
current_unified_source_theorems = 0
current_submission_ready = 0
p25_v2_exactp_spine_payload_separation_rows=1/1
```

## Verdict

Exact-P is still a valuable moonshot because it gives a concrete upstream
finite spine into the unified target. But the bridge is basis-sensitive:

```text
exact-P 75 atoms are fixed payload factors, not 75 tries;
the 156-support H90 target is not the plain 75-atom product;
the atom count 75 is not an R_m^75 row-power theorem;
unified support-156 does not recover exact-P without C,D,K/orientation,
equal-weight atoms, theta2 payload, or an explicit reverse theorem.
```

So the useful exact-P ask remains narrow: find an arithmetic source theorem
for the compact exact-P packet or accepted theta2 payload, not just a source
that mentions 75 atoms, theta functions, or the unified target.
