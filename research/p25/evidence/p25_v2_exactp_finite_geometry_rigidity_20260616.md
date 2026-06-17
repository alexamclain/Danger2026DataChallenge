# P25 v2 Exact-P Finite-Geometry Rigidity

Updated: 2026-06-16 07:43 PDT

Marker: `p25_v2_exactp_finite_geometry_rigidity_rows=1/1`

## Purpose

Promote the exact-P finite-geometry result that matters after the KSY source
ingest: the normalized-y vocabulary is not enough, but the accepted finite
payload is now sharply constrained. This pass reran three archived gates after
the wiki reorganization and records the theorem target they force.

## Pages Read

- `lanes/exact-p.md`
- `evidence/p25_v2_ksy_1007_2307_source_ingest_scan_20260616.md`
- `evidence/p25_ksy_y_normalized_y_product_upgrade_frontier_20260614.md`
- `evidence/lane_B_quotient_checkpoint.md`
- `archive/notes/subsqrt_moonshot_laneB_robert_ksy_theta2_kubert_lang_atomic_weight_rigidity.md`
- `archive/notes/subsqrt_moonshot_laneB_square_axis_bridge_hilbert90_source_chain_corner_row_polynomial.md`
- `archive/notes/p25_ksy_y_subsqrt_arithmetic_producer_route_packet_20260614.md`

## Commands

```bash
PYTHONPATH=research/p25/archive/gates:research/p25/archive/harness \
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_laneB_robert_ksy_theta2_kubert_lang_atomic_weight_rigidity_gate.py

PYTHONPATH=research/p25/archive/gates:research/p25/archive/harness \
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_row_polynomial_gate.py

PYTHONPATH=research/p25/archive/gates:research/p25/archive/harness \
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_laneB_square_axis_quotient_shift_normal_form_gate.py
```

The lightweight v2 contract gate returned
`p25_v2_exactp_finite_geometry_rigidity_rows=1/1`.

## Results

Atomic weight rigidity:

```text
atom_count = 75
support_per_atom = 4
pairwise_intersecting_atom_pairs = 0
atom_union_support = 300
linear_rank_from_disjoint_support = 75
linear_nullity_from_disjoint_support = 0
theta2_inverse_solution = all 75 weights +1
theta2_solution = all 75 weights -1
missing_atom_rejected = true
alternating_k_weights_rejected = true
marker = robert_ksy_theta2_kubert_lang_atomic_weight_rigidity_rows=1/1
```

Corner row polynomial:

```text
source rows r = 0,1,2
c13 shadow c0(r) = 4*r^2 - r
fiber f(r) = r*(1-r)
c169 values = 0, 3, 144
q values = 0, 172, 482
marker = square_axis_bridge_hilbert90_source_chain_corner_row_polynomial_rows=1/1
```

Quotient shift normal form:

```text
right_degree = 3
square_c = 169
quotient_order = 507
D = (right+1, c+1)
X = (right+1, c-42)
Y = (right, c+3)
D^3 = Y
selected_count = 18/18
marker = square_axis_quotient_shift_normal_form_rows=1/1
```

## Interpretation

The finite exact-P payload is rigid in a useful way:

- The accepted normalized-y/theta2 footprint has disjoint four-cell support per
  atom.
- Because the 75 atom supports are disjoint, the theta2 target reads off all
  atom weights independently.
- There is no nonuniform `K`-trace, missing-atom, or atomic-weight null
  direction inside this finite geometry.
- One active corner is not arbitrary: it is a quadratic row graph in `C_169`,
  plus the forced raw `K` trace.

## Verdict

Exact-P remains open, but the target is sharper:

```text
continue_exactp = yes
new_positive_artifact = finite geometry rigidity and row-polynomial normal form
still_missing = arithmetic source theorem selecting this exact equal-weight
                K-traced anti-invariant normalized-y product, with orientation
                and period-156/challenge-legal framing
discarded_escape = any theorem that only emits nonuniform weights, a partial
                   atom subset, or a generic ray-class generator
```

## Recommendation

Do not ask for "a 75-atom construction" loosely. Ask for a theorem that
produces the exact equal-weight anti-invariant product, or an equivalent
accepted theta2 payload, and that explains the quadratic `C_3 -> C_169`
row graph plus raw `K` trace.
