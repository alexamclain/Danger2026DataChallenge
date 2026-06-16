# p24 Right-Difference Affine Gate

Date: 2026-06-07

## Point

The affine quotient-profile theorem can be stated without characters and
without unknown offsets.

Recall the affine target:

```text
M_i(D) = 388430*b_i + gamma_D
```

for right `H=<2^7>` cosets `i` and nonzero relative `<p>`-cosets `D`.  Taking
the cyclic right difference removes `gamma_D`:

```text
M_{i+1}(D)-M_i(D) = 388430*(b_{i+1}-b_i).
```

Conversely, because `p` is prime to `7`, this right-difference identity
recovers the offsets by right averaging:

```text
gamma_D = (1/7) * sum_i (M_i(D)-388430*b_i).
```

So the current theorem target can be written as:

```text
The right derivative of every recombined relative quotient profile equals
388430 times the right derivative of the selected-child profile.
```

## p24 Counts

The redundant cyclic-difference formulation has

```text
7 right differences * 8 relative cosets = 56 equations.
```

The sum of the seven right differences is automatically zero, so the
independent count is still

```text
6 * 8 = 48.
```

This is the same `48`-equation target as the recombined balance and affine
profile gates.

## Why This Helps

The arithmetic proof no longer has to introduce the offsets first.  It can
instead construct the difference identity directly from a CM/Lang divisor,
modular-unit relation, or trace-GCD potential:

```text
Delta_right M(D) = 388430 * Delta_right b.
```

Once this is proved, the offsets are forced by the averaging formula above.
This is the most concrete finite target so far for an explicit embedded
potential.

## Checked Gate

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_fixed_frequency_p24_right_difference_gate.py
```

Key markers:

```text
right_difference_equivalence_failures=0
right_average_recovery_failures=0
random_right_difference_true=0/96
forced_affine_right_difference_true=96/96
forced_affine_right_average_reconstructs=96/96
column_sum_only_right_difference_false=96/96
row_defect_right_difference_false=96/96
p24_redundant_right_difference_equations=56
p24_independent_right_difference_equations=48
affine_profile_iff_right_difference_matches_selected_child=1
offsets_recovered_by_right_average_when_differences_match=1
arithmetic_target_can_be_stated_without_characters_or_offsets=1
```

## Updated Proof Target

For each relative `<p>`-coset `D`, prove in the actual trace-GCD weighted
packet:

```text
sum_{r in H_{i+1}} sum_{k in D} j_{r+m*k}
- sum_{r in H_i} sum_{k in D} j_{r+m*k}
=
388430 * (
  sum_{r in H_{i+1}} j_r
  - sum_{r in H_i} j_r
)
```

for the seven adjacent right quotient cosets `H_i`.  This is equivalent to
the `48` compressed verifier equations, but it is better shaped for a direct
CM/Lang potential proof.
