#!/usr/bin/env python3
"""Machine-readable manifest for the centered-profile p24 rank certificate."""

from __future__ import annotations

import json


P = 10**24 + 7
LEFT = 157
RIGHT = 211
LEFT_DIM = 156


def manifest() -> dict[str, object]:
    leading_positions = list(range(LEFT_DIM))
    return {
        "name": "p24_centered_profile_moore_certificate_manifest",
        "p": P,
        "left_modulus": LEFT,
        "right_modulus": RIGHT,
        "left_degree": LEFT_DIM,
        "profile_positions": list(range(RIGHT)),
        "centered_relation": "sum_s G_s^0 = 0",
        "candidate_scalar": {
            "name": "M_profile_leading",
            "meaning": (
                "Moore determinant of the first 156 centered right-profile "
                "values G_s^0 in L=F_p(mu_157)"
            ),
            "positions": leading_positions,
            "required_status": "nonzero_mod_p",
        },
        "trace_gram_scalar": {
            "name": "Gamma_profile_leading",
            "meaning": (
                "trace-Gram determinant det(Tr_{L/F_p}(G_s^0*G_t^0)) "
                "for 0 <= s,t < 156"
            ),
            "equivalent_to_candidate_scalar_nonzero": True,
            "identity": "Gamma_profile_leading = M_profile_leading^2",
            "equivalence_scope": "only for the full 156-by-156 square window",
            "required_status": "nonzero_mod_p",
        },
        "base_field_gram_scalar": {
            "name": "B_profile_leading",
            "meaning": (
                "det(A_lead^T*J_inv*A_lead), where A_lead is the 157-by-156 "
                "centered left-coefficient matrix and J_inv is r -> -r mod 157"
            ),
            "identity": "Gamma_profile_leading = 157^156 * B_profile_leading",
            "equivalent_to_candidate_scalar_nonzero": True,
            "required_status": "nonzero_mod_p",
        },
        "base_field_minor_scalar": {
            "name": "D_profile_leading",
            "meaning": (
                "determinant of A_lead after dropping any one left residue row; "
                "the manifest uses dropped row r=0"
            ),
            "identity": "B_profile_leading = 157 * D_profile_leading^2",
            "combined_identity": (
                "Gamma_profile_leading = 157^157 * D_profile_leading^2"
            ),
            "equivalent_to_candidate_scalar_nonzero": True,
            "required_status": "nonzero_mod_p",
        },
        "base_field_difference_minor_scalar": {
            "name": "Delta_C_leading",
            "meaning": (
                "determinant of the leading 156-by-156 square minor of the "
                "doubly-centered marginal C(r,s)=M(r,s)-M(r,0)-M(0,s)+M(0,0), "
                "using rows r=1..156 and columns s=1..156"
            ),
            "sufficient_for_centered_mixed_rank": True,
            "equivalent_to_candidate_scalar_nonzero": False,
            "required_status": "nonzero_mod_p",
        },
        "origin_product_difference_minor_scalar": {
            "name": "Pi_C",
            "meaning": (
                "product over alpha mod 66254 of the alpha-translated "
                "leading difference minors Delta_C(alpha); beta shifts cancel "
                "in the Hermitian pairing"
            ),
            "p24_reduction": (
                "because the left component 157 is odd prime, the left "
                "translation determinant is always +1; Pi_C is the 314th "
                "power of the product over the 211 cyclic right translates"
            ),
            "reduced_factor_count": 211,
            "sufficient_for_delta_c_leading_nonzero": True,
            "required_status": "nonzero_mod_p",
        },
        "cyclic_resultant_difference_minor_scalar": {
            "name": "Pi_C_right",
            "meaning": (
                "the 211-factor right-translation product, equivalently "
                "Res_Y(Y^211 - 1, f_C(Y)) over F_p(mu_211), where f_C "
                "interpolates the right-translation determinant sequence"
            ),
            "factorization_over_Fp": (
                "one value F(0) and six size-35 Frobenius-orbit products; "
                "these are not presently norms of a base-coefficient "
                "interpolant because small analogues fail F(q*t)=F(t); "
                "the exact exterior right-character expansion is dense in "
                "small actual-CM rows"
            ),
            "factor_count": 7,
            "sufficient_for_delta_c_leading_nonzero": True,
            "required_status": "nonzero_mod_p",
        },
        "phase_aware_borcherds_orbit_surface": {
            "name": "Psi_O",
            "meaning": (
                "for each of the seven right Frobenius orbits O, a proposed "
                "p-integral phase-aware Borcherds/Fitting section whose "
                "selected CM value equals the orbit product Pi_O up to p-units"
            ),
            "orbit_count": 7,
            "payload_with_inverses": 14,
            "finite_gate": "p24/lean/CenteredBorcherdsPUnitGate.lean",
            "target_note": "p24/centered_marginal_phase_borcherds_target.md",
            "fitting_target_note": (
                "p24/centered_marginal_crossed_product_fitting_target.md"
            ),
            "required_status": "p_unit_at_selected_prime_above_p",
        },
        "phase_aware_full_origin_surface": {
            "name": "Psi_C_full",
            "meaning": (
                "a proposed p-integral phase-aware Borcherds/Fitting section "
                "whose selected CM value equals the full-origin centered Chow "
                "product up to p-units; by origin covariance this is a p-unit "
                "multiple of Pi_C_right^(975736474)"
            ),
            "full_origin_exponent": 975736474,
            "payload_with_inverse": 2,
            "finite_gate": "p24/lean/CenteredFullOriginBorcherdsGate.lean",
            "power_bridge_note": (
                "p24/centered_marginal_origin_norm_power_theorem.md"
            ),
            "power_bridge_audit": (
                "p24/centered_marginal_origin_norm_power_audit.py"
            ),
            "target_note": "p24/centered_marginal_full_origin_borcherds_gate.md",
            "required_status": "p_unit_at_selected_prime_above_p",
        },
        "sufficient_implication": [
            "M_profile_leading nonzero",
            "span_Fp{G_s^0 : s mod 211}=F_p(mu_157)",
            "rank_Fp C_{157,211}=156",
        ],
        "alternate_difference_minor_implication": [
            "Delta_C_leading nonzero",
            "rank_Fp C_{157,211}=156",
        ],
        "alternate_origin_product_implication": [
            "Pi_C_right nonzero",
            "Pi_C = Pi_C_right^314 nonzero",
            "Delta_C_leading nonzero for the selected embedded origin",
            "rank_Fp C_{157,211}=156",
        ],
        "alternate_normal_frame_route": [
            "the profile span contains the full Frobenius orbit of one normal element",
            "that normal orbit has rank 156",
            "therefore span_Fp{G_s^0 : s mod 211}=F_p(mu_157)",
        ],
        "not_implied": [
            "delete-one right-orbit support",
            "representative leading-erasure p-unit L_rep",
        ],
        "finite_gates": [
            "p24/lean/CenteredProfileGate.lean",
            "p24/lean/CenteredProfilePayloadGate.lean",
            "p24/lean/CenteredArcProductGate.lean",
            "p24/lean/CenteredBorcherdsPUnitGate.lean",
            "p24/lean/CenteredFullOriginBorcherdsGate.lean",
            "p24/lean/CenteredHermitianPluckerGate.lean",
        ],
        "related_notes": [
            "p24/hermitian_mixed_centered_right_profile_theorem.md",
            "p24/relative_content_to_mixed_rank_boundary.md",
            "p24/centered_profile_normal_frame_toy.py",
            "p24/centered_profile_trace_gram_toy.py",
            "p24/centered_profile_moore_trace_gram_identity_toy.py",
            "p24/centered_profile_base_minor_identity_toy.py",
            "p24/centered_marginal_leading_minor_audit.py",
            "p24/centered_marginal_cauchy_binet_audit.py",
            "p24/centered_marginal_origin_product_audit.py",
            "p24/centered_marginal_alpha_sequence_complexity.py",
            "p24/centered_marginal_cyclic_code_boundary.py",
            "p24/centered_marginal_resultant_factor_audit.py",
            "p24/centered_marginal_exterior_dft_audit.py",
            "p24/centered_marginal_exterior_dft_boundary.md",
            "p24/plateau_uncertainty_boundary_toy.py",
            "p24/centered_marginal_plateau_uncertainty_boundary.md",
            "p24/centered_marginal_plateau_intersection_audit.py",
            "p24/centered_marginal_affine_arc_theorem.md",
            "p24/centered_marginal_full_arc_audit.py",
            "p24/centered_marginal_full_arc_boundary.md",
            "p24/centered_marginal_projective_geometry_audit.py",
            "p24/centered_marginal_projective_geometry_boundary.md",
            "p24/centered_marginal_cyclic_resultant_theorem.md",
            "p24/centered_marginal_transversality_boundary.md",
            "p24/centered_profile_theorem_family_synthesis.md",
            "p24/centered_marginal_phase_borcherds_target.md",
            "p24/centered_marginal_chow_integral_model.md",
            "p24/centered_marginal_crossed_product_fitting_target.md",
            "p24/centered_marginal_difference_code_boundary.md",
            "p24/centered_marginal_difference_code_audit.py",
            "p24/centered_marginal_difference_mds_boundary.md",
            "p24/centered_marginal_difference_mds_audit.py",
            "p24/centered_marginal_difference_geometry_boundary.md",
            "p24/centered_marginal_difference_geometry_audit.py",
            "p24/centered_marginal_plucker_kummer_descent_boundary.md",
            "p24/centered_marginal_plucker_kummer_descent_audit.py",
            "p24/centered_marginal_padic_filtration_boundary.md",
            "p24/centered_marginal_padic_filtration_audit.py",
            "p24/lean/CenteredHermitianPluckerGate.lean",
            "p24/centered_marginal_shape_shortlist.py",
            "p24/centered_marginal_holdout_rows_boundary.md",
            "p24/centered_marginal_origin_norm_power_theorem.md",
            "p24/centered_marginal_full_origin_borcherds_gate.md",
            "p24/centered_marginal_origin_norm_power_audit.py",
            "p24/centered_marginal_phase_unit_span_scan.py",
            "p24/centered_marginal_phase_unit_span_boundary.md",
            "p24/centered_marginal_global_product_miner.py",
            "p24/centered_marginal_global_product_mining_boundary.md",
            "p24/centered_plateau_lang_support_audit.py",
            "p24/centered_plateau_factor_support_audit.py",
            "p24/centered_plateau_lang_support_boundary.md",
            "p24/centered_profile_trace_gram_basefield_formula.md",
            "p24/representative_leading_punit_certificate.md",
        ],
        "missing_arithmetic_theorem": (
            "current best surface: prove the phase-aware centered "
            "Schubert/Fitting orbit product Pi_C_right, or equivalently the "
            "closed full-origin centered Chow norm, is a p-unit at the "
            "selected p24 ordinary prime"
        ),
    }


def main() -> None:
    print(json.dumps(manifest(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
