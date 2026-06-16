# Reduced Anchor Kernel Polynomial Gate

Date: 2026-06-07

## Point

The elliptic subgroup divisor has an explicit principal function.  For an odd
cyclic subgroup `H=<P>` of order `c`, define

```text
K_H(x) = prod_{Q in (H \ {O})/{+-1}} (x - x(Q)).
```

Since `x-x(Q)` has zeros at `Q` and `-Q` and a double pole at `O`,

```text
div(K_H) = sum_{Q in H, Q != O} [Q] - (c - 1)[O].
```

Thus `K_H` is the exact subgroup/diamond residual function.  The square
`K_H^2` is the denominator shape in the `x`-coordinate of Vélu-style isogeny
formulas; the unsquared kernel polynomial is the reduced-anchor target.

## p24 Consequence

For p24:

```text
c = 179
deg K_H = 89
pole order of K_H at O = 178
```

The live producer target can now be stated concretely:

```text
construct the selected CM/Lang specialization of the kernel polynomial
for the 179-subgroup/divisor, p-integrally and without class enumeration.
```

The companion final-curve guardrail shows this is not an `F_p`-rational
`179`-isogeny on the final selected curve: `179` does not divide `#E(F_p)`,
and `t^2-4p` is nonsquare modulo `179`.  The `K_H` object must therefore live
in the auxiliary CM/Lang or cyclotomic layer.

This still does not prove the producer.  It replaces the abstract subgroup
unit with a concrete kernel-polynomial object and separates it from the
squared Vélu denominator and the c-th-power Miller overshoot.

## Check

```text
PYTHONPYCACHEPREFIX=/private/tmp/codex-pycache PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH=p24 python3 \
  p24/trace_gcd_fixed_frequency_reduced_anchor_kernel_polynomial_gate.py
```

Expected markers:

```text
actual_kernel_root_pair_rows=6/6
actual_kernel_paired_x_rows=6/6
actual_kernel_subgroup_sum_zero_rows=6/6
formal_kernel_degree_rows=6/6
formal_kernel_pole_order_rows=6/6
p24_kernel_polynomial_degree=89
p24_kernel_divisor_pole_order=178
kernel_polynomial_has_exact_subgroup_residual_divisor=1
p24_target_can_be_kernel_polynomial_for_selected_179_subgroup=1
```
