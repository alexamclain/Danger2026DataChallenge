# P25 v2 KL Cyclotomic Norm Route Audit

Updated: 2026-06-17

Marker: `p25_v2_kl_cyclotomic_norm_route_audit_rows=1/1`

## Purpose

Classify the Kubert-Lang / Robert-unit cyclotomic-unit route against the
current p25 theorem kernel. This was a narrow external source check for the
exact-P/KL support row, not a broad Kubert-Lang reread.

## Pages Read

- `frontier.md`
- `lanes/exact-p.md`
- `sources/kubert-lang.md`
- `evidence/p25_v2_current_theorem_kernel_20260617.md`
- `evidence/p25_v2_live_theorem_ask_packet_20260617.md`
- `evidence/p25_v2_kubert_lang_selector_boundary_20260616.md`
- `evidence/p25_v2_kl_primitive_word_source_split_20260617.md`
- `evidence/p25_v2_exactp_theta2_lookup_row_status_20260617.md`

## External Sources Checked

- D. Kubert and S. Lang, *Modular Units Inside Cyclotomic Units*:
  `https://www.numdam.org/item/10.24033/bsmf.1890.pdf`
- D. Kubert and S. Lang, *Units in the Modular Function Field. III.
  Distribution Relations*: `https://eudml.org/doc/162800`
- W. Bley, *On the equivariant Tamagawa number conjecture for abelian
  extensions of a quadratic imaginary field*:
  `https://eudml.org/doc/116736`
- D. Kersey, *Modular units inside cyclotomic units*:
  `https://annals.math.princeton.edu/1980/112-2/p04`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_kl_cyclotomic_norm_route_audit_gate.py
```

The gate returned `p25_v2_kl_cyclotomic_norm_route_audit_rows=1/1`.

## Source Rows

```text
kubert_lang_cyclotomic_norm
  useful = modular/Robert-unit norm and regulator-level theorem expressing
           modular-unit structures inside cyclotomic-unit structures
  gap    = does not select one p25 support-156 row, does not name
           Norm_156(Y_507), and does not provide a scalar-fixed finite F_p
           value/additive payload
  route  = support_cyclotomic_norm_context_not_p25_row_theorem

kubert_lang_distribution_relations
  useful = distribution-relation source context for Siegel/modular units
  gap    = distribution and unit-generation language remains rowless unless
           upgraded to the exact p25 selector and finite theorem
  route  = support_distribution_context_not_source_stage_close

bley_robert_units
  useful = confirms Robert-unit products and equivariant/unit-module language
           as legitimate arithmetic context
  gap    = Robert-unit module relations are not the exact p25 primitive word,
           mixed C_3 x C_169 selector, or theta2 payload theorem
  route  = support_unit_module_context_not_exactp_hook

kersey_general_case
  useful = points to a generalization of modular units inside cyclotomic units
  gap    = no inspected text here emits C,D,K,orientation, equal-weight 75
           atoms, period-156 theta2 payload, or a legal support-156 row theorem
  route  = bibliography_pointer_not_actionable_close
```

## Boundary

The Kubert-Lang cyclotomic-norm route is support, not a source-stage closer.
It is genuine theorem-level structure, but at the current p25 interface it
stops at a modular/Robert-unit norm and regulator-level theorem.
It does not provide a scalar-fixed finite F_p value/additive payload, and it
does not recover exact-P without C,D,K,orientation or the 75-atom/theta2
selector.

For p25, promotion would require one of these extra clauses:

```text
one oriented legal support-156 row R_m with Norm_156(Y_507) boundary
scalar-fixed finite F_p value/additive/telescoping payload for that row
exact C,D,K,orientation packet with an accepted raw branch
exact equal-weight 75-atom theorem
accepted theta2/theta2-inverse payload with the period-156 bridge
explicit reverse reconstruction from the unified target to exact-P selector data
```

The checked cyclotomic-norm source family does not recover exact-P without
C,D,K,orientation or the 75-atom/theta2 selector. It therefore belongs beside
the existing Kubert-Lang selector boundary and KL primitive-word source split:
useful normalizer/source vocabulary, not a p25 source theorem.

## Counts

```text
external_sources_checked = 4
cyclotomic_norm_theorems_found = 1
finite_p25_row_theorems_found = 0
current_source_stage_closers = 0
current_exactp_upstream_theorems = 0
current_submission_ready = 0
p25_v2_kl_cyclotomic_norm_route_audit_rows=1/1
```

## Verdict

Continue exact-P/KL only through the existing heavy hooks: exact primitive
word, mixed `C_3 x C_169` selector with orientation, compact
`C,D,K,orientation`, equal-weight 75 atoms, or accepted theta2 payload with the
period-156 bridge. Do not promote cyclotomic-unit containment, Robert-unit
module relations, distribution relations, or regulator-level formulas unless
they emit one of those exact p25 payloads.
