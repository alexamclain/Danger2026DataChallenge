# Subsqrt Moonshot Lane B McCarthy Power Transport Raw-Y

Date: 2026-06-13

## Result

The powered McCarthy quotient coefficient descends cleanly to the p25
coefficient field, and after its determined normalization it recovers the
existing raw-Y closure.

From the power-descent gate:

```text
support(R(q)^2029 - 1) = (138,)
R(138)^2029 = zeta_39^5
```

The p25 raw-Y harness works over:

```text
F_2029
```

and `39 | 2028`, so the order-39 root is available in the same field.  Using
the primitive-root convention already used by the local gates:

```text
primitive root of F_2029 = 2
zeta_39 = 2^52 = 1358
zeta_39^5 = 1376
zeta_39^5 - 1 = 1375
(zeta_39^5 - 1)^-1 = 636
```

The unnormalized powered quotient has the right singleton support, but not the
right p25 payload:

```text
anomaly_projector_coefficient = 1375
corrected seed payload at (2,1) = 656
quotient_packet_exact = False
raw_y_harness_ok = False
```

After multiplying by the determined inverse `636`:

```text
anomaly_projector_coefficient = 1
corrected seed payload = all ones
quotient_packet_exact = True
raw_y_nonzero = 6300
raw_y_harness_ok = True
```

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_mccarthy_power_transport_raw_y_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_mccarthy_power_transport_raw_y_gate.py
```

Observed:

```text
coefficient_transport_canonical = True
normalized_raw_y_closes = True
unnormalized_control_fails_exact_packet = True
square_axis_mccarthy_power_transport_raw_y_rows=1/1
```

## Consequence

This closes the finite McCarthy-to-raw-Y bridge conditional on the powered
quotient being a legitimate arithmetic producer:

```text
McCarthy theorem quotient R(q)
  -> power descent R(q)^2029
  -> singleton q=138 with order-39 coefficient
  -> canonical F_2029 transport zeta_39^5 - 1
  -> determined inverse normalization
  -> exact GK anomaly projector
  -> existing raw-Y closure
```

The remaining debt is no longer finite payload geometry or coefficient-field
descent.  It is:

```text
justify the 2029th power as an allowed powered unit quotient before raw lift
justify the coefficient normalization by (zeta_39^5 - 1)^-1 as part of the
producer, not as an arbitrary after-the-fact scalar
preserve the explicit S trace and kernel-trivial raw lift
```

Continue condition:

```text
candidate gives a theorem-level powered quotient R^2029, or an equivalent
order-39 quotient, with the determined coefficient normalization
```

Discard condition:

```text
candidate uses the unnormalized coefficient 1375 and fails the raw-Y harness
candidate cannot justify the 2029th power before raw lift
candidate needs any scalar other than the transported (zeta_39^5 - 1)^-1
```
