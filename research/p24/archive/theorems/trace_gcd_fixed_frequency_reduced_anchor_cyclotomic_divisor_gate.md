# Reduced Anchor Cyclotomic Divisor Gate

Date: 2026-06-07

## Point

The C-slice gate split the reduced anchor into:

```text
h = h_triv + h_nontriv
```

with:

```text
h_nontriv(0,0)=-(c-1)/c
h_nontriv(0,k)=1/c for k != 0
h_nontriv(r,k)=0 for r != 0.
```

Multiplying by `c` clears the denominator:

```text
c*h_nontriv = sum_{k != 0} [zeta_c^k] - (c-1)[1].
```

For prime `c`, this is the divisor of:

```text
R_c(X) = Phi_c(X) / (X - 1)^(c - 1).
```

So the `C/E`-nontrivial residual is a concrete principal divisor after
clearing the factor `c`, not an arbitrary `7*(c-1)`-channel condition.

## p24 Consequence

For p24:

```text
c = 179
R_179(X) = Phi_179(X) / (X - 1)^178
nonzero C/E-nontrivial Fourier channels = 7*(179-1)=1246
```

The remaining arithmetic theorem is now sharper:

```text
show that the selected trace-GCD/CM-Lang degenerate anchor specializes to the
appropriate p-integral analogue of R_179, and that it matches both the b=0
row-sum slice and the C/E-nontrivial residual against the raw
Hasse-Davenport packet.
```

This gate does not prove that CM/Lang specialization.  It only proves the
finite divisor identity that the specialization should realize.

## Check

```text
PYTHONPYCACHEPREFIX=/private/tmp/codex-pycache PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH=p24 python3 \
  p24/trace_gcd_fixed_frequency_reduced_anchor_cyclotomic_divisor_gate.py
```

Expected markers:

```text
integral_residual_matches_cyclotomic_divisor_rows=6/6
cyclotomic_residual_degree_zero_rows=6/6
cyclotomic_residual_spatial_formula_rows=6/6
cyclotomic_residual_fourier_profile_rows=6/6
principal_cyclotomic_divisor_profile_rows=6/6
cyclotomic_residual_channel_count_rows=6/6
p24_cyclotomic_residual_divisor_degree_zero=1
p24_residual_integral_fourier_channels=1246
c_nontrivial_residual_is_cyclotomic_principal_divisor_after_clearing_c=1
p24_candidate_unit_is_R_179_equals_Phi_179_over_X_minus_1_power_178=1
p24_remaining_arithmetic_is_cm_lang_specialization_and_p_integrality=1
```
