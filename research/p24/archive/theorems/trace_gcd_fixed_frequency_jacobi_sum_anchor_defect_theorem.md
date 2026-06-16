# Jacobi-Sum Anchor-Defect Theorem Candidate

Date: 2026-06-07

## Point

The product-formula target has now split more sharply.

For a literal finite-field Jacobi-sum packet:

```text
U_t = J(chi^(u*t), chi^(v*t))
```

with `N=7*c`, `u=7*s`, and `(u,v)` in the admissible C-axis family, small
exact models show:

```text
1. off-C-zero pair-products are constant;
2. selected row-product ratios are constant on the six nonzero right rows;
3. the only row-product-ratio failure is the right-zero anchor;
4. that anchor defect is universal across sampled admissible pairs for each c;
5. the universal anchor defect is not a μ_(7c), μ_7, or μ_c multiplier.
```

This is much better than the first raw Jacobi-sum boundary: the row-ratio
problem is not spread across the right axis.  It is a single anchor scalar.

## Hasse-Davenport Shape

The expected proof source is Hasse-Davenport applied along the `C_c` fiber.

For `r != 0`, the C-fiber product:

```text
prod_c J(chi^(u*t(r,c)), chi^(v*t(r,c)))
```

has no trivial-character degeneration.  Since `u` is C-axis and `v` and
`u+v` have the same right component after quotienting by the C-axis shift,
the Gauss-sum products should collapse to a right-independent scalar after
dividing by `U(r,0)^c`.

For `r = 0`, the same fiber contains degenerate Jacobi sums involving the
trivial character.  The Hasse-Davenport collapse changes by a scalar
`delta_c`.  With the convention that every character vanishes at `0`,

```text
J(1,1)=q-2,
J(1,lambda)=-1 for lambda nontrivial.
```

Thus the literal finite-field anchor defect is:

```text
delta_c = (q-2)^(-(c-1)).
```

In the small probes:

```text
c=5:  delta_c = 44  in F_211
c=11: delta_c = 586 in F_617
c=13: delta_c = 589 in F_911
```

The scalar is universal across sampled admissible pairs but is not a small
root of unity and has no `c`-th root in the sampled value field.

## Consequence For p24

The selected weighted trace-GCD theorem can now be split as:

```text
Jacobi/Hasse-Davenport punctured-right theorem
  => structural inversion complement
  => row-product ratio on right != 0

selected anchor correction theorem
  => right-zero row-product ratio matches the nonzero rows

together
  => selected affine row balance
  => full value-side identities
  => rank-621 admissible span
```

This is a narrower missing theorem than before.  Instead of proving all three
global balances from scratch, try to prove:

```text
the actual selected trace-GCD packet carries exactly the universal
Hasse-Davenport anchor correction delta_179.
```

Equivalently, in additive language, the row-sum defect after the punctured
Jacobi/Hasse-Davenport theorem should be a pure right-zero anchor, and the
selected-child/trace-defect term must cancel it.

## Guardrail

A simple root-of-unity multiplier normalization is insufficient:

```text
right_mixed_non_cyclotomic_defect_rows=3/3
right_mixed_non_mu7_defect_rows=3/3
right_mixed_non_muc_defect_rows=3/3
anchor_defect_has_c_root=0 in each sampled row
```

So the correction must be a genuine unit/distribution/selected-anchor factor,
not just a Siegel multiplier phase.

## Check

```text
PYTHONPYCACHEPREFIX=/private/tmp/codex-pycache PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH=p24 python3 \
  p24/trace_gcd_fixed_frequency_jacobi_sum_row_ratio_miner.py
```

Observed:

```text
right_mixed_no_constant_row_ratio_rows=3/3
right_mixed_nonzero_right_constant_row_ratio_rows=3/3
right_mixed_non_cyclotomic_defect_rows=3/3
right_mixed_universal_anchor_defect_rows=3/3
right_mixed_anchor_defect_formula_rows=3/3
```

No p24 class-set enumeration is used.
