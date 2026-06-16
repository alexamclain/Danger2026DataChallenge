# P25 Lane B: theta2 Factor-Certificate Intake Harness

Updated: 2026-06-13 15:04 PDT

## Purpose

The sparse theta2 harness accepts `300` triples, and the compact theta2 harness
accepts KSY center/half-edge parameters.  This harness lowers the theorem-output
contract to the p24-derived bridge factors:

```text
base * K_trace * D_segment * (1 - T)
```

A theorem hit may emit only the eight source coordinates

```text
base_right base_c
K_right    K_c
D_right    D_c
T_right    T_c
```

with fixed lengths `K_trace=25` and `D_segment=3`.

## Accepted Target

```text
base = (25, 25)
K    = (57, 0)
D    = (22, 3)
T    = (38, 113)
```

The harness derives

```text
H           = T / 2      = (19, 141)
center_base = base + H   = (44, 166)
half_shift  = -H         = (56, 28)
```

and then reuses the compact theta2 harness for both `theta2^-1` and `theta2`.

## Result

```text
factor support budget                 = 31
factor product support                 = 150
factor product passes bridge contract = true
derived compact theta2^-1 passes       = true
derived compact theta2 passes          = true
period-156 K_trace absorption passes   = true

accepted gauge:
  base -> base + K also passes

rejected controls:
  wrong D=(22,4) fails bridge contract
  wrong T=2T fails bridge and compact theta2 contracts
  collapsed K=(0,0) fails bridge and period absorption
```

## Local Gate

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_factor_certificate_harness.py
```

Expected marker:

```text
robert_ksy_theta2_factor_certificate_harness_rows=1/1
```

## Candidate Mode

Positive target:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_factor_certificate_harness.py \
  --base-right 25 --base-c 25 \
  --k-right 57 --k-c 0 \
  --d-right 22 --d-c 3 \
  --t-right 38 --t-c 113
```

Expected marker:

```text
robert_ksy_theta2_factor_certificate_candidate_rows=1/1
```

## Interpretation

This is now the smallest concrete finite verifier target in the KSY/theta lane.
A literature or theorem hit does not need to emit sparse triples.  It can emit
the bridge factor tuple, and the harness derives the KSY theta2 footprint,
checks the support-period absorption law, and recovers the bridge through the
existing theta2 machinery.

This still does not prove the missing arithmetic theta2 producer.  It gives
that producer a sharply bounded output contract.
