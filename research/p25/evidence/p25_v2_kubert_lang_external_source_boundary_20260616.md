# P25 v2 Kubert-Lang External Source Boundary

Updated: 2026-06-16

## Purpose

Record the narrow value of the external Kubert-Lang sources for the p25
exact-P route. The sources are real anchors for modular-unit generator and
congruence vocabulary, but the p25 ask is much more specific:

```text
z^121 * (1 + z + z^2) * (1 - z^263)
```

or the equivalent row-labeled mixed `C_3 x C_169` selector with orientation, or
an accepted theta2/theta2-inverse payload with period-156 context.

This page is a boundary, not a source-stage close.

## Sources Read

- EuDML/GDZ record for Kubert-Lang IV:
  `https://eudml.org/doc/162977`
- Springer/Google Books record for `Modular Units`:
  `https://books.google.com/books/about/Modular_Units.html?id=BwwzmZjjVdgC`
- Accessible modern summary of the Kubert-Lang theorem-K style condition:
  `https://afolsom.people.amherst.edu/Folsom-ModUnitsSel-MRL.pdf`
- Modern notation/context around Kubert-Lang Siegel functions:
  `https://www.numdam.org/item/10.5802/ahl.160.pdf`

## Pages Read

- `sources/kubert-lang.md`
- `lanes/exact-p.md`
- `evidence/p25_v2_kubert_lang_selector_boundary_20260616.md`
- `evidence/p25_v2_exactp_minimal_hook_20260616.md`
- `evidence/p25_v2_exactp_orientation_branch_router_20260616.md`
- `evidence/p25_v2_theta2_period156_support_contract_20260616.md`
- `evidence/p25_v2_constructive_payload_source_scan_20260616.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_kubert_lang_external_source_boundary_gate.py
```

The gate returned `p25_v2_kubert_lang_external_source_boundary_rows=1/1`.

## Boundary Rows

```text
kubert_lang_iv_eudml_gdz
  decision = source_anchor_general_generators_not_p25_hook
  use      = primary bibliographic/full-text anchor for KL IV
  missing  = exact p25 primitive word with orientation or theta2 payload

kubert_lang_modular_units_book
  decision = book_anchor_general_theory_not_p25_hook
  use      = primary book/source anchor for modular-unit theory
  missing  = row-labeled mixed C3 x C169 selector, primitive bridge word, or
             accepted theta2/theta2-inverse payload

accessible_theorem_k_summary
  decision = necessary_congruence_screen_not_selector_theorem
  use      = accessible theorem-K-style summary of KL congruence framework
  missing  = p25 six-term primitive word and orientation

modern_gamma1_generators_context
  decision = notation_context_not_exactp_source
  use      = context for KL/Siegel notation and modern generator language
  missing  = conductor and orientation data for the p25 exact-P packet

future_exact_kl_hit
  decision = accepted_if_arithmetic_source_theorem_present
  accepted = exact primitive word, mixed selector, or theta2 payload with
             arithmetic source theorem
  missing  = DANGER3 framing and extraction after theorem hit
```

## Counts

```text
general_framework_rows = 5
p25_primitive_word_rows = 1
p25_orientation_payload_rows = 1
repair_rows = 4
accepted_future_hook_rows = 1
current_kl_source_theorems = 0
```

## Verdict

```text
positive_artifact = external KL source boundary
continue_exactp = yes, but only through exact hook language
accepted_future_hook = theorem-legal arithmetic source result for the rigid
                       primitive word, the mixed C3 x C169 selector with
                       orientation, or accepted theta2/theta2-inverse payload
discard_condition = source lead only cites KL generator theory, generic unit
                    generation, quadratic congruence conditions, raw exponent
                    balance, or C169 projection data
```

The KL framework remains important because the p25 finite packet passes the
necessary exponent/congruence screens. But the source-stage gap is not the
general KL theorem; it is an arithmetic theorem emitting the exact p25
selector/payload.
