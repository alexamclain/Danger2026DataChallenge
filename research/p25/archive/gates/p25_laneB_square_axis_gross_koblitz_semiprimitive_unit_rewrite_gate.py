#!/usr/bin/env python3
"""Semiprimitive cubic Gauss-sum unit rewrite for the p25 GK residue.

The gamma-reflection precheck leaves a formal two-cell residue

    (1,2): +234 * U(169)
    (2,1): -234 * U(169)

where `U(169)` is the Gross-Koblitz unit attached to the cubic character
exponent on the `N=507` cycle.  A targeted literature scout found the
semiprimitive Gauss-sum evaluation: since `p == -1 mod 3` and the live field
degree is `f=78=2*39`, the cubic Gauss sum is pure.  In GK normalization this
rewrites `U(169)` and `U(338)` to 1.

This gate records the local effect.  The free unit symbol is removed, but the
reflection residue still has two signed scalar cells, including the false
positive `(1,2)`.  Thus semiprimitive purity alone is not the missing projector;
it must be paired with another multiplication/endpoint relation or the HD/GK
lane remains killed at this point.
"""

from __future__ import annotations

from dataclasses import dataclass


P25 = 10**25 + 13
N = 507
FIELD_DEGREE = 78
HALF_DEGREE = 39
UNIT_EXPONENTS = (169, 338)
REFLECTION_RESIDUE = {
    (1, 2): (234, 169),
    (2, 1): (-234, 169),
}
TARGET_CELL = (2, 1)
FALSE_POSITIVE_CELL = (1, 2)


@dataclass(frozen=True)
class SemiprimitiveUnitRewriteProfile:
    p_mod_3: int
    p39_mod_507: int
    field_degree: int
    half_degree: int
    unit_rewrites: tuple[tuple[int, int], ...]
    residue_after_rewrite: tuple[tuple[tuple[int, int], int], ...]
    free_unit_symbol_removed: bool
    target_cell_present: bool
    false_positive_cell_present: bool
    semiprimitive_rewrite_alone_killed: bool


def rewrite_unit(unit_exponent: int) -> int:
    if unit_exponent in UNIT_EXPONENTS:
        return 1
    raise ValueError(f"no semiprimitive cubic rewrite for U({unit_exponent})")


def semiprimitive_unit_rewrite_profile() -> SemiprimitiveUnitRewriteProfile:
    rewritten: dict[tuple[int, int], int] = {}
    for cell, (coefficient, unit_exponent) in REFLECTION_RESIDUE.items():
        rewritten[cell] = coefficient * rewrite_unit(unit_exponent)
    residue_after = tuple(sorted(rewritten.items()))
    free_unit_removed = all(unit in UNIT_EXPONENTS for _coeff, unit in REFLECTION_RESIDUE.values())
    target_present = rewritten.get(TARGET_CELL, 0) != 0
    false_positive_present = rewritten.get(FALSE_POSITIVE_CELL, 0) != 0
    return SemiprimitiveUnitRewriteProfile(
        p_mod_3=P25 % 3,
        p39_mod_507=pow(P25, HALF_DEGREE, N),
        field_degree=FIELD_DEGREE,
        half_degree=HALF_DEGREE,
        unit_rewrites=tuple((unit, rewrite_unit(unit)) for unit in UNIT_EXPONENTS),
        residue_after_rewrite=residue_after,
        free_unit_symbol_removed=free_unit_removed,
        target_cell_present=target_present,
        false_positive_cell_present=false_positive_present,
        semiprimitive_rewrite_alone_killed=free_unit_removed
        and target_present
        and false_positive_present,
    )


def main() -> int:
    print("p25 Lane B Gross-Koblitz semiprimitive unit rewrite gate")
    profile = semiprimitive_unit_rewrite_profile()
    row_ok = (
        profile.p_mod_3 == 2
        and profile.p39_mod_507 == 506
        and profile.field_degree == 78
        and profile.half_degree == 39
        and profile.unit_rewrites == ((169, 1), (338, 1))
        and profile.residue_after_rewrite == (((1, 2), 234), ((2, 1), -234))
        and profile.free_unit_symbol_removed
        and profile.target_cell_present
        and profile.false_positive_cell_present
        and profile.semiprimitive_rewrite_alone_killed
    )

    print(f"semiprimitive_unit_rewrite_profile={profile}")
    print("semiprimitive_laws")
    print("  p_mod_3=-1_and_p^39=-1_mod_507=1")
    print("  cubic_GK_units_U169_and_U338_rewrite_to_1=1")
    print("  free_U169_symbol_is_removed=1")
    print("  signed_two_cell_scalar_residue_remains=1")
    print("interpretation")
    print("  semiprimitive_purity_alone_does_not_make_the_anomaly_projector=1")
    print("  hd_gk_route_still_needs_a_relation_removing_the_(1,2)_false_positive=1")
    print(f"square_axis_gross_koblitz_semiprimitive_unit_rewrite_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_gross_koblitz_semiprimitive_unit_rewrite_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
