# P25 KSY-y H0/Y507 Period-156 Value Compatibility

Updated: 2026-06-14 14:35 PDT

## Purpose

This packet attaches the period-`156` value discipline directly to the
surviving H0/Y507 Hilbert-90 route.

The rule is:

```text
H0 value claim:
  needs exact boundary (1-Frob_p)H0 = Norm_156(Y_507)
  needs period-156 branch/root/telescoping context

H0 divisor/additive identity:
  needs exact boundary to Norm_156(Y_507)
  does not need a multiplicative value branch
```

## Period And H0 Facts

```text
Y_507 minimum doubling period        = 156
gcd(4^156 - 1, p - 1)                = 1
gcd(4^780 - 1, p - 1)                = 11
H0 support period                    = 156
canonical H0 positive factors        = 78
canonical H0 negative factors        = 78
canonical H0 boundary equals norm    = 1
legal H0 orbit count                 = 4
legal H0 stabilizer size             = 3
```

## Compatibility Rows

```text
canonical_h0_value_with_boundary_period156:
  decision = source_theorem_closed_policy_or_framing_missing
  missing  = DANGER3 finite-identity/non-CM framing

canonical_h0_value_missing_boundary:
  decision = conditional_h0_missing_boundary_to_norm
  missing  = (1-Frob_p)H0 = Norm_156(Y_507)

canonical_h0_value_missing_period156:
  decision = conditional_missing_period_156_context
  missing  = period-156 branch/root/telescoping context

canonical_h0_divisor_boundary_no_period_value_branch:
  decision = source_theorem_closed_policy_or_framing_missing
  missing  = DANGER3 finite-identity/non-CM framing

y507_value_with_period156:
  decision = source_theorem_closed_policy_or_framing_missing
  missing  = DANGER3 finite-identity/non-CM framing

formal_one_coset_h_value:
  decision = reject_illegal_or_insufficient_target
  missing  = exact P, Y_507, canonical H0, H0 translate, or conductor-39 mixed source

ambient_780_value:
  decision = reject_illegal_or_insufficient_target
  missing  = exact P, Y_507, canonical H0, H0 translate, or conductor-39 mixed source

h0_finite_payload_without_source:
  decision = conditional_finite_payload_without_source_theorem
  missing  = challenge-legal arithmetic source theorem

h0_finite_identity_without_arithmetic_source:
  decision = conditional_finite_identity_without_arithmetic_source
  missing  = challenge-legal arithmetic source theorem
```

## Counts

```text
row_count             = 9
source_closing_rows   = 3
value_closing_rows    = 2
divisor_closing_rows  = 1
rejected_rows         = 2
conditional_rows      = 4
finite_payload_rows   = 1
```

## Meaning

The H0/Y507 route is viable but narrow.  A bare H0 value, a formal one-coset
value, an ambient-period value, or a finite payload without an arithmetic
source theorem is not enough.  A real source-stage closer is one of:

```text
canonical H0 value + boundary + period 156
Y_507 value + period 156
canonical H0 divisor/additive identity + boundary
```

All three still need DANGER3 framing, extraction to `(A,x0)`, and official
`vpp.py`.

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_h0_period156_value_compatibility_gate.py
```

Marker:

```text
ksy_y_h0_period156_value_compatibility_rows=1/1
```
