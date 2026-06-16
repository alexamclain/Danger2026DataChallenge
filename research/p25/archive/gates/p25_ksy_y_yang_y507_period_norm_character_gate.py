#!/usr/bin/env python3
"""Period-norm character boundary for the compact p25 Y_507 word.

For the compact target

    Y_507 = [2]^*U_507 / U_507^4,

the support period is 156.  A tempting value-side shortcut is to hope that the
period product telescopes away.  It does not.  Summing the 156 doubling
translates cancels the nonunit layer and leaves a dense signed index-two
character on all units of Z/507Z.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd

from p25_ksy_y_yang_y507_modular_period_certificate_gate import SUPPORT_PERIOD
from p25_ksy_y_yang_y507_primitive_factor_word_gate import (
    profile_yang_y507_primitive_factor_word,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_exponent_matrix_gate import (
    QUOTIENT_LEVEL,
)


@dataclass(frozen=True)
class PeriodOrbitSummary:
    name: str
    period: int
    word_support: int
    orbit_union_support: int
    orbit_visit_counts: tuple[int, ...]
    period_norm_support: int
    period_norm_coefficient_counts: tuple[tuple[int, int], ...]
    period_norm_gcd_classes: tuple[tuple[int, int], ...]
    ok: bool


@dataclass(frozen=True)
class YangY507PeriodNormCharacter:
    level: int
    support_period: int
    unit_count: int
    doubling_subgroup_size: int
    u_summary: PeriodOrbitSummary
    y_summary: PeriodOrbitSummary
    y_norm_equals_minus_three_u_norm: bool
    y_positive_coset_is_negative_doubling_subgroup: bool
    y_negative_coset_is_doubling_subgroup: bool
    nonunit_layer_cancels_in_period_norm: bool
    log_parity_character_matches_doubling_subgroup: bool
    direct_closer: bool
    positive_payload: str
    first_missing_clause: str
    recommendation: str
    row_ok: bool


def nonzero(word: dict[int, int]) -> dict[int, int]:
    return dict(sorted((residue, coefficient) for residue, coefficient in word.items() if coefficient))


def push_doubling(word: dict[int, int], power: int = 1) -> dict[int, int]:
    multiplier = pow(2, power, QUOTIENT_LEVEL)
    out: dict[int, int] = {}
    for residue, coefficient in word.items():
        target = (multiplier * residue) % QUOTIENT_LEVEL
        out[target] = out.get(target, 0) + coefficient
    return nonzero(out)


def add_words(left: dict[int, int], right: dict[int, int]) -> dict[int, int]:
    out = dict(left)
    for residue, coefficient in right.items():
        out[residue] = out.get(residue, 0) + coefficient
    return nonzero(out)


def coefficient_counts(word: dict[int, int]) -> tuple[tuple[int, int], ...]:
    counts: dict[int, int] = {}
    for coefficient in word.values():
        counts[coefficient] = counts.get(coefficient, 0) + 1
    return tuple(sorted(counts.items()))


def gcd_classes(residues: set[int]) -> tuple[tuple[int, int], ...]:
    counts: dict[int, int] = {}
    for residue in residues:
        divisor = gcd(residue, QUOTIENT_LEVEL)
        counts[divisor] = counts.get(divisor, 0) + 1
    return tuple(sorted(counts.items()))


def word_period(word: dict[int, int], limit: int) -> int:
    for period in range(1, limit + 1):
        if push_doubling(word, period) == word:
            return period
    raise AssertionError("period exceeds limit")


def period_norm(word: dict[int, int], period: int) -> dict[int, int]:
    out: dict[int, int] = {}
    for power in range(period):
        out = add_words(out, push_doubling(word, power))
    return out


def orbit_union_and_visits(word: dict[int, int], period: int) -> tuple[set[int], tuple[int, ...]]:
    visits: dict[int, int] = {}
    for power in range(period):
        image = push_doubling(word, power)
        for residue in image:
            visits[residue] = visits.get(residue, 0) + 1
    return set(visits), tuple(sorted(set(visits.values())))


def residue_orbit(seed: int) -> set[int]:
    out: set[int] = set()
    residue = seed
    while residue not in out:
        out.add(residue)
        residue = (2 * residue) % QUOTIENT_LEVEL
    return out


def log2_mod_169() -> dict[int, int]:
    out: dict[int, int] = {}
    residue = 1
    for exponent in range(156):
        out[residue] = exponent
        residue = (2 * residue) % 169
    if len(out) != 156:
        raise AssertionError("2 is not primitive modulo 169 in this table")
    return out


def subgroup_parity_predicate_ok(doubling_subgroup: set[int]) -> bool:
    logs = log2_mod_169()
    for residue in range(1, QUOTIENT_LEVEL):
        if gcd(residue, QUOTIENT_LEVEL) != 1:
            continue
        parity_class = 1 if logs[residue % 169] % 2 == 0 else 2
        predicted_in_subgroup = residue % 3 == parity_class
        if predicted_in_subgroup != (residue in doubling_subgroup):
            return False
    return True


def summarize(name: str, word: dict[int, int], period: int) -> tuple[PeriodOrbitSummary, dict[int, int]]:
    actual_period = word_period(word, period)
    union, visit_counts = orbit_union_and_visits(word, period)
    norm = period_norm(word, period)
    summary = PeriodOrbitSummary(
        name=name,
        period=actual_period,
        word_support=len(word),
        orbit_union_support=len(union),
        orbit_visit_counts=visit_counts,
        period_norm_support=len(norm),
        period_norm_coefficient_counts=coefficient_counts(norm),
        period_norm_gcd_classes=gcd_classes(set(norm)),
        ok=actual_period == period,
    )
    return summary, norm


def profile_yang_y507_period_norm_character() -> YangY507PeriodNormCharacter:
    primitive = profile_yang_y507_primitive_factor_word()
    u_word = dict(primitive.u_primitive_word)
    y_word = dict(primitive.y507_primitive_word)
    u_summary, u_norm = summarize("U_507", u_word, SUPPORT_PERIOD)
    y_summary, y_norm = summarize("Y_507", y_word, SUPPORT_PERIOD)
    doubling_subgroup = residue_orbit(1)
    negative_subgroup = {(-residue) % QUOTIENT_LEVEL for residue in doubling_subgroup}
    units = {residue for residue in range(1, QUOTIENT_LEVEL) if gcd(residue, QUOTIENT_LEVEL) == 1}
    y_positive = {residue for residue, coefficient in y_norm.items() if coefficient > 0}
    y_negative = {residue for residue, coefficient in y_norm.items() if coefficient < 0}
    y_equals = y_norm == {residue: -3 * coefficient for residue, coefficient in u_norm.items()}
    positive_is_negative_subgroup = y_positive == negative_subgroup
    negative_is_subgroup = y_negative == doubling_subgroup
    nonunits_cancel = set(y_norm) == units and all(gcd(residue, QUOTIENT_LEVEL) == 1 for residue in y_norm)
    log_character_ok = subgroup_parity_predicate_ok(doubling_subgroup)
    direct_closer = False
    row_ok = (
        primitive.row_ok
        and QUOTIENT_LEVEL == 507
        and SUPPORT_PERIOD == 156
        and len(units) == 312
        and len(doubling_subgroup) == 156
        and doubling_subgroup.isdisjoint(negative_subgroup)
        and doubling_subgroup | negative_subgroup == units
        and u_summary.ok
        and y_summary.ok
        and u_summary.word_support == 6
        and y_summary.word_support == 12
        and u_summary.orbit_union_support == 468
        and y_summary.orbit_union_support == 468
        and u_summary.orbit_visit_counts == (2,)
        and y_summary.orbit_visit_counts == (4,)
        and u_summary.period_norm_support == 312
        and y_summary.period_norm_support == 312
        and u_summary.period_norm_coefficient_counts == ((-2, 156), (2, 156))
        and y_summary.period_norm_coefficient_counts == ((-6, 156), (6, 156))
        and u_summary.period_norm_gcd_classes == ((1, 312),)
        and y_summary.period_norm_gcd_classes == ((1, 312),)
        and y_equals
        and positive_is_negative_subgroup
        and negative_is_subgroup
        and nonunits_cancel
        and log_character_ok
        and not direct_closer
    )
    return YangY507PeriodNormCharacter(
        level=QUOTIENT_LEVEL,
        support_period=SUPPORT_PERIOD,
        unit_count=len(units),
        doubling_subgroup_size=len(doubling_subgroup),
        u_summary=u_summary,
        y_summary=y_summary,
        y_norm_equals_minus_three_u_norm=y_equals,
        y_positive_coset_is_negative_doubling_subgroup=positive_is_negative_subgroup,
        y_negative_coset_is_doubling_subgroup=negative_is_subgroup,
        nonunit_layer_cancels_in_period_norm=nonunits_cancel,
        log_parity_character_matches_doubling_subgroup=log_character_ok,
        direct_closer=direct_closer,
        positive_payload=(
            "The 156-period norm of Y_507 cancels all nonunits and becomes a "
            "dense signed index-two unit character: +6 on -<2> and -6 on <2>."
        ),
        first_missing_clause=(
            "the dense period norm is not a finite-field value/divisor theorem "
            "and does not extract a DANGER3 triple"
        ),
        recommendation=(
            "value-side theorem hits must account for this dense unit-character "
            "period norm; reject claims that treat the period product as trivial "
            "or as a sparse lower-level telescope"
        ),
        row_ok=row_ok,
    )


def print_summary(summary: PeriodOrbitSummary) -> None:
    print(f"  {summary.name}:")
    print(f"    period={summary.period}")
    print(f"    word_support={summary.word_support}")
    print(f"    orbit_union_support={summary.orbit_union_support}")
    print(f"    orbit_visit_counts={summary.orbit_visit_counts}")
    print(f"    period_norm_support={summary.period_norm_support}")
    print(f"    period_norm_coefficient_counts={summary.period_norm_coefficient_counts}")
    print(f"    period_norm_gcd_classes={summary.period_norm_gcd_classes}")
    print(f"    ok={int(summary.ok)}")


def main() -> int:
    profile = profile_yang_y507_period_norm_character()
    print("p25 KSY-y Yang Y_507 period-norm character gate")
    print(f"level={profile.level}")
    print(f"support_period={profile.support_period}")
    print(f"unit_count={profile.unit_count}")
    print(f"doubling_subgroup_size={profile.doubling_subgroup_size}")
    print("orbit_summaries")
    print_summary(profile.u_summary)
    print_summary(profile.y_summary)
    print("period_norm_character")
    print(f"  y_norm_equals_minus_three_u_norm={int(profile.y_norm_equals_minus_three_u_norm)}")
    print(
        "  y_positive_coset_is_negative_doubling_subgroup="
        f"{int(profile.y_positive_coset_is_negative_doubling_subgroup)}"
    )
    print(f"  y_negative_coset_is_doubling_subgroup={int(profile.y_negative_coset_is_doubling_subgroup)}")
    print(f"  nonunit_layer_cancels_in_period_norm={int(profile.nonunit_layer_cancels_in_period_norm)}")
    print(
        "  log_parity_character_matches_doubling_subgroup="
        f"{int(profile.log_parity_character_matches_doubling_subgroup)}"
    )
    print("checks")
    print(f"  direct_closer={int(profile.direct_closer)}")
    print("interpretation")
    print("  period_product_is_dense_unit_character_not_trivial_telescope=1")
    print("  positive_coset_is_minus_doubling_subgroup_and_negative_coset_is_doubling_subgroup=1")
    print("  still_missing_value_or_divisor_theorem_and_DANGER3_extraction=1")
    print(
        "ksy_y_yang_y507_period_norm_character_rows="
        f"{int(profile.row_ok)}/1"
    )
    if not profile.row_ok:
        raise SystemExit("Yang Y_507 period-norm character regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
