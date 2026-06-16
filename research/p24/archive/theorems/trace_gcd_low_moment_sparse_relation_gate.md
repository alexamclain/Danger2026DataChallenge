# Trace-GCD Low-Moment Sparse-Relation Gate

Date: 2026-06-07

This note sharpens the low-moment selector hypothesis into a coding/additive
combinatorics statement.

For child candidates `S,T` of the same size, equality of the first `k` power
sums

```text
sum_{x in S} x^d = sum_{x in T} x^d,  1 <= d <= k
```

is equivalent, after canceling `S cap T`, to a disjoint signed relation on
the moment curve:

```text
sum_{a in A} (a,a^2,...,a^k) =
sum_{b in B} (b,b^2,...,b^k),
|A| = |B|.
```

Newton identities give the deterministic boundary: if the reduced collision
has size `s=|A|=|B|` and `k >= s`, then the first `s` power sums force the same
elementary symmetric functions, hence `A=B` as multisets.  Therefore every
nontrivial reduced collision must have `s > k`.

Script:

```text
p24/trace_gcd_low_moment_sparse_relation_gate.py
```

Run:

```text
PYTHONPYCACHEPREFIX=/private/tmp/codex-pycache PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=p24 python3 p24/trace_gcd_low_moment_sparse_relation_gate.py
```

Output markers:

```text
random_control=F_101_20_choose_10
  degree=1 matches=1820 min_reduced_collision_size=2
  degree=2 matches=20   min_reduced_collision_size=3
  degree=3 matches=1

actual_cm_collision_profiles:
  D=-200:  degree 1 has a reduced collision of size 2; degree 2 isolates
  D=-239:  degree 1 has reduced collisions of size at least 2; degree 2 isolates
  D=-5000: degree 1 has reduced collisions of size at least 3; degree 2 isolates

p24_sparse_relation_entropy:
  first_layer_target_collision_log10=-2.823452
  first_layer_union_over_two_parents_log10=-2.522422
  second_layer_target_collision_log10=-7.218491
  second_layer_union_over_314_parents_log10=-4.721562
```

Interpretation:

```text
equal_moment_subsets_are_sparse_signed_moment_curve_relations=1
canceling_overlap_reduces_to_disjoint_equal_size_relations=1
newton_identities_forbid_reduced_collisions_of_size_at_most_k=1
observed_nontrivial_collisions_respect_the_newton_boundary=1
p24_low_moment_theorem_is_cm_sparse_relation_avoidance=1
p24_union_entropy_still_favors_4_plus_26_moments=1
```

The theorem target is now:

```text
For the p24 embedded CM quotient-root sets, the moment curve has no disjoint
equal-cardinality signed relations of sizes:

  first layer:  5 <= s <= 157, using k=4 moments;
  second layer: 27 <= s <= 211, using k=26 moments.
```

This does not construct the moments.  It cleanly separates the two remaining
inputs:

```text
1. intrinsic relative-trace construction of the selected low moments;
2. CM sparse-relation avoidance / anti-collision for the moment curve image.
```
