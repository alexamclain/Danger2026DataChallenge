# Jacobi-Sum Single-Anchor Correction Gate

Date: 2026-06-07

## Point

The row-ratio miner found the exact finite-field defect:

```text
delta_c = (q - 2)^(-(c - 1)).
```

This note records the next sharpening.  For literal right-mixed admissible
Jacobi packets:

```text
U_t = J(chi^(u*t), chi^(v*t))
```

on `C_7 x C_c`, the entire product-formula failure is repaired by changing
one value:

```text
U(0,0)=J(1,1)=q-2
U'(0,0)=U(0,0)/(q-2)=1
U'(r,c)=U(r,c) otherwise.
```

## Why This Works

With the convention that characters vanish at `0`:

```text
J(1,1)=q-2
J(1,lambda)=-1 for lambda nontrivial.
```

Therefore the raw C-zero pair-product at the right-zero row is `(q-2)^2`,
while the nonzero right rows have C-zero pair-product `1`.  Multiplying only
`U(0,0)` by `(q-2)^(-1)` makes the C-zero pair-products constant.

The same correction also fixes the selected row-product ratio.  Only the
denominator `U(0,0)^c` and one numerator factor in the right-zero row change,
so the right-zero row ratio is multiplied by:

```text
((q-2)^(-1))^(1-c) = (q-2)^(c-1).
```

This cancels the previously observed defect:

```text
delta_c = (q-2)^(-(c-1)).
```

Off-C-zero pair-products and all nonzero right-row ratios are unchanged.

## Consequence

The literal finite-field Jacobi theorem now has a clean split:

```text
punctured Hasse-Davenport along C_c
  => off-C-zero pair-products and nonzero right-row ratio;

single degenerate-anchor normalization J(1,1)/(q-2)
  => C-zero pair-products and right-zero row ratio;

together
  => full multiplicative producer identities.
```

This is stronger than "there is some non-cyclotomic defect."  The defect is a
single degenerate Jacobi anchor.

For p24, the missing arithmetic input is now more precise:

```text
identify the selected trace-GCD/CM-Lang analogue of the single
J(1,1)/(q-2) anchor normalization after Tr_{B/C}.
```

If such an anchor unit exists, the remaining row-balance identities should
come from the punctured product formula instead of from three unrelated
global equations.

## Check

```text
PYTHONPYCACHEPREFIX=/private/tmp/codex-pycache PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH=p24 python3 \
  p24/trace_gcd_fixed_frequency_jacobi_sum_anchor_correction_gate.py
```

Observed:

```text
exhaustive_right_mixed_pairs=72 for c=5
exhaustive_right_mixed_pairs=540 for c=11
exhaustive_right_mixed_pairs=792 for c=13
raw_full_pair_failure_rows=3/3
raw_row_ratio_failure_rows=3/3
expected_zero_fiber_degeneracy_rows=3/3
single_anchor_correction_rows=3/3
corrected_pair_product_rows=3/3
corrected_row_ratio_rows=3/3
corrected_product_formula_rows=3/3
anchor_scale_formula_rows=3/3
```

No p24 class-set enumeration is used.
