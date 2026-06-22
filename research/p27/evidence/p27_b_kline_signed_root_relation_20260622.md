# P27 B/K Signed-Root Relation Screen

Date: 2026-06-22

## Claim

The selected signed K root over a legal B value does not expose an additional
low-degree plane relation in `(B,K)`.

The full bridge cover is

```text
K^2 = (B - 2)^4 / (8*B*(B + 2)^2).
```

For each legal B target row, the bridge cover has two K roots, and exactly one
appears in the signed-doubling K-line target packet.  This probe compares the
full two-root cover with the selected one-root sheet.  In q1471, q1607, q1847,
and q2087, the selected sheet has no positive extra low-degree relation beyond
the inherited bridge-cover equation.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_b_kline_root_relation_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_b_kline_root_relation_probe_q1471_q1607_q1847_q2087_deg12_20260622.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_kline_root_relation_probe.py \
  --small-primes 1471,1607,1847,2087 \
  --families d3,d4 \
  --degrees 2,4,6,8,10,12 \
  | tee research/p27/archive/probe_outputs/p27_b_kline_root_relation_probe_q1471_q1607_q1847_q2087_deg12_20260622.txt
```

## Results

For d3, the selected sheet and the full two-root cover have identical extra
nullity through the non-interpolation range:

```text
q1471 d3:
  deg2 selected_minus_cover_extra = 0
  deg4 selected_minus_cover_extra = 0
  deg6 selected_minus_cover_extra = 0
  deg8 selected_minus_cover_extra = 0

q1607 d3:
  deg2 selected_minus_cover_extra = 0
  deg4 selected_minus_cover_extra = 0
  deg6 selected_minus_cover_extra = 0
  deg8 selected_minus_cover_extra = 0

q1847 d3:
  deg2 selected_minus_cover_extra = 0
  deg4 selected_minus_cover_extra = 0
  deg6 selected_minus_cover_extra = 0
  deg8 selected_minus_cover_extra = 0

q2087 d3:
  deg2 selected_minus_cover_extra = 0
  deg4 selected_minus_cover_extra = 0
  deg6 selected_minus_cover_extra = 0
  deg8 selected_minus_cover_extra = 0
```

For d4 after d3, the same pattern holds through the meaningful range; late
degree values are dominated by small selected-row counts:

```text
q1471/q1607/q1847 d4:
  deg2, deg4, deg6 selected_minus_cover_extra = 0

q2087 d4:
  deg2, deg4 selected_minus_cover_extra = 0
  deg6 selected_minus_cover_extra = -3
```

Negative values mean the selected sample has fewer relations after accounting
for forced interpolation; they are not source evidence.

## Interpretation

Positive:

```text
The B/K bridge is coherent and exact, but the signed-root choice is not a
cheap low-degree plane curve in (B,K).
```

Negative:

```text
The selected K root over B is not explained by an extra low-degree relation
beyond K^2=(B-2)^4/(8B(B+2)^2).
Do not expect a direct sampler from selecting one sheet of the B/K cover using
a small plane equation.
```

This reinforces the current GPU/CAS plan:

```text
continue = exact quartic support in B or K as coordinate alternatives
continue = offline divisor/Kummer-class extraction if quartics are negative
kill = signed K root over B as a simple low-degree plane-curve source
```

```text
p27_b_kline_signed_root_relation_rows=1/1
```
