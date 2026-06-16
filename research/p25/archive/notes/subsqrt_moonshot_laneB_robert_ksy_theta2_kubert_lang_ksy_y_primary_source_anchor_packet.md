# P25 Lane B: KSY-y Primary-Source Anchor Packet

Updated: 2026-06-13 19:34 PDT

## Purpose

The source-clause audit says no primary source closes the route as currently
stated.  This packet names the exact source anchors to inspect next and the one
missing closure clause each live anchor would need to supply.

## Anchor Rows

```text
Koo-Shin-Yoon Theorem 5.3 / ray-class generation
  source = https://arxiv.org/pdf/1007.2307
  supplies = ray-class-field generation context
  missing = exact p25 product P with C=(47,28), D=(22,3), K=(57,0)
  ask = can Theorem 5.3 be specialized or strengthened to emit exact P?

Koo-Shin-Yoon normalized-y / Siegel formula
  source = https://mathsci.kaist.ac.kr/bk21/morgue/research_report_pdf/09-20.pdf
  supplies = y(Q)=-g(2Q)/g(Q)^4 formula language
  missing = selection of 75 atoms, mixed source graph, and period-156 context
  ask = can normalized-y be promoted from language to exact product theorem?

Siegel-Robert value units
  source = https://eudml.org/doc/162977
  supplies = value-unit language compatible with the value closure shape
  missing = period-156 branch/root/telescoping data for exact P
  ask = can a value theorem include support-period 156 fixedness?

Sprang Proposition 5.4 / Kato-Siegel dlog
  source = https://arxiv.org/pdf/1802.04996
  supplies = differential/additive output family compatible with divisor route
  missing = D=2 exact p25 anti-invariant product P
  ask = can the D-variant/Kronecker identity emit P?

Kubert-Lang Siegel functions are generators
  source = https://eudml.org/doc/162977
  supplies = Siegel-function generator and exponent-matrix language
  missing = mixed C_75 x C_169 graph selector and exact finite intake
  ask = can generator/exponent data be tied to the exact p25 mixed graph?

DANGER3 policy
  source = https://github.com/AndrewVSutherland/DANGER3
  supplies = challenge acceptance boundary, not a theorem
  missing = whether finite-field identity for P avoids the no-CM concern

Generic field generation / ambient value shadows
  rejected unless reframed as one of the closure-template theorem shapes
```

## Counts

```text
closing anchors     = 0
conditional anchors = 5
policy questions    = 1
rejected anchors    = 1
```

## Handoff Rule

A literature hit must name one anchor row and supply its missing
closure-template clause before it counts as moonshot progress.

## Local Gate

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_primary_source_anchor_packet_gate.py
```

Expected marker:

```text
robert_ksy_theta2_kubert_lang_ksy_y_primary_source_anchor_packet_rows=1/1
```
