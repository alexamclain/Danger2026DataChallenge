# p25 Lane B: McCarthy Idempotent-Unit Gate

Updated: 2026-06-13 13:02 PDT

## Result

The powered McCarthy quotient, after q-power projection and the determined
coefficient transport, is exactly the pointwise unit

```text
U(q) = 1 + (zeta_39^5 - 1) * e_138(q)
```

in the function algebra on `C_507` over `F_2029`.

Verified constants:

```text
modulus = 2029
quotient_order = 507
target_q_exp = 138
zeta_39^5 = 1376
zeta_39^5 - 1 = 1375
(zeta_39^5 - 1)^-1 = 636
```

Verified laws:

```text
support(e_138) = 1
degree(e_138) = 1
e_138^2 = e_138
support(U) = 507
support(U - 1) = 1
order(U) = 39
U^-1 = 1 + (zeta_39^-5 - 1) * e_138
(U - 1)/(zeta_39^5 - 1) = e_138
```

Fourier support over `C_507`:

```text
support_DFT(e_138) = 507
support_DFT(U - 1) = 507
support_DFT(U) = 507
```

## Interpretation

This is the sharpest current form of the Barnes/McCarthy moonshot target.
Pointwise, the object is exactly the sparse order-39 correction needed to
repair the p25 square-axis anomaly.  Frequency-side, the same object is dense
on all `507` characters, so an ordinary group-ring/Fourier-filter producer is
not a cheap explanation.

Continue McCarthy/Barnes only with theorem endpoint production, exceptional
delta production, or an equivalent arithmetic unit identity that first creates
the multiplicative quotient.  Then q-power projection and the determined
normalization can recover the raw-Y passing payload.

## Local Gate

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_mccarthy_idempotent_unit_gate.py
```

Observed:

```text
square_axis_mccarthy_idempotent_unit_rows=1/1
conclusion=reported_p25_laneB_square_axis_mccarthy_idempotent_unit_gate
```
