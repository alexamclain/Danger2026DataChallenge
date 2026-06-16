# Reduced Anchor Elliptic Subgroup Divisor Gate

Date: 2026-06-07

## Point

The diamond residual can be read in two different ways.

On a cyclotomic or `P^1` coordinate, the one-point divisor
`[zeta_c]-[1]` is principal.  On an elliptic curve, the analogous divisor
`[P]-[O]` is not principal for nonzero torsion `P`; its Abel-Jacobi sum is
`P`.

The correct elliptic-unit target is the whole subgroup divisor:

```text
D_H = sum_{Q in H, Q != O} [Q] - (c - 1)[O].
```

For odd `c`, the nonzero subgroup sum is zero, so `D_H` has degree zero and
Abel-Jacobi sum zero.  It is principal by the genus-one divisor criterion.

The Miller divisor `c[P]-c[O]` is also principal, but diamond-norming those
individual Miller divisors gives `c*D_H`, i.e. `R_c^c`.  That is a c-th-power
overshoot if the target is `R_c`.

## p24 Consequence

For p24:

```text
c = 179
deg(D_H positive part) = 178
sum_{a=1}^{178} a = 0 mod 179
```

So the live producer theorem should be phrased as:

```text
construct the p-integral CM/Lang specialization of the whole
179-subgroup/diamond divisor D_H,
```

or equivalently work on a descended cyclotomic coordinate where the one-point
factor is principal.  Do not require an elliptic unit with divisor
`[P]-[O]`; that object does not exist.

## Check

```text
PYTHONPYCACHEPREFIX=/private/tmp/codex-pycache PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH=p24 python3 \
  p24/trace_gcd_fixed_frequency_reduced_anchor_elliptic_subgroup_divisor_gate.py
```

Expected markers:

```text
single_point_elliptic_nonprincipal_rows=6/6
miller_c_power_principal_rows=6/6
nonzero_subgroup_sum_zero_rows=6/6
diamond_subgroup_residual_principal_rows=6/6
diamond_subgroup_matches_cyclotomic_residual_rows=6/6
miller_diamond_is_c_times_residual_rows=6/6
direct_subgroup_divisor_target_rows=6/6
p24_subgroup_order=179
p24_nonzero_subgroup_divisor_degree=178
p24_target_can_be_direct_diamond_subgroup_divisor_not_single_point_factor=1
```
