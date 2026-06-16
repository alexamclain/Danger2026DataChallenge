#!/usr/bin/env python3
"""McCarthy numeric point-delta to p25 raw-Y bridge integration gate.

The numeric McCarthy gate verifies that Theorem 1.7 produces a singleton
transformed-difference delta at q_exp=138 over F_2029.  The projector raw-Y
gate verifies that a singleton anomaly projector at the same seed closes the
finite square-axis theta_{3,1} payload after adding the deterministic C13
fiber background.

This integration gate checks that these are the same finite object:

    McCarthy singleton q_exp=138
      -> outer S image {138,310,482}
      -> same anomaly terms used by the GK/Frobenius projector
      -> raw-Y harness passes.

It does not yet construct a Lean certificate or a DANGER3 triple; it records
that the McCarthy arithmetic point-delta lands on the existing p25 finite
payload closure.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_square_axis_gross_koblitz_frobenius_projector_gate import (
    frobenius_projector_profile,
)
from p25_laneB_square_axis_gross_koblitz_projector_raw_y_gate import (
    projector_raw_y_profile,
)
from p25_laneB_square_axis_group_ring_normal_form_gate import S_STEP
from p25_laneB_square_axis_mccarthy_well_poised_numeric_delta_gate import (
    TARGET_Q_EXP,
    mccarthy_numeric_delta_profile,
)
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER


@dataclass(frozen=True)
class McCarthyRawYBridgeProfile:
    mccarthy_support: tuple[int, ...]
    mccarthy_exceptional_support: tuple[int, ...]
    outer_s_image: tuple[int, ...]
    frobenius_projected_anomaly_terms: tuple[int, ...]
    raw_y_length: int
    raw_y_nonzero: int
    raw_y_harness_ok: bool
    numeric_delta_matches_projector: bool
    raw_y_payload_closed: bool


def outer_s_image(seed_support: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(
        sorted(
            (seed + layer * S_STEP) % QUOTIENT_ORDER
            for seed in seed_support
            for layer in range(3)
        )
    )


def mccarthy_raw_y_bridge_profile() -> McCarthyRawYBridgeProfile:
    numeric = mccarthy_numeric_delta_profile()
    projector = frobenius_projector_profile()
    raw_y = projector_raw_y_profile()
    image = outer_s_image(numeric.transformed_difference_support)
    numeric_matches = (
        numeric.transformed_difference_support == (TARGET_Q_EXP,)
        and numeric.exceptional_support == (TARGET_Q_EXP,)
        and image == projector.projected_anomaly_terms
    )
    raw_closed = (
        raw_y.quotient_packet_exact
        and raw_y.raw_y_length == 12675
        and raw_y.raw_y_nonzero == 6300
        and raw_y.ray_local_harness_ok
    )
    return McCarthyRawYBridgeProfile(
        mccarthy_support=numeric.transformed_difference_support,
        mccarthy_exceptional_support=numeric.exceptional_support,
        outer_s_image=image,
        frobenius_projected_anomaly_terms=projector.projected_anomaly_terms,
        raw_y_length=raw_y.raw_y_length,
        raw_y_nonzero=raw_y.raw_y_nonzero,
        raw_y_harness_ok=raw_y.ray_local_harness_ok,
        numeric_delta_matches_projector=numeric_matches,
        raw_y_payload_closed=raw_closed,
    )


def main() -> int:
    print("p25 Lane B McCarthy numeric delta raw-Y bridge gate")
    profile = mccarthy_raw_y_bridge_profile()
    row_ok = (
        profile.mccarthy_support == (138,)
        and profile.mccarthy_exceptional_support == (138,)
        and profile.outer_s_image == (138, 310, 482)
        and profile.frobenius_projected_anomaly_terms == (138, 310, 482)
        and profile.raw_y_length == 12675
        and profile.raw_y_nonzero == 6300
        and profile.raw_y_harness_ok
        and profile.numeric_delta_matches_projector
        and profile.raw_y_payload_closed
    )

    print(f"mccarthy_raw_y_bridge_profile={profile}")
    print("mccarthy_raw_y_bridge_laws")
    print("  mccarthy_numeric_delta_support_q_exp_138_matches_projector_anomaly=1")
    print("  outer_S_image_is_138_310_482=1")
    print("  formal_raw_Y_payload_closes_and_passes_ray_local_harness=1")
    print("interpretation")
    print("  mccarthy_point_delta_lands_on_the_existing_p25_square_axis_payload_closure=1")
    print("  remaining_gap_is_parameter_normalization_to_an_actual_p25_raw_unit_vector=1")
    print(f"square_axis_mccarthy_numeric_delta_raw_y_bridge_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_mccarthy_numeric_delta_raw_y_bridge_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
