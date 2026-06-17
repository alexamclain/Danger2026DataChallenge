# P25 v2 Reverse Exact-P Information Loss

Updated: 2026-06-16

## Purpose

Record the non-equivalence between the exact-P moonshot and the unified
H0/conductor-39 first-pass target.  Exact-P remains a stronger upstream
producer, but a theorem for the unified support-156 product does not by itself
recover the exact 75-atom product.

## Pages Read

- `frontier.md`
- `lanes/exact-p.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_exactp_theorem_interface_contract_20260616.md`
- `evidence/p25_v2_exactp_to_unified_target_spine_20260616.md`
- `evidence/p25_v2_unified_group_ring_payload_20260616.md`
- `evidence/p25_v2_post_theorem_extraction_router_20260616.md`

## Command

```bash
python3 research/p25/archive/gates/p25_v2_reverse_exactp_information_loss_gate.py
```

The gate returned `p25_v2_reverse_exactp_information_loss_rows=1/1`.

## Boundary

The forward route is valid:

```text
compact exact-P theorem
-> exact equal-weight 75-atom normalized-y product
-> theta2 / theta2^-1 certificate path
-> Y_507 / Norm_156 bridge spine
-> unified support-156 H0/conductor-39 target
```

The reverse route is not established:

```text
unified support-156 value/divisor theorem
-> exact-P C,D,K,orientation packet
```

The unified group-ring payload records the four support-156 product rows:

```text
m in {1,2,4,8}
coefficient pattern in quotient C4
P/N conductor-39 residue sets
78 positive / 78 negative level-507 factors
boundary Norm_156(Y_507)
```

It does not record the exact-P data:

```text
C = (47, 28)
D = (22, 3)
K = (57, 0)
orientation / theta2 direction
equal-weight 75 normalized-y atoms
```

## Routing Rule

A unified H0/conductor-39 theorem hit should route to the post-theorem
extraction ladder:

```text
source theorem
finite/non-CM framing
same-j X_1(8112)
practical X_1(16) payload
halving/direct x0
official vpp.py
```

It should not be promoted as an exact-P theorem unless it also supplies the
missing exact-P selector data.

## Accepted Reverse Repairs

A future reverse-exact-P claim needs one of:

```text
the exact equal-weight 75-atom theorem
the compact C,D,K,orientation packet
an accepted period-156 theta2 or theta2^-1 divisor/additive payload
an explicit theorem proving the reverse reconstruction
```

Without one of those, the unified theorem is first-pass progress but not a
moonshot exact-P close.

## Verdict

```text
forward_exactp_to_unified = accepted
reverse_unified_to_exactp = rejected without extra selector structure
unified_hit_route = post-theorem extraction, not exact-P recovery
exactp_status = still live as stronger upstream producer
```
