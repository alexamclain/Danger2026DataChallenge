# P25 v2 Priority-1 Source Lookup Capsule

Updated: 2026-06-17

Marker: `p25_v2_priority1_source_lookup_capsule_rows=1/1`

## Purpose

Convert the priority-1 divisor/additive work order into a source-search and
expert-check capsule. This is the checklist for the next Koo-Shin,
Kubert-Lang, Schertz-Scholl, Sprang, or Drew pass: what would count as a
positive theorem hook, and what should be killed immediately as already-screened
support language.

This page is not a source theorem. It is the narrow lookup/falsifier interface
for finding one.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `sources/koo-shin-2010.md`
- `sources/kubert-lang.md`
- `sources/schertz-scholl.md`
- `sources/sprang.md`
- `evidence/p25_v2_priority1_divisor_additive_work_order_20260617.md`
- `evidence/p25_v2_priority1_candidate_sweep_20260617.md`
- `evidence/p25_v2_minimal_expert_ask_20260616.md`
- `evidence/p25_v2_first_pass_expert_intake_packet_20260616.md`
- `evidence/p25_v2_source_stage_normalization_spine_20260617.md`
- `evidence/p25_v2_koo_shin_distribution_noncloser_20260616.md`
- `evidence/p25_v2_period156_value_source_hook_20260616.md`
- `evidence/p25_v2_q_route_source_hook_scan_20260616.md`
- `evidence/p25_v2_kubert_lang_selector_boundary_20260616.md`
- `evidence/p25_v2_schertz_scholl_external_source_boundary_20260616.md`
- `evidence/p25_v2_sprang_theta2_source_intake_20260616.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_priority1_source_lookup_capsule_gate.py
```

The gate returned `p25_v2_priority1_source_lookup_capsule_rows=1/1`.

## Lookup Rows

```text
koo_shin_h0_or_conductor39_divisor_additive
  source_family   = Koo-Shin 2010 / H0 / conductor 39
  positive_hook   = finite scalar-fixed divisor/additive theorem for one legal
                    row with Norm_156(Y_507) boundary
  first_falsifier = Theorem 6.2 legality, Lemma 6.1 distribution, or Theorem
                    5.2 constant-product context without finite scalar-fixing
                    identity
  decision         = search_as_priority1_frontdoor

h0_y507_support_period156_value
  source_family   = Koo-Shin / Schertz-Shin-Scholl value side
  positive_hook   = support-period-156 finite value theorem for canonical H0
                    or Y_507 with branch/root/telescoping data
  first_falsifier = ambient-period-780 value, mu_11 quotient, class-field
                    generation, or value up to unspecified F_p^* scalar
  decision         = search_as_priority2_value_side

conductor39_q_or_yang_h90_hook
  source_family   = conductor 39 / Yang / Hilbert-90 / Q support
  positive_hook   = finite Q or Q^3 theorem plus diagonal split/root, or direct
                    mixed U_chi/W theorem normalizing to one edge
  first_falsifier = Q source-only, Q^6 boundary-only, diagonal aggregate
                    without pure quartic split, or split without oriented
                    root/sign
  decision         = search_as_support_only_until_selector_paid

quartic_or_row_labeled_normalizer
  source_family   = row-labeled, reciprocal, quartic selector, or power-value
                    presentations
  positive_hook   = exact row label/phase/orientation or R_m^e value with
                    inverse recovery, plus scalar-fixed finite theorem
  first_falsifier = selector-only, unordered orbit, reciprocal with wrong
                    boundary sign, or power value without row selector
  decision         = accept_only_if_normalizes_to_one_row

kubert_lang_exactp_upstream
  source_family   = Kubert-Lang / exact-P mixed selector
  positive_hook   = theorem emitting the exact primitive word, mixed
                    C_3 x C_169 selector, orientation, or accepted theta2
                    bridge
  first_falsifier = generic modular-unit generation, exponent balance, or
                    prime-power projection without the exact p25 selector
  decision         = keep_as_heavy_upstream_only

sprang_theta2_sparse_packet
  source_family   = Sprang / Kato-Siegel / theta2
  positive_hook   = sparse p25 theta2 or theta2-inverse divisor-additive
                    payload with period-156 branch and extraction bridge
  first_falsifier = full distribution/kernel identity, D=2 support vocabulary,
                    or theta language without sparse selector and branch data
  decision         = search_only_for_exact_specialization
```

## Counts

```text
evidence_markers_ok = 11/11
lookup_rows = 6
current_priority1_source_theorems = 0
current_source_stage_closers = 0
current_submission_ready = 0
p25_v2_priority1_source_lookup_capsule_rows=1/1
```

## Verdict

The next source or expert pass should not ask broadly for p25-relevant modular
unit theory. It should ask whether one of the six rows above has a named
finite theorem with the listed positive hook. If the answer is only legality,
class-field generation, distribution context, boundary data, selector data, or
value data with an unspecified scalar/branch, it is a repair row and should not
change H0, conductor 39, exact-P, or submission status.

The current best target remains the first row: a challenge-legal arithmetic
theorem producing a finite scalar-fixed divisor/additive identity for one
normalized legal support-156 row with `Norm_156(Y_507)` boundary.
