# p24 Multiplicative Producer Dictionary Gate

Date: 2026-06-07

## Point

The selected-defect raw identities have a direct multiplicative/product-formula
interpretation.

Let:

```text
U(r,c) = omega ^ g(r,c)
```

where `g(r,c)` is the raw post-`Tr_{B/C}` packet and `omega` is a cyclic
torus coordinate.  Then the additive producer theorem:

```text
g(r,0)+g(-r,0)=A_0
g(r,c)+g(-r,-c)=A_1, c != 0
sum_c g(r,c)-179*g(r,0) is independent of r
```

is equivalent to the multiplicative theorem:

```text
U(r,0) * U(-r,0) = alpha_0
U(r,c) * U(-r,-c) = alpha_1, c != 0
prod_c U(r,c) / U(r,0)^179 = beta
```

with constants independent of `r` and `c`.

## Consequence

This is the most product-formula-shaped version of the current missing
theorem:

```text
construct a modular-unit / elliptic-unit / CM-Lang product U(r,c)
whose pair-products and selected row-product ratios are constant.
```

Then the selected logarithmic defect:

```text
f(r,c)=g(r,c)-g(r,0)
```

satisfies the three value-side identities, hence the four Fourier families,
hence the admissible Jacobi span and the verifier pipeline.

Controls show the two multiplicative pieces are independent:

```text
constant pair-products without row-product ratios leak row balances;
constant row-product ratios without pair-products leak structural symmetry.
```

## Check

```text
PYTHONPYCACHEPREFIX=/private/tmp/codex-pycache PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH=p24 python3 \
  p24/trace_gcd_fixed_frequency_p24_multiplicative_producer_dictionary_gate.py
```

Observed:

```text
multiplicative_additive_equivalence=3/3
forced_product_formula_hits=3/3
inversion_product_without_row_ratio_controls=3/3
row_ratio_without_inversion_product_controls=3/3
```

No p24 class set or CM root enumeration is used.
