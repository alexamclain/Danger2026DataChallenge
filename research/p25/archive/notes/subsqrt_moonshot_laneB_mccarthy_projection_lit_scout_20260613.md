# P25 Lane B: McCarthy Projection Literature Scout

Updated: 2026-06-13 13:45 PDT

## Verdict

No credible theorem-level route was found that legitimizes forming the dense
McCarthy quotient `R(q)=LHS(q)/main_sum(q)` and then applying the post-hoc
projection `R(q)^2029`.  The route remains valuable as a diagnostic and finite
payload recipe, but not as a certificate producer unless a new identity cancels
the auxiliary `mu_2029` component before projection.

## Inspected

Local artifacts:

- `subsqrt_moonshot_laneB_square_axis_mccarthy_multiplicative_route_falsifier.md`
- `subsqrt_moonshot_laneB_square_axis_mccarthy_aux_prime_invariance.md`
- `subsqrt_moonshot_laneB_square_axis_mccarthy_theorem_factor_normalization.md`
- `subsqrt_moonshot_laneB_gk_hd_projection_legitimacy_scout.md`

Primary/near-primary sources checked by the scout:

- McCarthy, finite-field well-poised hypergeometric transformations:
  https://www.math.ttu.edu/~mccarthy/publications/Hyp%20Trans.pdf
- Greene, hypergeometric functions over finite fields:
  https://doi.org/10.1090/S0002-9947-1987-0879564-8
- Gross-Koblitz:
  https://annals.math.princeton.edu/1979/109-3/p06
- Hasse-Davenport:
  https://eudml.org/doc/149908

## Assessment

McCarthy Theorem 1.7 is still the real positive hook: with the existing p25
parameters its exceptional delta fires exactly at `q=138`, and the local
finite check gives `support(LHS-main)=(138,)` with stable difference value
`2028`.

The obstruction is that the theorem supplies an additive/transformed-difference
identity.  Since `main(q)` is nonzero everywhere, the quotient `R=LHS/main` is
algebraically available and `R-1` is singleton-supported, but the inspected
Greene/McCarthy/Gross-Koblitz/Hasse-Davenport identities do not authorize
erasing the extra value-field `mu_2029` component afterward by `x -> x^2029`.

Auxiliary-prime invariance remains the decisive falsifier:

```text
ell=20574061:  ord(R(138)^2029)=39
ell=82296241:  ord(R(138)^2029)=5070
ell=144018421: ord(R(138)^2029)=23660
```

The theorem delta persists across these fields; the projection does not.  The
normalization scan also found no repair by visible denominators, prefactors,
`main`, `lhs`, or small Gauss monomials.

## Recommendation

Kill the powered McCarthy quotient as a certificate route for now; keep it as a
diagnostic.  Continue only if a candidate supplies one of:

- a balanced Gauss/Jacobi quotient with uniform auxiliary-prime cancellation;
- a genuine arithmetic object naturally living modulo the extra `mu_2029`
  roots;
- a direct endpoint identity producing `U=R^2029` or `e_138` without post-hoc
  projection.
