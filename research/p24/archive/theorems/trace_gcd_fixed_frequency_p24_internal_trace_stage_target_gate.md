# Fixed-Frequency p24 Internal-Trace Stage Target Gate

Date: 2026-06-06

## Point

The right-coboundary theorem now reduces to a nested internal trace identity:

```text
Tr_{B/E}(R_obstruction)=0,
Tr_{B/E}=Tr_{C/E} o Tr_{B/C}.
```

Since:

```text
5549 = 31 * 179,
```

there are two possible proof strengths:

```text
strong:  Tr_{B/C}(R_obstruction)=0;
weak:    Tr_{C/E}(Tr_{B/C}(R_obstruction))=0.
```

The finite stage gate shows the strong target is unnecessarily strong.  On
quotient eigenpackets, the `B/C` trace has rank `179` in the p24 analogue,
while the nested trace has rank `1`.

## Theorem Guidance

Do not try to prove:

```text
Tr_{B/C}(R_obstruction)=0.
```

That would impose a whole intermediate vector vanishing.

The certificate-shaped theorem is instead:

```text
Tr_{C/E}(Y_C)=0,
where Y_C = Tr_{B/C}(R_obstruction).
```

This is one scalar internal trace condition per relevant quotient-eigenpacket.

## Checked Gate

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_fixed_frequency_p24_internal_trace_stage_target_gate.py
```

Key output:

```text
b_over_c_trace_rank_on_quotient_eigenpackets=5
nested_trace_rank_on_quotient_eigenpackets=1
p24_B_over_C_trace_rank_target=179
p24_nested_trace_rank_target=1
random_nested_trace_zeroes=1/48
random_B_over_C_trace_zeroes=0/48
forced_nested_zero_b_trace_nonzero=48/48
forced_B_over_C_trace_zeroes=48/48
forced_B_over_C_zero_implies_nested_zero=48/48
B_over_C_trace_zero_is_sufficient_but_too_strong=1
nested_internal_trace_zero_is_the_minimal_stage_target=1
prove_C_over_E_trace_of_B_over_C_trace_zero_not_B_over_C_zero=1
p24_internal_trace_stage_target_has_codimension_one=1
```

