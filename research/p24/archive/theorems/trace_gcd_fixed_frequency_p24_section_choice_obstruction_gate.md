# p24 Section-Choice Obstruction Gate

Date: 2026-06-06

## Point

The trace-average anchor surface is:

```text
D_r = Tr_relative(j_{r+m*bullet}) - n*j_r.
```

A tempting compression is to keep only the quotient trace profile

```text
T_r = Tr_relative(j_{r+m*bullet})
```

and hope the anchor equations are independent of which relative child is
selected.  This is false.  The selected child profile is arithmetic data, not
bookkeeping.

## Finite Counterexample

The gate constructs two child-section choices with the same quotient trace
profile.  Child `0` has zero defect and passes the H-coset anchor check; child
`1` has the same trace profile but fails.

Thus:

```text
quotient trace profile alone
  does not determine
trace-defect H-coset sums.
```

For p24 this means the `m=66254` trace-only profile is not an authenticated
anchor payload.  The known explicit sub-sqrt surface remains the
section-aware profile:

```text
T_r = Tr_relative(j_{r+m*bullet})
S_r = j_r
payload = 2*m = 132508.
```

## Actual-CM Check

On the pinned actual-CM right-combo analogue

```text
D=-13319, q=13463, m=28, n=5,
```

globally shifting the chosen child changes the anchor defect.  None of the
five global child shifts satisfies the generic anchor equation, and the five
defects are all distinct.

This reinforces the theorem target: the p24 proof must construct an embedded
section, or an equivalent section-aware defect payload.  Unordered relative
trace coefficients do not authenticate the defect.

## Checked Gate

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_fixed_frequency_p24_section_choice_obstruction_gate.py
```

Key markers:

```text
same_trace_profile_counterexample=1
same_trace_child0_anchor_passes=1
same_trace_child1_anchor_passes=0
random_child_shift_changes_defect_sums=48/48
actual_cm_global_child_shift_anchor_zeroes=0/5
actual_cm_global_child_shift_distinct_defects=5/5
actual_cm_distinct_child_coefficients=5/5
p24_trace_only_profile_payload=66254
p24_trace_plus_child_profile_payload=132508
p24_trace_plus_child_profile_payload_over_sqrt=1.325080000000e-07
quotient_trace_profile_alone_does_not_determine_anchor=1
selected_child_section_is_arithmetic_data_not_bookkeeping=1
unordered_relative_trace_coefficients_do_not_authenticate_defect=1
p24_anchor_producer_must_be_section_aware=1
```
