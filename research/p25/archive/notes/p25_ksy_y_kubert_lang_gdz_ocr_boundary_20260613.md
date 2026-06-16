# P25 KSY-y Kubert-Lang GDZ/OCR Boundary

Updated: 2026-06-13 22:50 PDT

## Purpose

This note records the exact boundary of the direct Kubert-Lang IV source probe.
The source remains the right Siegel-unit/modular-unit framework for the p25
KSY-y lane, but the current GDZ visual pass does not find the p25-specific
mixed graph, reflection center, or raw equal-weight K-traced product.

## Source Handle

```text
source = Kubert-Lang, Units in the Modular Function Field IV
EuDML = https://eudml.org/doc/162977
GDZ PDF = https://gdz.sub.uni-goettingen.de/download/pdf/PPN235181684_0227/LOG_0038.pdf
article = Math. Ann. 227 (1977), 223-242
local_pdf = /tmp/p25_lit_scout/kubert_lang_1977_probe/LOG_0038.pdf
bytes = 1596008
md5 = 1a1e75393a31bdb8f921b0169d819562
pdf_pages = 21
article_image_pages = 20
```

The pypdf extraction boundary is also explicit:

```text
local_text = /tmp/p25_lit_scout/kubert_lang_1977_probe/LOG_0038_pypdf_text.txt
page 1 = GDZ/license text
pages 2-21 = image-only article body, only page-number-sized extracted text
```

Rendered pages are in:

```text
/tmp/p25_lit_scout/kubert_lang_1977_probe/pages_all/
```

## Visual Source Rows

```text
article page 223:
  evidence = pages_all/page-02.png
  positive = the paper frames Siegel functions as generators of modular units
             modulo constants, with q-expansion and product/root methods
  boundary = generator language is exponent hygiene, not the p25 mixed
             C_3 x C_169 selector

article page 224:
  evidence = pages_all/page-03.png
  positive = the setup defines Siegel functions as powers of Klein forms,
             modular up to constants, with distribution language
  boundary = valid source coordinates, but no row labels, reflection center, or
             raw K-traced equality

article pages 239-240:
  evidence = pages_all/page-18.png and pages_all/page-19.png
  positive = constant products of Siegel functions, distribution,
             lower-level induction, and prime-power independence/dependence
             criteria are visible
  boundary = these criteria constrain denominators and exponents globally;
             they do not select the p25 row graph or orientation

article pages 241-242:
  evidence = pages_all/page-20.png and pages_all/page-21.png
  positive = the Delta/Klein-form dependence section and prime-power
             unit-group conclusion are visible
  boundary = still modular-unit generation/dependence, not a finite p25
             producer
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_kubert_lang_gdz_ocr_boundary_gate.py
```

Expected counts:

```text
pdf_retrieval_rows             = 1
render_rows                    = 1
embedded_article_text_rows     = 0
image_only_article_pages       = 20
visual_source_rows             = 4
generator_language_rows        = 1
multiplicative_dependence_rows = 1
delta_dependence_rows          = 1
row_labeled_pair_rows          = 0
reflection_center_rows         = 0
raw_k_traced_product_rows      = 0
direct_closing_rows            = 0
ocr_required_rows              = 1
```

Marker:

```text
ksy_y_kubert_lang_gdz_ocr_boundary_rows=1/1
```

## Verdict

Kubert-Lang IV stays live as framework, vocabulary, and dependence machinery.
It is not a direct p25 closer from the current source pass.  Continue this lane
only if OCR, the p-primary sequel, or a human/literature hit returns one of:

```text
exact C_3 x C_169 row-labeled pairs
quotient reflection center C=(2,28), D=(1,3)
raw equal-weight K-traced product with arithmetic producer status
```

Kill generator theorem language, generic multiplicative-dependence criteria,
and prime-power/Delta generation as direct p25 closers unless they are upgraded
to one of those exact finite payloads.
