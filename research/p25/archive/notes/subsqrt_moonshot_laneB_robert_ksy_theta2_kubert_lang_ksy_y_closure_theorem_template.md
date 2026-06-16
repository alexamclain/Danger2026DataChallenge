# P25 Lane B: KSY-y Closure-Theorem Template

Updated: 2026-06-13 19:18 PDT

## Purpose

The theorem-legality boundary says which output types are acceptable.  This
note states the exact theorem template that would close the KSY-y moonshot
route, and separates it from nearby non-closing claims.

## Formal Product

```text
P = prod_{j=-1..1} prod_{k=0..24}
      y(C + jD + kK) / y(-C - jD - kK)

C = (47,28)
D = (22,3)
K = (57,0)
y(Q) = -g(2Q) / g(Q)^4
```

Finite budgets already checked:

```text
source atoms                 = 75
KSY-y Siegel footprint       = 300
compact telescoping budget   = 975
factor-period budget         = 31
```

## Closing Theorem Shapes

Two theorem shapes would close the route:

```text
1. Divisor/additive product identity.
   Prove the exact KSY-y identity for P, preserving C/D/K, orientation, and
   the mixed C_75 x C_169 source graph.  The local certificate path then routes
   through theta2-inverse.

2. Value identity with period-156 context.
   Prove the exact finite-field value of P and include period-156 fixedness,
   telescoping, or equivalent branch/root data.  Then gcd(4^156-1,p-1)=1
   selects the F_p^* root.
```

## Non-Closing Shadows

These do not close the route by themselves:

```text
conditional:
  exact value of P without period-156 context
  finite theta2/theta2-inverse spine without arithmetic source
  CM/Lang or KSY field generation without exact finite-field identity

rejected:
  ambient 780-period value data
  Kubert-Lang exponent balance alone
```

## Source Question Packet

```text
KSY: can the normalized-y formula prove the exact P identity, not just generate
     a ray class field?

Siegel-Robert: can the value theorem include period-156 branch/root/telescoping
     data?

Sprang/Kronecker: can a D=2 differential/additive identity emit this exact
     anti-invariant product?

Kubert-Lang: can the exponent matrix be tied to the mixed C_75 x C_169 graph,
     not just congruence hygiene?

Challenge policy: if phrased as a finite-field identity for P, is this
     considered non-CM enough for DANGER3?
```

Primary source pointers for the next pass:

```text
Koo-Shin-Yoon normalized-y/ray-class fields:
  https://arxiv.org/abs/1007.2307
  https://mathsci.kaist.ac.kr/bk21/morgue/research_report_pdf/09-20.pdf

Kubert-Lang Siegel functions:
  https://eudml.org/doc/162977

Sprang/Kronecker D-variant differential route:
  https://arxiv.org/abs/1802.04996
```

## Local Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_closure_theorem_template_gate.py
```

Expected marker:

```text
robert_ksy_theta2_kubert_lang_ksy_y_closure_theorem_template_rows=1/1
```

## Interpretation

The finite side is sub-sqrt and executable.  The open item is not another
finite search artifact; it is a challenge-legal source theorem matching one of
the two closing shapes above.
