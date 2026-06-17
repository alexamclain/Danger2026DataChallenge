# P25 v2 Exact-P To Unified Target Spine

Updated: 2026-06-16

## Purpose

Check whether exact-P is a separate downstream moonshot target, or a stronger
upstream producer for the same unified H0/conductor-39 finite target.

## Pages Read

- `frontier.md`
- `lanes/exact-p.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `concepts/transfer-matrix.md`
- `evidence/p25_v2_exactp_theorem_interface_contract_20260616.md`
- `evidence/p25_v2_h0_conductor39_unified_target_20260616.md`

## Command

```bash
PYTHONPATH=research/p25/archive/gates:research/p25/archive/harness \
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_exactp_to_unified_target_spine_gate.py
```

The gate returned `p25_v2_exactp_to_unified_target_spine_rows=1/1`.

## Spine

The verified finite ladder is:

```text
compact exact-P interface
  C=(47,28), D=(22,3), primitive K=(57,0), orientation
  base = C-D
  T = -2C+K

-> exact equal-weight normalized-y product
-> theta2 / theta2^-1 certificate path
-> Y_507 / Norm_156 bridge spine
-> unified H0/conductor-39 support-156 product family
```

Counts:

```text
source parameter budget = 31
atom count = 75
theta2 payload support = 300
quotient Y_507 support = 12
period norm support = 312
unified H90 support = 156
unified lift = 78 positive / 78 negative
unified target rows = 4
```

## One-Way Implication

The implication is one-way:

```text
exact-P theorem hit -> unified H0/conductor-39 target
unified target theorem hit -> exact-P theorem hit is not proved
```

So exact-P is not a separate downstream target. It is a stronger upstream
producer for the same support-156 H0/conductor-39 family.

## Current Meaning

The theorem search now has a clean ladder:

```text
cheaper first-pass route:
  prove finite value/divisor theorem for one unified support-156 product

heavier exact-P route:
  prove the compact exact-P identity, which would feed the same unified target
  through the 75 -> 300 -> 12 -> 312 -> 156 bridge
```

The exact-P route remains harder because it must still produce the exact
equal-weight 75-atom normalized-y product or an accepted equivalent
theta2/divisor payload.

## Falsifiers

Reject a proposed exact-P-to-unified claim if it:

```text
skips the exact equal-weight normalized-y product
emits only raw KL exponent balance
treats the unified H0/conductor-39 theorem as proving exact-P
collapses the one-way bridge into an equivalence
loses period-156 branch/root/telescoping context for value-level claims
omits DANGER3 framing and extraction after the finite theorem
```

## Verdict

```text
continue_exactp = yes
continue_unified_first_pass = yes
frontier_shape = one downstream finite target family with a stronger exact-P
                 upstream producer route
still_missing_exactp = challenge-legal arithmetic producer for compact exact-P
still_missing_unified = finite value/divisor theorem for support-156 product
submission_gap = DANGER3 framing, same-j X_1(8112), X_1(16), halving, vpp.py
```
