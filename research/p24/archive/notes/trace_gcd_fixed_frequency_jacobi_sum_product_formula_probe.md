# Jacobi-Sum Product-Formula Probe

Date: 2026-06-07

## Point

The current multiplicative target asks for a packet `U(r,c)` satisfying:

```text
U(r,0)U(-r,0)=alpha_0
U(r,c)U(-r,-c)=alpha_1 for c != 0
prod_c U(r,c)/U(r,0)^c = beta independent of r.
```

The admissible-carry algebra looks exactly like the Stickelberger divisor of a
Jacobi sum.  This probe tests the most literal small-model candidate:

```text
U_t = J(chi^(u*t), chi^(v*t))
```

for small orders `N=7*c`, with `u=7*s` and `(u,v)` admissible.  Degenerate
characters are included, because the `C`-zero fiber is where one character can
become trivial.

## Result

Raw finite-field Jacobi sums do supply the off-`C=0` pair-product complement:

```text
J(chi^a,chi^b) * J(chi^-a,chi^-b) = constant
```

in every sampled admissible row.  This is exactly the expected arithmetic
source for the inversion-complement half of the value-side theorem.

However, raw Jacobi sums do **not** automatically supply the full selected
producer target:

```text
C-zero two-level pair-products are not uniformly constant;
selected row-product ratios are not constant in r;
normalizing the C-zero fiber alone does not fix the row ratios.
```

Observed on the sampled admissible pairs:

```text
c=5:  raw_off_c_pair_products_constant=8/8, row_ratios=1/8
c=11: raw_off_c_pair_products_constant=8/8, row_ratios=1/8
c=13: raw_off_c_pair_products_constant=8/8, row_ratios=1/8
```

The lone row-ratio hit in each row is `(u,v)=(7,7)`, which is right-trivial.
On the right-mixed part relevant to the six nontrivial right characters:

```text
c=5:  right_mixed_raw_row_ratios_constant=0/7
c=11: right_mixed_raw_row_ratios_constant=0/7
c=13: right_mixed_raw_row_ratios_constant=0/7
```

## Consequence

This is a useful partial positive and a guardrail:

```text
Jacobi sums explain the off-zero inversion complement;
they do not by themselves prove the selected affine row balance.
```

So a viable Jacobi/CM-Lang proof needs an extra ingredient:

```text
Hasse-Davenport-style distribution,
C-axis norm relation,
residue theorem,
or selected trace-GCD correction
```

that forces:

```text
prod_c U(r,c)/U(r,0)^179
```

to be independent of `r`.

This aligns with the rank split:

```text
structural symmetry is the 629-equation side;
three global balances remain after structural symmetry.
```

The new proof target is therefore sharper:

```text
combine Jacobi-sum inversion complement with a selected C-axis distribution
relation.
```

## Check

```text
PYTHONPYCACHEPREFIX=/private/tmp/codex-pycache PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH=p24 python3 \
  p24/trace_gcd_fixed_frequency_jacobi_sum_product_formula_probe.py
```

Observed:

```text
raw_off_c_pair_product_rows=3/3
raw_two_level_pair_product_rows=0/3
raw_row_ratio_rows=0/3
c_zero_normalized_row_ratio_rows=0/3
right_mixed_no_row_ratio_rows=3/3
right_mixed_no_c_zero_normalized_row_ratio_rows=3/3
```

No p24 class-set enumeration is used.
