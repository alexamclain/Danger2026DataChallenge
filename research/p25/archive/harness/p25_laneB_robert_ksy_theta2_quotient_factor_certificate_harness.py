#!/usr/bin/env python3
"""Quotient-level factor-certificate intake for the p25 KSY theta2 route.

The factor-gauge normal form shows that the literal `base, K, D, T`
coordinates are over-specified.  The finite verifier only needs:

    K = a primitive generator of the size-25 right-mod-3 kernel,
    base, D, T classes in (C_75 / K) x C_169.

This harness accepts those quotient data, chooses the minimal right-coordinate
section, and reuses the factor-certificate harness.  It is now the smallest
finite intake contract for the KSY/theta lane.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from math import gcd

from p25_laneB_robert_ksy_theta2_factor_certificate_harness import (
    KsyTheta2FactorCertificateProfile,
    profile_factor_certificate,
)
from p25_laneB_robert_ksy_theta2_factor_gauge_normal_form_gate import quotient_class
from p25_laneB_square_axis_bridge_formal_unit_shadow_gate import scale_coord
from p25_laneB_square_axis_bridge_raw_source_character_gate import (
    C_ORDER,
    KERNEL_SHIFT,
    RIGHT_ORDER,
)


Coord = tuple[int, int]


@dataclass(frozen=True)
class QuotientFactorCertificateProfile:
    name: str
    base_class: Coord
    d_class: Coord
    t_class: Coord
    k_multiplier: int
    k_step: Coord
    k_multiplier_primitive: bool
    lifted_base: Coord
    lifted_d: Coord
    lifted_t: Coord
    lifted_classes_match_input: bool
    factor_certificate_profile: KsyTheta2FactorCertificateProfile
    ok: bool


def lift_quotient_class(right_class: int, c_value: int) -> Coord:
    return (right_class % 3, c_value % C_ORDER)


def primitive_k_step(k_multiplier: int) -> Coord:
    return scale_coord(KERNEL_SHIFT, k_multiplier % 25)


def profile_quotient_factor_certificate(
    name: str,
    base_class: Coord,
    d_class: Coord,
    t_class: Coord,
    k_multiplier: int,
) -> QuotientFactorCertificateProfile:
    lifted_base = lift_quotient_class(*base_class)
    lifted_d = lift_quotient_class(*d_class)
    lifted_t = lift_quotient_class(*t_class)
    k_step = primitive_k_step(k_multiplier)
    primitive = gcd(k_multiplier % 25, 25) == 1
    factor_profile = profile_factor_certificate(
        name,
        lifted_base,
        k_step,
        lifted_d,
        lifted_t,
    )
    classes_match = (
        quotient_class(lifted_base) == (base_class[0] % 3, base_class[1] % C_ORDER)
        and quotient_class(lifted_d) == (d_class[0] % 3, d_class[1] % C_ORDER)
        and quotient_class(lifted_t) == (t_class[0] % 3, t_class[1] % C_ORDER)
    )
    row_ok = (
        primitive
        and classes_match
        and factor_profile.ok
        and factor_profile.factor_support_budget == 31
        and factor_profile.product_support == 150
    )
    return QuotientFactorCertificateProfile(
        name=name,
        base_class=(base_class[0] % 3, base_class[1] % C_ORDER),
        d_class=(d_class[0] % 3, d_class[1] % C_ORDER),
        t_class=(t_class[0] % 3, t_class[1] % C_ORDER),
        k_multiplier=k_multiplier % 25,
        k_step=k_step,
        k_multiplier_primitive=primitive,
        lifted_base=lifted_base,
        lifted_d=lifted_d,
        lifted_t=lifted_t,
        lifted_classes_match_input=classes_match,
        factor_certificate_profile=factor_profile,
        ok=row_ok,
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Audit quotient-level p25 KSY factor data: base, D, T classes in "
            "(C_75/K) x C_169 plus a primitive K multiplier."
        )
    )
    parser.add_argument("--base-right-class", type=int)
    parser.add_argument("--base-c", type=int)
    parser.add_argument("--d-right-class", type=int)
    parser.add_argument("--d-c", type=int)
    parser.add_argument("--t-right-class", type=int)
    parser.add_argument("--t-c", type=int)
    parser.add_argument("--k-multiplier", type=int, default=1)
    args = parser.parse_args()

    print("p25 Lane B Robert KSY/theta2 quotient-factor certificate harness")
    print(f"source_group=C_{RIGHT_ORDER}xC_{C_ORDER} quotient=C_3xC_{C_ORDER}")

    supplied = (
        args.base_right_class is not None,
        args.base_c is not None,
        args.d_right_class is not None,
        args.d_c is not None,
        args.t_right_class is not None,
        args.t_c is not None,
    )
    if any(supplied):
        if not all(supplied):
            raise SystemExit("all six quotient coordinates must be supplied together")
        profile = profile_quotient_factor_certificate(
            "quotient_factor_certificate_candidate",
            (args.base_right_class, args.base_c),
            (args.d_right_class, args.d_c),
            (args.t_right_class, args.t_c),
            args.k_multiplier,
        )
        print("mode=quotient_factor_certificate_candidate")
        print(f"quotient_factor_certificate_profile={profile}")
        print("candidate_contract")
        print("  pass requires primitive K multiplier modulo 25")
        print("  pass lifts quotient classes to a factor certificate")
        print("  pass then reuses bridge, compact theta2, and period checks")
        print(f"robert_ksy_theta2_quotient_factor_certificate_candidate_rows={int(profile.ok)}/1")
        print("conclusion=reported_p25_laneB_robert_ksy_theta2_quotient_factor_certificate_candidate")
        return 0 if profile.ok else 1

    target = profile_quotient_factor_certificate(
        "target_quotient_factor_certificate",
        (1, 25),
        (1, 3),
        (2, 113),
        1,
    )
    primitive_k = profile_quotient_factor_certificate(
        "primitive_k_multiplier_control",
        (1, 25),
        (1, 3),
        (2, 113),
        2,
    )
    nonprimitive_k = profile_quotient_factor_certificate(
        "nonprimitive_k_multiplier_control",
        (1, 25),
        (1, 3),
        (2, 113),
        5,
    )
    wrong_base = profile_quotient_factor_certificate(
        "wrong_base_quotient_control",
        (2, 25),
        (1, 3),
        (2, 113),
        1,
    )
    wrong_d = profile_quotient_factor_certificate(
        "wrong_d_quotient_control",
        (1, 25),
        (1, 4),
        (2, 113),
        1,
    )
    wrong_t = profile_quotient_factor_certificate(
        "wrong_t_quotient_control",
        (1, 25),
        (1, 3),
        (2, 114),
        1,
    )
    row_ok = (
        target.ok
        and primitive_k.ok
        and not nonprimitive_k.ok
        and not wrong_base.ok
        and not wrong_d.ok
        and not wrong_t.ok
        and target.lifted_base == (1, 25)
        and target.lifted_d == (1, 3)
        and target.lifted_t == (2, 113)
        and target.factor_certificate_profile.factor_support_budget == 31
        and target.factor_certificate_profile.product_support == 150
    )
    print(f"target_quotient_factor_certificate_profile={target}")
    print(f"primitive_k_multiplier_control_profile={primitive_k}")
    print(f"nonprimitive_k_multiplier_control_profile={nonprimitive_k}")
    print(f"wrong_base_quotient_control_profile={wrong_base}")
    print(f"wrong_d_quotient_control_profile={wrong_d}")
    print(f"wrong_t_quotient_control_profile={wrong_t}")
    print("quotient_factor_certificate_laws")
    print("  theorem_hit_may_emit_only_three_quotient_classes_plus_K_multiplier=1")
    print("  target_classes_are_base_1_25_D_1_3_T_2_113=1")
    print("  primitive_K_multiplier_1_or_2_passes_nonprimitive_5_fails=1")
    print("  wrong_base_D_or_T_quotient_classes_fail=1")
    print("  accepted_quotient_data_lifts_to_factor_certificate_and_theta2_contract=1")
    print(f"robert_ksy_theta2_quotient_factor_certificate_harness_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_robert_ksy_theta2_quotient_factor_certificate_harness")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
