# P25 KSY-y Sprang/Kronecker D=2 Scout

Updated: 2026-06-13 20:50 PDT

## Source Inspected

Sprang, `Eisenstein-Kronecker series via the Poincare bundle`:
<https://arxiv.org/abs/1801.05677>.

Primary clauses checked:

```text
Introduction / Section 5: Kronecker-section construction of Kato-Siegel logarithmic derivatives
Corollary 5.7: omega_D construction and comparison with dlog Dtheta
Appendix A: Theorem A.2 and Corollaries A.3-A.4 distribution relations
```

## Result

Sprang remains one of the best live source families, but only for a narrow
divisor/additive theorem target.

Matched clauses:

```text
even-D Kronecker/differential construction remains live
omega_D is defined beyond the ordinary prime-to-6 Kato-Siegel theta_D setting
distribution relations provide a plausible arithmetic producer surface
```

First missing clause:

```text
explicit even-D identity emitting exact P, exact theta2/theta2^-1 divisor data,
or compact KSY center/half/orientation data for the p25 mixed product
```

## Local Classification

```text
sprang_even_d_kronecker_section:
  parameter decision = conditional_needs_even_D_kronecker_clause
  product decision   = conditional_formula_language_without_product_proof

sprang_corollary_5_7_omega_d:
  parameter decision = conditional_needs_even_D_kronecker_clause
  product decision   = conditional_missing_exact_product

sprang_appendix_distribution_relation:
  product decision = conditional_missing_exact_product

ordinary_kato_theta_d2_shortcut:
  parameter decision = reject_ordinary_kato_theta_2_prime_to_6_violation

sprang_exact_p_additive_identity_hypothetical:
  product decision = closing_exact_product_identity
```

Local gate:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_sprang_kronecker_d2_primary_source_scout_gate.py
```

Boundary probes:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_exact_product_intake_gate.py \
  --candidate --name sprang_even_d_kronecker_section \
  --anchor sprang_prop_5_4_kato_siegel_dlog \
  --output-kind formula-language

PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_exact_product_intake_gate.py \
  --candidate --name sprang_exact_p_additive_identity_hypothetical \
  --anchor sprang_prop_5_4_kato_siegel_dlog \
  --output-kind divisor-additive --exact-product --mixed-graph \
  --equal-weight --orientation --arithmetic-producer --challenge-legal \
  --finite-intake
```

## Continue / Kill

Continue Sprang/Kronecker for one thing: an explicit even-`D`
differential/additive identity that emits exact `P`, exact theta2 data, or the
compact KSY theorem payload.

Kill direct ordinary Kato-Siegel `theta_D` import at `D=2`, generic dlog
framework claims, and distribution relations that do not instantiate the p25
mixed graph and K-traced product.

## Completed Gate

```text
even_d_live_rows          = 2
direct_closing_rows       = 0
conditional_rows          = 3
rejected_rows             = 1
hypothetical_closing_rows = 1
```

Marker:

```text
ksy_y_sprang_kronecker_d2_primary_source_scout_rows=1/1
```
