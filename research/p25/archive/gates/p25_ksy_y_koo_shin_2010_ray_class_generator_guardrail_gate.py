#!/usr/bin/env python3
"""Koo-Shin 2010 ray-class generators versus the conductor-39 source.

Koo-Shin 2010 Theorems 9.8, 9.10, and 9.11 are useful ray-class generator
context, but their visible level-N shapes are not the p25 conductor-39 mixed
character source.  They use all-unit sums/products and single-index
normalizations; the active source is U_chi=-chi_39, whose proper pushforwards
to mod 3 and mod 13 vanish.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from math import gcd

from p25_ksy_y_koo_shin_2010_full_surface_screen_gate import (
    profile_koo_shin_2010_full_surface_screen,
)
from p25_ksy_y_yang_y507_conductor39_mixed_tensor_character_gate import (
    profile_yang_y507_conductor39_mixed_tensor_character,
)
from p25_ksy_y_yang_y507_conductor39_primitive_character_unit_gate import (
    profile_yang_y507_conductor39_primitive_character_unit,
)
from p25_ksy_y_yang_y507_period_norm_conductor_gate import CONDUCTOR, chi39


PHI_CONDUCTOR = 24
THEOREM_98_POWER = 24 * CONDUCTOR
THEOREM_910_POWER = 12 * CONDUCTOR


@dataclass(frozen=True)
class RayClassGeneratorShapeRow:
    name: str
    theorem: str
    kind: str
    is_product_word: bool
    word: tuple[tuple[int, int], ...]
    support: int
    coefficient_counts: tuple[tuple[int, int], ...]
    exponent_sum_mod_12: int
    quadratic_sum_mod_level: int
    pushforward_mod3: tuple[tuple[int, int], ...]
    pushforward_mod13: tuple[tuple[int, int], ...]
    proper_pushforwards_vanish: bool
    equals_scaled_u_chi: bool
    residual_from_best_scaled_u_chi_support: int | None
    direct_source_candidate: bool
    decision: str
    first_missing_clause: str
    ok: bool


@dataclass(frozen=True)
class RayClassRouteRow:
    name: str
    accepted_use: str
    decision: str
    ray_class_context: bool
    conductor39_source_identified: bool
    finite_value_theorem_ready: bool
    extraction_ready: bool
    submission_ready: bool
    first_missing_clause: str
    ok: bool


@dataclass(frozen=True)
class KooShinRayClassGeneratorGuardrail:
    level: int
    units: tuple[int, ...]
    theorem_98_present: bool
    theorem_910_present: bool
    theorem_911_present: bool
    primitive_unit_ok: bool
    mixed_tensor_ok: bool
    shape_rows: tuple[RayClassGeneratorShapeRow, ...]
    route_rows: tuple[RayClassRouteRow, ...]
    ray_class_context_rows: int
    conductor39_source_identified_rows: int
    direct_source_candidate_rows: int
    finite_value_theorem_ready_rows: int
    extraction_ready_rows: int
    submission_ready_rows: int
    rejected_direct_rows: int
    positive_payload: str
    remaining_upgrade: str
    row_ok: bool


def units_mod_level() -> tuple[int, ...]:
    return tuple(residue for residue in range(1, CONDUCTOR) if gcd(residue, CONDUCTOR) == 1)


def coefficient_counts(word: dict[int, int]) -> tuple[tuple[int, int], ...]:
    return tuple(sorted(Counter(word.values()).items()))


def pushforward(word: dict[int, int], modulus: int) -> tuple[tuple[int, int], ...]:
    out: dict[int, int] = {}
    for residue, coefficient in word.items():
        target = residue % modulus
        out[target] = out.get(target, 0) + coefficient
    return tuple(sorted((residue, coefficient) for residue, coefficient in out.items() if coefficient))


def u_chi_word(scale: int = 1) -> dict[int, int]:
    return {
        residue: -scale * chi39(residue)
        for residue in units_mod_level()
        if chi39(residue)
    }


def ray_class_sum_mask_word() -> dict[int, int]:
    return {residue: THEOREM_98_POWER for residue in units_mod_level()}


def ray_class_all_unit_product_word() -> dict[int, int]:
    return {residue: THEOREM_910_POWER for residue in units_mod_level()}


def ray_class_single_index_normalized_word() -> dict[int, int]:
    word = {residue: -THEOREM_910_POWER for residue in units_mod_level()}
    word[1] += THEOREM_910_POWER * PHI_CONDUCTOR
    return word


def scaled_u_chi_match(word: dict[int, int]) -> tuple[bool, int | None]:
    target = u_chi_word()
    if set(word) != set(target):
        residual_support = len(set(word) ^ set(target))
        return False, residual_support
    scales = {word[residue] // target[residue] for residue in target}
    integer_scaled = all(word[residue] == next(iter(scales)) * target[residue] for residue in target)
    if len(scales) == 1 and integer_scaled:
        return True, 0
    best_scale = round(sum(word[r] * target[r] for r in target) / sum(target[r] * target[r] for r in target))
    residual_support = sum(1 for residue in target if word[residue] != best_scale * target[residue])
    return False, residual_support


def shape_row(
    name: str,
    theorem: str,
    kind: str,
    is_product_word: bool,
    word: dict[int, int],
    decision: str,
    first_missing_clause: str,
) -> RayClassGeneratorShapeRow:
    pf3 = pushforward(word, 3)
    pf13 = pushforward(word, 13)
    equals_scaled, residual_support = scaled_u_chi_match(word)
    direct_source = is_product_word and equals_scaled and not pf3 and not pf13
    exponent_sum = sum(word.values())
    quadratic_sum = sum(residue * residue * coefficient for residue, coefficient in word.items())
    return RayClassGeneratorShapeRow(
        name=name,
        theorem=theorem,
        kind=kind,
        is_product_word=is_product_word,
        word=tuple(sorted(word.items())),
        support=len(word),
        coefficient_counts=coefficient_counts(word),
        exponent_sum_mod_12=exponent_sum % 12,
        quadratic_sum_mod_level=quadratic_sum % CONDUCTOR,
        pushforward_mod3=pf3,
        pushforward_mod13=pf13,
        proper_pushforwards_vanish=not pf3 and not pf13,
        equals_scaled_u_chi=equals_scaled,
        residual_from_best_scaled_u_chi_support=residual_support,
        direct_source_candidate=direct_source,
        decision=decision,
        first_missing_clause=first_missing_clause,
        ok=True,
    )


def shape_rows() -> tuple[RayClassGeneratorShapeRow, ...]:
    return (
        shape_row(
            "target_mixed_character_U_chi",
            "active p25 conductor-39 source",
            "mixed_character_product",
            True,
            u_chi_word(),
            "accept_target_shape_only",
            "finite-field value/divisor theorem and extraction still missing",
        ),
        shape_row(
            "koo_shin_98_TN_all_unit_sum",
            "Theorem 9.8",
            "all_unit_sum",
            False,
            ray_class_sum_mask_word(),
            "reject_sum_not_character_product",
            "multiplicative mixed-character product U_chi",
        ),
        shape_row(
            "koo_shin_910_MN_all_unit_product",
            "Theorem 9.10",
            "all_unit_product",
            True,
            ray_class_all_unit_product_word(),
            "reject_all_unit_product_loses_character",
            "vanishing mod-3/mod-13 pushforwards and signed chi_3 tensor chi_13",
        ),
        shape_row(
            "koo_shin_910_single_index_normalized_generator",
            "Theorem 9.10",
            "single_index_normalized_product",
            True,
            ray_class_single_index_normalized_word(),
            "reject_delta_background_not_character",
            "pure U_chi character word rather than one spike plus full-unit background",
        ),
    )


def route_rows() -> tuple[RayClassRouteRow, ...]:
    return (
        RayClassRouteRow(
            name="ray_class_generator_vocabulary",
            accepted_use="CM/ray-class vocabulary and Shimura reciprocity context",
            decision="continue_as_context_only",
            ray_class_context=True,
            conductor39_source_identified=False,
            finite_value_theorem_ready=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="finite-field identity for the exact p25 source",
            ok=True,
        ),
        RayClassRouteRow(
            name="all_unit_or_single_index_generator_as_U_chi",
            accepted_use="none as a direct conductor-39 source",
            decision="reject_as_direct_source",
            ray_class_context=True,
            conductor39_source_identified=False,
            finite_value_theorem_ready=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="proper pushforwards vanish and scaled U_chi equality",
            ok=True,
        ),
        RayClassRouteRow(
            name="independent_mixed_character_theorem",
            accepted_use="a theorem that emits U_chi, V_bal, or W and preserves the mixed tensor",
            decision="source_shape_ready_value_theorem_missing",
            ray_class_context=False,
            conductor39_source_identified=True,
            finite_value_theorem_ready=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="finite-field value/divisor theorem, Yang/H90 descent, and extraction",
            ok=True,
        ),
    )


def profile_koo_shin_ray_class_generator_guardrail() -> KooShinRayClassGeneratorGuardrail:
    full_screen = profile_koo_shin_2010_full_surface_screen()
    primitive = profile_yang_y507_conductor39_primitive_character_unit()
    mixed = profile_yang_y507_conductor39_mixed_tensor_character()
    shapes = shape_rows()
    routes = route_rows()
    ray_context = sum(row.ray_class_context for row in routes)
    source_identified = sum(row.conductor39_source_identified for row in routes)
    direct_source = sum(row.direct_source_candidate for row in shapes)
    value_ready = sum(row.finite_value_theorem_ready for row in routes)
    extraction_ready = sum(row.extraction_ready for row in routes)
    submission_ready = sum(row.submission_ready for row in routes)
    rejected = sum(row.decision.startswith("reject_") for row in shapes)
    row_ok = (
        full_screen.row_ok
        and full_screen.text_scan.has_theorem_9_8
        and full_screen.text_scan.has_theorem_9_10
        and full_screen.text_scan.has_theorem_9_11
        and primitive.row_ok
        and mixed.row_ok
        and CONDUCTOR == 39
        and PHI_CONDUCTOR == len(units_mod_level()) == 24
        and THEOREM_98_POWER == 936
        and THEOREM_910_POWER == 468
        and shapes[0].proper_pushforwards_vanish
        and shapes[0].equals_scaled_u_chi
        and shapes[0].direct_source_candidate
        and not shapes[1].is_product_word
        and not shapes[1].proper_pushforwards_vanish
        and not shapes[1].equals_scaled_u_chi
        and not shapes[2].proper_pushforwards_vanish
        and not shapes[2].equals_scaled_u_chi
        and shapes[2].coefficient_counts == ((468, 24),)
        and not shapes[3].proper_pushforwards_vanish
        and not shapes[3].equals_scaled_u_chi
        and shapes[3].coefficient_counts == ((-468, 23), (10764, 1))
        and shapes[3].residual_from_best_scaled_u_chi_support == 12
        and ray_context == 2
        and source_identified == 1
        and direct_source == 1
        and value_ready == 0
        and extraction_ready == 0
        and submission_ready == 0
        and rejected == 3
        and all(row.ok for row in shapes)
        and all(row.ok for row in routes)
    )
    return KooShinRayClassGeneratorGuardrail(
        level=CONDUCTOR,
        units=units_mod_level(),
        theorem_98_present=full_screen.text_scan.has_theorem_9_8,
        theorem_910_present=full_screen.text_scan.has_theorem_9_10,
        theorem_911_present=full_screen.text_scan.has_theorem_9_11,
        primitive_unit_ok=primitive.row_ok,
        mixed_tensor_ok=mixed.row_ok,
        shape_rows=shapes,
        route_rows=routes,
        ray_class_context_rows=ray_context,
        conductor39_source_identified_rows=source_identified,
        direct_source_candidate_rows=direct_source,
        finite_value_theorem_ready_rows=value_ready,
        extraction_ready_rows=extraction_ready,
        submission_ready_rows=submission_ready,
        rejected_direct_rows=rejected,
        positive_payload=(
            "Koo-Shin 9.x supplies ray-class generator context, but its all-unit "
            "and single-index generator shapes are not the mixed U_chi source."
        ),
        remaining_upgrade=(
            "an independent mixed-character finite-field value/divisor theorem, "
            "Yang/Hilbert-90 descent, X_1(16) extraction surface, halving payload, "
            "and vpp.py verification"
        ),
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_koo_shin_ray_class_generator_guardrail()
    print("p25 KSY-y Koo-Shin 2010 ray-class generator guardrail gate")
    print("inputs")
    print(f"  level={profile.level}")
    print(f"  units={profile.units}")
    print(f"  theorem_9_8={int(profile.theorem_98_present)}")
    print(f"  theorem_9_10={int(profile.theorem_910_present)}")
    print(f"  theorem_9_11={int(profile.theorem_911_present)}")
    print(f"  primitive_unit_ok={int(profile.primitive_unit_ok)}")
    print(f"  mixed_tensor_ok={int(profile.mixed_tensor_ok)}")
    print("shape_rows")
    for row in profile.shape_rows:
        print(
            "  "
            f"{row.name}: theorem={row.theorem} kind={row.kind} "
            f"product={int(row.is_product_word)} support={row.support} "
            f"counts={row.coefficient_counts} sum_mod12={row.exponent_sum_mod_12} "
            f"quad_mod39={row.quadratic_sum_mod_level} "
            f"pf3={row.pushforward_mod3} pf13={row.pushforward_mod13} "
            f"pushforwards_vanish={int(row.proper_pushforwards_vanish)} "
            f"scaled_U_chi={int(row.equals_scaled_u_chi)} "
            f"residual_support={row.residual_from_best_scaled_u_chi_support} "
            f"direct_source={int(row.direct_source_candidate)} "
            f"decision={row.decision} missing={row.first_missing_clause}"
        )
    print("route_rows")
    for row in profile.route_rows:
        print(
            "  "
            f"{row.name}: decision={row.decision} context={int(row.ray_class_context)} "
            f"source={int(row.conductor39_source_identified)} "
            f"value={int(row.finite_value_theorem_ready)} "
            f"extraction={int(row.extraction_ready)} "
            f"submission={int(row.submission_ready)} missing={row.first_missing_clause}"
        )
    print("counts")
    print(f"  ray_class_context_rows={profile.ray_class_context_rows}")
    print(f"  conductor39_source_identified_rows={profile.conductor39_source_identified_rows}")
    print(f"  direct_source_candidate_rows={profile.direct_source_candidate_rows}")
    print(f"  finite_value_theorem_ready_rows={profile.finite_value_theorem_ready_rows}")
    print(f"  extraction_ready_rows={profile.extraction_ready_rows}")
    print(f"  submission_ready_rows={profile.submission_ready_rows}")
    print(f"  rejected_direct_rows={profile.rejected_direct_rows}")
    print("interpretation")
    print("  koo_shin_9x_is_ray_class_context_not_U_chi_source=1")
    print("  all_unit_and_single_index_shapes_do_not_have_vanishing_proper_pushforwards=1")
    print("  single_index_normalization_has_large_non_character_residual=1")
    print(f"  remaining_upgrade={profile.remaining_upgrade}")
    print(f"ksy_y_koo_shin_2010_ray_class_generator_guardrail_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("Koo-Shin 2010 ray-class generator guardrail regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
