# P25 KSY-y Koo-Shin 2010 PDF/OCR Intake Contract

Updated: 2026-06-14 07:32 PDT

## Purpose

This is the drop-in contract for the missing Koo-Shin 2010 source.  It records
what counts as a usable source artifact and what gets rejected as insufficient
retrieval evidence.

## Target

```text
title = On some arithmetic properties of Siegel functions
authors = Ja Kyung Koo and Dong Hwa Shin
journal = Math. Z. 264 (2010), 137-177
doi = 10.1007/s00209-008-0456-9
KOASAS bitstream = 000271750900008.pdf
expected KOASAS size = 501978
expected KOASAS md5 = 39bf3ab80a349709394165f27f0eafbf
```

## Accept

```text
exact KOASAS PDF:
  PDF bytes match size 501978 and md5 39bf3ab80a349709394165f27f0eafbf

library/Springer PDF variant:
  file starts with %PDF and metadata/text/OCR identifies the target title,
  DOI, authors, and pages 137-177

OCR or page images:
  full Section 5 / Theorem 5.2 statement, including hypotheses, notation,
  product formula, and adjacent definitions needed to parse it
```

## Reject

```text
Springer metadata/access HTML
KOASAS metadata without bitstream
search snippets
the open arXiv sequel 1007.2318v1.pdf
anything missing the full theorem body or surrounding notation
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_koo_shin_pdf_intake_contract_gate.py
```

Candidate example:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_koo_shin_pdf_intake_contract_gate.py \
  --candidate /path/to/candidate.pdf
```

Marker:

```text
ksy_y_koo_shin_pdf_intake_contract_rows=1/1
```

## Next Step After Acceptance

Extract or OCR Section 5 and run:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_koo_shin_theorem_clause_intake_gate.py
```

The theorem-clause gate will accept only exact `P`/mixed-graph/equal-weight
orientation payloads.  Prime-power hygiene alone remains non-closing.
