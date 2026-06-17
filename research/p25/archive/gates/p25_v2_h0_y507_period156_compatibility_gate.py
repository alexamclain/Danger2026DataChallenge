#!/usr/bin/env python3
"""V2 wrapper for the H0/Y507 period-156 compatibility screen."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys


GATE_DIR = Path(__file__).resolve().parent
HARNESS_DIR = GATE_DIR.parent / "harness"
sys.path.insert(0, str(GATE_DIR))
sys.path.insert(0, str(HARNESS_DIR))

from p25_ksy_y_h0_period156_value_compatibility_gate import (  # noqa: E402
    profile_h0_period156_value_compatibility,
)
from p25_v2_period156_value_source_hook_gate import build_hook  # noqa: E402


@dataclass(frozen=True)
class H0Y507Period156Compatibility:
    legacy_screen_ok: bool
    value_source_hook_ok: bool
    y507_minimum_doubling_period: int
    support_period_root_gcd: int
    ambient_period_root_gcd: int
    h0_support_period: int
    canonical_h0_positive_count: int
    canonical_h0_negative_count: int
    canonical_h0_boundary_equals_norm: bool
    legal_h0_orbit_count: int
    legal_h0_stabilizer_size: int
    row_count: int
    source_closing_rows: int
    value_closing_rows: int
    divisor_closing_rows: int
    rejected_rows: int
    conditional_rows: int
    finite_payload_rows: int
    current_period156_value_theorems: int
    accepted_shapes: tuple[str, ...]
    repair_or_reject_shapes: tuple[str, ...]
    decision: str
    row_ok: bool


def build_compatibility() -> H0Y507Period156Compatibility:
    legacy = profile_h0_period156_value_compatibility()
    hook = build_hook()
    accepted = (
        "canonical H0 value with boundary and period-156 branch context",
        "Y_507 value with period-156 context",
        "canonical H0 divisor/additive identity with boundary",
    )
    repairs = (
        "H0 value missing Norm_156(Y_507) boundary",
        "H0 value missing period-156 branch/root/telescoping context",
        "formal one-coset H value",
        "ambient period-780 value",
        "finite payload without arithmetic source theorem",
        "finite identity without arithmetic source theorem",
    )
    row_ok = (
        legacy.row_ok
        and hook.row_ok
        and legacy.y507_minimum_doubling_period == 156
        and legacy.support_period_root_gcd == 1
        and legacy.ambient_period_root_gcd == 11
        and legacy.h0_support_period == 156
        and legacy.canonical_h0_positive_count == 78
        and legacy.canonical_h0_negative_count == 78
        and legacy.canonical_h0_boundary_equals_norm
        and legacy.legal_h0_orbit_count == 4
        and legacy.legal_h0_stabilizer_size == 3
        and legacy.row_count == 9
        and legacy.source_closing_rows == 3
        and legacy.value_closing_rows == 2
        and legacy.divisor_closing_rows == 1
        and legacy.rejected_rows == 2
        and legacy.conditional_rows == 4
        and legacy.finite_payload_rows == 1
        and hook.current_period156_value_theorems == 0
    )
    return H0Y507Period156Compatibility(
        legacy_screen_ok=legacy.row_ok,
        value_source_hook_ok=hook.row_ok,
        y507_minimum_doubling_period=legacy.y507_minimum_doubling_period,
        support_period_root_gcd=legacy.support_period_root_gcd,
        ambient_period_root_gcd=legacy.ambient_period_root_gcd,
        h0_support_period=legacy.h0_support_period,
        canonical_h0_positive_count=legacy.canonical_h0_positive_count,
        canonical_h0_negative_count=legacy.canonical_h0_negative_count,
        canonical_h0_boundary_equals_norm=legacy.canonical_h0_boundary_equals_norm,
        legal_h0_orbit_count=legacy.legal_h0_orbit_count,
        legal_h0_stabilizer_size=legacy.legal_h0_stabilizer_size,
        row_count=legacy.row_count,
        source_closing_rows=legacy.source_closing_rows,
        value_closing_rows=legacy.value_closing_rows,
        divisor_closing_rows=legacy.divisor_closing_rows,
        rejected_rows=legacy.rejected_rows,
        conditional_rows=legacy.conditional_rows,
        finite_payload_rows=legacy.finite_payload_rows,
        current_period156_value_theorems=hook.current_period156_value_theorems,
        accepted_shapes=accepted,
        repair_or_reject_shapes=repairs,
        decision="period156_h0_y507_value_route_live_but_no_current_theorem",
        row_ok=row_ok,
    )


def main() -> int:
    screen = build_compatibility()
    print("p25 v2 H0/Y507 period-156 compatibility")
    print(f"legacy_screen_ok={int(screen.legacy_screen_ok)}")
    print(f"value_source_hook_ok={int(screen.value_source_hook_ok)}")
    print(f"y507_minimum_doubling_period={screen.y507_minimum_doubling_period}")
    print(f"support_period_root_gcd={screen.support_period_root_gcd}")
    print(f"ambient_period_root_gcd={screen.ambient_period_root_gcd}")
    print(f"h0_support_period={screen.h0_support_period}")
    print(f"canonical_h0_positive_count={screen.canonical_h0_positive_count}")
    print(f"canonical_h0_negative_count={screen.canonical_h0_negative_count}")
    print(
        "canonical_h0_boundary_equals_norm="
        f"{int(screen.canonical_h0_boundary_equals_norm)}"
    )
    print(f"legal_h0_orbit_count={screen.legal_h0_orbit_count}")
    print(f"legal_h0_stabilizer_size={screen.legal_h0_stabilizer_size}")
    print("counts")
    print(f"  row_count={screen.row_count}")
    print(f"  source_closing_rows={screen.source_closing_rows}")
    print(f"  value_closing_rows={screen.value_closing_rows}")
    print(f"  divisor_closing_rows={screen.divisor_closing_rows}")
    print(f"  rejected_rows={screen.rejected_rows}")
    print(f"  conditional_rows={screen.conditional_rows}")
    print(f"  finite_payload_rows={screen.finite_payload_rows}")
    print(f"  current_period156_value_theorems={screen.current_period156_value_theorems}")
    print("accepted_shapes")
    for shape in screen.accepted_shapes:
        print(f"  {shape}")
    print("repair_or_reject_shapes")
    for shape in screen.repair_or_reject_shapes:
        print(f"  {shape}")
    print(f"decision={screen.decision}")
    print(f"p25_v2_h0_y507_period156_compatibility_rows={int(screen.row_ok)}/1")
    return 0 if screen.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
