# p24 Sub-Sqrt Scale Discipline Gate

Date: 2026-06-06

## Point

This gate separates genuine quotient/recovery-scale certificate surfaces from
constant-factor variants of the forbidden class-set/sqrt scale.

For p24:

```text
sqrt(p) = 1000000000000
h = 205880396014
m = 66254
n = 3107441
h = m*n
```

The selected-chain and full-relative-table surfaces are genuinely far below
sqrt for this instance:

```text
selected chain:       3107811 = 3.107811e-6 * sqrt(p)
full relative table:  3174011 = 3.174011e-6 * sqrt(p)
```

By contrast, the oriented composite correspondence
`2 * 463 * 223^(-1)` has optimistic seeded proxy:

```text
311808 * 3107441 = 968924963328
                  = 0.968924963328 * sqrt(p).
```

That is numerically below `sqrt(p)` for this p, but it is still
constant-factor sqrt/class-table scale, not the requested asymptotic
speedup.  It is also an optimistic seeded/oriented proxy, not a seedless
producer.

## Checked Gate

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/p24_subsqrt_scale_discipline_gate.py
```

Key markers:

```text
m_times_n_equals_h=1
hcoset_verifier_scalars=1092
trace_plus_child_payload=132508
selected_chain_payload=3107811
full_relative_table_payload=3174011
composite_seeded_proxy=968924963328
composite_seeded_proxy_over_sqrt=9.689249633280e-01
composite_seeded_proxy_over_selected_chain=3.117708777426e+05
hcoset_equations_are_verifier_scalars_not_producer_scale=1
trace_plus_child_is_anchor_payload_not_full_j_certificate=1
selected_chain_and_full_relative_table_are_genuine_subsqrt_surfaces_for_p24=1
h_sized_class_table_is_rejected_even_though_h_less_than_sqrt_for_this_p=1
composite_seeded_correspondence_is_constant_factor_sqrt_scale=1
asymptotic_speedup_requires_quotient_recovery_or_punit_producer_not_seeded_walk=1
```
