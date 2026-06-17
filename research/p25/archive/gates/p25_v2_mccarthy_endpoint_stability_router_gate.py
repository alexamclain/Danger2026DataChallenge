#!/usr/bin/env python3
"""Route the McCarthy square-axis endpoint after auxiliary-prime checks.

This is a support-lane router, not a source theorem gate.  It records the
current status of the archived McCarthy/Lane-B microscope:

* the minimal auxiliary field has an exceptional `R(138)^2029 in mu_39`
  projection;
* that projection is not auxiliary-prime invariant;
* simple theorem-side target factors do not repair the invariance failure;
* the finite endpoint `e_138` / `1 + (zeta_39^5 - 1)e_138` is exact and
  round-trips through the existing raw-Y closure; and
* the endpoint is Fourier-dense on `C_507`, so ordinary filter language is not
  a cheap source theorem.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys


RESEARCH = Path(__file__).resolve().parents[2]
ARCHIVE = RESEARCH / "archive"
for extra_path in (ARCHIVE / "gates", ARCHIVE / "harness"):
    extra = str(extra_path)
    if extra not in sys.path:
        sys.path.insert(0, extra)

from p25_laneB_square_axis_mccarthy_aux_prime_invariance_probe import (  # noqa: E402
    mccarthy_aux_prime_invariance_profile,
)
from p25_laneB_square_axis_mccarthy_endpoint_candidate_harness import (  # noqa: E402
    profile_endpoint_candidate,
    target_projector_entries,
    target_unit_minus_one_entries,
)
from p25_laneB_square_axis_mccarthy_idempotent_unit_gate import (  # noqa: E402
    mccarthy_idempotent_unit_profile,
)
from p25_laneB_square_axis_mccarthy_power_transport_raw_y_gate import (  # noqa: E402
    mccarthy_power_transport_raw_y_profile,
)
from p25_laneB_square_axis_mccarthy_theorem_factor_normalization_scan import (  # noqa: E402
    mccarthy_theorem_factor_normalization_profile,
)


MARKER = "p25_v2_mccarthy_endpoint_stability_router_rows=1/1"


@dataclass(frozen=True)
class McCarthyEndpointStabilityRouterProfile:
    target_q_exp: int
    probe_multipliers: tuple[int, ...]
    minimal_projection_ok: bool
    other_projection_ok: tuple[bool, ...]
    q_power_projection_aux_prime_invariant: bool
    posthoc_projection_representation_specific: bool
    theorem_factor_scans: int
    theorem_factor_all_mu39_hits: int
    easy_theorem_factor_normalization_found: bool
    transported_minus_one: int
    transported_minus_one_inverse: int
    normalized_raw_y_closes: bool
    unnormalized_control_fails_exact_packet: bool
    endpoint_projector_ok: bool
    endpoint_unit_minus_one_ok: bool
    endpoint_fourier_support: int
    endpoint_unit_order: int
    endpoint_fourier_dense: bool
    current_source_theorems: int
    current_source_stage_closers: int
    current_submission_ready: int


def build_profile() -> McCarthyEndpointStabilityRouterProfile:
    aux = mccarthy_aux_prime_invariance_profile()
    normalizer = mccarthy_theorem_factor_normalization_profile()
    raw_y = mccarthy_power_transport_raw_y_profile()
    idempotent = mccarthy_idempotent_unit_profile()
    projector = profile_endpoint_candidate(
        "target_projector_roundtrip",
        "projector",
        target_projector_entries(),
    )
    unit_minus_one = profile_endpoint_candidate(
        "target_unit_minus_one_roundtrip",
        "unit_minus_one",
        target_unit_minus_one_entries(),
    )
    theorem_factor_scans = (
        normalizer.single_factors_scanned
        + normalizer.gauss_monomials_scanned
        + normalizer.theorem_monomials_scanned
    )
    theorem_factor_all_hits = (
        normalizer.single_factor_all_mu39_count
        + normalizer.gauss_monomial_all_mu39_count
        + normalizer.theorem_monomial_all_mu39_count
    )
    return McCarthyEndpointStabilityRouterProfile(
        target_q_exp=aux.target_q_exp,
        probe_multipliers=aux.probe_multipliers,
        minimal_projection_ok=aux.minimal_prime_projection_ok,
        other_projection_ok=aux.other_primes_projection_ok,
        q_power_projection_aux_prime_invariant=aux.q_power_projection_aux_prime_invariant,
        posthoc_projection_representation_specific=aux.posthoc_projection_is_representation_specific,
        theorem_factor_scans=theorem_factor_scans,
        theorem_factor_all_mu39_hits=theorem_factor_all_hits,
        easy_theorem_factor_normalization_found=normalizer.easy_theorem_factor_normalization_found,
        transported_minus_one=raw_y.transported_minus_one,
        transported_minus_one_inverse=raw_y.transported_minus_one_inverse,
        normalized_raw_y_closes=raw_y.normalized_raw_y_closes,
        unnormalized_control_fails_exact_packet=raw_y.unnormalized_control_fails_exact_packet,
        endpoint_projector_ok=projector.ok,
        endpoint_unit_minus_one_ok=unit_minus_one.ok,
        endpoint_fourier_support=idempotent.point_idempotent_fourier_support,
        endpoint_unit_order=idempotent.powered_unit_order,
        endpoint_fourier_dense=idempotent.fourier_filter_dense,
        current_source_theorems=0,
        current_source_stage_closers=0,
        current_submission_ready=0,
    )


def main() -> int:
    profile = build_profile()
    row_ok = (
        profile.target_q_exp == 138
        and profile.probe_multipliers == (1, 4, 7)
        and profile.minimal_projection_ok
        and profile.other_projection_ok == (False, False)
        and not profile.q_power_projection_aux_prime_invariant
        and profile.posthoc_projection_representation_specific
        and profile.theorem_factor_scans == 236
        and profile.theorem_factor_all_mu39_hits == 0
        and not profile.easy_theorem_factor_normalization_found
        and profile.transported_minus_one == 1375
        and profile.transported_minus_one_inverse == 636
        and profile.normalized_raw_y_closes
        and profile.unnormalized_control_fails_exact_packet
        and profile.endpoint_projector_ok
        and profile.endpoint_unit_minus_one_ok
        and profile.endpoint_fourier_support == 507
        and profile.endpoint_unit_order == 39
        and profile.endpoint_fourier_dense
        and profile.current_source_theorems == 0
        and profile.current_source_stage_closers == 0
        and profile.current_submission_ready == 0
    )

    print("p25 v2 McCarthy endpoint stability router")
    print(f"target_q_exp={profile.target_q_exp}")
    print(f"probe_multipliers={profile.probe_multipliers}")
    print(f"minimal_projection_ok={int(profile.minimal_projection_ok)}")
    print(f"other_projection_ok={profile.other_projection_ok}")
    print(
        "q_power_projection_aux_prime_invariant="
        f"{int(profile.q_power_projection_aux_prime_invariant)}"
    )
    print(
        "posthoc_projection_representation_specific="
        f"{int(profile.posthoc_projection_representation_specific)}"
    )
    print(f"theorem_factor_scans={profile.theorem_factor_scans}")
    print(f"theorem_factor_all_mu39_hits={profile.theorem_factor_all_mu39_hits}")
    print(
        "easy_theorem_factor_normalization_found="
        f"{int(profile.easy_theorem_factor_normalization_found)}"
    )
    print(f"transported_minus_one={profile.transported_minus_one}")
    print(f"transported_minus_one_inverse={profile.transported_minus_one_inverse}")
    print(f"normalized_raw_y_closes={int(profile.normalized_raw_y_closes)}")
    print(
        "unnormalized_control_fails_exact_packet="
        f"{int(profile.unnormalized_control_fails_exact_packet)}"
    )
    print(f"endpoint_projector_ok={int(profile.endpoint_projector_ok)}")
    print(f"endpoint_unit_minus_one_ok={int(profile.endpoint_unit_minus_one_ok)}")
    print(f"endpoint_fourier_support={profile.endpoint_fourier_support}")
    print(f"endpoint_unit_order={profile.endpoint_unit_order}")
    print(f"endpoint_fourier_dense={int(profile.endpoint_fourier_dense)}")
    print(f"current_source_theorems={profile.current_source_theorems}")
    print(f"current_source_stage_closers={profile.current_source_stage_closers}")
    print(f"current_submission_ready={profile.current_submission_ready}")
    print("decisions")
    print("  raw_q_power_projection=repair_not_auxiliary_prime_invariant")
    print("  easy_target_factor_normalization=reject_no_repair_found")
    print("  sparse_endpoint=evidence_test_object_not_source_theorem")
    print("  ordinary_fourier_filter_route=repair_dense_filter_debt")
    print(MARKER if row_ok else "p25_v2_mccarthy_endpoint_stability_router_rows=0/1")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
