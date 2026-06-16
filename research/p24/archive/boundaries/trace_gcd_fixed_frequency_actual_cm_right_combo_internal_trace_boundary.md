# Actual-CM Right-Combo Internal Trace Boundary

This boundary checks whether the right-combo obstruction shape alone forces
internal trace zero.  It does not.

The pinned actual-CM analogue is:

```text
D = -13319
q = 13463
m = 28 = 4*7
n = 5
```

For this row, the E-relative Frobenius generator on the `n` layer has order
`2`, giving two internal trace orbits:

```text
[1, 4], [2, 3]
```

Both actual right-combo traces are nonzero:

```text
right_combo_internal_trace_zeroes=0/2
right_combo_terms_all_nonzero=2/2
```

So the p24 theorem cannot be stated as a generic "right combo has zero
internal trace" principle.  It must use the specific p24 `211`-axis H-coset
equality after internally tracing the Gauss-reduced `G_chi` profile.

Harness markers:

```text
actual_cm_right_combo_internal_trace_zeroes_are_not_generic=1
p24_needs_specific_211_axis_H_coset_equality_after_internal_trace=1
right_combo_shape_alone_does_not_prove_trace_zero=1
conclusion=reported_trace_gcd_fixed_frequency_actual_cm_right_combo_internal_trace_boundary
```
