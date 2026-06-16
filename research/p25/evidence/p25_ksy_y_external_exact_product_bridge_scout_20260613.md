# P25 KSY-y External Exact-Product Bridge Scout

Updated: 2026-06-13 21:54 PDT

## Purpose

The primary Sprang/KSY pass found real distribution and formula machinery but
no exact p25 product theorem.  This scout asks a narrower question: is there an
external source bridge from Kronecker/Siegel/Kato-Siegel distribution language
to the exact finite product

```text
P = prod_{j=-1..1} prod_{k=0..24} y(C+jD+kK)/y(-C-jD-kK)
C = (47,28), D = (22,3), K = (57,0)
```

## Rows

```text
Koo-Shin 2010 Siegel-function distribution candidate
  source = https://link.springer.com/article/10.1007/s00209-008-0456-9
  status = source handle verified, theorem text not yet verified
  positive = article is about arithmetic properties/products of Siegel functions;
             search snippets indicate a Theorem 3.1 and distribution relation
  blocker = KAIST PDF host did not resolve locally; Springer returned HTML
  verdict = candidate_needs_pdf_or_ocr_before_theorem_use
  next = retrieve/OCR PDF, then feed any claimed row through exact-product intake

Bannai-Kobayashi Kronecker theta distribution
  source = https://arxiv.org/abs/math/0610163
  inspected = EKnumber-v3.0-2007.12.11.tex:1070-1182
  positive = exact Kronecker theta distribution relation over ideal-torsion sums
  verdict = verified_additive_theta_distribution_not_product_bridge
  missing = finite multiplicative normalized-y/Siegel product for the p25 atoms
  next = keep as Sprang source ancestor, not as a direct closer

Scholl Kato-Siegel multiplicative distribution control
  source = https://www.dpmms.cam.ac.uk/~ajs1005/preprints/euler.pdf
  inspected = scholl_euler.txt:377-600
  positive = multiplicative norm/distribution relation for canonical theta_D
  verdict = verified_multiplicative_distribution_but_D2_ineligible
  missing = theorem assumes (6,D)=1 and Robert subgroup order prime to 6
  next = keep as odd-D control; do not import directly for p25 D=2
```

## Completed Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_external_exact_product_bridge_scout_gate.py
```

```text
source_handle_rows              = 3
verified_theorem_rows           = 2
access_blocked_candidate_rows   = 1
direct_closing_rows             = 0
continue_rows                   = 1
kill_as_direct_closer_rows      = 2
all_rows_have_missing_clause    = 1
```

Marker:

```text
ksy_y_external_exact_product_bridge_scout_rows=1/1
```

## Next Action

The only live external-source action from this scout is Koo-Shin 2010
PDF/OCR/access.  It should be accepted only if the theorem text emits exact
row-labeled pairs, a quotient reflection center, or a raw equal-weight
K-traced product that passes the mixed-graph and exact-product intake gates.
