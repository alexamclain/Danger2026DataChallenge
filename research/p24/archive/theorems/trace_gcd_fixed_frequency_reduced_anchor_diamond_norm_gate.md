# Reduced Anchor Diamond Norm Gate

Date: 2026-06-07

## Point

The cyclotomic-divisor gate identified the denominator-cleared residual as:

```text
D_c = sum_{k != 0} [zeta_c^k] - (c - 1)[1].
```

This gate sharpens the producer shape.  For prime `c`, `D_c` is the
diamond/unit norm over the nonzero multipliers of `C_c` of the single divisor:

```text
[zeta_c] - [1].
```

Equivalently:

```text
prod_{a in (Z/cZ)^*} (X - zeta_c^a)/(X - 1)
  = Phi_c(X)/(X - 1)^(c - 1).
```

This is a norm over the diamond automorphism orbit of the `C_c` coordinate,
not the cyclic `C/E` trace norm.

## p24 Consequence

For p24:

```text
c = 179
diamond norm orbit size = 178
residual Fourier channels = 7*(179-1)=1246
```

The live arithmetic producer target is now:

```text
construct one p-integral selected CM/Lang factor realizing [zeta_179]-[1],
take its diamond norm over (Z/179Z)^*,
then apply the auxiliary Kummer/sign descent to match the selected anchor.
```

This is narrower than "construct the whole residual unit" and avoids confusing
the diamond norm with the cyclic `C/E` trace norm.

## Check

```text
PYTHONPYCACHEPREFIX=/private/tmp/codex-pycache PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH=p24 python3 \
  p24/trace_gcd_fixed_frequency_reduced_anchor_diamond_norm_gate.py
```

Expected markers:

```text
diamond_norm_divisor_rows=6/6
diamond_norm_polynomial_rows=6/6
diamond_norm_fourier_profile_rows=6/6
diamond_norm_orbit_size_rows=6/6
p24_diamond_norm_orbit_size=178
p24_diamond_norm_residual_fourier_channels=1246
R_c_residual_is_diamond_norm_of_single_point_divisor=1
this_is_diamond_norm_not_cyclic_C_over_E_trace_norm=1
p24_candidate_is_diamond_norm_of_one_p_integral_cm_lang_factor=1
```
