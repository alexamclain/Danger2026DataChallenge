# Fixed-Frequency p24 Complete Factor Descent Gate

Date: 2026-06-06

## Point

The p24 factor-cycle route needs a complete 70-factor statement, not a
representative-factor statement.

Let `Z_delta(chi)` be the contribution of the `delta`-th E-tensor factor to
the fixed-frequency packet product sum.  The theorem target separates into:

```text
Complete recombination:
  S_chi = sum_{delta=0}^{69} Z_delta(chi)
  is the original L-valued fixed-frequency projection.

Factor covariance:
  Z_{delta+10}(chi) = lambda_chi * rho(Z_delta(chi)),
  rho = p^780.
```

Because `rho` fixes `L=F_p(mu_157)`, complete recombination gives
`rho(S_chi)=S_chi`.  Factor covariance gives
`rho(S_chi)=lambda_chi^(-1)S_chi`.  For nontrivial `chi`, the intersection is
zero, so `S_chi=0`.

## Boundary

Covariance alone is not enough.  The finite gate generates random covariant
70-factor arrays and checks that their complete sums are usually nonzero and
not descended.  A single 7-cycle is also usually nonzero and not descended.

Thus the arithmetic theorem must prove covariance for the complete idempotent
factor decomposition of the original projection, not merely for a representative
factor or a post-fit cycle.

## Check

The gate is:

```text
p24/trace_gcd_fixed_frequency_p24_complete_factor_descent_gate.py
```

It verifies:

```text
tensor_factor_count_over_E=70
tensor_factor_degree_over_E=5549
rho_order_on_E=7
rho_factor_step_mod_70=10
rho_factor_cycle_count=10
rho_factor_cycle_lengths=[7, 7, 7, 7, 7, 7, 7, 7, 7, 7]
factor_covariance_failures=0
complete_covariant_sums_eigen_failures=0
constructed_zero_sum_covariance_failures=0
constructed_descended_zero_sum_nonzero_components=6/6
constructed_descended_zero_sum_verified=6/6
complete_70_factor_recombination_is_the_descent_input=1
factor_covariance_alone_does_not_descend=1
one_factor_cycle_is_not_a_valid_descended_certificate=1
descended_plus_covariant_complete_sum_forces_h_coset_zero=1
```

## Refined Missing Theorem

The remaining arithmetic target is now:

```text
For each nontrivial order-7 chi, construct the complete 70-factor idempotent
decomposition of S_chi in the embedded CM/Lang tower and prove
Z_{delta+10}(chi)=lambda_chi*rho(Z_delta(chi)).
```

The descent is then formal because the complete recombination is the original
`L`-valued fixed-frequency projection.
