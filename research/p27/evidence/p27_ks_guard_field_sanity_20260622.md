# P27 K/S Guard-Field Sanity

Date: 2026-06-22

## Claim

The K/S branch-extraction equations and H90/order-4 identities have now been
validated in the actual p27-signature guard fields q1607/q1847/q2087.

This is not the branch/genus extraction itself.  It is the cheap prerequisite
that says the offline CAS normalization should use the same equations over
these fields.

## Artifact

Probe:

```text
research/p27/archive/gates/p27_ks_guard_sanity_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_ks_guard_sanity_probe_q1607_q1847_q2087_20260622.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_ks_guard_sanity_probe.py \
  --small-primes 1607,1847,2087 \
  | tee research/p27/archive/probe_outputs/p27_ks_guard_sanity_probe_q1607_q1847_q2087_20260622.txt
```

## Checks

For every nondegenerate residual-E point, the probe checks:

```text
Sroot^2 = K
K*K_den = K_num
2*Sroot*W*(X^2+1) = Sroot_num
Salpha^2 = X*L
m0^2 - mt^2*T2 = 4*T2*Salpha^2
```

## Results

```text
q1607:
  q_mod_16 = 7
  chi_minus_one = -1
  chi_two = 1
  checked_points = 1604
  skipped_denominator = 3
  total_mismatches = 0

q1847:
  q_mod_16 = 7
  chi_minus_one = -1
  chi_two = 1
  checked_points = 1844
  skipped_denominator = 3
  total_mismatches = 0

q2087:
  q_mod_16 = 7
  chi_minus_one = -1
  chi_two = 1
  checked_points = 2084
  skipped_denominator = 3
  total_mismatches = 0
```

## Interpretation

Positive:

```text
The K/S map and H90 data are valid in the promotion guard fields.
The post-quartic CAS extraction can use q1607/q1847/q2087 directly.
```

Negative:

```text
This does not prove low genus or sourceability.
It only clears the algebraic sanity layer before normalization.
```

Continue:

```text
offline normalization over P1_K and P1_Sroot in q1607/q1847/q2087
branch divisor degree / support degree / genus computation
Sroot -> -Sroot decomposition
```

```text
p27_ks_guard_field_sanity_rows=1/1
```
