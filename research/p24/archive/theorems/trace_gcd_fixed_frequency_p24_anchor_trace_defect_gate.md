# p24 Anchor Trace-Defect Gate

Date: 2026-06-06

## Point

The recombined period-coset balance has one anchor equation per nontrivial
right quotient character:

```text
sum_{k != 0} c_k(chi) = (n - 1) * c_0(chi).
```

Equivalently:

```text
sum_k c_k(chi) = n * c_0(chi).
```

With

```text
c_k(chi) = sum_r chi^(-1)(r mod 211) j_{r + m*k},
```

this is the same as:

```text
sum_r chi^(-1)(r mod 211)
  * (Tr_relative(j_{r + m*bullet}) - n*j_r)
= 0.
```

So the anchor is not a constant-term bookkeeping condition.  It is the
nontrivial right quotient-character vanishing of the relative trace defect:

```text
D_r = Tr_relative(j_{r + m*bullet}) - n*j_r.
```

Across the six nontrivial right quotient characters, the anchor equations are
equivalent to saying that the seven `H=<2^7>` coset sums of this trace-defect
profile on `F_211^*` are equal.

## Theorem Target

For p24, the sharper anchor theorem is:

```text
The relative trace defect of the embedded child section k=0 has zero
nontrivial order-7 right spectrum.
```

This is more arithmetic than the raw coefficient-balance phrase.  It points
at the class-field trace from the full `h`-torsor to the `m`-quotient, paired
with the chosen embedded child root.  The missing proof must explain why that
trace defect has no order-7 right quotient component.

## Checked Gate

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_fixed_frequency_p24_anchor_trace_defect_gate.py
```

Key markers:

```text
anchor_defect_projection_mismatches=0
anchor_zero_iff_trace_defect_h_coset_equal_failures=0
random_anchor_nonzero=48/48
forced_trace_defect_equal_cosets=48/48
forced_anchor_zero=48/48
p24_anchor_equations=6
anchor_equation_equals_relative_trace_defect_character_projection=1
six_anchors_zero_iff_trace_defect_has_equal_H_coset_sums=1
p24_anchor_target_is_relative_trace_defect_order7_spectrum_zero=1
```

This gate is finite algebra, not the p24 arithmetic proof.  Its purpose is to
name the exact object the proof has to control.
