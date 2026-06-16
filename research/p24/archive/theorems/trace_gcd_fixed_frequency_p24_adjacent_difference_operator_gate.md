# p24 Adjacent-Difference Operator Gate

Date: 2026-06-07

## Point

The adjacent anchor is not a new independent arithmetic target.  Under the
p24 covariance convention,

```text
Y_{i+6} = rho(Y_i),
```

and since `6=-1 mod 7`,

```text
Y_1 = rho^6(Y_0).
```

Therefore

```text
T_0 = Y_1 - Y_0 = (rho^6 - 1)Y_0.
```

On the nontrivial order-7 rho-projector channel `k`, the operator
`rho^6-1` multiplies by

```text
omega^(6k)-1,
```

which is nonzero for `k=1,...,6`.  Thus the finite-difference operator is
invertible on the nonfixed quotient.  The adjacent-anchor descent theorem is
equivalent to the older right-axis theorem that the selected internally traced
H-coset profile has equal H-coset sums.

## Checked Gate

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_fixed_frequency_p24_adjacent_difference_operator_gate.py
```

Key markers:

```text
derivative_operator=rho^6_minus_1
derivative_rank=6
derivative_kernel_dim=1
telescope_failures=0
derivative_projector_factor_failures=0
nontrivial_projector_equivalence_failures=0
right_axis_anchor_iff_adjacent_anchor_failures=0
equal_profile_iff_zero_adjacent_differences_failures=0
adjacent_anchor_is_invertible_difference_on_nonfixed_quotient=1
adjacent_anchor_descent_equivalent_to_right_axis_anchor_descent=1
remaining_arithmetic_is_same_equal_H_coset_sum_theorem_for_selected_packet=1
```

## Consequence

The proof frontier is now cleaner:

```text
Prove that the selected trace-GCD weighted/section-aware internally traced
right H-coset profile has no nontrivial order-7 rho-projector component.
```

The adjacent-trace formulation, right-axis H-coset equality formulation, and
six projector formulation are the same finite target after covariance.
