#!/usr/bin/env python3
"""Koo-Shin 2010 versus the new conductor-39 Yang distribution source.

The Yang Y_507 distribution-lift gate compresses the period-norm source to
U_chi=-chi_3*chi_13 on X_1(39), followed by the 13-fiber lift to X_1(507).
This gate asks whether that compression changes the Koo-Shin 2010 Theorem 5.2
verdict.

It does not close p25 directly: Theorem 5.2 is still prime-level/root-descent
context, while the live source is a mixed conductor-39 tensor whose proper
prime-axis pushforwards vanish.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_ksy_y_koo_shin_2010_theorem52_actual_verdict_gate import (
    profile_actual_theorem52_verdict,
)
from p25_ksy_y_yang_y507_conductor39_distribution_lift_gate import (
    profile_yang_y507_conductor39_distribution_lift,
)
from p25_ksy_y_yang_y507_conductor39_mixed_tensor_character_gate import (
    profile_yang_y507_conductor39_mixed_tensor_character,
)


@dataclass(frozen=True)
class KooShinConductor39DistributionBridge:
    koo_shin_actual_ok: bool
    distribution_lift_ok: bool
    mixed_tensor_ok: bool
    source_level: int
    target_level: int
    lift_length: int
    primitive_support: int
    prime13_columns: int
    mod3_rows: int
    row2_is_negative_row1: bool
    proper_pushforwards_vanish: bool
    prime13_projection_support: int
    mod3_projection_support: int
    theorem52_prime_level_rigidity: bool
    theorem52_root_descent_helper: bool
    theorem52_emits_mixed_tensor_source: bool
    theorem52_closes_distribution_source: bool
    first_missing_clause: str
    positive_use: str
    recommendation: str
    row_ok: bool


def profile_koo_shin_conductor39_distribution_bridge() -> KooShinConductor39DistributionBridge:
    koo_shin = profile_actual_theorem52_verdict()
    lift = profile_yang_y507_conductor39_distribution_lift()
    mixed = profile_yang_y507_conductor39_mixed_tensor_character()

    theorem52_emits_mixed_tensor_source = (
        koo_shin.mixed_c3_c169_graph_emitted
        and koo_shin.exact_p25_product_emitted
        and koo_shin.normalized_y_product_emitted
    )
    theorem52_closes_distribution_source = (
        theorem52_emits_mixed_tensor_source
        and lift.row_ok
        and mixed.tensor_factorization_ok
    )
    row_ok = (
        koo_shin.row_ok
        and lift.row_ok
        and mixed.row_ok
        and lift.source_level == 39
        and lift.target_level == 507
        and lift.lift_length == 13
        and lift.primitive_support == 24
        and mixed.units_mod13 == tuple(range(1, 13))
        and mixed.row2_is_negative_row1
        and mixed.proper_pushforwards_vanish
        and len(mixed.pushforward_mod13) == 0
        and len(mixed.pushforward_mod3) == 0
        and koo_shin.prime_level_product_rigidity
        and koo_shin.root_descent_statement
        and not theorem52_emits_mixed_tensor_source
        and not theorem52_closes_distribution_source
    )
    return KooShinConductor39DistributionBridge(
        koo_shin_actual_ok=koo_shin.row_ok,
        distribution_lift_ok=lift.row_ok,
        mixed_tensor_ok=mixed.row_ok,
        source_level=lift.source_level,
        target_level=lift.target_level,
        lift_length=lift.lift_length,
        primitive_support=lift.primitive_support,
        prime13_columns=len(mixed.units_mod13),
        mod3_rows=2,
        row2_is_negative_row1=mixed.row2_is_negative_row1,
        proper_pushforwards_vanish=mixed.proper_pushforwards_vanish,
        prime13_projection_support=len(mixed.pushforward_mod13),
        mod3_projection_support=len(mixed.pushforward_mod3),
        theorem52_prime_level_rigidity=koo_shin.prime_level_product_rigidity,
        theorem52_root_descent_helper=koo_shin.root_descent_statement,
        theorem52_emits_mixed_tensor_source=theorem52_emits_mixed_tensor_source,
        theorem52_closes_distribution_source=theorem52_closes_distribution_source,
        first_missing_clause=(
            "mixed conductor-39 theorem preserving the chi_3 row sign, "
            "chi_13 column character, and Yang 13-fiber lift"
        ),
        positive_use=(
            "Koo-Shin 2010 Theorem 5.2 can still police constant products or "
            "root descent after an independent mixed producer is found."
        ),
        recommendation=(
            "do not route the conductor-39 distribution source through a "
            "prime-13 or C169 projection; require a genuinely mixed chi_3 tensor "
            "chi_13 source theorem"
        ),
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_koo_shin_conductor39_distribution_bridge()
    print("p25 KSY-y Koo-Shin/conductor-39 distribution bridge gate")
    print("inputs")
    print(f"  koo_shin_actual_ok={int(profile.koo_shin_actual_ok)}")
    print(f"  distribution_lift_ok={int(profile.distribution_lift_ok)}")
    print(f"  mixed_tensor_ok={int(profile.mixed_tensor_ok)}")
    print("conductor39_source")
    print(f"  source_level={profile.source_level}")
    print(f"  target_level={profile.target_level}")
    print(f"  lift_length={profile.lift_length}")
    print(f"  primitive_support={profile.primitive_support}")
    print(f"  mod3_rows={profile.mod3_rows}")
    print(f"  prime13_columns={profile.prime13_columns}")
    print(f"  row2_is_negative_row1={int(profile.row2_is_negative_row1)}")
    print(f"  proper_pushforwards_vanish={int(profile.proper_pushforwards_vanish)}")
    print(f"  prime13_projection_support={profile.prime13_projection_support}")
    print(f"  mod3_projection_support={profile.mod3_projection_support}")
    print("koo_shin_theorem52")
    print(f"  prime_level_rigidity={int(profile.theorem52_prime_level_rigidity)}")
    print(f"  root_descent_helper={int(profile.theorem52_root_descent_helper)}")
    print(f"  emits_mixed_tensor_source={int(profile.theorem52_emits_mixed_tensor_source)}")
    print(f"  closes_distribution_source={int(profile.theorem52_closes_distribution_source)}")
    print("interpretation")
    print("  conductor39_source_needs_mixed_chi3_tensor_chi13_theorem=1")
    print("  prime13_or_c169_projection_loses_the_source=1")
    print("  koo_shin_theorem52_remains_helper_not_target=1")
    print(
        "ksy_y_koo_shin_conductor39_distribution_bridge_rows="
        f"{int(profile.row_ok)}/1"
    )
    if not profile.row_ok:
        raise SystemExit("Koo-Shin/conductor-39 distribution bridge regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
