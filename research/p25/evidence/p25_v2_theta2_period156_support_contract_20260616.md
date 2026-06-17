# P25 v2 Theta2 Period-156 Support Contract

Updated: 2026-06-16

## Purpose

Promote the narrow useful part of the older Lane B theta2 work: the finite
theta2/theta2-inverse payload already has a period-156 factor certificate and a
precise intake contract. This page does not claim a source-stage theorem
exists.

## Pages Read

- `frontier.md`
- `lanes/exact-p.md`
- `sources/schertz-scholl.md`
- `evidence/p25_v2_exactp_minimal_hook_20260616.md`
- `evidence/p25_v2_period156_value_source_hook_20260616.md`
- `archive/gates/p25_laneB_robert_ksy_theta2_factor_period_certificate_gate.py`
- `archive/gates/p25_laneB_robert_ksy_theta2_arithmetic_producer_contract_gate.py`
- `archive/gates/p25_laneB_robert_ksy_theta2_d2_theorem_obligation_gate.py`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 \
  python3 research/p25/archive/gates/p25_v2_theta2_period156_support_contract_gate.py
```

The wrapper restores `archive/gates` and `archive/harness` on `sys.path`, so
the preservation-first wiki reorg does not break replay of the older Lane B
checks.

The gate returned `p25_v2_theta2_period156_support_contract_rows=1/1`.

## Factor-Period Certificate

```text
source_group = C_75 x C_169
base = (25,25)
K = (57,0)
D = (22,3)
T = (38,113)
support_period = 156
doubling_power_156_scale = (61,1)
factor_support_budget = 31
expanded_period_budget = 900
proper_divisors_fail_theta2_fixedness = yes
```

At period 156, doubling fixes the base and preserves the 25-point `K` trace.
The `D` and `T` drifts are absorbed by the same `K` trace, so the bridge and
theta2 fixedness can be checked at factor level. Every proper divisor of 156
fails the expanded bridge/theta2 fixedness check.

## Accepted Finite Interfaces

```text
hilbert90_two_signs
source_quotient_packet
quotient_factor_classes
source_factor_tuple
sparse_theta2_divisor
sparse_theta2_inverse_divisor
compact_ksy_theta2
```

The exact-P heavy route may therefore accept a challenge-legal theorem that
emits theta2 or theta2-inverse divisor/additive data, or the compact KSY
center/half/orientation payload.

## Rejected Shortcuts

```text
normalized_y_footprint_as_bridge
coefficient_abs_4_layer_filter
kato_siegel_dlog_chain_rule_alone
formal_two_norm_or_transport
square_root_or_half_dlog_escape
value_unit_without_branch
```

The multiplicative value-only route still has an 11-branch ambiguity:

```text
value_branch_count = 11
finite_bridge_contract_selects_value_branch = no
```

So a Schertz/Scholl/Siegel-Robert value theorem helps only if it supplies
period-156 branch/root/telescoping data or divisor/additive normalization.

## Counts

```text
finite_theta2_support_contracts = 1
accepted_theta2_interfaces = 7
accepted_d2_obligations = 3
current_arithmetic_producers = 0
source_stage_closers = 0
submission_ready_rows = 0
p25_v2_theta2_period156_support_contract_rows=1/1
```

## Verdict

This promotes theta2 as a sharper support payload, not as a theorem. The next
valid exact-P/value-side ask is:

```text
Find a challenge-legal arithmetic identity that emits exact theta2 or
theta2^-1 divisor/additive data, or the compact KSY center/half/orientation
payload, with period-156 branch/root/telescoping context. A value-only unit
claim without explicit branch selection remains repair.
```
