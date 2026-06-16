# P25 KSY-y Koo-Shin Distribution Access Probe

Updated: 2026-06-13 22:02 PDT

## Purpose

The external exact-product scout left one live literature lead: Koo-Shin 2010,
which may contain a prime-level Siegel-function product/distribution theorem.
This note records the current evidence level so snippet evidence does not get
promoted into a p25 source theorem.

Target product:

```text
P = prod_{j=-1..1} prod_{k=0..24} y(C+jD+kK)/y(-C-jD-kK)
C = (47,28), D = (22,3), K = (57,0)
```

## Probe Rows

```text
Springer primary metadata
  source = https://link.springer.com/article/10.1007/s00209-008-0456-9
  evidence = source handle verified
  positive = article is exactly Koo-Shin, Math. Z. 264 (2010), 137-177;
             abstract says it establishes criteria for products of Siegel
             functions and treats class invariants
  blocker = subscription preview; no theorem body
  verdict = source_handle_positive_but_not_theorem_body
  next = continue only with full PDF/OCR

ASARC / search snippet for Theorem 5.2
  source = https://asarc.kaist.ac.kr/bbs/download.php?board_id=preprint&file=1239862589_0.691233.pdf&no=14
  evidence = snippet positive, not source text
  local = /tmp/p25_lit_scout/koo_shin_2010_probe/fetch_24.bin:147-155
  positive = snippet says the paper first gives distribution relations of
             Siegel functions and Theorem 5.2 begins with an odd-prime product
             over a primitive 1/p lattice quotient
  blocker = hypotheses/conclusion/exponent conventions are unknown
  verdict = snippet_positive_but_not_usable_theorem
  next = retrieve full theorem text, then run exact-product intake

Access attempts
  tested = direct ASARC URL, r.jina reader variants, Google cache, Springer PDF
  evidence = local DNS and r.jina report asarc.kaist.ac.kr NXDOMAIN;
             Springer PDF returns HTML/idp access flow; Google cache returns
             search challenge HTML
  verdict = current_handles_do_not_recover_pdf
  next = alternate mirror, library access, author preprint, or OCR

Koo-Shin II / open context
  source = https://arxiv.org/abs/1007.2318
  local = /tmp/p25_lit_scout/koo_shin_ii_1007_2318/src/Siegel.tex:282-299
  positive = gives a Kubert-Lang product modularity criterion for products of
             Siegel functions and confirms the surrounding vocabulary
  blocker = product congruence hygiene alone does not select the p25 mixed
            C_3 x C_169 graph or the 75 equal-weight atoms
  verdict = verified_context_product_criterion_not_exact_p25_product
  next = keep as hygiene context, not as a direct closer
```

## Completed Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_koo_shin_distribution_access_probe_gate.py
```

```text
source_handle_verified_rows   = 2
snippet_positive_rows         = 1
theorem_body_rows             = 0
access_failure_rows           = 1
context_product_criterion_rows = 1
direct_closing_rows           = 0
continue_rows                 = 3
kill_as_direct_closer_rows    = 2
all_rows_have_missing_clause  = 1
```

Marker:

```text
ksy_y_koo_shin_distribution_access_probe_rows=1/1
```

## Verdict

Koo-Shin 2010 remains the best external exact-product retrieval target, but it
is not yet source evidence for the p25 theorem.  It should get a narrow
retrieval/OCR/subagent job.  The first falsifier is simple: without the full
Theorem 5.2 body and an exact map to the p25 mixed graph, this lead cannot
advance the moonshot beyond literature-priority status.
