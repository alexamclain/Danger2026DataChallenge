#!/usr/bin/env python3
"""Payload accounting for an oriented recovery-cycle certificate surface.

The selected-chain surface carries a selected degree-n recovery polynomial.
There is a more literal fallback: carry one full oriented recovery cycle for
the composite class

    a = 2 * 463 * 223^(-1),       order(a)=n=3107441.

To verify one step of this oriented product without a huge composite modular
polynomial, a certificate can provide two intermediate j-values per edge:

    j_i --Phi_2-- u_i --Phi_463-- v_i <--Phi_223-- j_{i+1}.

Thus one length-n cycle uses 3n field elements for (j_i,u_i,v_i), plus the
small post-j Montgomery tail.  This is not the preferred final surface and it
does not solve the seed problem, but it is still a strict sub-sqrt finite
artifact for p24 and is a useful fallback target if a producer lands at a
cycle rather than a recovery polynomial.
"""

from __future__ import annotations

from math import isqrt


P = 10**24 + 7
SQRT_FLOOR = isqrt(P)
N = 3_107_441
M = 66_254
COMPOSITE_PATH_PRIMES = (2, 463, -223)
SELECTED_CHAIN_SLOTS = 3_107_811
FULL_RELATIVE_TABLE_SLOTS = 3_174_011

# Small calibrated toy from oriented_composite_path_toy.py:
TOY_CLASS_NUMBER = 30
TOY_MOVE_ORDER = 5
TOY_INDEX = 6


def dense_modular_polynomial_slots(ell: int) -> int:
    """Conservative dense bivariate slots for Phi_ell modulo p."""
    degree = ell + 1
    return (degree + 1) * (degree + 1)


def main() -> None:
    path_intermediates_per_edge = len(COMPOSITE_PATH_PRIMES) - 1
    field_elements_per_edge = 1 + path_intermediates_per_edge
    cycle_path_slots = field_elements_per_edge * N
    post_j_tail_slots = 2  # A and x0; j0 is already one cycle vertex.
    cycle_with_tail_slots = cycle_path_slots + post_j_tail_slots
    dense_phi_slots = sum(
        dense_modular_polynomial_slots(abs(ell))
        for ell in COMPOSITE_PATH_PRIMES
    )
    cycle_with_dense_phi_tables = cycle_with_tail_slots + dense_phi_slots

    toy_cycle_path_slots = field_elements_per_edge * TOY_MOVE_ORDER

    print("oriented recovery-cycle payload gate")
    print(f"p={P}")
    print(f"sqrt_floor={SQRT_FLOOR}")
    print(f"quotient_index_m={M}")
    print(f"recovery_order_n={N}")
    print(f"oriented_composite_path={COMPOSITE_PATH_PRIMES}")
    print(f"path_intermediates_per_edge={path_intermediates_per_edge}")
    print(f"field_elements_per_edge={field_elements_per_edge}")
    print()
    print("p24_payload_counts")
    print(f"selected_chain_slots={SELECTED_CHAIN_SLOTS}")
    print(f"full_relative_table_slots={FULL_RELATIVE_TABLE_SLOTS}")
    print(f"oriented_cycle_path_slots={cycle_path_slots}")
    print(f"oriented_cycle_plus_A_x0_slots={cycle_with_tail_slots}")
    print(f"dense_phi_table_slots_if_serialized={dense_phi_slots}")
    print(f"cycle_plus_tail_plus_dense_phi_slots={cycle_with_dense_phi_tables}")
    print(f"selected_chain_over_sqrt={SELECTED_CHAIN_SLOTS / SQRT_FLOOR:.12e}")
    print(f"oriented_cycle_plus_A_x0_over_sqrt={cycle_with_tail_slots / SQRT_FLOOR:.12e}")
    print(
        "cycle_plus_tail_plus_dense_phi_over_sqrt="
        f"{cycle_with_dense_phi_tables / SQRT_FLOOR:.12e}"
    )
    print()
    print("toy_analogue_counts")
    print(f"toy_class_number={TOY_CLASS_NUMBER}")
    print(f"toy_cycle_order={TOY_MOVE_ORDER}")
    print(f"toy_cycle_index={TOY_INDEX}")
    print(f"toy_oriented_cycle_path_slots={toy_cycle_path_slots}")
    print()
    print("verifier_contract")
    print("  check_j0_equals_j_of_A=1")
    print("  check_DANGER_xonly_replay_for_A_x0=1")
    print("  check_cycle_closes_after_n_steps=1")
    print("  check_cycle_vertices_distinct_for_exact_order=1")
    print("  check_each_step_by_Phi_2_Phi_463_and_Phi_223=1")
    print("interpretation")
    print("  oriented_cycle_payload_is_larger_than_selected_chain_but_subsqrt=1")
    print("  modular_polynomial_tables_are_canonical_not_h_sized=1")
    print("  producer_still_must_find_one_target_cycle_or_final_A_x0=1")
    print("  this_surface_does_not_remove_the_seedless_cycle_problem=1")
    print("conclusion=reported_oriented_recovery_cycle_payload_gate")

    if cycle_with_tail_slots >= SQRT_FLOOR:
        raise SystemExit(1)
    if cycle_with_dense_phi_tables >= SQRT_FLOOR:
        raise SystemExit(1)
    if not (SELECTED_CHAIN_SLOTS < cycle_with_tail_slots):
        raise SystemExit(1)
    if toy_cycle_path_slots != 15:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
