# P25 v2 Source Family Gap Matrix

Updated: 2026-06-16

## Purpose

Summarize how the inspected source families line up against the current p25
one-edge theorem target. This is meant to keep source search and expert asks
narrow: each source family has useful vocabulary, but none currently supplies
the finite theorem needed for a p25 certificate route.

## Pages Read

- `frontier.md`
- `sources/koo-shin-2010.md`
- `sources/koo-shin-yoon-1007-2307.md`
- `sources/koo-shin-ii-1007-2318.md`
- `sources/sprang.md`
- `sources/kubert-lang.md`
- `sources/schertz-scholl.md`
- `sources/p24-prior-art.md`
- `evidence/p25_v2_self_contained_theorem_statement_20260616.md`
- `evidence/p25_v2_source_graph_normal_form_20260616.md`
- `evidence/p25_v2_edge_lattice_intake_classifier_20260616.md`
- `evidence/p25_v2_source_snippet_intake_20260616.md`
- `evidence/p25_v2_current_expert_response_rubric_20260616.md`
- `evidence/p25_v2_additive_normalizer_source_scan_20260616.md`
- `evidence/p25_v2_koo_shin_distribution_noncloser_20260616.md`
- `evidence/p25_v2_exactp_theorem_interface_contract_20260616.md`
- `evidence/p25_v2_sprang_theta2_source_intake_20260616.md`
- `evidence/p25_v2_kubert_lang_selector_boundary_20260616.md`
- `evidence/p25_v2_h0_y507_period156_compatibility_20260616.md`
- `evidence/p25_v2_quartic_selector_payload_20260616.md`
- `evidence/p25_v2_quartic_reciprocal_orientation_20260616.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/archive/gates/p25_v2_source_family_gap_matrix_gate.py
```

The gate returned `p25_v2_source_family_gap_matrix_rows=1/1`.

## Matrix

```text
koo_shin_2010
  use      = source legality, distribution/root-descent context
  has      = one-edge source object vocabulary
  missing  = finite scalar-fixed value/divisor theorem for one oriented edge
  decision = helper_source_not_closer

koo_shin_yoon_1007_2307
  use      = normalized-y and ray-class vocabulary for exact-P
  has      = exact-P vocabulary
  missing  = 75-atom exact-P theorem or bridge to the one-edge target
  decision = exactp_vocabulary_not_closer

koo_shin_ii_1007_2318
  use      = normal-basis/ring-class background
  has      = class-field / normal-basis vocabulary
  missing  = one-edge theorem, period-156 value theorem, or exact-P producer
  decision = background_source_not_closer

sprang
  use      = D=2 Poincare/Kronecker/theta support
  has      = D=2 support avoiding the classical coprime-to-6 obstruction
  missing  = exact p25 theta2 divisor/additive payload or compact KSY
             specialization
  decision = d2_support_source_not_theta2_closer

kubert_lang
  use      = finite selector/exponent machinery for exact-P
  has      = exact packet survives the KL screen; primitive bridge word and
             quotient selector are rigid
  missing  = theorem-legal mixed C3 x C169 product emitting the rigid selector,
             primitive word, or theta2 payload
  decision = finite_selector_rigid_source_theorem_missing

schertz_scholl
  use      = period-value vocabulary for the H0/Y507 support-period route
  has      = H0/Y507 compatibility screen with three accepted value/divisor
             shapes and ambient/formal falsifiers
  missing  = canonical H0 or Y_507 period-156 value theorem with branch
             context, or matching divisor/additive identity
  decision = h0_y507_value_route_live_no_theorem

p24_prior_art
  use      = practical and negative-route transfer constraints
  has      = transfer constraints and failure-mode history
  missing  = p25-specific arithmetic source theorem
  decision = prior_art_not_p25_source_theorem
```

## Counts

```text
evidence_markers_ok = 13/13
source_rows = 7
vocabulary_sources = 7
one_edge_source_objects = 1
scalar_fixed_finite_theorems = 0
period156_value_theorems = 0
exactp_upstream_theorems = 0
first_pass_closers = 0
current_submission_ready = 0
p25_v2_source_family_gap_matrix_rows=1/1
```

## Verdict

The source-side situation is now compact:

```text
Koo-Shin 2010 gives the closest one-edge source object.
Sprang gives the sharpest D=2/theta support language.
Kubert-Lang gives the sharpest finite exact-P selector boundary.
Schertz/Scholl now routes through the H0/Y507 period-156 compatibility screen.
No inspected source gives the scalar-fixed finite theorem, period-156 value
theorem, or exact-P upstream theorem.
```

So the next expert/literature ask should not be broad. It should ask whether a
known theorem upgrades the Koo-Shin/Yang source object to a scalar-fixed finite
divisor/additive identity, or gives a period-156 value theorem, for one
oriented quotient-`C4` edge. If the answer is stated in character language, it
must include the exact row-antisymmetric `C4_1` selector, mixed tensor row sign,
oriented row/boundary-sign convention, and the same scalar-fixed finite theorem.
