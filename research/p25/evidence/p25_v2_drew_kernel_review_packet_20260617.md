# P25 v2 Drew Kernel Review Packet

Updated: 2026-06-17

Marker: `p25_v2_drew_kernel_review_packet_rows=1/1`

## Purpose

Make the current p25 theorem ask ready for a Drew/expert review after the
current theorem kernel. This is not another broad source prompt. It is the
smallest current packet that prevents two old confusions:

```text
1. row-labeled powers now include e in {3,5,13,39,75,169,507};
2. exact-P 75 atoms are not the same object as a row-power R_m^75 theorem.
```

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `lanes/exact-p.md`
- `evidence/p25_v2_current_theorem_kernel_20260617.md`
- `evidence/p25_v2_self_contained_theorem_statement_20260616.md`
- `evidence/p25_v2_first_pass_expert_intake_packet_20260616.md`
- `evidence/p25_v2_extended_unique_power_intake_20260617.md`
- `evidence/p25_v2_period156_lookup_row_status_20260617.md`
- `evidence/p25_v2_q_yang_lookup_row_status_20260617.md`
- `evidence/p25_v2_matched_quotient_closure_packet_20260617.md`
- `evidence/p25_v2_exactp_spine_payload_separation_20260617.md`
- `evidence/p25_v2_local_source_hook_coverage_audit_20260617.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_drew_kernel_review_packet_gate.py
```

The gate returned `p25_v2_drew_kernel_review_packet_rows=1/1`.

## Ask

```text
p = 10000000000000000000000013

Does a known challenge-legal arithmetic theorem provide one of these exact
finite objects?
```

### 1. Scalar-Fixed Row Theorem

```text
object:
  one exact oriented support-156 row R_m, m in {1,2,4,8}

positive answer:
  finite scalar-fixed divisor/additive identity with Norm_156(Y_507) boundary

reject/repair:
  source legality, boundary-only, divisor class, or value up to unspecified
  F_p^* scalar
```

### 2. Row-Labeled Unique Power

```text
object:
  exact source theorem for R_m^e on one labeled legal row
  e in {3,5,13,39,75,169,507}

positive answer:
  exact finite F_p value plus row label and accepted boundary or period bridge;
  recover R_m by inverse exponent

reject/repair:
  rowless power value, powered boundary only, value up to scalar, or exact-P
  75-atom vocabulary
```

All seven exponents are units modulo `p - 1`, but they do not mean the same
thing as exact-P atoms:

```text
gcd(e, p - 1) = 1 for e in {3,5,13,39,75,169,507}
```

### 3. Support-Period-156 Value

```text
object:
  canonical H0 or Y_507 with support-period-156 branch/root/telescoping data

positive answer:
  finite value theorem plus legal-row bridge and no ambient-period-780 mu_11
  ambiguity

reject/repair:
  H0/Y507 name only, norm identity only, class-field generation, ambient-period
  value, or value up to scalar
```

## Support Or Heavy Rows

```text
Q/Yang/H90:
  useful only if it gives finite Q or Q^3 theorem data with period-156 context
  plus oriented split/direct row normalization. Q source language, Q^6
  boundary, diagonal aggregate, Q-square without extraction map, or selector
  without finite value is support/repair.

matched aggregate:
  useful only if it gives an arithmetic theorem for R^v plus an arithmetic
  theorem for the exact matched zero-lattice value R^(v - (sum v)e_m), with
  gcd(sum v,p-1)=1. Aggregate-only, quotient-only, unmatched quotient,
  zero-sum, or nonunit-sum packets are support/repair.

exact-P/theta2:
  useful only if it carries compact C,D,K/orientation, equal-weight atoms,
  exact KL mixed selector, or accepted theta2 payload with the
  75->300->12->312->156 bridge. Vocabulary, finite fixtures, atom counts, and
  unified target alone are repair.

reverse unified -> exact-P:
  reject without extra selector structure reconstructing C,D,K/orientation,
  equal-weight atoms, or accepted theta2 payload.
```

## What A Positive Expert Answer Should Contain

```text
row identity:
  m in {1,2,4,8}, row label/orientation, or a row-labeled theorem containing
  one legal row

source theorem:
  arithmetic theorem specialized enough to emit the finite p25 object

boundary:
  Norm_156(Y_507), or a period-156 bridge that normalizes to that row

finite normalization:
  scalar-fixed additive/divisor value, branch/root/telescoping data, or exact
  finite row-power value with inverse recovery

downstream:
  after a positive theorem, still route through DANGER3 framing, same-j
  X_1(8112), X_1(16), halving/direct x0, and official vpp.py
```

## Counts

```text
evidence_markers_ok = 9/9
review_rows = 7
source_stage_rows = 3
support_rows = 2
heavy_rows = 1
reject_rows = 1
current_positive_answers = 0
current_submission_ready = 0
p25_v2_drew_kernel_review_packet_rows=1/1
```

## Verdict

This is the current expert packet. A useful answer is a theorem for one
scalar-fixed row, one row-labeled unique power, or one support-period-156
value with legal-row bridge. `Q`/Yang is support until selector and finite
theorem debt are paid. Matched aggregates are support until both the aggregate
and exact matched zero-lattice quotient theorems are present. Exact-P/theta2
is a heavy upstream route, not the first-pass row theorem and not
interchangeable with `R_m^75`.
