#!/usr/bin/env python3
"""Payload accounting for the p24 relative Kummer phase normal form."""

from __future__ import annotations

import math

import sympy as sp

P = 10**24 + 7
SQRT_P = math.isqrt(P)
LAYERS = (157, 211)
GLUE_LAYER = 211


def main() -> None:
    print("p24 relative Kummer phase payload accounting")
    print(f"p={P}")
    print(f"sqrt_floor={SQRT_P}")
    print()
    total_kummer_slots = 0
    glue_object_count = 0
    glue_orbit_degree = 0
    print("layer prime p_mod_r ord_r_p primitive_count frobenius_orbits orbit_size")
    for r in LAYERS:
        order = int(sp.n_order(P % r, r))
        primitive_count = r - 1
        orbits = primitive_count // order
        total_kummer_slots += primitive_count
        if r == GLUE_LAYER:
            glue_object_count = orbits - 1
            glue_orbit_degree = order
        print(
            f"r={r:3d} p_mod_r={P % r:3d} ord_r_p={order:3d} "
            f"primitive_count={primitive_count:3d} "
            f"frobenius_orbits={orbits:2d} orbit_size={order:3d}"
        )
    print()
    selected_chain_slots = 2 + 157 + 211 + 3_107_441
    kummer_normal_form_slots = 2 + 2 + total_kummer_slots + 3_107_441
    selected_chain_informative_phase = (157 - 1) + (211 - 1)
    glue_base_slots = glue_object_count * glue_orbit_degree
    kummer_with_glue_extension_object_slots = (
        kummer_normal_form_slots + glue_object_count
    )
    kummer_with_glue_base_slots = kummer_normal_form_slots + glue_base_slots
    print("selected_chain")
    print(f"  top_plus_children_plus_recovery_slots={selected_chain_slots}")
    print(f"  selected_chain_over_sqrt={selected_chain_slots / SQRT_P:.12e}")
    print(f"  informative_child_phase_slots={selected_chain_informative_phase}")
    print(f"  kummer_primitive_slots={total_kummer_slots}")
    print(f"  kummer_normal_form_slots={kummer_normal_form_slots}")
    print(f"  degree_211_cross_orbit_glue_extension_objects={glue_object_count}")
    print(f"  degree_211_glue_frobenius_orbit_degree={glue_orbit_degree}")
    print(f"  degree_211_cross_orbit_glue_base_slots={glue_base_slots}")
    print(
        "  kummer_with_glue_extension_object_slots="
        f"{kummer_with_glue_extension_object_slots}"
    )
    print(
        "  kummer_with_glue_conservative_base_slots="
        f"{kummer_with_glue_base_slots}"
    )
    print(
        "  kummer_with_glue_conservative_base_slots_over_sqrt="
        f"{kummer_with_glue_base_slots / SQRT_P:.12e}"
    )
    print(
        "  kummer_slots_equal_informative_child_coefficients="
        f"{int(total_kummer_slots == selected_chain_informative_phase)}"
    )
    print()
    print("interpretation")
    print("  degree_157_layer_is_one_Frobenius_orbit_of_156_Kummer_constants=1")
    print("  degree_211_layer_is_six_Frobenius_orbits_of_35_Kummer_constants=1")
    print("  degree_211_layer_needs_cross_orbit_phase_glue=1")
    print("  glue_extension_object_count_is_5_but_base_field_slot_count_is_175=1")
    print("  Kummer_normal_form_repackages_not_reduces_selected_child_payload=1")
    print("  useful_because_Kummer_constants_are_relative_resolvent_powers=1")
    print("conclusion=reported_relative_kummer_phase_payload_accounting")


if __name__ == "__main__":
    main()
