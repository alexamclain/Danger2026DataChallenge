# P27 E-Prime Reciprocal R-Quotient Branch Screen

Date: 2026-06-21

## Claim

The staged E-prime `d3` z-source has a genuine reciprocal quotient, but that
quotient forgets exactly the squareclass bit we need.

Writing `s = z^2`, the reverse-source equation is reciprocal in `s`.  Setting

```text
r = s + 1/s
```

turns the z equation into a quadratic quotient over the saturated first-half
layer:

```text
2*C*(A_den*r + A_num) - U_den*D*A_den*(r^2 - 4) = 0
```

where `C = U_num_scaled + B*U_den*D = 2*U_den*D*x5` on the selected first-half
branch.

On actual p27 rows and p27-signature guard fields, the quotient has a single
`r` value for every usable row and the quadratic discriminant is always square.
The remaining `d3` bit is exactly:

```text
d3 = chi(r + 2) = chi(r - 2)
```

So the reciprocal quotient is useful normalization data, but not a low-genus
source shortcut by itself.

## Artifacts

Magma quotient smoke:

```text
research/p27/archive/fixtures/p27_eprime_d3_rquotient_after_firsthalf_saturation_q7_magma.m
research/p27/archive/probe_outputs/p27_eprime_d3_rquotient_after_firsthalf_saturation_q7_magma_20260621.txt
research/p27/archive/probe_outputs/p27_eprime_d3_rquotient_after_firsthalf_saturation_q7_magma_20260621.html
```

Branch probe:

```text
research/p27/archive/gates/p27_eprime_rquotient_branch_probe.py
research/p27/archive/probe_outputs/p27_eprime_rquotient_branch_probe_20260621.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_eprime_rquotient_branch_probe.py \
  --target 5000 \
  --small-primes 1607,1847,2087 \
  | tee research/p27/archive/probe_outputs/p27_eprime_rquotient_branch_probe_20260621.txt
```

## Magma Smoke

Online Magma reaches the same dimension-1 checkpoint as the full z-source:

```text
AFTER_FIRSTHALF_SAT 2 61 0
D3_RQUOT_AFTER_FIRSTHALF_SCHEME 1 62 0
System Error: User memory limit has been reached
RESULT p27_eprime_d3_rquotient_after_firsthalf_saturation_q7 done
```

Interpretation:

```text
The reciprocal quotient is a real staged curve, but web Magma still cannot
compute genus/normalization from the saturated ideal.
```

## Branch Probe Results

Two independent p27 samples:

```text
p27 train:
  candidates = 20000
  d3_plus/d3_minus = 9864/10136
  single_r_value = 20000
  r_discriminant_square = 20000
  r_plus_2_matches_d3 = 20000
  r_minus_2_matches_d3 = 20000

p27 heldout:
  candidates = 20000
  d3_plus/d3_minus = 10088/9912
  single_r_value = 20000
  r_discriminant_square = 20000
  r_plus_2_matches_d3 = 20000
  r_minus_2_matches_d3 = 20000
```

Promotion guard fields:

```text
q1607:
  candidates = 784
  single_r_value = 784
  r_discriminant_square = 784
  r_plus_2_matches_d3 = 784

q1847:
  candidates = 1008
  single_r_value = 1008
  r_discriminant_square = 1008
  r_plus_2_matches_d3 = 1008

q2087:
  candidates = 912
  single_r_value = 912
  r_discriminant_square = 912
  r_plus_2_matches_d3 = 912
```

## Interpretation

Positive:

```text
The z-source now has a named two-stage structure:
  first quotient by s <-> 1/s, yielding r;
  then recover the actual d3 selector as chi(r+2).

This is a cleaner CAS target than the raw z-source.
```

Negative:

```text
The r quotient itself does not shrink the continuation space.
Its discriminant is square on every usable row tested.
Thus quotienting by r has removed the d3 squareclass rather than explaining it.
```

This aligns the E-prime z-source lane with the earlier `u+2` identity:

```text
if r = x_next + 1/x_next, then chi(x_next) = chi(r+2) = chi(r-2).
```

The remaining sqrt-beating problem is not "find r"; it is to find a source,
recurrence, theta/Kummer identity, or low-genus quotient that makes many
`chi(r_j+2)` bits non-random at once.

## Continue / Kill

```text
continue = normalize the r-quotient only as a branch/Kummer-class target
continue = extract the divisor of r+2 on the normalized quotient
continue = test recurrence/sourceability for the sequence of r_j + 2 classes

kill = treating the reciprocal r quotient alone as a d3 source
kill = expecting the r-quadratic discriminant to be the missing selector
kill = widening U-polynomial searches instead of extracting the r+2 class
```

```text
p27_eprime_rquotient_branch_screen_rows=1/1
```
