# Actual-CM Mixed-Spectrum Boundary

Date: 2026-06-07

## Point

The p24 recombined theorem has two nontrivial quotient axes: the right
order-7 quotient and the relative octic quotient.  A bounded shape scan found
a small actual-CM calibration row with the same qualitative feature:

```text
D = -4751
q = 4787
h = 91 = 7 * 13
right quotient:    (F_7^*) / <q>,  order 3
relative quotient: (F_13^*) / <q>, order 4
full cycle prime: ell = 2
```

This is smaller than p24 but has both axes nontrivial, unlike the earlier
actual-CM right-combo rows where the recombined relative quotient was trivial.

## Result

The script checks all global origin shifts of the embedded 2-isogeny cycle.
For each shift it evaluates:

```text
mixed equations:     2 * 3 = 6
anchor equations:    2
balance equations:   2 * 4 = 8
```

No shift satisfies the full mixed-spectrum target, the full anchor target, or
the full recombined balance.

## Checked Gate

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_fixed_frequency_actual_cm_mixed_spectrum_boundary.py
```

Key markers:

```text
D=-4751
q=4787
h=91
m=7
n=13
right_quotient=3
relative_quotient=4
mixed_equations_per_shift=6
anchor_equations_per_shift=2
balance_equations_per_shift=8
full_mixed_zero_shifts=0/91
full_anchor_zero_shifts=0/91
full_recombined_balance_shifts=0/91
actual_cm_both_axes_nontrivial_boundary=1
actual_cm_mixed_spectrum_vanishing_is_not_generic=1
actual_cm_origin_shift_does_not_rescue_mixed_balance=1
```

## Interpretation

The mixed-spectrum theorem is not a generic consequence of having a cyclic CM
torsor with nontrivial right and relative quotient axes.  The p24 proof must
use the specific trace-GCD weighted CM/Lang packet, or an explicit potential,
not merely the existence of both quotient decompositions.
