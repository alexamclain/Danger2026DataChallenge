# p24 Trace-Average Anchor Payload Gate

Date: 2026-06-06

## Point

The anchor trace-defect theorem gives a small verifier surface:

```text
D_r = Tr_relative(j_{r + m*bullet}) - n*j_r.
```

The six anchor equations are equivalent to equal `H=<2^7>` coset sums of the
right-axis defect profile.  Thus an honest producer could supply just:

```text
7 defect H-coset sums.
```

The verifier checks that those seven values are equal.

## Larger Honest Profile Surface

A more explicit but still sub-sqrt p24 surface is:

```text
quotient trace profile:     T_r = Tr_relative(j_{r + m*bullet}),  r mod m
selected child profile:     S_r = j_r,                            r mod m
```

Then

```text
D_r = T_r - n*S_r.
```

For p24:

```text
m = 66254
2*m = 132508
132508 / floor(sqrt(p)) = 1.32508e-7.
```

So even the full trace-average plus selected-child profile is far below
sqrt(p) for this prime.  The catch is producer honesty: constructing `T_r`
and `S_r` without enumerating the class set is exactly embedded tower/morphism
data.

## Checked Gate

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_fixed_frequency_p24_trace_average_anchor_payload_gate.py
```

Key markers:

```text
profile_decomposition_failures=0
random_trace_average_anchor_passes=0/48
forced_defect_h_sums_equal=48/48
fake_equal_h_sum_payloads_pass=48/48
p24_defect_hcoset_sum_payload=7
p24_full_trace_average_plus_child_payload=132508
p24_full_trace_average_plus_child_payload_over_sqrt=1.325080000000e-07
anchor_can_be_verified_from_seven_defect_H_coset_sums=1
full_trace_average_plus_child_profile_is_subsqrt_for_p24=1
equal_sum_payload_requires_producer_honesty=1
trace_average_route_still_needs_embedded_child_or_morphism=1
```

This gate keeps the verifier/proof distinction explicit.  Seven equal numbers
are easy to fake; the missing theorem is an embedded CM/Lang construction of
the trace-average or defect sums.
