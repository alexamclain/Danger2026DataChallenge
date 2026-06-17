# P25 v2 Current Theorem Kernel

Updated: 2026-06-17

Marker: `p25_v2_current_theorem_kernel_rows=1/1`

## Purpose

Update the self-contained theorem handoff after the newer
basis-sensitive, unique-power, and exact-P separation filters. This is the
current compact theorem kernel to use before asking an expert, reading a new
source snippet, or classifying a proof attempt.

It supersedes the older minimal-ask wording where it is narrower or more
current, but it does not replace the detailed row definitions in the
self-contained theorem statement.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `lanes/exact-p.md`
- `evidence/p25_v2_self_contained_theorem_statement_20260616.md`
- `evidence/p25_v2_live_theorem_ask_packet_20260617.md`
- `evidence/p25_v2_basis_sensitive_anchor_sieve_20260617.md`
- `evidence/p25_v2_source_stage_normalization_spine_20260617.md`
- `evidence/p25_v2_common_scalar_anchor_filter_20260617.md`
- `evidence/p25_v2_extended_unique_power_intake_20260617.md`
- `evidence/p25_v2_period156_lookup_row_status_20260617.md`
- `evidence/p25_v2_exactp_theta2_lookup_row_status_20260617.md`
- `evidence/p25_v2_exactp_spine_payload_separation_20260617.md`
- `evidence/p25_v2_q_yang_lookup_row_status_20260617.md`
- `evidence/p25_v2_matched_quotient_closure_packet_20260617.md`
- `evidence/p25_v2_unified_submission_extraction_contract_20260616.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_current_theorem_kernel_gate.py
```

The gate returned `p25_v2_current_theorem_kernel_rows=1/1`.

## Current Kernel

```text
p = 10000000000000000000000013
target = one exact oriented support-156 row R_m, m in {1,2,4,8}
boundary = Norm_156(Y_507)
downstream = DANGER3 framing -> same-j X_1(8112) -> X_1(16) payload
             -> halving/direct x0 -> official vpp.py
```

The source-stage row can enter through exactly these current front doors:

```text
unit_edge_divisor_additive
  object   = one exact oriented row R_m
  payload  = scalar-fixed finite divisor/additive theorem with boundary
  route    = source-stage normalization, then extraction

row_labeled_unique_power
  object   = one exact oriented row R_m and e in {3,5,13,39,75,169,507}
  payload  = exact finite source theorem for R_m^e
  route    = inverse exponent in F_p^*, then ordinary one-row intake

support_period156_value
  object   = canonical H0/Y_507 or one legal row with support-period-156 bridge
  payload  = finite value theorem with branch/root/telescoping or additive normalization
  route    = period-156 value hook, then source-stage normalization
```

Support or heavy routes:

```text
q_yang_support_route
  object   = mixed conductor-39 Q/Yang/H90 object tied to one legal row
  payload  = finite Q or Q^3 theorem plus selector debt paid
  status   = support until oriented split/direct row theorem and finite theorem data appear

matched_quotient_aggregate_route
  object   = aggregate row product R^v plus target row m and exact matched zero-lattice quotient
  payload  = arithmetic theorem for R^v and arithmetic theorem for R^(v - (sum v)e_m), with gcd(sum v,p-1)=1
  status   = support-normalization route; aggregate-only, quotient-only, unmatched, zero-sum, and nonunit-sum packets remain repair

exactp_theta2_upstream
  object   = C,D,K/orientation, equal-weight 75 atoms, or accepted theta2 payload
  payload  = arithmetic theorem carrying exact-P packet and 75->300->12->312->156 bridge
  status   = heavy upstream route into the unified target, not a first-pass shortcut

reverse_unified_to_exactp
  object   = unified support-156 theorem plus exact-P reverse selector data
  payload  = explicit reverse reconstruction to C,D,K/orientation, equal-weight atoms, or theta2 payload
  status   = reject as exact-P recovery without that extra selector structure
```

## Current Falsifiers

```text
source legality only
boundary only
divisor class or value up to unspecified F_p^* scalar
coefficient-sum-one nonunit row vector without matched zero-lattice value
zero-lattice quotient data before a row anchor exists
aggregate-only or unmatched matched-quotient packet
ambient-period-780 value or mu_11 quotient
rowless power value, including rowless 75/169/507 language
Q source language, Q^6 boundary, Q diagonal, or Q-square value without selector/extraction debt paid
exact-P 75-atom vocabulary, finite fixture, KL balance, or unified target alone
finite payload without arithmetic source theorem
```

## Counts

```text
evidence_markers_ok = 12/12
kernel_rows = 7
accepted_source_stage_rows = 3
support_rows = 2
heavy_upstream_rows = 1
reject_rows = 1
current_source_stage_closers = 0
current_submission_ready = 0
p25_v2_current_theorem_kernel_rows=1/1
```

## Verdict

The current theorem kernel is sharp but still open:

```text
Find a challenge-legal arithmetic theorem for one scalar-fixed row, one
row-labeled unique power, or one support-period-156 value with row bridge.
```

Everything else is either support, a heavy exact-P upstream theorem, or a
repair/reject row until it normalizes to one scalar-fixed legal row and then
survives the DANGER3 extraction ladder.
