# Actual-CM Right-Combo Anchor Section Scan

Date: 2026-06-07

## Point

The pinned right-combo anchor boundary checked one origin in the small
actual-CM analogue:

```text
D = -13319
q = 13463
h = 140
m = 28 = 4 * 7
n = 5
```

For this row the recombined relative quotient has one nonzero coset, so the
full recombined balance is exactly the anchor equation:

```text
sum_{k != 0} c_k = (n - 1) * c_0.
```

This scan rotates the embedded CM cycle through all `140` global
origin/section choices and recomputes the actual right-combo `G_chi`
analogue.

## Result

```text
origin_sections_checked=140
anchor_zero_sections=0/140
anchor_nonzero_sections=140/140
distinct_anchor_defects=140
```

Thus the generic right-combo anchor identity is not rescued by choosing a
better embedded section in this actual-CM row.

## Consequence

The p24 proof still needs something more specific than:

```text
actual CM right-combo packet
+ selected origin/section choice
```

The remaining theorem must use the p24-specific weighted `G_chi` structure,
the `211`-axis H-coset equality after internal trace, or an explicit
CM/Lang potential.

## Checked Gate

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_fixed_frequency_actual_cm_right_combo_anchor_section_scan.py
```

Key markers:

```text
anchor_zero_sections=0/140
anchor_nonzero_sections=140/140
actual_cm_right_combo_anchor_not_rescued_by_origin_section=1
selected_section_choice_alone_does_not_prove_anchor_balance=1
p24_anchor_still_needs_specific_weighted_G_chi_or_explicit_potential=1
conclusion=reported_trace_gcd_fixed_frequency_actual_cm_right_combo_anchor_section_scan
```
