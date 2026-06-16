# Trace-GCD Low-Moment Automatic-P1 Entropy Gate

Date: 2026-06-07

The first moment on each low-moment selector layer is automatic:

```text
P_1(parent) = sum(children) = parent period.
```

This means `P_1` is not a new producer value.  But it is still a selector
constraint: candidate child subsets must have the correct sum.  This gate
compares full moments `P_1..P_k` with higher-only moments `P_2..P_k`.

Script:

```text
p24/trace_gcd_low_moment_automatic_p1_entropy_gate.py
```

Run:

```text
PYTHONPYCACHEPREFIX=/private/tmp/codex-pycache PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=p24 python3 p24/trace_gcd_low_moment_automatic_p1_entropy_gate.py
```

Output summary:

```text
random_control=F_101_20_choose_10:
  p1_only=1820
  higher_only=17
  full_with_p1=1

actual_cm_controls:
  D=-200:   p1_only=2,  higher_only=2, full_with_p1=1
  D=-239:   p1_only=13, higher_only=4, full_with_p1=1
  D=-5000:  p1_only=2,  higher_only=4, full_with_p1=1
```

p24 entropy:

```text
first_layer_higher_only_target_collision_log10=21.176548
first_layer_with_parent_p1_target_collision_log10=-2.823452
second_layer_higher_only_target_collision_log10=16.781509
second_layer_with_parent_p1_target_collision_log10=-7.218491
```

Interpretation:

```text
automatic_P1_is_not_a_new_producer_value=1
automatic_P1_remains_a_selector_constraint=1
p24_higher_only_entropy_is_not_enough_for_random_unique_selection=1
p24_full_selector_still_uses_30_constraints_but_only_28_new_values=1
```

Thus the current target should be described carefully:

```text
verifier / anti-collision constraints: 30 selected low moments
new producer values:                   28 higher moments
already carried values:                 2 parent/P1 values
```
