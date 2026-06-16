# Actual-CM Internal Character Boundary

This boundary checks whether the new internal-character target is automatic
for ordinary embedded CM period data.  It is not.

The toy has the p24-shaped tower split:

```text
D = -5000
h = 30 = 2 * 5 * 3
top quotient = 2
C/E analogue = 5
B/C analogue = 3
q = 3851
```

For each origin and each top packet, the script forms the `B/C` trace of the
raw embedded `j` cycle, then projects the resulting 5-vector to C-characters.
Across all 60 origin/top rows:

```text
trivial_C_projection_zeroes=0/60
all_nontrivial_C_projections_nonzero=60/60
```

So the p24 theorem cannot be:

```text
ordinary CM period packets have zero trivial internal C/E component.
```

The theorem must instead use the special right-obstruction/product-coboundary
structure before the internal character projection.

Harness markers:

```text
ordinary_cm_periods_do_not_satisfy_internal_character_filter=1
internal_filter_needs_specific_obstruction_not_raw_j_cycle=1
small_cm_cycle_has_full_C_character_support=1
conclusion=reported_trace_gcd_fixed_frequency_actual_cm_internal_character_boundary
```
