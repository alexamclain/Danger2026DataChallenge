# P25 v2 Value / Divisor Source-Family Router

Updated: 2026-06-16

## Purpose

Convert the v2 theorem interface into a literature/source routing rule.  The
first-pass target is already fixed; this page says which source families can
still help, what exact theorem shape they must emit, and what should be
discarded without broad rereading.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `lanes/exact-p.md`
- `sources/koo-shin-2010.md`
- `sources/koo-shin-ii-1007-2318.md`
- `sources/koo-shin-yoon-1007-2307.md`
- `sources/sprang.md`
- `sources/kubert-lang.md`
- `sources/schertz-scholl.md`
- `evidence/p25_v2_unified_value_divisor_interface_20260616.md`
- `evidence/p25_v2_unified_source_theorem_gap_20260616.md`
- `evidence/p25_v2_h0_y507_period156_compatibility_20260616.md`
- `evidence/p25_v2_quartic_selector_payload_20260616.md`
- `evidence/p25_v2_quartic_reciprocal_orientation_20260616.md`
- `evidence/p25_v2_h0_conductor39_canonical_frontier_pass_20260616.md`
- `evidence/p25_ksy_y_priority1_primary_source_verdict_20260613.md`
- `evidence/p25_ksy_y_sprang_exact_specialization_frontier_20260614.md`
- `evidence/p25_ksy_y_kubert_lang_visual_theorem_boundary_20260614.md`
- `evidence/p25_ksy_y_external_exact_product_bridge_scout_20260613.md`
- `evidence/p25_v2_ksy_1007_2307_source_ingest_scan_20260616.md`
- `evidence/p25_v2_koo_shin_ii_first_pass_source_scan_20260616.md`

## Command

```bash
python3 research/p25/archive/gates/p25_v2_value_divisor_source_family_router_gate.py
```

The gate returned `p25_v2_value_divisor_source_family_router_rows=1/1`.

## Router Rows

```text
unified_h0_conductor39_divisor_additive
  source_family = Koo-Shin/Yang/Yu/Ray-class source language
  target        = one legal support-156 H0/conductor-39 product
  accept only   = finite divisor/additive theorem with Hilbert-90 boundary
                  (1-Frob_p)H = Norm_156(Y_507)
  current       = target certified; no arithmetic value/divisor theorem in hand
  decision      = primary_frontdoor_ask_continue
  falsifier     = source legality, boundary, or product normal form without
                  value/divisor theorem

period156_value_route
  source_family = Schertz/Shin/Siegel-Robert/Scholl value-unit family
  target        = same legal support-156 product family
  accept only   = finite value identity for canonical H0 with
                  Norm_156(Y_507) boundary, or for Y_507 with period-156
                  branch/root/telescoping context
  current       = value-unit vocabulary exists; ambient period-780 route keeps
                  mu_11 ambiguity
  decision      = conditional_frontdoor_support_continue
  falsifier     = value theorem with no canonical H0/Y507 period-156 context
                  or only ambient period-780 data

character_quartic_selector_route
  source_family = H0/conductor-39 character or projector language
  target        = one legal quotient-C4 edge presented by character data
  accept only   = W boundary, exact row-antisymmetric C4_1 phase, mixed tensor
                  row sign, oriented row/boundary-sign convention, and
                  scalar-fixed finite value/divisor theorem
  current       = selector payload certified; no arithmetic finite theorem in
                  hand
  decision      = active_frontdoor_shape_only
  falsifier     = coarse quartic phase, magnitude, quadratic component, or
                  missing row sign, or reciprocal phase with wrong/missing
                  boundary sign

exactp_upstream_product
  source_family = KSY/Kubert-Lang/Sprang/Scholl exact-product family
  target        = compact exact-P C,D,K,orientation or accepted period-156
                  theta2 payload
  accept only   = challenge-legal exact-P theorem feeding 75->300->12->312->156
  current       = rigid finite target known; no source theorem selecting the
                  75 atoms
  decision      = heavy_second_pass_continue_only_on_exact_theorem_hook
  falsifier     = field generation, exponent balance, or value-only statement
                  without exact product

koo_shin_2010
  source_family = Koo-Shin 2010
  target        = H0 and conductor-39 source legality
  accept only   = a new clause emits the exact finite value/divisor theorem
  current       = source-legality asset; killed as current source-stage closer
  decision      = use_as_evidence_not_broad_read
  falsifier     = another source-certification or ray-class-generation statement

koo_shin_ii_1007_2318
  source_family = Koo-Shin II 1007.2318
  target        = background ray-class/Siegel context
  accept only   = exact H0/conductor-39 period-156 value/divisor clause
  current       = screened negative for H0, conductor 39, period-156, and H90
                  terms
  decision      = background_only
  falsifier     = general sequel context without the p25 finite theorem

ksy_1007_2307
  source_family = Koo-Shin-Yoon 1007.2307
  target        = normalized-y atom vocabulary for exact-P
  accept only   = exact 75-atom selector/product theorem with orientation and
                  bridge
  current       = exact-P vocabulary; killed as H0/conductor-39 closer
  decision      = exactp_vocabulary_only
  falsifier     = single-value generator or field-generation theorem only

sprang_d2
  source_family = Sprang D=2/Kronecker distribution family
  target        = exact-P finite P/theta2 divisor or value identity
  accept only   = named exact specialization emitting source packet,
                  orientation, and K-traced payload
  current       = additive/differential vocabulary; broad D=2 readings
                  screened out
  decision      = exact_specialization_only
  falsifier     = kernel distribution, torsion shadow, or cohomology statement
                  without finite product

kubert_lang
  source_family = Kubert-Lang modular-unit machinery
  target        = exact exponent/dependence control for the mixed p25 product
  accept only   = row-labeled exponent matrix tied to compact exact-P or
                  period-156 payload
  current       = useful dependence language; no exact mixed selector or finite
                  payload
  decision      = machinery_only
  falsifier     = generic modular-unit generation or tower torsion control only

schertz_scholl
  source_family = Schertz/Shin/Scholl value-unit and distribution family
  target        = period-156 finite value identity or exact-product bridge
  accept only   = canonical H0/Y507 support-period branch/root/telescoping
                  theorem; not ambient-only value data
  current       = value-unit context; direct Scholl D=2 import blocked by
                  hypotheses
  decision      = period156_hook_only
  falsifier     = ambient period-780 claim or direct D=2 import under odd-D
                  hypotheses
```

## Counts

```text
evidence_markers_ok = 12/12
route_rows = 10
active_frontdoor_rows = 3
heavy_route_rows = 4
direct_closer_rows = 0
broad_reading_allowed_rows = 0
```

## Verdict

The literature/source side is now router-shaped:

```text
preferred_next_ask = finite divisor/additive theorem for one legal
                     support-156 H0/conductor-39 product with
                     Norm_156(Y_507) boundary, or the same theorem stated
                     with exact C4_1 selector and orientation data
supporting_ask     = period-156 value theorem with branch/root/telescoping
                     context for canonical H0/Y507
heavy_ask          = exact-P theorem selecting the 75 atoms and feeding
                     75->300->12->312->156
current_closers    = 0
```

Do not spend another pass on broad Koo-Shin, KSY, Sprang, Kubert-Lang, or
Schertz/Scholl reading.  Continue only when a source snippet or expert lead is
already shaped like one of the accepted theorem rows above.
