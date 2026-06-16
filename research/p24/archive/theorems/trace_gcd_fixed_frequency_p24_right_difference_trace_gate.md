# p24 Right-Difference Trace Gate

Date: 2026-06-07

## Point

The right-difference target can be restated as a small family of explicit
decomposition-field trace vanishings.

Let

```text
A_i(k) = sum_{r in H_i} j_{r+m*k}
```

where `H_i` is the `i`th right `H=<2^7>` coset.  For each adjacent right
coset difference, define the relative polynomial

```text
P_i(X) = sum_k (A_{i+1}(k)-A_i(k)) X^k.
```

The right-difference theorem

```text
sum_{k in D} (A_{i+1}(k)-A_i(k))
  = 388430 * (A_{i+1}(0)-A_i(0))
```

for every nonzero relative `<p>`-coset `D` is equivalent, by the Gaussian
period inversion already used in the period-coset gate, to

```text
Tr_{Q(zeta_n)/Q(zeta_n)^<p>}(P_i(zeta_n)) = 0
```

modulo the selected prime above `p`.

## p24 Counts

There are seven cyclic adjacent differences and eight relative `<p>`-cosets:

```text
7 * 8 = 56
```

redundant trace/balance equations.  Since the seven adjacent differences sum
to zero, the independent count is still

```text
6 * 8 = 48.
```

This is exactly the same compressed theorem target as the affine profile and
mixed-spectrum gates, but the arithmetic object is now explicit:

```text
the seven adjacent right-difference polynomials P_i.
```

## Why This Helps

The proof can now target a named degree-8 decomposition trace for each
adjacent right derivative, rather than all characters or all offsets.  This is
closer to a CM/Lang divisor or modular-unit identity:

```text
P_i(zeta_n) should have zero trace to Q(zeta_n)^<p>.
```

The cyclic dependency among the seven `P_i` is automatic, so it is enough to
prove six independent trace vanishings if the proof chooses a spanning set.

## Checked Gate

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_fixed_frequency_p24_right_difference_trace_gate.py
```

Key markers:

```text
toy_period_matrix_rank=8/8
right_difference_trace_equivalence_failures=0
random_right_difference_trace_zero=0/72
forced_right_difference_trace_zero=72/72
forced_right_difference_balanced=72/72
single_defect_trace_nonzero=72/72
single_defect_balance_false=72/72
p24_redundant_adjacent_trace_equations=56
p24_independent_adjacent_trace_equations=48
adjacent_right_difference_balance_iff_decomposition_trace_zero=1
right_difference_polynomials_are_the_new_trace_zero_targets=1
proof_target_is_explicit_degree8_trace_zero_for_each_adjacent_right_difference=1
```

## Updated Proof Target

Construct the seven adjacent right-difference polynomials

```text
P_i(X)=sum_k (A_{i+1}(k)-A_i(k))X^k
```

from the embedded trace-GCD weighted CM/Lang packet and prove

```text
Tr_{Q(zeta_n)/Q(zeta_n)^<p>}(P_i(zeta_n)) = 0
```

for `i=0,...,6`.  This implies the right-difference identity, recovers the
affine offsets by averaging, and gives the `48` compressed verifier equations.
