# Left-Descent Marginal Gate

Date: 2026-06-06

## Statement

For an uncentered Hermitian double marginal `M(a,b)`, the centered mixed block
is

```text
C(a,b) = M(a,b) - M(a,0) - M(0,b) + M(0,0),
a,b nonzero.
```

For a right H-coset `Q`, define the uncentered leakage

```text
D_Q(a) = sum_{b in Q} M(a,b) - |Q| M(a,0).
```

Then

```text
sum_{b in Q} C(a,b) = 0 for every nonzero a
```

if and only if

```text
D_Q(a) = D_Q(0) for every a.
```

So the p24 H-kernel theorem `C P_H = 0` is equivalently:

```text
each right H-period leakage descends to the left-constant component.
```

This is the base-field version of the paired-kernel equations `A(Pi_k L_0)=0`.

## Boundary

The pinned actual-CM Hermitian marginal

```text
D=-13319, q=13463, h=140, m=28=4*7, n=5
```

has two right H-cosets for `right=7`.  It reports:

```text
actual_centered_H_sum_zeroes=0/6
actual_left_descent_failures=6/6
```

Thus left descent of H-period leakage is not a generic Hermitian packet
property.  The p24 proof must establish it for the specific trace-GCD
weighted packet/section.

## Verification

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_fixed_frequency_left_descent_marginal_gate.py
```
