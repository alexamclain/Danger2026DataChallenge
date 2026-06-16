# P25 KSY-y Koo-Shin Public Mirror / Sequel Falsifier

Updated: 2026-06-13 22:31 PDT

## Purpose

The KOASAS probe made the Koo-Shin 2010 target exact.  This note records the
complementary public-source pass: currently visible public handles and the open
sequel do not provide the missing theorem body or a p25 product producer.

Target product:

```text
P = prod_{j=-1..1} prod_{k=0..24} y(C+jD+kK)/y(-C-jD-kK)
C = (47,28), D = (22,3), K = (57,0)
```

## Source Rows

```text
ASARC indexed preprint
  url = https://asarc.kaist.ac.kr/bbs/download.php?board_id=preprint&file=1239862589_0.691233.pdf&no=14
  positive = search still indexes this as the likely preprint PDF
  local = curl and r.jina both report asarc.kaist.ac.kr cannot be resolved
  verdict = indexed_but_unreachable_no_theorem_body

Springer public article page
  url = https://link.springer.com/article/10.1007/s00209-008-0456-9
  positive = official metadata, DOI, pages, authors, abstract, access status
  local = fetched PDF endpoint is HTML; page metadata says access is not free
  theorem text = not present
  verdict = official_metadata_only_no_public_theorem

KOASAS handle and METS
  url = https://koasas.kaist.ac.kr/handle/10203/96547
  positive = exact bitstream target 000271750900008.pdf is known
  size = 501978
  md5 = 39bf3ab80a349709394165f27f0eafbf
  blocker = direct bitstream redirects to authorization-required HTML
  verdict = exact_bitstream_target_but_no_theorem_body

Koo-Shin II / arXiv sequel
  url = https://arxiv.org/abs/1007.2318
  local source = /tmp/p25_lit_scout/koo_shin_public_mirror_probe/Siegel_II.tex
  positive = open TeX gives the Siegel-function definition, transformation and
             integrality facts, Kubert-Lang modularity criterion, and
             corollary for g_r^(12N/gcd(6,N))
  blocker = those clauses are hygiene/context, not an exact p25 product
  verdict = open_sequel_hygiene_only_not_exact_p25_product
```

## Completed Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_koo_shin_public_mirror_sequel_falsifier_gate.py
```

```text
source_handles_checked              = 4
unreachable_indexed_preprint_rows   = 1
metadata_only_rows                  = 1
restricted_bitstream_rows           = 1
open_sequel_source_rows             = 1
inherited_hygiene_clause_rows       = 3
public_main_theorem_rows            = 0
direct_closing_rows                 = 0
continue_retrieval_rows             = 2
kill_as_direct_closer_rows          = 2
all_rows_have_missing_clause        = 1
```

Marker:

```text
ksy_y_koo_shin_public_mirror_sequel_falsifier_rows=1/1
```

## Verdict

The public sequel is useful context, not the missing producer.  The live
Koo-Shin action remains exact retrieval of the 2010 PDF/OCR, then theorem-clause
intake.  Do not treat the open sequel's modularity/integrality criteria as a
closing source theorem for the p25 product.
