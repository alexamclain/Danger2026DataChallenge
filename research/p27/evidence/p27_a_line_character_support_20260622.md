# P27 A-Line Character Support Screen

Date: 2026-06-22

## Claim

The persistent A-level selected-prefix descent is not explained by the nearest
visible low-degree characters on `P1_A`.

The screen kills the simple genus `<= 1` branch-support shortcut:

```text
d_j(A) = chi(f_j(A)), deg(f_j) <= 4
```

for the tested visible families.  It does **not** kill the A-line Kummer-class
moonshot: the surviving route is normalized cover / divisor-class extraction,
not another coefficient or branch-factor scan.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_a_line_character_support_probe.py
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_a_line_character_support_probe_q1607_q1847_q2087_deg4_quad_d3d4_20260622.txt
research/p27/archive/probe_outputs/p27_a_line_character_support_probe_auto2200_count8_split_deg4_20260622.txt
```

Commands:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_a_line_character_support_probe.py \
  --small-primes 1607,1847,2087 \
  --depth 8 \
  --min-rows 40 \
  --max-weight 4 \
  --quadratic-gates 3,4 \
  | tee research/p27/archive/probe_outputs/p27_a_line_character_support_probe_q1607_q1847_q2087_deg4_quad_d3d4_20260622.txt

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_a_line_character_support_probe.py \
  --small-primes '' \
  --auto-start 2200 \
  --auto-count 8 \
  --depth 6 \
  --min-rows 40 \
  --max-weight 4 \
  | tee research/p27/archive/probe_outputs/p27_a_line_character_support_probe_auto2200_count8_split_deg4_20260622.txt
```

## Families Tested

For an A-labeled gate row set, the probe tests:

```text
split support: product of up to 4 rational linear factors (A-a_i)
quadratic + linears: one irreducible quadratic times up to 2 rational factors
two quadratics: product of up to two irreducible quadratics
```

Together, the quadratic-enabled screen covers the visible squarefree degree
`<= 4` branch-support families on `P1_A`, up to global polarity.

The probe also reports a rough random-fit calibration so small-tail exact fits
are not promoted accidentally.

## Complete Degree <= 4 Results

For d3 on the three main guard fields:

```text
q1607 d3 rows=49:
  split degree <=4: none
  irreducible quadratic + <=2 linears: none
  two irreducible quadratics: none

q1847 d3 rows=63:
  split degree <=4: none
  irreducible quadratic + <=2 linears: none
  two irreducible quadratics: none

q2087 d3 rows=57:
  split degree <=4: none
  irreducible quadratic + <=2 linears: none
  two irreducible quadratics: none
```

For d4, only q1847 had enough non-one-sided rows for a useful complete
degree-4 screen in this run:

```text
q1847 d4 rows=45:
  split degree <=4: none
  irreducible quadratic + <=2 linears: none
  two irreducible quadratics: none
```

q1607 and q2087 d4 had too few rows under the `min_rows=40` promotion bar.

## Split-Support Stability Sweep

The nearby `7 mod 8` auto fields also reject split rational branch support for
d3:

```text
q2207 d3 rows=64: none_weight_le_4
q2239 d3 rows=86: none_weight_le_4
q2287 d3 rows=70: none_weight_le_4
q2311 d3 rows=78: none_weight_le_4
q2351 d3 rows=79: none_weight_le_4
q2383 d3 rows=66: none_weight_le_4
q2399 d3 rows=42: none_weight_le_4
q2423 d3 rows=69: none_weight_le_4
```

d4 split support is also negative in the healthy auto fields:

```text
q2239 d4 rows=52: none_weight_le_4
q2351 d4 rows=50: none_weight_le_4
```

Other d4/d5 rows in the auto sweep were one-sided or below the row bar, so
they are not used as evidence.

## Interpretation

Positive:

```text
The low-degree visible A-character shortcut is now directly falsified.
The A-line descent remains real and should be treated as a Kummer-class object.
The screen gives a clean next CAS ask: extract divisor classes, do not scan
more visible degree-4 supports.
```

Negative:

```text
No tested d3 field has a visible degree <=4 A-line branch support.
q1847 also kills the visible degree <=4 d4 branch support.
Split rational branch support is stable-negative across nearby fields.
```

## Continue / Kill

```text
continue = normalized A-level Kummer class extraction for d3..d10
continue = class comparison / coboundary / recurrence search on the A-cover
continue = use low-degree support only if CAS produces a named divisor reason

kill = blind low-degree A polynomial scans
kill = visible genus <=1 A-line support as the immediate sqrt-beating source
kill = GPU production from A-prefix descent without a class/source law
```

Next packet:
[P27 A-Level Kummer Extraction Packet](p27_a_level_kummer_extraction_packet_20260622.md)
emits the q1607/q1847/q2087 A-labeled d3/d4 fixture and the normalized-cover
CAS acceptance criteria.

```text
p27_a_line_character_support_rows=1/1
```
