#!/usr/bin/env python3
"""Degree bookkeeping for the first-trace level-2^19 temptation.

Since the split prime above 2 is a full class-group generator for the first
strict trace, the desired quotient by <g^19> can be described as residues
modulo 19 along a horizontal 2-isogeny cycle.  It is tempting to replace the
subgroup average by level 2^19 data.

This audit separates the degrees:

* X0(2^19) -> X(1) has small modular degree 3*2^18.
* the particular horizontal 2^19 edge/path has full CM class orbit h.
* the quotient degree 19 appears only after summing over the whole <g^19>
  orbit of size h/19.
"""

from __future__ import annotations

import math

import sympy as sp


P = 10**24 + 7
TRACE = 1020608380936
D_K = -739589633190799177940983
H = 278733727154
MOVE = 19
QUOTIENT = 19
RECOVERY = H // QUOTIENT
SQRT_P = math.isqrt(P)


def gamma0_index_power2(level_exp: int) -> int:
    return 3 * (1 << (level_exp - 1))


def main() -> None:
    gamma0 = gamma0_index_power2(MOVE)
    unoriented_edge_orbit = H
    fricke_stabilizer_possible = int((2 * MOVE) % H == 0)
    subgroup_projector_support = RECOVERY

    print("order-19 power-2-level audit")
    print(f"p={P}")
    print(f"sqrt_floor={SQRT_P}")
    print(f"trace={TRACE}")
    print(f"D_K={D_K}")
    print(f"class_number_h={H}")
    print(f"class_number_factor={sp.factorint(H)}")
    print(f"split2_class_order={H}")
    print(f"move_power=19")
    print(f"subgroup=<g^19>")
    print(f"quotient_degree={QUOTIENT}")
    print(f"recovery_degree={RECOVERY}")
    print()

    print("level_2_power_data")
    print(f"  X0_2^19_degree_to_j={gamma0}")
    print(f"  X0_2^19_degree_over_sqrt={gamma0 / SQRT_P:.6e}")
    print(f"  horizontal_edge=(j_i,j_i+19)")
    print(f"  oriented_horizontal_edge_class_orbit={H}")
    print(f"  unoriented_horizontal_edge_class_orbit={unoriented_edge_orbit}")
    print(f"  fricke_swap_stabilizes_edge={fricke_stabilizer_possible}")
    print(f"  edge_orbit_over_sqrt={unoriented_edge_orbit / SQRT_P:.6e}")
    print()

    print("quotient_projector")
    print(f"  desired_component=sum_k j_(r+19*k)")
    print(f"  projector_support={subgroup_projector_support}")
    print(f"  projector_support_over_sqrt={subgroup_projector_support / SQRT_P:.6e}")
    print(f"  quotient_degree_after_projector={QUOTIENT}")
    print()

    print("interpretation")
    print("  small_modular_map_degree=1")
    print("  large_class_stabilizer_from_level_data=0")
    print("  horizontal_2^19_edge_is_a_long_edge_not_a_coset_average=1")
    print("  quotient_requires_subgroup_projector_or_character_traces=1")
    print(
        "conclusion=level_2^19_data_does_not_by_itself_construct_the_"
        "order19_period_quotient"
    )


if __name__ == "__main__":
    main()
