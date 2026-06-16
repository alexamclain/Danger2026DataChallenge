#!/usr/bin/env python3
"""Distribution lift from the conductor-39 primitive unit to Norm_156(Y_507).

The primitive conductor-39 gate isolates U_chi=-chi_39 on X_1(39).  The
period-norm conductor gate says Norm_156(Y_507) is its scaled inflation to
level 507.  This gate makes the bridge explicit as Yang's 13-fold distribution
fiber:

    level 507 = 13 * 39,
    Norm_156(Y_507) = distribution_lift_39_to_507(6 * U_chi).
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_ksy_y_yang_y507_conductor39_mixed_tensor_character_gate import (
    profile_yang_y507_conductor39_mixed_tensor_character,
)
from p25_ksy_y_yang_y507_conductor39_primitive_character_unit_gate import (
    primitive_word,
    profile_yang_y507_conductor39_primitive_character_unit,
)
from p25_ksy_y_yang_y507_period_norm_character_gate import (
    period_norm,
)
from p25_ksy_y_yang_y507_primitive_factor_word_gate import (
    profile_yang_y507_primitive_factor_word,
)
from p25_ksy_y_yang_y507_modular_period_certificate_gate import SUPPORT_PERIOD
from p25_ksy_y_yang_y507_period_norm_conductor_gate import CONDUCTOR
from p25_laneB_robert_ksy_theta2_kubert_lang_exponent_matrix_gate import (
    QUOTIENT_LEVEL,
)


LIFT_LENGTH = QUOTIENT_LEVEL // CONDUCTOR


@dataclass(frozen=True)
class DistributionFiberRow:
    residue_mod39: int
    coefficient_mod39: int
    lifted_residues_mod507: tuple[int, ...]
    lifted_coefficients: tuple[int, ...]
    fiber_length: int
    constant_on_fiber: bool
    ok: bool


@dataclass(frozen=True)
class YangY507Conductor39DistributionLift:
    source_level: int
    target_level: int
    lift_length: int
    primitive_unit_ok: bool
    mixed_tensor_ok: bool
    primitive_support: int
    scaled_source_support: int
    lifted_support: int
    period_norm_support: int
    scaled_source_coefficient_counts: tuple[tuple[int, int], ...]
    lifted_coefficient_counts: tuple[tuple[int, int], ...]
    period_norm_coefficient_counts: tuple[tuple[int, int], ...]
    lifted_equals_period_norm: bool
    period_norm_equals_six_lifted_primitive: bool
    fiber_rows: tuple[DistributionFiberRow, ...]
    all_fibers_constant: bool
    yang_distribution_interpretation: str
    direct_closer: bool
    positive_payload: str
    first_missing_clause: str
    recommendation: str
    row_ok: bool


def nonzero(word: dict[int, int]) -> dict[int, int]:
    return dict(sorted((residue, coefficient) for residue, coefficient in word.items() if coefficient))


def coefficient_counts(word: dict[int, int]) -> tuple[tuple[int, int], ...]:
    counts: dict[int, int] = {}
    for coefficient in word.values():
        counts[coefficient] = counts.get(coefficient, 0) + 1
    return tuple(sorted(counts.items()))


def scale_word(word: dict[int, int], scale: int) -> dict[int, int]:
    return nonzero({residue: scale * coefficient for residue, coefficient in word.items()})


def distribution_lift(word_mod39: dict[int, int]) -> dict[int, int]:
    out: dict[int, int] = {}
    for residue, coefficient in word_mod39.items():
        for layer in range(LIFT_LENGTH):
            lifted = (residue + CONDUCTOR * layer) % QUOTIENT_LEVEL
            out[lifted] = out.get(lifted, 0) + coefficient
    return nonzero(out)


def fiber_row(residue: int, coefficient: int, lifted: dict[int, int]) -> DistributionFiberRow:
    residues = tuple((residue + CONDUCTOR * layer) % QUOTIENT_LEVEL for layer in range(LIFT_LENGTH))
    coefficients = tuple(lifted.get(item, 0) for item in residues)
    constant = all(value == coefficient for value in coefficients)
    return DistributionFiberRow(
        residue_mod39=residue,
        coefficient_mod39=coefficient,
        lifted_residues_mod507=residues,
        lifted_coefficients=coefficients,
        fiber_length=len(residues),
        constant_on_fiber=constant,
        ok=len(residues) == LIFT_LENGTH and len(set(residues)) == LIFT_LENGTH and constant,
    )


def profile_yang_y507_conductor39_distribution_lift() -> YangY507Conductor39DistributionLift:
    primitive = profile_yang_y507_conductor39_primitive_character_unit()
    mixed = profile_yang_y507_conductor39_mixed_tensor_character()
    y507 = profile_yang_y507_primitive_factor_word()
    primitive39 = primitive_word()
    scaled39 = scale_word(primitive39, 6)
    lifted = distribution_lift(scaled39)
    lifted_primitive = distribution_lift(primitive39)
    y_norm = period_norm(dict(y507.y507_primitive_word), SUPPORT_PERIOD)
    rows = tuple(fiber_row(residue, coefficient, lifted) for residue, coefficient in sorted(scaled39.items()))
    direct_closer = False
    row_ok = (
        primitive.row_ok
        and mixed.row_ok
        and y507.row_ok
        and CONDUCTOR == 39
        and QUOTIENT_LEVEL == 507
        and LIFT_LENGTH == 13
        and len(primitive39) == 24
        and len(scaled39) == 24
        and len(lifted) == 312
        and len(y_norm) == 312
        and coefficient_counts(scaled39) == ((-6, 12), (6, 12))
        and coefficient_counts(lifted) == ((-6, 156), (6, 156))
        and coefficient_counts(y_norm) == ((-6, 156), (6, 156))
        and lifted == y_norm
        and scale_word(lifted_primitive, 6) == y_norm
        and len(rows) == 24
        and all(row.ok for row in rows)
        and not direct_closer
    )
    return YangY507Conductor39DistributionLift(
        source_level=CONDUCTOR,
        target_level=QUOTIENT_LEVEL,
        lift_length=LIFT_LENGTH,
        primitive_unit_ok=primitive.row_ok,
        mixed_tensor_ok=mixed.row_ok,
        primitive_support=len(primitive39),
        scaled_source_support=len(scaled39),
        lifted_support=len(lifted),
        period_norm_support=len(y_norm),
        scaled_source_coefficient_counts=coefficient_counts(scaled39),
        lifted_coefficient_counts=coefficient_counts(lifted),
        period_norm_coefficient_counts=coefficient_counts(y_norm),
        lifted_equals_period_norm=lifted == y_norm,
        period_norm_equals_six_lifted_primitive=scale_word(lifted_primitive, 6) == y_norm,
        fiber_rows=rows,
        all_fibers_constant=all(row.ok for row in rows),
        yang_distribution_interpretation=(
            "By Yang's X_1(N) distribution relation with 507=13*39, each "
            "level-39 residue expands to the 13 residues a+39k at level 507."
        ),
        direct_closer=direct_closer,
        positive_payload=(
            "Norm_156(Y_507) is exactly the 13-fold Yang distribution lift of "
            "6*U_chi from X_1(39) to X_1(507)."
        ),
        first_missing_clause=(
            "distribution lifting identifies the compact period-norm source, "
            "but not the finite-field value/divisor theorem or DANGER3 extraction"
        ),
        recommendation=(
            "source theorems may target the primitive mixed X_1(39) unit U_chi "
            "plus Yang distribution to level 507; reject level-507 explanations "
            "that do not descend to this 13-fiber lift"
        ),
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_yang_y507_conductor39_distribution_lift()
    print("p25 KSY-y Yang Y_507 conductor-39 distribution-lift gate")
    print(f"source_level={profile.source_level}")
    print(f"target_level={profile.target_level}")
    print(f"lift_length={profile.lift_length}")
    print(f"primitive_unit_ok={int(profile.primitive_unit_ok)}")
    print(f"mixed_tensor_ok={int(profile.mixed_tensor_ok)}")
    print("supports")
    print(f"  primitive_support={profile.primitive_support}")
    print(f"  scaled_source_support={profile.scaled_source_support}")
    print(f"  lifted_support={profile.lifted_support}")
    print(f"  period_norm_support={profile.period_norm_support}")
    print("coefficient_counts")
    print(f"  scaled_source={profile.scaled_source_coefficient_counts}")
    print(f"  lifted={profile.lifted_coefficient_counts}")
    print(f"  period_norm={profile.period_norm_coefficient_counts}")
    print("checks")
    print(f"  lifted_equals_period_norm={int(profile.lifted_equals_period_norm)}")
    print(
        "  period_norm_equals_six_lifted_primitive="
        f"{int(profile.period_norm_equals_six_lifted_primitive)}"
    )
    print(f"  all_fibers_constant={int(profile.all_fibers_constant)}")
    print(f"  direct_closer={int(profile.direct_closer)}")
    print("sample_fibers")
    for row in profile.fiber_rows[:4]:
        print(
            "  "
            f"residue39={row.residue_mod39} coeff={row.coefficient_mod39} "
            f"fiber={row.lifted_residues_mod507} "
            f"constant={int(row.constant_on_fiber)} ok={int(row.ok)}"
        )
    print("interpretation")
    print("  norm_y507_is_yang_distribution_lift_of_6_U_chi=1")
    print("  primitive_mixed_X1_39_unit_is_source_of_level507_period_norm=1")
    print("  still_missing_value_or_divisor_theorem_and_DANGER3_extraction=1")
    print(
        "ksy_y_yang_y507_conductor39_distribution_lift_rows="
        f"{int(profile.row_ok)}/1"
    )
    if not profile.row_ok:
        raise SystemExit("Yang Y_507 conductor-39 distribution lift regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
