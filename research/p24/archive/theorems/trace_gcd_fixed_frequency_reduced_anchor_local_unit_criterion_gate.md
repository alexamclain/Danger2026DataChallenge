# Reduced Anchor Local-Unit Criterion Gate

Date: 2026-06-07

This note records the finite local criterion behind the reduced-anchor
producer target.  The previous gates identify the residual as either the
cyclotomic divisor

```text
R_c(X) = Phi_c(X) / (X - 1)^(c - 1)
```

or the elliptic whole-subgroup kernel polynomial

```text
K_H(x) = prod_{Q in (H \ {O})/{+-1}} (x - x(Q)).
```

After reduction at a prime away from `c`, the local-unit test is exact:

```text
R_c(x) is a unit  iff  x is not in mu_c
K_H(T) is a unit iff  T is neither O nor a nonzero point of H
```

For the p24 residual with `c=179`, the forbidden cyclotomic anchor locus has
size `179`.  In the split finite check over modulus `32579`, this gives
`32400 = 32579 - 179` unit specializations.

## Interpretation

This does not construct the missing CM/Lang producer.  It sharpens the
producer obligation:

```text
1. construct the selected CM/Lang coordinate or subgroup polynomial
   p-integrally;
2. prove its reduction avoids the forbidden anchor/subgroup locus.
```

So the search-theorem target is now narrower than "find a p-unit": find the
selected p-integral object, then certify it is not one of the `179` forbidden
anchor specializations.

## Checks

Run:

```text
PYTHONPYCACHEPREFIX=/private/tmp/codex-pycache PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=p24 python3 p24/trace_gcd_fixed_frequency_reduced_anchor_local_unit_criterion_gate.py
```

Expected summary:

```text
cyclotomic_diamond_product_identity_rows=6/6
cyclotomic_local_unit_criterion_rows=6/6
cyclotomic_unit_count_rows=6/6
kernel_local_unit_criterion_rows=4/4
kernel_unit_count_rows=4/4
kernel_zero_pole_count_rows=4/4
p24_forbidden_cyclotomic_anchor_count=179
R_c_specialization_is_unit_iff_coordinate_avoids_mu_c=1
K_H_specialization_is_unit_iff_point_avoids_H_and_O=1
p24_producer_must_prove_selected_cm_lang_coordinate_avoids_forbidden_anchor_locus=1
local_unit_criterion_is_finite_algebra_not_the_cm_lang_producer=1
```

The Lean proof-contract scaffold is:

```text
p24/lean/TraceGcdReducedAnchorLocalUnitCriterionGate.lean
```
