# P25 KSY-y Kubert-Lang Mixed-Graph Scout

Updated: 2026-06-13 20:44 PDT

## Source Inspected

Kubert-Lang, `Units in the Modular Function Field IV. The Siegel Functions are
Generators`: <https://eudml.org/doc/162977>.

Verified source handle:

```text
EuDML doc 162977
GDZ article range LOG_0038
Math. Ann. 227 (1977), 223-242
PDF: https://gdz.sub.uni-goettingen.de/download/pdf/PPN235181684_0227/LOG_0038.pdf
```

The GDZ PDF article range is verified, but the local extraction path is
image-only for the theorem body.  This scout therefore records the verified
source handle and the local p25 finite-obligation tests; it does not claim that
an OCR pass recovered a closing theorem from the article body.

## Result

Kubert-Lang remains useful as Siegel-function generator and exponent language,
but the inspected source handle does not by itself emit the exact p25 mixed
graph.

Matched clause:

```text
Siegel-function generator / modular-unit exponent framework
```

First missing clause:

```text
exact C_3 x C_169 row-labeled pairs, quotient reflection center, or raw
equal-weight K-traced product with an arithmetic producer theorem
```

## Local Classification

```text
kl77_generator_theorem_handle:
  source decision = reject_exponent_hygiene_only
  mixed decision  = reject_c169_or_kl_screen_without_mixed_graph

kl77_c169_projection_screen:
  mixed decision = reject_c169_or_kl_screen_without_mixed_graph

kl77_fixed_t_without_base_anchor:
  mixed decision = conditional_fixed_t_without_base_row_anchor

kl77_exact_row_labeled_pairs_hypothetical:
  mixed decision = finite_mixed_graph_met_by_row_labeled_pairs

kl77_raw_product_arithmetic_producer_hypothetical:
  source decision = closing_divisor_or_additive_identity
  mixed decision  = closing_raw_product_with_arithmetic_producer
```

Local gate:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_kubert_lang_mixed_graph_primary_source_scout_gate.py
```

Boundary probes:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_source_claim_intake_gate.py \
  --candidate --name kl77_generator_theorem_handle \
  --anchor kubert_lang_siegel_functions_generators \
  --output-kind exponent-hygiene

PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_mixed_graph_obligation_gate.py \
  --candidate --name kl77_c169_projection_screen --kind kubert-lang \
  --c169-projection --kl-congruences

PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_mixed_graph_obligation_gate.py \
  --candidate --name kl77_exact_row_labeled_pairs_hypothetical \
  --kind kubert-lang --c169-projection --kl-congruences \
  --one-pair-per-row --fixed-t-edge --base-row-anchor \
  --exact-row-labeled-pairs
```

## Continue / Kill

Continue Kubert-Lang only if a source or formula hit emits exact row labels,
the reflection center `C=(2,28), D=(1,3)`, or the raw equal-weight
K-traced product.

Kill generator theorem, exponent congruence hygiene, and `C169` projection as
direct p25 closers.  They are screens and vocabulary, not the mixed-graph
arithmetic producer.

## Completed Gate

```text
generator_language_rows   = 1
direct_closing_rows       = 0
finite_payload_rows       = 1
conditional_rows          = 1
rejected_rows             = 2
hypothetical_closing_rows = 1
```

Marker:

```text
ksy_y_kubert_lang_mixed_graph_primary_source_scout_rows=1/1
```
