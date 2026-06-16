# Reduced Anchor Cyclic Vs Diamond Norm Gate

Date: 2026-06-07

## Point

The reduced-anchor residual is produced by the diamond/unit norm of the
one-point divisor:

```text
[zeta_c] - [1].
```

The tempting cyclic `C/E` trace norm is the wrong operation.  It telescopes:

```text
sum_t ([zeta_c^(1+t)] - [zeta_c^t]) = 0
prod_t (X - zeta_c^(1+t))/(X - zeta_c^t) = 1.
```

By contrast, the diamond norm over nonzero multipliers gives:

```text
sum_{a in (Z/cZ)^*} ([zeta_c^a] - [1])
  = sum_{k != 0} [zeta_c^k] - (c - 1)[1]

prod_{a in (Z/cZ)^*} (X - zeta_c^a)/(X - 1)
  = Phi_c(X)/(X - 1)^(c - 1).
```

## p24 Consequence

For p24:

```text
c = 179
cyclic translation orbit size = 179
diamond orbit size = 178
```

Any implementation of the producer theorem that applies the ordinary cyclic
`C/E` trace/norm to the one-point factor loses the selected-anchor residual.
The tower identity must expose the diamond/unit action or an equivalent
finite-field identity.

## Check

```text
PYTHONPYCACHEPREFIX=/private/tmp/codex-pycache PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH=p24 python3 \
  p24/trace_gcd_fixed_frequency_reduced_anchor_cyclic_vs_diamond_norm_gate.py
```

Expected markers:

```text
cyclic_translation_trace_zero_rows=6/6
cyclic_product_telescopes_rows=6/6
diamond_norm_residual_rows=6/6
diamond_product_residual_rows=6/6
cyclic_translation_not_residual_rows=6/6
p24_cyclic_translation_orbit_size=179
p24_diamond_orbit_size=178
cyclic_C_over_E_translation_norm_of_one_point_factor_is_trivial=1
p24_producer_must_use_diamond_norm_not_cyclic_C_over_E_norm=1
```
