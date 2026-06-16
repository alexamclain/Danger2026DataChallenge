# Reduced Anchor Resultant-Avoidance Gate

Date: 2026-06-07

This note refines the local-unit criterion into the certificate form a future
CM/Lang producer can supply.

If the selected coordinate is represented in a finite etale algebra

```text
A = F_q[T] / (M(T))
x = X(T) mod M(T),
```

then the reduced-anchor forbidden-locus avoidance is exactly:

```text
gcd(M(T), X(T)^c - 1) = 1.
```

Equivalently:

```text
Res(M(T), X(T)^c - 1) != 0
```

or a Bezout identity:

```text
A(T) M(T) + B(T) (X(T)^c - 1) = 1.
```

This packages the earlier local statement

```text
R_c(x)=Phi_c(x)/(x-1)^(c-1) is a unit iff x notin mu_c
```

without requiring the verifier to enumerate or adjoin all `c`-th roots of
unity.

For p24:

```text
c = 179
forbidden polynomial degree = 179
kernel polynomial degree = 89
```

## Checks

Run:

```text
PYTHONPYCACHEPREFIX=/private/tmp/codex-pycache PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=p24 python3 p24/trace_gcd_fixed_frequency_reduced_anchor_resultant_avoidance_gate.py
```

Expected summary:

```text
scalar_resultant_criterion_rows=6/6
scalar_unit_count_rows=6/6
quotient_component_unit_rows=8/8
quotient_xc_minus_one_resultant_rows=8/8
quotient_bezout_rows=8/8
quotient_combined_criterion_rows=8/8
p24_c_degree=179
p24_forbidden_polynomial_degree=179
p24_kernel_polynomial_degree=89
R_c_unit_iff_X_power_c_minus_one_is_unit_in_selected_algebra=1
resultant_nonzero_equiv_forbidden_locus_avoidance=1
bezout_identity_equiv_resultant_unit_certificate=1
criterion_works_without_adjoining_all_c_roots_of_unity=1
p24_reduced_anchor_can_be_certified_by_one_resultant_or_bezout_punit=1
resultant_avoidance_is_finite_algebra_not_the_cm_lang_producer=1
```

Lean proof-contract scaffold:

```text
p24/lean/TraceGcdReducedAnchorResultantAvoidanceGate.lean
```

## Interpretation

This still does not construct the selected p24 CM/Lang coordinate.  It reduces
the post-producer p-unit check to one algebraic p-unit certificate:

```text
Res(M, X^179 - 1)
```

or an equivalent Bezout identity in the selected finite algebra.
