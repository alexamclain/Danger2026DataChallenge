# P25 KSY-y Priority-1 Primary-Source Verdict

Updated: 2026-06-13 21:48 PDT

## Purpose

The theorem-query packet asked whether the live Sprang/KSY handles already
contain an exact theorem that closes the p25 anti-invariant normalized-y
product:

```text
P = prod_{j=-1..1} prod_{k=0..24} y(C+jD+kK)/y(-C-jD-kK)
C = (47,28), D = (22,3), K = (57,0)
```

This pass inspected the primary arXiv TeX sources by exact theorem blocks.  The
result is useful but not a closure: the sources provide real distribution and
formula language, but not the exact p25 finite product identity.

## Verdict Rows

```text
Sprang 1801 Appendix distribution relation
  source = https://arxiv.org/abs/1801.05677
  inspected = PaperEisensteinPoincare.tex:1714-1798
  positive = additive distribution relation for translated Kronecker sections
  verdict = conditional_additive_section_distribution_not_exact_P
  missing = specialization to exact K-traced normalized-y product P
  recommendation = continue only if exact product specialization appears

Sprang 1802 D-variant / Kato-Siegel comparison
  source = https://arxiv.org/abs/1802.04996
  inspected = deRhamRealization.tex:1100-1182
  positive = D-variant Kronecker section and dlog theta_D comparison
  verdict = conditional_derham_dlog_not_d2_product
  missing = D=2 multiplicative product identity; the displayed Kato-Siegel
            comparison is stated under a prime-to-6 condition
  recommendation = keep as source vocabulary, not as a closer

Sprang 1802 de Rham Eisenstein-class formula
  source = https://arxiv.org/abs/1802.04996
  inspected = deRhamRealization.tex:1645-1708
  positive = cohomology/Eisenstein-series formula using distribution machinery
  verdict = cohomology_eisenstein_class_not_finite_product
  missing = finite multiplicative normalized-y product or theta2 divisor payload
  recommendation = kill as direct closer; keep as context

KSY Equation (3.4)
  source = https://arxiv.org/abs/1007.2307
  inspected = source.tex:420-466
  positive = exact atom formula y_(r1,r2)=-g_(2r1,2r2)/g_(r1,r2)^4
  verdict = formula_language_not_product_distribution
  missing = distribution/product theorem selecting all 75 p25 atoms
  recommendation = continue only if upgraded to exact product theorem

KSY main torsion-generation theorem
  source = https://arxiv.org/abs/1007.2307
  inspected = source.tex:1000-1080
  positive = ray-class field generation from a single torsion point
  verdict = field_generation_not_product_identity
  missing = equality for the whole p25 anti-invariant product P
  recommendation = kill as direct closer

KSY Schertz-style primitive generator
  source = https://arxiv.org/abs/1007.2307
  inspected = source.tex:1160-1280
  positive = single-value generator / Siegel-Ramachandra ratio
  verdict = single_value_generator_not_k_traced_product
  missing = upgrade from one generator to exact K-traced p25 product
  recommendation = context only until exact product theorem exists
```

## Completed Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_priority1_primary_source_verdict_gate.py
```

```text
inspected_source_rows       = 6
exact_formula_rows          = 1
distribution_rows           = 3
field_generation_rows       = 2
direct_closing_rows         = 0
continue_rows               = 3
kill_as_direct_closer_rows  = 2
all_rows_have_missing_clause = 1
```

Marker:

```text
ksy_y_priority1_primary_source_verdict_rows=1/1
```

## Next Action

The next useful literature work is no longer "read Sprang/KSY."  It is a
targeted search for an external exact product/distribution specialization that
bridges:

```text
Sprang additive Kronecker distribution
or KSY normalized-y atom formula
```

to:

```text
exact finite p25 product P with mixed C_3 x C_169 graph, equal weights,
orientation, arithmetic producer, and DANGER3-legal finite-field framing
```
