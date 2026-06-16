# Trace-GCD Low-Moment Relative-Trace Gate

Date: 2026-06-07

This note identifies the intrinsic construction target behind the low-moment
selector route.

If `Y` is the fine quotient-period element over a parent quotient layer, then
the power sums of the child fiber above a parent are exactly relative traces:

```text
P_d(parent) = sum_{child y above parent} y^d
            = Tr(Y^d) from fine quotient to parent quotient.
```

Thus the low moments are not arbitrary subset hashes.  They are class-field
relative traces of powers.

Script:

```text
p24/trace_gcd_low_moment_relative_trace_gate.py
```

Run:

```text
PYTHONPYCACHEPREFIX=/private/tmp/codex-pycache PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=p24 python3 p24/trace_gcd_low_moment_relative_trace_gate.py
```

Toy result for `D=-5000`, `q=1259`, tower `2 <- 6`:

```text
full_newton_recovery_rows=2/2
degree_one_low_moment_unique_rows=2/2
moment_parent_interpolation_rows=3/3
```

Meaning:

```text
child_power_sums_are_relative_traces_of_quotient_period_powers=1
all_relative_degree_many_traces_recover_child_polynomial_by_newton=1
low_traces_plus_sparse_relation_avoidance_can_replace_full_child_polynomial=1
moment_values_are_parent_field_elements_not_postfit_subset_labels=1
```

For p24 the corresponding low-moment constructor target is:

```text
first layer:  Tr(Y^d),  d=1..4
second layer: Tr(W^d),  d=1..26
selected path total: 30 selected relative-trace values
```

The first moment on each layer is automatic once the selected parent root is
known:

```text
P_1(parent) = sum(children) = parent period.
```

Thus the genuinely new p24 target is `28` higher relative-trace values:

```text
first layer:  P_2, P_3, P_4   = 3
second layer: P_2..P_26       = 25
```

This refinement is checked in:

```text
p24/trace_gcd_low_moment_function_complexity_gate.md
p24/trace_gcd_low_moment_automatic_p1_entropy_gate.md
p24/trace_gcd_low_moment_truncated_polynomial_gate.md
p24/lean/TraceGcdLowMomentAutomaticP1Gate.lean
p24/lean/TraceGcdLowMomentTruncatedPolynomialGate.lean
```

If one constructs the moment functions over the parent fields instead of only
their selected evaluations, the coefficient surface is still small:

```text
2 * 4 + 314 * 26 = 8172 parent-field coefficients.
```

This is not yet the p24 certificate.  It cleanly splits the remaining theorem
into:

```text
1. construct these selected relative traces intrinsically, without class
   enumeration;
2. prove the sparse signed moment-curve anti-collision theorem for the p24
   embedded quotient-root sets;
3. feed the selected child/section into the reduced-anchor subgroup-kernel
   producer.
```
