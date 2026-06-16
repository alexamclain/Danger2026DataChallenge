# P25 Lane B: KSY-y Primary-Source Clause Audit

Updated: 2026-06-13 19:29 PDT

## Purpose

The closure theorem template says what would close the route.  This audit
checks the current primary-source families against those clauses, without
giving broad source relevance credit for a proof.

## Result

```text
closing source rows     = 0
conditional source rows = 4
rejected source rows    = 1
```

No primary source family, as currently identified, closes the route as stated.
The live paths are all upgrade paths.

## Clause Rows

```text
Koo-Shin-Yoon normalized y:
  supplies formula language = yes
  missing = exact C/D/K product identity for P
  ask = can normalized-y prove exact P, not just generate ray class fields?

Siegel-Robert value units:
  supplies value-unit language = yes
  missing = period-156 branch/root/telescoping data
  ask = can a value theorem carry support-period 156 fixedness?

Sprang/Kronecker D-variant:
  supplies differential/additive technology = yes
  missing = D=2 differential/additive identity for exact P
  ask = can the D-variant identity emit the p25 anti-invariant product?

Kubert-Lang Siegel exponent matrix:
  supplies Siegel-function/exponent language = yes
  missing = mixed C_75 x C_169 graph selector
  ask = can the matrix select the exact mixed source graph, not only KL hygiene?

Ordinary field generation / ambient values:
  rejected
  missing = exact finite-field identity for P
```

## Primary Source Pointers

```text
Koo-Shin-Yoon:
  https://arxiv.org/abs/1007.2307
  https://mathsci.kaist.ac.kr/bk21/morgue/research_report_pdf/09-20.pdf

Kubert-Lang:
  https://eudml.org/doc/162977

Sprang:
  https://arxiv.org/abs/1802.04996
```

## Local Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_primary_source_clause_audit_gate.py
```

Expected marker:

```text
robert_ksy_theta2_kubert_lang_ksy_y_primary_source_clause_audit_rows=1/1
```

## Interpretation

The exact finite side is still alive, but the proof-side source debt is now
audited: either upgrade KSY/Sprang/Kubert-Lang to an exact product identity, or
upgrade Siegel-Robert to a period-156 value theorem.  Everything else remains
diagnostic scaffolding.
