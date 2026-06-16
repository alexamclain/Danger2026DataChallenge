# Tensor Factor Trace Coordinate Support

This note audits beta-character support for coordinate minors of the p24
trace-frame maps.

## Setup

For p24:

```text
n = 3107441,
a = p^ord_m(p) mod n = 209035,
|<a>| = 5549 = 31*179.
```

The trace-frame coordinates are indexed by:

```text
i = 0,1,2       top window / theta-twist,
t = 0..178      C/E Frobenius coordinate.
```

For fixed `(i,t)`, the beta-character support is the size-31 trace subgroup
coset:

```text
a^t * <a^179>.
```

Thus a coordinate Plucker minor can only be recurrence-compressed if the
sumset of its selected trace-coordinate cosets is small.

## Audit

The script is:

```text
p24/tensor_factor_trace_coordinate_support_audit.py
```

Run with the bundled NumPy runtime:

```text
/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/tensor_factor_trace_coordinate_support_audit.py \
  --random-trials 30 --sample-size 6 --max-prefix 8
```

It reports:

```text
consecutive prefixes:
size=1 covered=31
size=2 covered=961
size=3 covered=29636
size=4 covered=799428
size=5 covered=3107068 missing=373
size=6 covered=3107441 missing=0

random six-coordinate samples:
full_support_trials=30/30
```

So six trace-coordinate cosets already give full beta-character support in
the tested generic choices.

## Consequence

The p24 coordinate minors are much larger:

```text
Omega_1:    select 158 of 179 Top_1 coordinates,
Omega_211:  select 210 of 358 Top_2 coordinates,
Omega_3:    select 368 of 537 Top_3 coordinates.
```

Therefore a coordinate-minor recurrence/resultant proof will not get a small
spectral factor merely by choosing ordinary trace coordinates.  It would need
a highly special CM-derived coordinate or cancellation identity.  The natural
remaining theorem is a full-support Plucker p-unit / rank-condenser theorem.
