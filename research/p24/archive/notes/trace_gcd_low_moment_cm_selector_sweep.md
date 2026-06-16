# Trace-GCD Low-Moment CM Selector Sweep

Date: 2026-06-07

This is the first concrete testing lane for the low-moment selector hypothesis.
It does not search for a p24 triple directly.  Instead, it asks whether actual
small embedded CM towers behave as if a few power sums can identify the
selected child fiber among all unordered child subsets.

Script:

```text
p24/trace_gcd_low_moment_cm_selector_sweep.py
```

Focused default run:

```text
PYTHONPYCACHEPREFIX=/private/tmp/codex-pycache PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=p24 python3 p24/trace_gcd_low_moment_cm_selector_sweep.py
```

Default result:

```text
rows=19
rows_all_unique_within_degree_bound=19
rows_unique_at_degree_one=14
rows_unique_no_later_than_random_entropy=16
```

Wider run:

```text
PYTHONPYCACHEPREFIX=/private/tmp/codex-pycache PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=p24 python3 p24/trace_gcd_low_moment_cm_selector_sweep.py \
  --max-cases 24 --max-h 120 --max-child-count 22 \
  --max-combinations 1000000 --max-refinements-per-case 10 --max-degree 6
```

Wider result:

```text
rows=65
rows_all_unique_within_degree_bound=65
rows_unique_at_degree_one=43
rows_unique_no_later_than_random_entropy=52
```

Interpretation:

```text
actual_cm_towers_can_be_tested_for_low_moment_child_selection=1
low_moment_collision_behavior_is_a_theorem_microscope_not_a_certificate=1
intrinsic_moment_construction_and_cm_anti_collision_remain_required=1
```

For p24, entropy predicts:

```text
first layer:  binomial(314,157),  4 random-like F_p moments
second layer: binomial(66254,211), 26 random-like F_p moments
total:        30 moment constraints
```

This is encouraging evidence for the low-moment theorem candidate, not a
replacement for the missing producer.  The proof still needs:

```text
1. intrinsic construction of the selected moments without class enumeration;
2. a CM anti-collision theorem showing those moments select the true child;
3. compatibility with the reduced-anchor / selected subgroup kernel producer.
```
