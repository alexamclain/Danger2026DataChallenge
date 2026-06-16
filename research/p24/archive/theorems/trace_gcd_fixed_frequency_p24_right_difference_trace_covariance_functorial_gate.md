# p24 Right-Difference Trace Covariance Functorial Gate

Date: 2026-06-07

## Point

The covariance input in the covariance-telescope gate is formal once the
adjacent difference polynomials have the right Frobenius functoriality.

Let

```text
T_i = Tr_{Q(zeta_n)/Q(zeta_n)^<p>}(P_i(zeta_n)).
```

If, for `rho=p^780`, the evaluated adjacent polynomials satisfy

```text
P_{i+6}(zeta_n^(rho*a)) = rho(P_i(zeta_n^a)),
```

and `rho mod n` lies in the trace subgroup `<p>`, then the trace cosets are
not permuted and

```text
T_{i+6} = rho(T_i).
```

So the covariance half of the current target reduces to pointwise
CM/Lang-Frobenius functoriality of the seven `P_i`.

## Guardrail

The multiplier being inside the trace subgroup matters.  If the relative
multiplier is outside the trace subgroup, pointwise covariance still gives a
trace covariance, but with the eight decomposition-field coordinates permuted.
That is not the same same-coset covariance needed by the telescope gate.

For p24, `rho=p^780` is in `<p>` by definition, so the finite obstruction is
not subgroup membership.  The remaining arithmetic work is to prove the
pointwise semilinear covariance for the actual embedded `P_i` packet.

## Checked Gate

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_fixed_frequency_p24_right_difference_trace_covariance_functorial_gate.py
```

Key markers:

```text
inside_point_covariance_failures=0
inside_same_coset_trace_covariance_failures=0
random_same_coset_trace_covariant=0/64
outside_one_step_same_coset_trace_fails=64/64
outside_one_step_permuted_trace_covariance_failures=0
pointwise_semilinear_covariance_with_multiplier_inside_trace_subgroup_implies_trace_covariance=1
multiplier_inside_trace_subgroup_keeps_decomposition_trace_cosets_fixed=1
multiplier_outside_trace_subgroup_only_gives_permuted_coset_covariance=1
remaining_covariance_theorem_is_pointwise_cm_lang_frobenius_functoriality_for_P_i=1
```

## Updated Proof Target

The `48` compressed equations now follow from:

```text
1. pointwise semilinear covariance:
   P_{i+6}(zeta_n^(rho*a)) = rho(P_i(zeta_n^a));

2. one anchor descent:
   rho(T_0)=T_0.
```

The first input should be attacked as Frobenius functoriality of the embedded
CM/Lang construction of the adjacent right-difference packet.  The second is
now the only non-formal descent input left in this branch.
