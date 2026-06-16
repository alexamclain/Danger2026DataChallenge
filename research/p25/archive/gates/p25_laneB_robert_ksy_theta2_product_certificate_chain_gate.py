#!/usr/bin/env python3
"""Certificate chain from normalized-y product to the p25 bridge.

The normalized-y product gate identifies a concrete finite KSY source law:

    prod_A y(A) / y(A+T) = theta2^-1.

This gate records the verifier path from that product payload to the bridge:
theta2^-1 recovers `-bridge` by the finite resolvent, the reversed quotient
recovers `bridge`, and the compact telescoping certificate provides the
smallest current certificate skeleton once the arithmetic product is proved.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_robert_ksy_theta2_normalized_y_product_gate import (
    profile_normalized_y_product,
    profile_normalized_y_product_source_law,
)
from p25_laneB_robert_ksy_theta2_support_resolvent_gate import (
    theta2_support_resolvent_profile,
)
from p25_laneB_robert_ksy_theta2_telescoping_certificate_gate import (
    profile_telescoping_certificate,
)
from p25_laneB_square_axis_bridge_raw_source_character_gate import (
    BASE_POINT,
    BRIDGE_SHIFT,
    D_SHIFT,
    KERNEL_SHIFT,
)


@dataclass(frozen=True)
class ProductCertificateChainProfile:
    product_source_law_ok: bool
    forward_product_exact_theta2_inverse: bool
    forward_product_recovered_sign: int
    forward_product_normalized_bridge_ok: bool
    reversed_product_exact_theta2: bool
    reversed_product_recovered_sign: int
    reversed_product_bridge_ok: bool
    controls_rejected: bool
    support_resolvent_ok: bool
    telescoping_certificate_ok: bool
    source_parameter_budget: int
    theta2_payload_support: int
    bridge_support: int
    support_resolvent_term_budget: int
    support_resolvent_union_support: int
    telescoping_compact_budget: int
    certificate_budget_improvement_factor: int
    orientation_rule: str
    remaining_theorem_debt: str
    row_ok: bool


def profile_product_certificate_chain() -> ProductCertificateChainProfile:
    source_law = profile_normalized_y_product_source_law()
    forward = profile_normalized_y_product(
        "product_chain_forward_theta2_inverse",
        BASE_POINT,
        KERNEL_SHIFT,
        D_SHIFT,
        BRIDGE_SHIFT,
    )
    reversed_product = profile_normalized_y_product(
        "product_chain_reversed_theta2",
        BASE_POINT,
        KERNEL_SHIFT,
        D_SHIFT,
        BRIDGE_SHIFT,
        reverse=True,
    )
    support_resolvent = theta2_support_resolvent_profile()
    telescoping = profile_telescoping_certificate()
    controls_rejected = (
        source_law.missing_k_rejected
        and source_law.collapsed_k_rejected
        and source_law.truncated_d_rejected
        and source_law.wrong_d_rejected
        and source_law.wrong_t_rejected
    )
    row_ok = (
        source_law.row_ok
        and forward.ok
        and forward.exact_theta2_inverse
        and forward.candidate_profile.recovered_sign == -1
        and forward.candidate_profile.normalized_recovered_profile.ok
        and reversed_product.ok
        and reversed_product.exact_theta2
        and reversed_product.candidate_profile.recovered_sign == 1
        and reversed_product.candidate_profile.normalized_recovered_profile.ok
        and controls_rejected
        and support_resolvent.row_ok
        and telescoping.row_ok
        and source_law.source_parameter_budget == 31
        and forward.footprint_support == 300
        and forward.candidate_profile.recovered_support == 150
        and support_resolvent.support_resolvent_term_budget == 46800
        and telescoping.compact_linear_cell_check_budget == 975
        and telescoping.compact_budget_improvement_factor == 48
    )
    return ProductCertificateChainProfile(
        product_source_law_ok=source_law.row_ok,
        forward_product_exact_theta2_inverse=forward.exact_theta2_inverse,
        forward_product_recovered_sign=forward.candidate_profile.recovered_sign,
        forward_product_normalized_bridge_ok=forward.candidate_profile.normalized_recovered_profile.ok,
        reversed_product_exact_theta2=reversed_product.exact_theta2,
        reversed_product_recovered_sign=reversed_product.candidate_profile.recovered_sign,
        reversed_product_bridge_ok=reversed_product.candidate_profile.normalized_recovered_profile.ok,
        controls_rejected=controls_rejected,
        support_resolvent_ok=support_resolvent.row_ok,
        telescoping_certificate_ok=telescoping.row_ok,
        source_parameter_budget=source_law.source_parameter_budget,
        theta2_payload_support=forward.footprint_support,
        bridge_support=forward.candidate_profile.recovered_support,
        support_resolvent_term_budget=support_resolvent.support_resolvent_term_budget,
        support_resolvent_union_support=support_resolvent.support_resolvent_union_support,
        telescoping_compact_budget=telescoping.compact_linear_cell_check_budget,
        certificate_budget_improvement_factor=telescoping.compact_budget_improvement_factor,
        orientation_rule=(
            "forward y(A)/y(A+T) gives theta2^-1 and recovers -bridge; "
            "reverse y(A+T)/y(A) gives theta2 and recovers bridge"
        ),
        remaining_theorem_debt=(
            "prove the normalized-y product is a challenge-legal arithmetic "
            "object; this gate only verifies the finite certificate chain"
        ),
        row_ok=row_ok,
    )


def main() -> int:
    print("p25 Lane B Robert KSY normalized-y product-to-certificate chain gate")
    profile = profile_product_certificate_chain()
    print(f"product_certificate_chain_profile={profile}")
    print("product_certificate_chain_laws")
    print("  forward_normalized_y_product_emits_theta2_inverse_and_recovers_negative_bridge=1")
    print("  reversed_normalized_y_product_emits_theta2_and_recovers_bridge=1")
    print("  support_period_resolvent_budget_is_46800_terms=1")
    print("  compact_telescoping_certificate_budget_is_975_cells=1")
    print("  missing_K_collapsed_K_truncated_D_wrong_D_and_wrong_T_controls_fail=1")
    print("interpretation")
    print("  theorem_proof_of_the_product_identity_would_feed_the_existing_theta2_certificate_path=1")
    print("  arithmetic_legality_of_the_product_remains_the_missing_theorem=1")
    print(f"robert_ksy_theta2_product_certificate_chain_rows={int(profile.row_ok)}/1")
    print("conclusion=reported_p25_laneB_robert_ksy_theta2_product_certificate_chain_gate")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
