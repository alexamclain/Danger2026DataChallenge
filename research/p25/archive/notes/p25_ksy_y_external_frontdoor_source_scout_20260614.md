# P25 KSY-y External Front-Door Source Scout

Updated: 2026-06-14 21:28 PDT

## Purpose

The local source scan found no source-closing hit.  This checkpoint records the
first external/front-door scout against primary or publisher sources and keeps
the ask narrow: a source matters only if it supplies one exact p25 front-door
identity.

Result:

```text
visible_source_closing_hits = 0
```

## External Rows

```text
kubert_lang_full_set_units:
  source   = Kubert-Lang modular units
  url      = https://eudml.org/doc/162791
  decision = context_modular_unit_generators_exact_mixed_product_missing
  missing  = exact mixed C3 x C169 exponent matrix or divisor identity for P/H0/U_chi
  action   = use as modular-unit language until a p25-specific product theorem appears

kubert_lang_modular_units_book:
  source   = Kubert-Lang book-level modular-unit theory
  url      = https://books.google.com/books/about/Modular_Units.html?id=BwwzmZjjVdgC
  decision = broad_modular_unit_theory_not_exact_frontdoor
  missing  = one of the four exact p25 front-door identities
  action   = do not cite broad generator theory as closure

schertz_klein_quotient_generators:
  source   = Schertz elliptic-unit/Klein-form quotients
  url      = https://www.numdam.org/item/JTNB_1997__9_2_383_0.pdf
  decision = context_elliptic_unit_quotient_generator_exact_p25_identity_missing
  missing  = quotient identified with exact P/H0/U_chi plus period-156 or divisor boundary
  action   = continue only if specialized to the p25 front-door payload

scholl_kato_siegel_functions:
  source   = Kato-Siegel theta / Robert generalization
  url      = https://www.dpmms.cam.ac.uk/~ajs1005/preprints/euler.pdf
  decision = context_norm_compatible_kato_siegel_direct_D2_missing
  missing  = D=2 exact product/divisor specialization for the p25 normalized-y payload
  action   = keep divisor language; reject ordinary prime-to-6 theta_D import as direct closer

ksy_normalized_y_ray_class_generators:
  source   = Koo-Shin-Yoon normalized-y ray-class generators
  url      = https://arxiv.org/abs/1007.2307
  decision = context_normalized_y_generator_exact_75_product_missing
  missing  = product/distribution theorem selecting all 75 p25 atoms with orientation
  action   = use as normalized-y vocabulary unless upgraded to exact p25 product theorem
```

## Counts

```text
row_count                                = 5
visible_source_closing_hits              = 0
promising_context_rows                   = 5
direct_closer_kill_rows                  = 3
exact_p25_specialization_needed_rows     = 5
period156_needed_rows                    = 2
arithmetic_source_needed_rows            = 5
primary_or_publisher_source_rows         = 5
exact_frontdoor_search_rows              = 4
```

## Interpretation

The external scout did not find a visible theorem that closes source stage.
It did confirm that the right external families are still the same ones:
Kubert-Lang/Siegel products, Schertz/Klein quotients, Kato-Siegel/Robert
divisor language, and KSY normalized-y formulas.

But the search target is no longer broad.  The next useful hit must be an
exact p25 specialization:

```text
exact H0 divisor/additive identity with H90 boundary
U_chi/W conductor-39 divisor or additive identity
twisted/H90 divisor identity with period-156 bridge context
exact 75-atom P divisor/additive theorem
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_external_frontdoor_source_scout_gate.py
```

Marker:

```text
ksy_y_external_frontdoor_source_scout_rows=1/1
```
