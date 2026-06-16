# Trace-GCD Low-Moment Function-Complexity Gate

Date: 2026-06-07

This note refines the low-moment relative-trace constructor target.

For a parent quotient period `Z_u` and child quotient periods `Y_{u+a v}`,
the first child power sum is tautological:

```text
P_1(u) = sum_v Y_{u+a v} = Z_u.
```

Thus the p24 low-moment count `4 + 26 = 30` includes two values already
carried by the selected parent chain.  The genuinely new higher-moment
producer target is:

```text
first layer:  P_2, P_3, P_4          = 3 new moments
second layer: P_2, ..., P_26         = 25 new moments
selected path total                  = 28 new moments
```

Script:

```text
p24/trace_gcd_low_moment_function_complexity_gate.py
```

Lean gate:

```text
p24/lean/TraceGcdLowMomentAutomaticP1Gate.lean
```

Run:

```text
PYTHONPYCACHEPREFIX=/private/tmp/codex-pycache PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=p24 python3 p24/trace_gcd_low_moment_function_complexity_gate.py

lean p24/lean/TraceGcdLowMomentAutomaticP1Gate.lean
```

Output summary:

```text
rows=125
p1_parent_identity_rows=25/25
nontrivial_moment_rows=100
nontrivial_parent_ge3_rows=40
nontrivial_full_interp_rows=100
nontrivial_low_interp_rows=60
nontrivial_parent_ge3_low_interp_rows=0
nontrivial_high_bm_rows=100
```

Interpretation:

```text
first_relative_trace_power_sum_is_the_parent_period=1
p24_low_moment_payload_has_two_automatic_P1_values=1
higher_relative_trace_moments_do_not_show_a_generic_low_degree_parent_formula=1
producer_must_construct_nontrivial_higher_moments_by_class_field_or_trace_formula=1
```

Important nuance: the `nontrivial_low_interp_rows=60` are exactly the
two-parent cases where every function is degree at most one by interpolation.
For parent count at least three, all tested higher moment functions have full
interpolation degree.  So the positive simplification is the automatic `P_1`,
not a cheap low-degree parent-period formula for `P_d, d >= 2`.

The companion entropy gate records why this automatic `P_1` still stays in
the verifier/anti-collision equations:

```text
p24/trace_gcd_low_moment_automatic_p1_entropy_gate.md
```

The companion truncated-polynomial gate records the equivalent class-field
shape of the producer target:

```text
p24/trace_gcd_low_moment_truncated_polynomial_gate.md
```
