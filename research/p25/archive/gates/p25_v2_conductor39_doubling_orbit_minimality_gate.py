#!/usr/bin/env python3
"""V2 conductor-39 doubling-orbit minimality checkpoint.

The unified first-pass target is fixed as a support-156 product family.  This
gate records one more negative shortcut: the conductor-39 source can be seeded
by E_7/E_1, but only after taking the full 12-step <2> orbit norm.  No proper
doubling suborbit is a legal standalone X_1(39) modular unit.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "harness"))

from p25_ksy_y_yang_y507_conductor39_doubling_orbit_minimality_gate import (  # noqa: E402
    profile_yang_y507_conductor39_doubling_orbit_minimality,
)
from p25_ksy_y_yang_y507_conductor39_doubling_orbit_norm_gate import (  # noqa: E402
    profile_yang_y507_conductor39_doubling_orbit_norm,
)


@dataclass(frozen=True)
class V2Conductor39DoublingOrbitMinimality:
    orbit_norm_ok: bool
    orbit_minimality_ok: bool
    unified_source_gap_marker_ok: bool
    seed_denominator: int
    seed_numerator: int
    orbit_length: int
    orbit_support: int
    single_seed_ratio_descends: bool
    full_orbit_required: bool
    frob_orbit_norm_is_inverse: bool
    proper_rows: int
    proper_legal_rows: int
    proper_elementary_congruence_rows: int
    proper_signed_orbit_failure_rows: int
    full_orbit_forced_by_yang_yu: bool
    shortcut_remaining: bool
    remaining_gap: str
    row_ok: bool


def marker_ok(path: str, needle: str) -> bool:
    p = Path(path)
    return p.exists() and needle in p.read_text()


def profile_v2_conductor39_doubling_orbit_minimality() -> V2Conductor39DoublingOrbitMinimality:
    norm = profile_yang_y507_conductor39_doubling_orbit_norm()
    minimality = profile_yang_y507_conductor39_doubling_orbit_minimality()
    source_gap = marker_ok(
        "research/p25/evidence/p25_v2_unified_source_theorem_gap_20260616.md",
        "p25_v2_unified_source_theorem_gap_rows=1/1",
    )
    shortcut_remaining = (
        norm.single_seed_ratio_descends
        or minimality.proper_legal_rows > 0
        or not minimality.full_orbit_forced_by_yang_yu
    )
    row_ok = (
        norm.row_ok
        and minimality.row_ok
        and source_gap
        and norm.seed_denominator == 1
        and norm.seed_numerator == 7
        and norm.orbit_length == 12
        and norm.orbit_support == 24
        and norm.no_cancellation_in_orbit_norm
        and norm.frob_seed_maps_to_skew_inverse_pair
        and norm.frob_orbit_norm_is_inverse
        and not norm.single_seed_ratio_descends
        and norm.full_orbit_required
        and minimality.proper_rows == 27
        and minimality.proper_legal_rows == 0
        and minimality.proper_elementary_congruence_rows == 9
        and minimality.proper_signed_orbit_failure_rows == 9
        and minimality.full_orbit_forced_by_yang_yu
        and not shortcut_remaining
    )
    return V2Conductor39DoublingOrbitMinimality(
        orbit_norm_ok=norm.row_ok,
        orbit_minimality_ok=minimality.row_ok,
        unified_source_gap_marker_ok=source_gap,
        seed_denominator=norm.seed_denominator,
        seed_numerator=norm.seed_numerator,
        orbit_length=norm.orbit_length,
        orbit_support=norm.orbit_support,
        single_seed_ratio_descends=norm.single_seed_ratio_descends,
        full_orbit_required=norm.full_orbit_required,
        frob_orbit_norm_is_inverse=norm.frob_orbit_norm_is_inverse,
        proper_rows=minimality.proper_rows,
        proper_legal_rows=minimality.proper_legal_rows,
        proper_elementary_congruence_rows=minimality.proper_elementary_congruence_rows,
        proper_signed_orbit_failure_rows=minimality.proper_signed_orbit_failure_rows,
        full_orbit_forced_by_yang_yu=minimality.full_orbit_forced_by_yang_yu,
        shortcut_remaining=shortcut_remaining,
        remaining_gap=(
            "finite arithmetic value/divisor theorem for the full 12-step "
            "doubling norm, not a seed or proper-suborbit shortcut"
        ),
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_v2_conductor39_doubling_orbit_minimality()
    print("p25 v2 conductor-39 doubling-orbit minimality gate")
    print("dependencies")
    print(f"  orbit_norm_ok={int(profile.orbit_norm_ok)}")
    print(f"  orbit_minimality_ok={int(profile.orbit_minimality_ok)}")
    print(f"  unified_source_gap_marker_ok={int(profile.unified_source_gap_marker_ok)}")
    print("orbit_norm")
    print(f"  seed_ratio=E_{profile.seed_numerator}/E_{profile.seed_denominator}")
    print(f"  orbit_length={profile.orbit_length}")
    print(f"  orbit_support={profile.orbit_support}")
    print(f"  single_seed_ratio_descends={int(profile.single_seed_ratio_descends)}")
    print(f"  full_orbit_required={int(profile.full_orbit_required)}")
    print(f"  frob_orbit_norm_is_inverse={int(profile.frob_orbit_norm_is_inverse)}")
    print("proper_suborbit_screen")
    print(f"  proper_rows={profile.proper_rows}")
    print(f"  proper_legal_rows={profile.proper_legal_rows}")
    print(f"  proper_elementary_congruence_rows={profile.proper_elementary_congruence_rows}")
    print(f"  proper_signed_orbit_failure_rows={profile.proper_signed_orbit_failure_rows}")
    print(f"  full_orbit_forced_by_yang_yu={int(profile.full_orbit_forced_by_yang_yu)}")
    print("interpretation")
    print(f"  shortcut_remaining={int(profile.shortcut_remaining)}")
    print("  seed_ratio_is_only_valid_inside_full_12_step_norm=1")
    print("  proper_doubling_suborbits_are_not_standalone_units=1")
    print(f"  remaining_gap={profile.remaining_gap}")
    print(f"p25_v2_conductor39_doubling_orbit_minimality_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("v2 conductor-39 doubling-orbit minimality regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
