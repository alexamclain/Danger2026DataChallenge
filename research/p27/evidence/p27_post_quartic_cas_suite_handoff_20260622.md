# P27 Post-Quartic CAS Suite Handoff

Date: 2026-06-22

## Claim

If the full B/K monic-quartic GPU suite is negative, the next credible
sqrt-beating route is not another coefficient scan.  It is offline
branch/genus/Kummer extraction over the K/S and B-line covers.

This handoff packages that fallback as an ordered CAS queue.

## Manifest

Machine-readable suite:

```text
research/p27/archive/fixtures/p27_post_quartic_cas_suite_20260622.json
```

Entry condition:

```text
full quartic GPU suite has no stable q1847/guard-field d3 hit
or
a quartic hit needs deeper sourceability/genus analysis
```

## Guard Sanity

Before offline normalization, the K/S equations were checked in the
p27-signature guard fields:

[P27 K/S Guard-Field Sanity](p27_ks_guard_field_sanity_20260622.md)

```text
q1607/q1847/q2087:
  q mod 16 = 7
  chi(-1) = -1
  chi(2) = 1
  total_mismatches = 0
```

The checked identities are:

```text
Sroot^2 = K
K*K_den = K_num
2*Sroot*W*(X^2+1) = Sroot_num
Salpha^2 = X*L
m0^2 - mt^2*T2 = 4*T2*Salpha^2
```

## Ordered CAS Queue

1. Normalize the d3 source over `P1_K`.

Compute:

```text
branch divisor degree
branch support field degrees
genus
component count
stability across q1607/q1847/q2087
```

2. Normalize the d3 source over `P1_Sroot`.

Compute:

```text
Sroot -> -Sroot decomposition
whether the class descends to K or needs signed Sroot
branch degrees and genus
```

3. Carry the H90/order-4 action through the normalized K/S model if feasible.

Compute:

```text
alpha action
quotient/Prym decomposition
whether d3/d4 are coupled by the action
```

4. Normalize the saturated B-line legal/d3 covers offline.

Use the existing q7 Magma fixtures as syntax/saturation seeds, but do not rely
on online Magma for the heavy computation:

```text
research/p27/archive/fixtures/p27_b_line_legal_saturation_q7_magma.m
research/p27/archive/fixtures/p27_b_line_legal_cover_q7_magma.m
research/p27/archive/fixtures/p27_b_line_d3_cover_q7_magma.m
```

5. Compare any named class through the B/K bridge:

```text
K^2 = (B - 2)^4 / (8*B*(B + 2)^2)
```

## Promotion / Kill

Promote if:

```text
stable low-genus/sourceable/recurrent class across q1607/q1847/q2087
or a cheap direct sampler / scope shrink without a fresh Legendre toll
```

Kill if:

```text
normalized branch degree is high/generic
d4 is an unrelated fresh half-cover
only visible K/S branch atoms appear
only small-field interpolation survives
```

## Do Not Reopen

```text
K degree 1/2 screens
small-integer K degree 3/4 scans
split K/S branch divisors of degree <=4
odd Sroot semi-invariant classes
B-line branch-set orbit shortcuts
online Magma as the main B-line normalization engine
```

```text
p27_post_quartic_cas_suite_handoff_rows=1/1
```
