#!/usr/bin/env python3
"""Connect the exact-P contract to the unified H0/conductor-39 target.

This gate checks the current p25 theorem lattice:

    compact exact-P interface
      -> exact equal-weight normalized-y product
      -> theta2 certificate path
      -> Y_507 / Norm_156 bridge spine
      -> unified H0/conductor-39 support-156 product family.

It is intentionally one-way.  A proof of the compact exact-P identity would
feed the unified target, but a value/divisor theorem for the unified target
does not recover the exact 75-atom product by itself.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys


GATE_DIR = Path(__file__).resolve().parent
HARNESS_DIR = GATE_DIR.parent / "harness"
sys.path.insert(0, str(GATE_DIR))
sys.path.insert(0, str(HARNESS_DIR))

from p25_laneB_robert_ksy_theta2_kubert_lang_anti_invariant_producer_contract_gate import (
    profile_anti_invariant_producer_contract,
)
from p25_laneB_robert_ksy_theta2_product_certificate_chain_gate import (
    profile_product_certificate_chain,
)
from p25_laneB_robert_ksy_theta2_arithmetic_producer_contract_gate import (
    profile_arithmetic_producer_contract,
)
from p25_ksy_y_yang_ksy_product_h90_bridge_spine_gate import (
    profile_ksy_yang_h90_bridge_spine,
)


UNIFIED_TARGET_EVIDENCE = Path(
    "research/p25/evidence/p25_v2_h0_conductor39_unified_target_20260616.md"
)
UNIFIED_TARGET_MARKER = "p25_v2_h0_conductor39_unified_target_rows=1/1"


@dataclass(frozen=True)
class ExactPToUnifiedTargetSpine:
    exactp_compact_contract_ok: bool
    arithmetic_producer_contract_ok: bool
    product_certificate_chain_ok: bool
    bridge_spine_ok: bool
    unified_target_evidence_ok: bool
    compact_payload: str
    source_parameter_budget: int
    atom_count: int
    theta2_payload_support: int
    quotient_y507_support: int
    period_norm_support: int
    unified_h90_support: int
    unified_positive_factor_count: int
    unified_negative_factor_count: int
    unified_target_rows: int
    exactp_implies_unified_target: bool
    unified_target_implies_exactp: bool
    exactp_is_stronger_upstream_route: bool
    exactp_still_missing_arithmetic_producer: bool
    unified_still_missing_value_divisor_theorem: bool
    row_ok: bool


def profile_exactp_to_unified_target_spine() -> ExactPToUnifiedTargetSpine:
    exactp = profile_anti_invariant_producer_contract()
    arithmetic = profile_arithmetic_producer_contract()
    product_chain = profile_product_certificate_chain()
    bridge = profile_ksy_yang_h90_bridge_spine()
    unified_evidence_ok = (
        UNIFIED_TARGET_EVIDENCE.exists()
        and UNIFIED_TARGET_MARKER in UNIFIED_TARGET_EVIDENCE.read_text()
        and "frontier_shape = one finite target family with two source languages"
        in UNIFIED_TARGET_EVIDENCE.read_text()
    )

    exactp_implies_unified = (
        exactp.row_ok
        and arithmetic.row_ok
        and product_chain.row_ok
        and bridge.row_ok
        and unified_evidence_ok
        and bridge.atom_count == 75
        and bridge.raw_siegel_term_count == product_chain.theta2_payload_support == 300
        and bridge.quotient_y507_support == 12
        and bridge.period_norm_support == 312
        and bridge.h90_potential_support == 156
        and bridge.h90_positive_factor_count == 78
        and bridge.h90_negative_factor_count == 78
        and bridge.legal_h90_product_orbit_count == 4
        and bridge.h90_boundary_ok
    )
    unified_implies_exactp = False
    exactp_stronger = exactp_implies_unified and not unified_implies_exactp
    exactp_missing = "prove a challenge-legal" in exactp.remaining_debt
    unified_missing = True

    row_ok = (
        exactp.derived.raw_center == (47, 28)
        and exactp.derived.raw_d_step == (22, 3)
        and exactp.derived.raw_k_step == (57, 0)
        and exactp.derived.raw_t_from_reflection == (38, 113)
        and exactp.finite_contract_accepts_anti_invariant_target
        and exactp.finite_contract_rejects_shortcuts
        and arithmetic.accepted_interfaces
        and arithmetic.plain_bridge_rejected_as_theta2
        and product_chain.forward_product_exact_theta2_inverse
        and product_chain.reversed_product_exact_theta2
        and product_chain.forward_product_recovered_sign == -1
        and product_chain.reversed_product_recovered_sign == 1
        and bridge.legal_h90_product_orbit_count == 4
        and bridge.legal_h90_product_stabilizer_size == 3
        and not bridge.atoms_are_independent_search_candidates
        and not bridge.h90_is_plain_75_atom_product
        and exactp_implies_unified
        and not unified_implies_exactp
        and exactp_stronger
        and exactp_missing
        and unified_missing
    )
    return ExactPToUnifiedTargetSpine(
        exactp_compact_contract_ok=exactp.row_ok,
        arithmetic_producer_contract_ok=arithmetic.row_ok,
        product_certificate_chain_ok=product_chain.row_ok,
        bridge_spine_ok=bridge.row_ok,
        unified_target_evidence_ok=unified_evidence_ok,
        compact_payload=exactp.compact_theorem_payload,
        source_parameter_budget=product_chain.source_parameter_budget,
        atom_count=bridge.atom_count,
        theta2_payload_support=bridge.raw_siegel_term_count,
        quotient_y507_support=bridge.quotient_y507_support,
        period_norm_support=bridge.period_norm_support,
        unified_h90_support=bridge.h90_potential_support,
        unified_positive_factor_count=bridge.h90_positive_factor_count,
        unified_negative_factor_count=bridge.h90_negative_factor_count,
        unified_target_rows=bridge.legal_h90_product_orbit_count,
        exactp_implies_unified_target=exactp_implies_unified,
        unified_target_implies_exactp=unified_implies_exactp,
        exactp_is_stronger_upstream_route=exactp_stronger,
        exactp_still_missing_arithmetic_producer=exactp_missing,
        unified_still_missing_value_divisor_theorem=unified_missing,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_exactp_to_unified_target_spine()
    print("p25 v2 exact-P to unified H0/conductor-39 target spine gate")
    print("dependencies")
    print(f"  exactp_compact_contract_ok={int(profile.exactp_compact_contract_ok)}")
    print(f"  arithmetic_producer_contract_ok={int(profile.arithmetic_producer_contract_ok)}")
    print(f"  product_certificate_chain_ok={int(profile.product_certificate_chain_ok)}")
    print(f"  bridge_spine_ok={int(profile.bridge_spine_ok)}")
    print(f"  unified_target_evidence_ok={int(profile.unified_target_evidence_ok)}")
    print("spine")
    print(f"  compact_payload={profile.compact_payload}")
    print(f"  source_parameter_budget={profile.source_parameter_budget}")
    print(f"  atom_count={profile.atom_count}")
    print(f"  theta2_payload_support={profile.theta2_payload_support}")
    print(f"  quotient_y507_support={profile.quotient_y507_support}")
    print(f"  period_norm_support={profile.period_norm_support}")
    print(f"  unified_h90_support={profile.unified_h90_support}")
    print(f"  unified_lift=+{profile.unified_positive_factor_count}/-{profile.unified_negative_factor_count}")
    print(f"  unified_target_rows={profile.unified_target_rows}")
    print("checks")
    print(f"  exactp_implies_unified_target={int(profile.exactp_implies_unified_target)}")
    print(f"  unified_target_implies_exactp={int(profile.unified_target_implies_exactp)}")
    print(f"  exactp_is_stronger_upstream_route={int(profile.exactp_is_stronger_upstream_route)}")
    print(
        "  exactp_still_missing_arithmetic_producer="
        f"{int(profile.exactp_still_missing_arithmetic_producer)}"
    )
    print(
        "  unified_still_missing_value_divisor_theorem="
        f"{int(profile.unified_still_missing_value_divisor_theorem)}"
    )
    print("interpretation")
    print("  exactp_is_not_a_separate_downstream_target_but_a_stronger_upstream_producer=1")
    print("  proving_exactp_would_feed_the_unified_H0_conductor39_target=1")
    print("  proving_unified_target_does_not_recover_exactp_without_extra_structure=1")
    print("  one_source_theorem_still_missing_on_each_route=1")
    print(f"p25_v2_exactp_to_unified_target_spine_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("exact-P to unified target spine regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
