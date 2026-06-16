# P25 KSY-y Front-Door Local Source Scan

Updated: 2026-06-16 05:14 PDT

## Purpose

This scan ties the current source-side negative result to durable local source
evidence.  It checks the Sprang, KSY, Koo-Shin 2010, and Koo-Shin II snippets
already pulled into the workbench against the four positive front doors.  The
Sprang/KSY rows are backed by the archived primary-source verdict artifact
rather than the vanished `/tmp/p25_lit_scout` TeX cache; Koo-Shin II now points
at the durable extracted PDF text under `incoming/extracted`.

Result:

```text
local_source_closing_hits = 0
```

## Source Windows

```text
sprang_1801_distribution_relation:
  file     = research/p25/p25_ksy_y_priority1_primary_source_verdict_20260613.md:22-29
  decision = conditional_additive_section_distribution_not_exact_P
  missing  = specialization to exact K-traced normalized-y product P

sprang_1802_d_variant_kato_siegel:
  file     = research/p25/p25_ksy_y_priority1_primary_source_verdict_20260613.md:31-38
  decision = conditional_derham_dlog_not_d2_product
  missing  = D=2 multiplicative product identity for the exact p25 payload

ksy_1007_2307_normalized_y_formula:
  file     = research/p25/p25_ksy_y_priority1_primary_source_verdict_20260613.md:48-54
  decision = formula_language_not_product_distribution
  missing  = product/distribution theorem selecting all 75 p25 atoms

ksy_1007_2307_single_generator:
  file     = research/p25/p25_ksy_y_priority1_primary_source_verdict_20260613.md:64-70
  decision = single_value_generator_not_k_traced_product
  missing  = upgrade from one generator to exact K-traced p25 product

koo_shin_2010_theorem62_h0_legality:
  file     = incoming/extracted/s00209-008-0456-9.pdf.extract.txt:1988-2045
  decision = source_certified_value_or_divisor_missing
  missing  = finite-field value/divisor theorem for one exact H0 product

koo_shin_2010_theorem9x_generators:
  file     = incoming/extracted/s00209-008-0456-9.pdf.extract.txt:4316-4638
  decision = reject_generic_generation_not_exact_p
  missing  = exact H0/conductor39/twisted/exact-75 finite identity

koo_shin_ii_section5_delta_context:
  file     = incoming/extracted/1007.2318v1.pdf.extract.txt:1516-1777
  decision = reject_prime_power_delta_context_not_p25_product
  missing  = mixed C3 x C169 p25 product or H0/conductor39 divisor identity
```

## Counts

```text
row_count                              = 7
file_present_rows                      = 7
required_terms_present_rows            = 7
current_evidence_rows                  = 7
local_source_closing_hits              = 0
direct_closer_rejected_rows            = 7
continue_as_context_rows               = 4
external_exact_upgrade_rows            = 4
source_certified_only_rows             = 1
formula_or_distribution_context_rows   = 3
generic_generation_context_rows        = 3
```

## Interpretation

The local source cache has no source-closing theorem for the current p25
front doors.  The positive local use is context or source certification only.

The next source search should therefore be external or expert-directed and ask
for one of:

```text
exact H0 divisor/additive identity with H90 boundary
U_chi/W conductor-39 divisor or additive identity
twisted/H90 divisor identity with period-156 bridge context
exact 75-atom P divisor/additive theorem
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_frontdoor_local_source_scan_gate.py
```

Marker:

```text
ksy_y_frontdoor_local_source_scan_rows=1/1
```
