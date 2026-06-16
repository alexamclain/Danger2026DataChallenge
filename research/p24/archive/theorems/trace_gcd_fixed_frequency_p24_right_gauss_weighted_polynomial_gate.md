# Right Gauss Weighted Polynomial Gate

This gate makes the current right obstruction explicit.

For the right factor

```text
R_{chi,-a} = sum_v chi(v) T_{0,v,-a},
```

write the class index as

```text
i = r + m*k,       0 <= r < m,      m = 2*157*211.
```

Because `211 | m`, the additive right character sees only `r mod 211`.
The finite Gauss-sum identity gives

```text
sum_v chi(v) zeta_211^(v*r)
  = tau(chi) * chi^{-1}(r)     if r != 0 mod 211,
  = 0                          if r == 0 mod 211.
```

So after dividing by the nonzero Gauss sum, the obstruction is the weighted
relative polynomial

```text
G_chi(X) = sum_r w_chi(r) F_r(X),
w_chi(r) = chi^{-1}(r mod 211),
F_r(X) = sum_k j_{r+m*k} X^k.
```

The current theorem target is therefore:

```text
Tr_{C/E}(Tr_{B/C}(G_chi(zeta_n^a))) = 0
```

for the six nontrivial order-7 right quotient characters.  In the internal
character language, this says the `B/C` trace of this **specific weighted CM
polynomial** has no trivial `C/E` component.

The gate also records the boundary:

```text
random_weighted_polynomial_internal_trace_nonzero=12/12
```

so the Gauss-sum reduction itself does not prove the internal trace identity.
It only names the exact polynomial to which the missing CM/Lang theorem must
apply.

Harness markers:

```text
right_obstruction_is_gauss_sum_times_weighted_relative_polynomial=1
weights_are_inverse_right_order7_character_on_nonzero_residues=1
residue_0_mod_211_drops_out_by_character_orthogonality=1
weighted_polynomial_internal_trace_zero_is_not_formal=1
remaining_theorem_is_internal_trace_zero_for_this_weighted_cm_polynomial=1
conclusion=reported_trace_gcd_fixed_frequency_p24_right_gauss_weighted_polynomial_gate
```
