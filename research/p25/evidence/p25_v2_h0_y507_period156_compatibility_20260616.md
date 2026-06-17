# P25 V2 H0/Y507 Period-156 Compatibility

Date: 2026-06-16

Marker: `p25_v2_h0_y507_period156_compatibility_rows=1/1`

## Purpose

Promote the archived H0/Y507 period-156 compatibility screen into the v2
wiki. This screen separates three accepted source-stage shapes from nearby
value, payload, and ambient-period repair rows.

## Pages And Gates Read

- `lanes/h0.md`
- `lanes/conductor39.md`
- `sources/schertz-scholl.md`
- `evidence/p25_v2_period156_value_source_hook_20260616.md`
- `archive/gates/p25_ksy_y_h0_period156_value_compatibility_gate.py`
- `archive/gates/p25_v2_period156_value_source_hook_gate.py`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/archive/gates/p25_v2_h0_y507_period156_compatibility_gate.py
```

## Findings

```text
Y_507 minimum doubling period = 156
gcd(4^156 - 1, p - 1) = 1
gcd(4^780 - 1, p - 1) = 11
H0 support period = 156
canonical H0 factors = 78 positive / 78 negative
canonical H0 boundary equals Norm_156(Y_507) = yes
legal H0 orbit count = 4
legal H0 stabilizer size = 3
```

Accepted source-stage shapes:

```text
canonical H0 value with boundary and period-156 branch context
Y_507 value with period-156 context
canonical H0 divisor/additive identity with boundary
```

Repair or reject shapes:

```text
H0 value missing Norm_156(Y_507) boundary
H0 value missing period-156 branch/root/telescoping context
formal one-coset H value
ambient period-780 value
finite payload without arithmetic source theorem
finite identity without arithmetic source theorem
```

Counts:

```text
compatibility rows = 9
source-closing row shapes = 3
value-closing row shapes = 2
divisor-closing row shapes = 1
rejected rows = 2
conditional rows = 4
finite-payload rows = 1
current period-156 value theorems = 0
```

## Verdict

The H0/Y507 value route remains live but exacting. The best value-side theorem
would be either a canonical H0 value with the `Norm_156(Y_507)` boundary and
period-156 branch data, or a `Y_507` period-156 value theorem. The
divisor/additive route can avoid multiplicative branch selection, but it still
must carry the exact boundary and scalar-fixing finite data.

Decision:
`period156_h0_y507_value_route_live_but_no_current_theorem`.
