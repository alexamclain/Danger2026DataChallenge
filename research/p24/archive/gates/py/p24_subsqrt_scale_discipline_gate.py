#!/usr/bin/env python3
"""Scale discipline for p24 sub-sqrt certificate candidates.

Some p24 artifacts are genuinely quotient/recovery-scale, while others are
only constant-factor variants of the forbidden class-set/sqrt scale.  This
gate keeps those categories separate.

The most tempting near miss is the oriented composite correspondence
2 * 463 * 223^(-1): its optimistic seeded proxy is just below sqrt(p), but it
is still proportional to the full recovery projector support times a
correspondence degree.  That is not the asymptotic speedup requested by the
goal.
"""

from __future__ import annotations

P24 = 10**24 + 7
SQRT_FLOOR = 10**12
CLASS_NUMBER = 205880396014
M = 66254
N = 3107441

HCOSSET_VERIFIER = 1092
TRACE_PLUS_CHILD = 2 * M
SELECTED_CHAIN = 2 + 157 + 211 + N
FULL_RELATIVE_TABLE = 2 + 2 * 157 + (2 * 157) * 211 + N

COMPOSITE_DELTA = 311808
COMPOSITE_SEEDED_PROXY = COMPOSITE_DELTA * N


def main() -> None:
    print("p24 sub-sqrt scale discipline gate")
    print(f"p24={P24}")
    print(f"sqrt_floor={SQRT_FLOOR}")
    print(f"class_number={CLASS_NUMBER}")
    print(f"m={M}")
    print(f"n={N}")
    print(f"m_times_n_equals_h={int(M * N == CLASS_NUMBER)}")
    print(f"class_number_over_sqrt={CLASS_NUMBER / SQRT_FLOOR:.12e}")
    print(f"hcoset_verifier_scalars={HCOSSET_VERIFIER}")
    print(f"hcoset_verifier_over_sqrt={HCOSSET_VERIFIER / SQRT_FLOOR:.12e}")
    print(f"trace_plus_child_payload={TRACE_PLUS_CHILD}")
    print(f"trace_plus_child_over_sqrt={TRACE_PLUS_CHILD / SQRT_FLOOR:.12e}")
    print(f"selected_chain_payload={SELECTED_CHAIN}")
    print(f"selected_chain_over_sqrt={SELECTED_CHAIN / SQRT_FLOOR:.12e}")
    print(f"full_relative_table_payload={FULL_RELATIVE_TABLE}")
    print(f"full_relative_table_over_sqrt={FULL_RELATIVE_TABLE / SQRT_FLOOR:.12e}")
    print(f"selected_chain_gain_factor={SQRT_FLOOR // SELECTED_CHAIN}")
    print(f"full_relative_table_gain_factor={SQRT_FLOOR // FULL_RELATIVE_TABLE}")
    print(f"composite_correspondence_delta={COMPOSITE_DELTA}")
    print(f"composite_seeded_proxy={COMPOSITE_SEEDED_PROXY}")
    print(f"composite_seeded_proxy_over_sqrt={COMPOSITE_SEEDED_PROXY / SQRT_FLOOR:.12e}")
    print(f"composite_delta_over_m={COMPOSITE_DELTA / M:.12e}")
    print(f"composite_seeded_proxy_over_h={COMPOSITE_SEEDED_PROXY / CLASS_NUMBER:.12e}")
    print(f"composite_seeded_proxy_over_selected_chain={COMPOSITE_SEEDED_PROXY / SELECTED_CHAIN:.12e}")
    print("interpretation")
    print("  hcoset_equations_are_verifier_scalars_not_producer_scale=1")
    print("  trace_plus_child_is_anchor_payload_not_full_j_certificate=1")
    print("  selected_chain_and_full_relative_table_are_genuine_subsqrt_surfaces_for_p24=1")
    print("  h_sized_class_table_is_rejected_even_though_h_less_than_sqrt_for_this_p=1")
    print("  composite_seeded_correspondence_is_constant_factor_sqrt_scale=1")
    print("  asymptotic_speedup_requires_quotient_recovery_or_punit_producer_not_seeded_walk=1")
    print("conclusion=reported_p24_subsqrt_scale_discipline_gate")

    if M * N != CLASS_NUMBER:
        raise SystemExit(1)
    if not (HCOSSET_VERIFIER < TRACE_PLUS_CHILD < SELECTED_CHAIN < FULL_RELATIVE_TABLE < SQRT_FLOOR):
        raise SystemExit(1)
    if COMPOSITE_SEEDED_PROXY >= SQRT_FLOOR:
        raise SystemExit(1)
    if COMPOSITE_SEEDED_PROXY <= 100 * SELECTED_CHAIN:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
