#!/usr/bin/env python3
"""Source-parameter hygiene gate for the p25 KSY-y moonshot.

The current moonshot target uses several overloaded symbols:

* the `[2]` in the KSY normalized-y formula `y(Q)=-g(2Q)/g(Q)^4`;
* the finite raw direction `D=(22,3)` and quotient direction `(1,3)`;
* the Kato-Siegel integer parameter in `D theta`;
* Kubert-Lang/Siegel-function levels such as `169`, `507`, and `12675`.

This gate prevents a theorem scout from moving a statement across those
boundaries without a source clause.  In particular, KSY's doubling operator is
not the ordinary Kato-Siegel `D theta` parameter, and the prime-power/C169
Kubert-Lang screen is not by itself an exact mixed `C_3 x C_169` producer.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd


P25 = 10000000000000000000000013
KSY_DOUBLING = 2
ORDINARY_KATO_THETA_PARAMETER = 2
RAW_D_STEP = (22, 3)
QUOTIENT_D_STEP = (1, 3)
RAW_LEVEL = 12675
MIXED_VISIBLE_LEVEL = 507
C_AXIS_LEVEL = 169
RIGHT_ORDER = 75
C_ORDER = 169


@dataclass(frozen=True)
class ParameterHygieneRow:
    name: str
    source_family: str
    symbol: str
    interpreted_as: str
    numeric_value: str
    prime_to_6_required: bool
    prime_to_6_ok: bool
    level: int | None
    level_prime_power_away_from_2_3: bool
    preserves_mixed_graph: bool
    decision: str
    first_missing_clause: str
    next_action: str
    row_ok: bool


@dataclass(frozen=True)
class SourceParameterHygieneProfile:
    p: int
    rows: tuple[ParameterHygieneRow, ...]
    safe_notational_rows: int
    conditional_source_rows: int
    rejected_misread_rows: int
    c_axis_level_ok_for_prime_power_kl_screen: bool
    mixed_levels_need_extra_source_clause: bool
    ordinary_kato_theta_2_rejected: bool
    ksy_doubling_remains_live: bool
    raw_d_remains_finite_direction_only: bool
    row_ok: bool


def is_prime_power_away_from_2_3(n: int) -> bool:
    if n <= 1 or gcd(n, 6) != 1:
        return False
    remaining = n
    prime = None
    d = 2
    while d * d <= remaining:
        if remaining % d == 0:
            prime = d
            while remaining % d == 0:
                remaining //= d
            break
        d += 1
    if prime is None:
        prime = remaining
        remaining = 1
    if remaining != 1:
        return False
    return prime not in (2, 3)


def row(
    name: str,
    source_family: str,
    symbol: str,
    interpreted_as: str,
    numeric_value: str,
    prime_to_6_required: bool,
    level: int | None,
    preserves_mixed_graph: bool,
    decision: str,
    first_missing_clause: str,
    next_action: str,
) -> ParameterHygieneRow:
    if not prime_to_6_required:
        prime_to_6_ok = True
    elif numeric_value.lstrip("-").isdigit():
        prime_to_6_ok = gcd(abs(int(numeric_value)), 6) == 1
    else:
        prime_to_6_ok = False
    level_ok = False if level is None else is_prime_power_away_from_2_3(level)
    expected_ok = decision in {
        "safe_ksy_doubling_not_kato_parameter",
        "safe_finite_D_direction_not_source_parameter",
        "conditional_needs_even_D_kronecker_clause",
        "conditional_prime_power_projection_only",
        "conditional_mixed_level_not_covered_by_prime_power_screen",
        "reject_ordinary_kato_theta_2_prime_to_6_violation",
    }
    if decision == "reject_ordinary_kato_theta_2_prime_to_6_violation":
        expected_ok = expected_ok and prime_to_6_required and not prime_to_6_ok
    if decision == "conditional_prime_power_projection_only":
        expected_ok = expected_ok and level_ok and not preserves_mixed_graph
    if decision == "conditional_mixed_level_not_covered_by_prime_power_screen":
        expected_ok = expected_ok and level is not None and not level_ok and preserves_mixed_graph
    return ParameterHygieneRow(
        name=name,
        source_family=source_family,
        symbol=symbol,
        interpreted_as=interpreted_as,
        numeric_value=numeric_value,
        prime_to_6_required=prime_to_6_required,
        prime_to_6_ok=prime_to_6_ok,
        level=level,
        level_prime_power_away_from_2_3=level_ok,
        preserves_mixed_graph=preserves_mixed_graph,
        decision=decision,
        first_missing_clause=first_missing_clause,
        next_action=next_action,
        row_ok=expected_ok,
    )


def profile_source_parameter_hygiene() -> SourceParameterHygieneProfile:
    rows = (
        row(
            "ksy_normalized_y_doubling",
            "Koo-Shin-Yoon normalized y / Siegel formula",
            "[2] in y(Q)=-g(2Q)/g(Q)^4",
            "multiplication-by-2 inside the normalized-y formula",
            str(KSY_DOUBLING),
            prime_to_6_required=False,
            level=RAW_LEVEL,
            preserves_mixed_graph=True,
            decision="safe_ksy_doubling_not_kato_parameter",
            first_missing_clause="exact theorem proving the full K-traced product P",
            next_action="keep KSY-y formula route; do not identify [2] with ordinary Kato Dtheta",
        ),
        row(
            "ordinary_kato_theta_parameter_2",
            "ordinary Kato-Siegel Dtheta",
            "D=2",
            "integer parameter in the ordinary Dtheta unit theorem",
            str(ORDINARY_KATO_THETA_PARAMETER),
            prime_to_6_required=True,
            level=None,
            preserves_mixed_graph=False,
            decision="reject_ordinary_kato_theta_2_prime_to_6_violation",
            first_missing_clause="ordinary Dtheta source clause allowing D=2",
            next_action="kill direct ordinary Kato Dtheta import at D=2; use only as odd-D sanity check",
        ),
        row(
            "sprang_kronecker_even_D_variant",
            "Sprang/Kronecker differential or additive route",
            "D=2",
            "even-D Kronecker/differential specialization, not ordinary Dtheta",
            str(ORDINARY_KATO_THETA_PARAMETER),
            prime_to_6_required=False,
            level=RAW_LEVEL,
            preserves_mixed_graph=True,
            decision="conditional_needs_even_D_kronecker_clause",
            first_missing_clause="explicit even-D Kronecker/differential clause emitting exact P",
            next_action="keep live only if the source supplies an even-D differential/additive identity for P",
        ),
        row(
            "raw_D_step_22_3",
            "p25 finite source geometry",
            "D=(22,3), quotient D=(1,3)",
            "finite raw/quotient direction in C_75 x C_169",
            f"{RAW_D_STEP}",
            prime_to_6_required=False,
            level=RAW_LEVEL,
            preserves_mixed_graph=True,
            decision="safe_finite_D_direction_not_source_parameter",
            first_missing_clause="arithmetic theorem using this finite direction",
            next_action="treat D as geometry only; do not use it to satisfy source integer-parameter hypotheses",
        ),
        row(
            "kubert_lang_c169_prime_power_projection",
            "Kubert-Lang/Siegel-function prime-power screen",
            "N=169",
            "C-axis prime-power level",
            str(C_AXIS_LEVEL),
            prime_to_6_required=False,
            level=C_AXIS_LEVEL,
            preserves_mixed_graph=False,
            decision="conditional_prime_power_projection_only",
            first_missing_clause="mixed C_3 x C_169 graph selector and row anchor",
            next_action="use as a necessary C-axis screen, not as an exact p25 producer",
        ),
        row(
            "kubert_lang_mixed_levels_507_12675",
            "Kubert-Lang/Siegel-function mixed p25 payload",
            "N=507 or N=12675",
            "mixed level carrying the C_3 row graph and raw K trace",
            f"{MIXED_VISIBLE_LEVEL}/{RAW_LEVEL}",
            prime_to_6_required=False,
            level=MIXED_VISIBLE_LEVEL,
            preserves_mixed_graph=True,
            decision="conditional_mixed_level_not_covered_by_prime_power_screen",
            first_missing_clause="source theorem covering the mixed row graph, not only C169 congruences",
            next_action="require exact mixed-level product theorem or reduction to an accepted finite identity",
        ),
    )
    safe_rows = sum(
        int(
            r.decision
            in {
                "safe_ksy_doubling_not_kato_parameter",
                "safe_finite_D_direction_not_source_parameter",
            }
        )
        for r in rows
    )
    conditional_rows = sum(int(r.decision.startswith("conditional_")) for r in rows)
    rejected_rows = sum(int(r.decision.startswith("reject_")) for r in rows)
    c_axis_ok = is_prime_power_away_from_2_3(C_AXIS_LEVEL)
    mixed_needs_clause = (
        not is_prime_power_away_from_2_3(MIXED_VISIBLE_LEVEL)
        and gcd(MIXED_VISIBLE_LEVEL, 6) == 3
        and gcd(RAW_LEVEL, 6) == 3
    )
    ordinary_kato_rejected = any(
        r.name == "ordinary_kato_theta_parameter_2"
        and r.decision == "reject_ordinary_kato_theta_2_prime_to_6_violation"
        and not r.prime_to_6_ok
        for r in rows
    )
    ksy_live = any(
        r.name == "ksy_normalized_y_doubling"
        and r.decision == "safe_ksy_doubling_not_kato_parameter"
        and r.preserves_mixed_graph
        for r in rows
    )
    raw_d_finite_only = any(
        r.name == "raw_D_step_22_3"
        and r.decision == "safe_finite_D_direction_not_source_parameter"
        and r.preserves_mixed_graph
        for r in rows
    )
    row_ok = (
        P25 == 10000000000000000000000013
        and RIGHT_ORDER == 75
        and C_ORDER == 169
        and RAW_LEVEL == RIGHT_ORDER * C_ORDER
        and MIXED_VISIBLE_LEVEL == 3 * C_ORDER
        and C_AXIS_LEVEL == C_ORDER
        and safe_rows == 2
        and conditional_rows == 3
        and rejected_rows == 1
        and c_axis_ok
        and mixed_needs_clause
        and ordinary_kato_rejected
        and ksy_live
        and raw_d_finite_only
        and all(r.row_ok for r in rows)
    )
    return SourceParameterHygieneProfile(
        p=P25,
        rows=rows,
        safe_notational_rows=safe_rows,
        conditional_source_rows=conditional_rows,
        rejected_misread_rows=rejected_rows,
        c_axis_level_ok_for_prime_power_kl_screen=c_axis_ok,
        mixed_levels_need_extra_source_clause=mixed_needs_clause,
        ordinary_kato_theta_2_rejected=ordinary_kato_rejected,
        ksy_doubling_remains_live=ksy_live,
        raw_d_remains_finite_direction_only=raw_d_finite_only,
        row_ok=row_ok,
    )


def print_row(row_: ParameterHygieneRow) -> None:
    print(
        "  "
        f"{row_.name}: family={row_.source_family} symbol={row_.symbol} "
        f"as={row_.interpreted_as} value={row_.numeric_value} "
        f"prime_to_6_required={int(row_.prime_to_6_required)} "
        f"prime_to_6_ok={int(row_.prime_to_6_ok)} "
        f"level={row_.level if row_.level is not None else 'none'} "
        f"level_pp_away_2_3={int(row_.level_prime_power_away_from_2_3)} "
        f"mixed_graph={int(row_.preserves_mixed_graph)} "
        f"decision={row_.decision} missing={row_.first_missing_clause}"
    )


def main() -> int:
    print("p25 Lane B Robert KSY Kubert-Lang KSY-y source-parameter hygiene gate")
    profile = profile_source_parameter_hygiene()
    print(f"source_parameter_hygiene_profile={profile}")
    print("rows")
    for hygiene_row in profile.rows:
        print_row(hygiene_row)
    print("counts")
    print(f"  safe_notational_rows={profile.safe_notational_rows}")
    print(f"  conditional_source_rows={profile.conditional_source_rows}")
    print(f"  rejected_misread_rows={profile.rejected_misread_rows}")
    print("interpretation")
    print(
        "  "
        f"c_axis_level_ok_for_prime_power_kl_screen="
        f"{int(profile.c_axis_level_ok_for_prime_power_kl_screen)}"
    )
    print(
        "  "
        f"mixed_levels_need_extra_source_clause="
        f"{int(profile.mixed_levels_need_extra_source_clause)}"
    )
    print(f"  ordinary_kato_theta_2_rejected={int(profile.ordinary_kato_theta_2_rejected)}")
    print(f"  ksy_doubling_remains_live={int(profile.ksy_doubling_remains_live)}")
    print(
        "  "
        f"raw_d_remains_finite_direction_only="
        f"{int(profile.raw_d_remains_finite_direction_only)}"
    )
    print("robert_ksy_theta2_kubert_lang_ksy_y_source_parameter_hygiene_rows=1/1")
    if not profile.row_ok:
        raise SystemExit("source-parameter hygiene regression failed")
    print("conclusion=reported_p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_source_parameter_hygiene")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
