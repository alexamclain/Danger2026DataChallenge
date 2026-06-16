# P25 KSY-y Kubert-Lang V Iwasawa Boundary

Updated: 2026-06-14 07:22 PDT

## Purpose

Kubert-Lang IV points onward to the next paper in the series.  This note
records the direct KL V probe so that the moonshot does not confuse a genuine
p-primary/Iwasawa modular-tower result with the exact finite p25 payload.

## Source Handle

```text
source = Kubert-Lang, Units in the Modular Function Field. V.
subtitle = Iwasawa Theory in the Modular Tower
EuDML = https://eudml.org/doc/182778
GDZ PDF = https://gdz.sub.uni-goettingen.de/download/pdf/PPN235181684_0237/LOG_0016.pdf
article = Math. Ann. 237 (1978), 97-104
local_pdf = /tmp/p25_lit_scout/kubert_lang_v_probe/LOG_0016.pdf
bytes = 691420
md5 = ca93ce860e3cd38717b15853ae30ead3
pdf_pages = 9
article_image_pages = 8
```

The local extraction boundary:

```text
local_text = /tmp/p25_lit_scout/kubert_lang_v_probe/LOG_0016_pypdf_text.txt
page 1 = GDZ/license text
pages 2-9 = image-only article body, only GDZ page-id-sized extracted text
```

Rendered pages are in:

```text
/tmp/p25_lit_scout/kubert_lang_v_probe/pages_log0016/
```

## Visual Source Rows

```text
article page 97:
  evidence = pages_log0016/page-2.png
  positive = modular curves X(p^n), Cartan action, projective group rings,
             Iwasawa algebra, and Kummer theory for units in the modular tower
  boundary = broad tower/Kummer structure, not exact p25 P or row graph

article page 101:
  evidence = pages_log0016/page-6.png
  positive = Theorem 1 gives a one-dimensional free-module structure over the
             Iwasawa algebra
  boundary = module freeness does not select p25 row labels, orientation, or
             the C_3 x C_169 packet

article pages 102-103:
  evidence = pages_log0016/page-7.png and pages_log0016/page-8.png
  positive = cyclotomic/Vandiver analogy, torsion/factor-group lemmas, and
             maximal unramified p-abelian extension structure
  boundary = class-field/tower analogy, not a challenge-legal finite-field
             identity for p25
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_kubert_lang_v_iwasawa_boundary_gate.py
```

Expected counts:

```text
source_handle_rows           = 1
pdf_retrieval_rows           = 1
embedded_article_text_rows   = 0
image_only_article_pages     = 8
visual_source_rows           = 3
iwasawa_tower_rows           = 1
theorem1_freeness_rows       = 1
vandiver_cyclotomic_rows     = 1
row_labeled_pair_rows        = 0
reflection_center_rows       = 0
raw_k_traced_product_rows    = 0
direct_closing_rows          = 0
ocr_required_rows            = 1
```

Marker:

```text
ksy_y_kubert_lang_v_iwasawa_boundary_rows=1/1
```

## Verdict

KL V is useful context for p-primary tower/Kummer structure.  It is not a
direct p25 closer from the current visual pass.  Continue only if OCR or a
human theorem hit upgrades this tower structure into one of the finite payloads
already required by the KL IV boundary:

```text
exact C_3 x C_169 row-labeled pairs
quotient reflection center C=(2,28), D=(1,3)
raw equal-weight K-traced product with arithmetic producer status
```

Kill p-primary/Iwasawa freeness, Vandiver/cyclotomic analogy, and generic
unramified-extension structure as direct p25 closers.
