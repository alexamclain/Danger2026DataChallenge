#!/usr/bin/env python3
"""Machine-readable theorem manifest for the p24 two-resultant route.

This is not a certificate producer.  It records the exact arithmetic
nonvanishing theorem that would make the conditional four-field-element
trace-GCD certificate sound.
"""

from __future__ import annotations

import json

import sympy as sp


P = 10**24 + 7
SQRT_P_FLOOR = 10**12
TRACE = -1178414874616
D_K = -652834595820939249713143
CLASS_NUMBER = 205880396014
N = 3107441
LEFT = 157
RIGHT = 211
M = CLASS_NUMBER // N
LEFT_DIM = 156
RIGHT_ORBIT_LEN = 35
PREFIX_BLOCKS = 4
PREFIX_DIM = PREFIX_BLOCKS * RIGHT_ORBIT_LEN
TAIL_LEN = LEFT_DIM - PREFIX_DIM
UNIT = 2


def frobenius_orbits(modulus: int, q: int, include_zero: bool) -> list[list[int]]:
    seen: set[int] = set()
    out: list[list[int]] = []
    starts = range(modulus) if include_zero else range(1, modulus)
    for start in starts:
        if start in seen:
            continue
        orbit: list[int] = []
        value = start
        while value not in seen:
            seen.add(value)
            orbit.append(value)
            value = (value * q) % modulus
        out.append(orbit)
    return out


def orbit_labels(orbits: list[list[int]]) -> dict[int, int]:
    return {
        value: index
        for index, orbit in enumerate(orbits)
        for value in orbit
    }


def unit_mapping(unit: int, orbits: list[list[int]]) -> dict[str, str]:
    labels = orbit_labels(orbits)
    return {
        f"O{index}": f"O{labels[(unit * orbit[0]) % RIGHT]}"
        for index, orbit in enumerate(orbits)
    }


def main() -> None:
    right_orbits = frobenius_orbits(RIGHT, P % RIGHT, include_zero=True)
    nonzero_orbits = [orbit for orbit in right_orbits if orbit != [0]]
    right_orbit_map = {
        f"O{index}": orbit for index, orbit in enumerate(right_orbits)
    }
    class_factorization = sp.factorint(CLASS_NUMBER)
    discriminant_factorization = sp.factorint(abs(D_K))
    class_number_squarefree = all(
        exponent == 1 for exponent in class_factorization.values()
    )
    discriminant_squarefree = all(
        exponent == 1 for exponent in discriminant_factorization.values()
    )
    theorem = {
        "name": "p24_trace_gcd_two_resultant_theorem_manifest",
        "p": P,
        "sqrt_p_floor": SQRT_P_FLOOR,
        "trace": TRACE,
        "D_K": D_K,
        "trace_discriminant_equals_4D": TRACE * TRACE - 4 * P == 4 * D_K,
        "class_number": CLASS_NUMBER,
        "factor_class_number": {
            str(prime): exponent
            for prime, exponent in class_factorization.items()
        },
        "class_group_structure": {
            "class_number_squarefree": class_number_squarefree,
            "abelian_squarefree_class_group_hence_cyclic": class_number_squarefree,
            "unique_cyclic_layers": [2, LEFT, RIGHT, 3107441],
            "genus_quotient_order": 2,
            "odd_layers_are_non_genus": True,
        },
        "discriminant_structure": {
            "factor_abs_D_K": {
                str(prime): exponent
                for prime, exponent in discriminant_factorization.items()
            },
            "D_K_squarefree": discriminant_squarefree,
            "D_K_mod_4": D_K % 4,
            "D_K_mod_8": D_K % 8,
        },
        "ordinary_prime_orientations": {
            "sqrtD_equals_plus_t_over_2_mod_p": (TRACE // 2) % P,
            "sqrtD_equals_minus_t_over_2_mod_p": (-(TRACE // 2)) % P,
        },
        "levels_prime_to_p": {
            str(level): sp.gcd(P, level) == 1
            for level in [2, LEFT, RIGHT, 2 * LEFT * RIGHT, 3107441, CLASS_NUMBER]
        },
        "left": {
            "modulus": LEFT,
            "p_mod": P % LEFT,
            "frobenius_order": int(sp.n_order(P % LEFT, LEFT)),
            "dimension": LEFT_DIM,
        },
        "right": {
            "modulus": RIGHT,
            "p_mod": P % RIGHT,
            "frobenius_order": int(sp.n_order(P % RIGHT, RIGHT)),
            "orbits": right_orbit_map,
            "unit": UNIT,
            "unit_mapping": unit_mapping(UNIT, right_orbits),
        },
        "representative_support": {
            "deleted_orbit": "O4",
            "prefix_orbits": ["O2", "O3", "O5", "O6"],
            "tail_orbit": "O1",
            "tail_len": TAIL_LEN,
            "prefix_dim": PREFIX_DIM,
            "source_dim": LEFT_DIM,
            "bad_support_size": RIGHT_ORBIT_LEN + (RIGHT_ORBIT_LEN - TAIL_LEN),
        },
        "diamond_support_transport": {
            "audit": "p24/diamond_support_transport_audit.py",
            "unit": UNIT,
            "deleted_cycle_covers_all_nonzero_orbits": True,
            "tail_cycle_covers_all_nonzero_orbits": True,
            "prefix_blocks_preserved": PREFIX_BLOCKS,
            "tail_windows_frobenius_contiguous": True,
            "final_tail_orbit": "O1",
            "final_tail_rotation_start": 17,
            "requires_internal_frobenius_rotation": True,
        },
        "full_product_determinant_line_equivariance": {
            "theorem": "p24/full_product_determinant_line_equivariance_theorem.md",
            "toy": "p24/full_product_determinant_transport_toy.py",
            "algebra": "A_211 = O_p[zeta_211], finite etale since p is prime to 211",
            "commuting_square": "B_2O d_K,O = d_T,O B_O",
            "determinant_relation": "Xi_2O = det(d_T,O) det(d_K,O)^(-1) Xi_O",
            "six_step_closure": "2^6 = p^17 mod 211",
            "literal_scalar_equality_required": False,
            "proves_transport_not_nonvanishing": True,
        },
        "two_resultant_arithmetic_inputs": {
            "Xi_O0": (
                "Res_p-lin(P_K0,T_0) is a p-unit for the fixed right orbit"
            ),
            "Xi_O1": (
                "Nrd_O1(Res_p-lin(P_Kt,T_t)) is a p-unit for one nonzero "
                "Frobenius orbit"
            ),
            "diamond_transport": (
                "multiplication by 2 on the right 211-phase transports "
                "determinant lines around O1..O6 by p-unit factors"
            ),
        },
        "diamond_transport_denominator_hygiene": {
            "criterion": "epsilon_O = det(d_T,O) * det(d_K,O)^(-1)",
            "lean_lemmas": [
                "punit_transition_from_integral_det_transport",
                "punit_arrow_from_commuting_integral_det_transport",
                "p24_unit2_prime_to_right_level",
                "p24_transport_denominators_prime_to_p",
                "p24_unit2_six_steps_is_frobenius_rotation17",
            ],
            "visible_denominators": [2, 7, 30, 35, 156, 157, 211, 5460, 66254, CLASS_NUMBER],
            "all_visible_denominators_prime_to_p": all(
                sp.gcd(P, denominator) == 1
                for denominator in [2, 7, 30, 35, 156, 157, 211, 5460, 66254, CLASS_NUMBER]
            ),
            "audit": "p24/diamond_transport_unit_denominator_audit.py",
        },
        "finite_payload": {
            "field_elements": 4,
            "ratio_to_sqrt_floor": 4 / SQRT_P_FLOOR,
            "values": ["Xi_O0", "Xi_O0_inverse", "Xi_O1", "Xi_O1_inverse"],
        },
        "payload_scale_discipline": {
            "gate": "p24/p24_subsqrt_scale_discipline_gate.py",
            "hcoset_verifier_scalars": LEFT_DIM * 7,
            "trace_plus_child_anchor_payload": 2 * M,
            "selected_chain_payload": 2 + 157 + 211 + N,
            "full_relative_table_payload": 2 + 2 * 157 + (2 * 157) * 211 + N,
            "composite_seeded_correspondence_proxy": 311808 * N,
            "composite_proxy_is_sqrt_scale_not_asymptotic": True,
        },
        "separate_hcoset_verifier_interface": {
            "left_rows": LEFT_DIM,
            "right_h_cosets": 7,
            "scalar_equations": LEFT_DIM * 7,
            "nontrivial_character_equations": 6 * LEFT_DIM,
            "ordinary_centering_equations": LEFT_DIM,
            "not_fitting_payload_count": True,
        },
        "fixed_frequency_order7_handoff": {
            "lean": "p24/lean/TraceGcdFixedFrequencyOrder7Gate.lean",
            "right_axis_anchor_lean": "p24/lean/TraceGcdRightAxisAnchorDescentGate.lean",
            "augmentation_identity": "T + P2 + P3 + P4 + P5 + P6 = 0 in R_7 tensor L",
            "negation_covariance": "P4 = y^(-2) T",
            "denominator_unit": "1 + y^(-2) is a unit in R_7",
            "right_axis_equivalence": "under Y_{c+6}=rho(Y_c), rho(Y0)=Y0 iff all seven H-coset sums are equal",
            "nontrivial_character_equations": 6,
            "fixed_frequency_relations": 7,
            "stable_support_candidates_before": 1260,
            "stable_support_candidates_after_no_fixed_defect": 35,
            "proves_finite_handoff_not_augmentation": True,
        },
        "period_coset_balance_handoff": {
            "gate": "p24/trace_gcd_fixed_frequency_p24_period_coset_balance_gate.py",
            "anchor_trace_defect_gate": (
                "p24/trace_gcd_fixed_frequency_p24_anchor_trace_defect_gate.py"
            ),
            "trace_average_anchor_payload_gate": (
                "p24/trace_gcd_fixed_frequency_p24_trace_average_anchor_payload_gate.py"
            ),
            "section_choice_obstruction_gate": (
                "p24/trace_gcd_fixed_frequency_p24_section_choice_obstruction_gate.py"
            ),
            "lean_trace_average_payload_gate": (
                "p24/lean/TraceGcdAnchorTraceAveragePayloadGate.lean"
            ),
            "internal_generator": "Q=p^5460 mod n=209035",
            "internal_subgroup_order": 5549,
            "nonzero_internal_cosets": (N - 1) // 5549,
            "recombined_subgroup_order": 388430,
            "recombined_nonzero_cosets": (N - 1) // 388430,
            "E_idempotents_per_Fp_factor": 388430 // 5549,
            "right_nontrivial_characters": 6,
            "recombined_scalar_equations": 6 * ((N - 1) // 388430),
            "recombined_nontrivial_octic_equations": 6 * (((N - 1) // 388430) - 1),
            "recombined_anchor_equations": 6,
            "recombined_compressed_values_with_c0": 6 * (((N - 1) // 388430) + 1),
            "coefficient_balance": (
                "sum_{k in D} c_k(chi) = 5549*c_0(chi) for every "
                "nonzero <Q>-coset D"
            ),
            "recombined_coefficient_balance": (
                "sum_{k in D} c_k(chi) = 388430*c_0(chi) for every "
                "nonzero <p>-coset D"
            ),
            "anchor_trace_defect_form": (
                "sum_r chi^-1(r)*(Tr_relative(j_{r+m*bullet}) - n*j_r)=0"
            ),
            "anchor_trace_defect_equivalence": (
                "six anchors zero iff relative trace defect has equal right H-coset sums"
            ),
            "trace_only_compression_status": (
                "false: quotient trace profile alone does not determine the anchor; "
                "selected child section or equivalent defect data is required"
            ),
            "anchor_defect_hcoset_sum_payload": 7,
            "trace_average_plus_child_payload": 2 * M,
            "scope": "per-factor balance is strong; complete recombination gives the 8-coset target",
        },
        "finite_gates": [
            "p24/lean/CyclicTowerSectionObstructionGate.lean",
            "p24/lean/TraceGcdCrossedCoinvariantNormGate.lean",
            "p24/lean/TraceGcdLinearizedResultantNormGate.lean",
            "p24/lean/TraceGcdDiamondEquivarianceGate.lean",
            "p24/lean/TraceGcdTwoOrbitCompressionGate.lean",
            "p24/lean/TraceGcdOrdinaryFittingCriterionGate.lean",
            "p24/lean/TraceGcdFixedFrequencyOrder7Gate.lean",
            "p24/lean/TraceGcdRightAxisAnchorDescentGate.lean",
        ],
        "best_holdout_falsifier": "p24/trace_gcd_two_resultant_holdout_audit.py",
        "false_shortcuts": [
            "ordinary F_p[Y] resultant for the nonzero orbit",
            "literal equality of printed unit-translated orbit norms",
            "small right-binomial or low-Heegner unit span",
            "generic cyclic uncertainty without the actual CM trace family",
        ],
        "missing_theorem": (
            "prove the two p-unit nonvanishing statements and the p-unit "
            "diamond determinant-line transport from embedded 157/211 "
            "phase-aware Fitting data, without enumerating the class set"
        ),
    }
    print(json.dumps(theorem, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
