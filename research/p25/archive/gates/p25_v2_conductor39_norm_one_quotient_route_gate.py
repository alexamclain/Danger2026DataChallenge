#!/usr/bin/env python3
"""Validate the conductor-39 norm-one quotient route for p25.

This promotes the compact quotient

    Q = prod_{h in <2>} E_{7h} / E_h

as a theorem-facing value object.  It is smaller than the 24-entry character
word and has the clean relation Frob_p(Q)=Q^-1, so Q^6 is a Hilbert-90
boundary.  The route is useful structure, not a source theorem by itself.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys


GATE_DIR = Path(__file__).resolve().parent
HARNESS_DIR = GATE_DIR.parent / "harness"
for import_dir in (GATE_DIR, HARNESS_DIR):
    if str(import_dir) not in sys.path:
        sys.path.insert(0, str(import_dir))

from p25_ksy_y_yang_y507_conductor39_coset_frobenius_pairing_gate import (  # noqa: E402
    profile_yang_y507_conductor39_coset_frobenius_pairing,
)
from p25_ksy_y_yang_y507_conductor39_coset_selector_gate import (  # noqa: E402
    profile_yang_y507_conductor39_coset_selector,
)
from p25_ksy_y_yang_y507_conductor39_frobenius_orbit_gate import (  # noqa: E402
    profile_yang_y507_conductor39_frobenius_orbit,
)
from p25_ksy_y_yang_y507_conductor39_primitive_character_unit_gate import (  # noqa: E402
    profile_yang_y507_conductor39_primitive_character_unit,
)
from p25_v2_period156_value_source_hook_gate import build_hook as build_value_hook  # noqa: E402


@dataclass(frozen=True)
class QuotientInvariant:
    name: str
    statement: str
    ok: bool


@dataclass(frozen=True)
class QuotientRoute:
    name: str
    decision: str
    first_missing_or_falsifier: str
    support_route: bool
    repair: bool
    reject: bool
    ok: bool


@dataclass(frozen=True)
class Conductor39NormOneQuotientRoute:
    invariants: tuple[QuotientInvariant, ...]
    routes: tuple[QuotientRoute, ...]
    invariant_rows_ok: int
    support_routes: int
    repair_rows: int
    reject_rows: int
    current_source_theorems: int
    row_ok: bool


def invariants() -> tuple[QuotientInvariant, ...]:
    primitive = profile_yang_y507_conductor39_primitive_character_unit()
    selector = profile_yang_y507_conductor39_coset_selector()
    pairing = profile_yang_y507_conductor39_coset_frobenius_pairing()
    orbit = profile_yang_y507_conductor39_frobenius_orbit()
    value_hook = build_value_hook()
    return (
        QuotientInvariant(
            "primitive_unit",
            "U_chi=-chi_39 is a legal mixed conductor-39 modular-unit word",
            primitive.row_ok
            and primitive.primitive_support == 24
            and primitive.primitive_frobenius_image_is_negative,
        ),
        QuotientInvariant(
            "coset_quotient",
            "U_chi is the 12-pair quotient 1_{7<2>} - 1_{<2>}",
            selector.row_ok
            and selector.kernel_size == 12
            and selector.coset_size == 12
            and selector.coset_quotient_word_equals_primitive,
        ),
        QuotientInvariant(
            "norm_one_quotient",
            "For Q=prod E_{7h}/E_h, Frob_p(Q)=Q^-1 and W=Q^6=(1-Frob_p)(Q^3)",
            pairing.row_ok
            and pairing.q_value_frobenius_inverse_contract
            and pairing.w_value_frobenius_inverse_contract,
        ),
        QuotientInvariant(
            "explicit_frobenius_shifts",
            "Frob sends denominator index i to numerator i+11 and numerator i to denominator i+9",
            pairing.row_ok
            and pairing.denominator_to_numerator_shift == 11
            and pairing.numerator_to_denominator_shift == 9
            and pairing.p2_cycle_shift == 8,
        ),
        QuotientInvariant(
            "pure_degree6_norm_cancels",
            "The naive degree-6 norm of the pure conductor-39 character word is zero",
            orbit.row_ok and orbit.pure_character_degree6_norm_cancels,
        ),
        QuotientInvariant(
            "value_hook_still_required",
            "A Q-route theorem still has to pass the period-156 value source hook",
            value_hook.row_ok and value_hook.current_period156_value_theorems == 0,
        ),
    )


def routes() -> tuple[QuotientRoute, ...]:
    return (
        QuotientRoute(
            "norm_one_Q_value_theorem_with_period156_context",
            "route_through_period156_value_source_hook",
            "downstream DANGER3 framing and extraction after a source theorem",
            support_route=True,
            repair=False,
            reject=False,
            ok=True,
        ),
        QuotientRoute(
            "explicit_Q3_hilbert90_preimage_with_finite_theorem",
            "normalize_h90_preimage_then_apply_source_snippet_intake",
            "same theorem data after legal Hilbert-90 descent normalization",
            support_route=True,
            repair=False,
            reject=False,
            ok=True,
        ),
        QuotientRoute(
            "coset_selector_or_Q_source_only",
            "repair_finite_value_divisor_theorem_missing",
            "finite value/divisor theorem for Q, Q^3, Q^6, or the selected Yang lift",
            support_route=False,
            repair=True,
            reject=False,
            ok=True,
        ),
        QuotientRoute(
            "Q6_boundary_only",
            "repair_additive_or_value_normalization_missing",
            "scalar-fixed finite value/additive data, not just the Hilbert-90 boundary",
            support_route=False,
            repair=True,
            reject=False,
            ok=True,
        ),
        QuotientRoute(
            "primitive_U_chi_power_only",
            "repair_yang_lift_descent_and_finite_theorem_missing",
            "Yang lift, Hilbert-90 descent, and finite theorem for the selected row",
            support_route=False,
            repair=True,
            reject=False,
            ok=True,
        ),
        QuotientRoute(
            "pure_character_degree6_norm",
            "reject_pure_character_degree6_norm_cancels",
            "Frobenius alternation makes the degree-6 norm zero",
            support_route=False,
            repair=False,
            reject=True,
            ok=True,
        ),
    )


def build_route() -> Conductor39NormOneQuotientRoute:
    invariant_rows = invariants()
    route_rows = routes()
    invariant_ok = sum(row.ok for row in invariant_rows)
    support = sum(row.support_route for row in route_rows)
    repairs = sum(row.repair for row in route_rows)
    rejects = sum(row.reject for row in route_rows)
    current_source_theorems = 0
    expected = (
        "route_through_period156_value_source_hook",
        "normalize_h90_preimage_then_apply_source_snippet_intake",
        "repair_finite_value_divisor_theorem_missing",
        "repair_additive_or_value_normalization_missing",
        "repair_yang_lift_descent_and_finite_theorem_missing",
        "reject_pure_character_degree6_norm_cancels",
    )
    row_ok = (
        invariant_ok == len(invariant_rows)
        and len(invariant_rows) == 6
        and len(route_rows) == 6
        and tuple(row.decision for row in route_rows) == expected
        and support == 2
        and repairs == 3
        and rejects == 1
        and current_source_theorems == 0
        and all(row.ok for row in route_rows)
    )
    return Conductor39NormOneQuotientRoute(
        invariants=invariant_rows,
        routes=route_rows,
        invariant_rows_ok=invariant_ok,
        support_routes=support,
        repair_rows=repairs,
        reject_rows=rejects,
        current_source_theorems=current_source_theorems,
        row_ok=row_ok,
    )


def main() -> int:
    route = build_route()
    print("p25 v2 conductor-39 norm-one quotient route")
    print("invariants")
    for invariant in route.invariants:
        print(f"  {invariant.name}: ok={int(invariant.ok)}")
        print(f"    {invariant.statement}")
    print("routes")
    for row in route.routes:
        print(f"  {row.name}: decision={row.decision}")
        print(f"    missing_or_falsifier={row.first_missing_or_falsifier}")
    print("counts")
    print(f"  invariant_rows_ok={route.invariant_rows_ok}/{len(route.invariants)}")
    print(f"  support_routes={route.support_routes}")
    print(f"  repair_rows={route.repair_rows}")
    print(f"  reject_rows={route.reject_rows}")
    print(f"  current_source_theorems={route.current_source_theorems}")
    print("interpretation")
    print("  compact_Q_route_is_live_support_structure_not_a_source_theorem=1")
    print("  naive_degree6_norm_of_pure_character_is_rejected=1")
    print(f"p25_v2_conductor39_norm_one_quotient_route_rows={int(route.row_ok)}/1")
    return 0 if route.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
