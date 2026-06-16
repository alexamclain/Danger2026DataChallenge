#!/usr/bin/env python3
"""Yang/Yu modular-unit and period certificate for the p25 Y_507 target.

The quotient normalized-y descent defines

    Y_507 = [2]^*U_507 / U_507^4.

This gate checks that Y_507 itself is a valid Yang/Yu modular unit on X_1(507)
and that its quotient-level doubling period is exactly 156.  That gives the
compact quotient target its own period-156 context, while still stopping short
of a finite-field value theorem or DANGER3 extraction.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd

from p25_ksy_y_yang_quotient_normalized_y_descent_gate import (
    profile_yang_quotient_normalized_y_descent,
)
from p25_ksy_y_yang_x1_orbit_distribution_bridge_gate import (
    orbit_bad_count,
    prime_factors,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_exponent_matrix_gate import (
    QUOTIENT_LEVEL,
)


P25 = 10**25 + 13
SUPPORT_PERIOD = 156
AMBIENT_PERIOD = 780


@dataclass(frozen=True)
class YangY507ModularPeriodCertificate:
    level: int
    y507_exponents: tuple[tuple[int, int], ...]
    exponent_sum_mod_12: int
    quadratic_sum_mod_level: int
    odd_level_modularity_congruences_ok: bool
    signed_orbit_bad_counts: tuple[tuple[int, int], ...]
    unsigned_orbit_bad_counts: tuple[tuple[int, int], ...]
    signed_orbit_condition_ok: bool
    unsigned_orbit_condition_fails_as_control: bool
    general_even_formula_linear_sum_mod_2: int
    general_even_formula_quadratic_sum_mod_2_level: int
    general_even_formula_control_fails: bool
    minimum_doubling_period: int
    fixed_by_period_156: bool
    proper_period_divisors_fail: bool
    support_period_root_gcd_fp_star: int
    ambient_period_root_gcd_fp_star: int
    quotient_descent_ok: bool
    direct_closer: bool
    positive_payload: str
    first_missing_clause: str
    recommendation: str
    row_ok: bool


def divisors(value: int) -> tuple[int, ...]:
    out = []
    for divisor in range(1, value + 1):
        if value % divisor == 0:
            out.append(divisor)
    return tuple(out)


def push_doubling(exponents: dict[int, int], period: int) -> dict[int, int]:
    multiplier = pow(2, period, QUOTIENT_LEVEL)
    out: dict[int, int] = {}
    for residue, exponent in exponents.items():
        target = (multiplier * residue) % QUOTIENT_LEVEL
        out[target] = out.get(target, 0) + exponent
    return dict(sorted((residue, exponent) for residue, exponent in out.items() if exponent))


def minimum_doubling_period(exponents: dict[int, int], limit: int) -> int:
    for period in range(1, limit + 1):
        if push_doubling(exponents, period) == exponents:
            return period
    raise AssertionError("doubling period exceeds limit")


def profile_yang_y507_modular_period_certificate() -> YangY507ModularPeriodCertificate:
    descent = profile_yang_quotient_normalized_y_descent()
    y507 = dict(descent.quotient_footprint)
    factors = prime_factors(QUOTIENT_LEVEL)
    exponent_sum = sum(y507.values())
    quadratic_sum = sum(residue * residue * exponent for residue, exponent in y507.items())
    linear_sum = sum(residue * exponent for residue, exponent in y507.items())
    signed_bad = tuple((prime, orbit_bad_count(y507, prime, signed=True)) for prime in factors)
    unsigned_bad = tuple((prime, orbit_bad_count(y507, prime, signed=False)) for prime in factors)
    signed_ok = all(count == 0 for _prime, count in signed_bad)
    unsigned_control = any(count > 0 for _prime, count in unsigned_bad)
    odd_modular_ok = (
        QUOTIENT_LEVEL % 2 == 1
        and exponent_sum % 12 == 0
        and quadratic_sum % QUOTIENT_LEVEL == 0
    )
    even_control_fails = (
        linear_sum % 2 != 0
        and quadratic_sum % (2 * QUOTIENT_LEVEL) != 0
    )
    min_period = minimum_doubling_period(y507, SUPPORT_PERIOD)
    fixed_156 = push_doubling(y507, SUPPORT_PERIOD) == y507
    proper_fail = all(
        push_doubling(y507, period) != y507
        for period in divisors(SUPPORT_PERIOD)
        if period < SUPPORT_PERIOD
    )
    support_gcd = gcd(pow(4, SUPPORT_PERIOD, P25 - 1) - 1, P25 - 1)
    ambient_gcd = gcd(pow(4, AMBIENT_PERIOD, P25 - 1) - 1, P25 - 1)
    direct_closer = False
    row_ok = (
        descent.row_ok
        and QUOTIENT_LEVEL == 507
        and factors == (3, 13)
        and len(y507) == 12
        and odd_modular_ok
        and signed_ok
        and unsigned_control
        and even_control_fails
        and min_period == SUPPORT_PERIOD
        and fixed_156
        and proper_fail
        and support_gcd == 1
        and ambient_gcd == 11
        and not direct_closer
    )
    return YangY507ModularPeriodCertificate(
        level=QUOTIENT_LEVEL,
        y507_exponents=tuple(sorted(y507.items())),
        exponent_sum_mod_12=exponent_sum % 12,
        quadratic_sum_mod_level=quadratic_sum % QUOTIENT_LEVEL,
        odd_level_modularity_congruences_ok=odd_modular_ok,
        signed_orbit_bad_counts=signed_bad,
        unsigned_orbit_bad_counts=unsigned_bad,
        signed_orbit_condition_ok=signed_ok,
        unsigned_orbit_condition_fails_as_control=unsigned_control,
        general_even_formula_linear_sum_mod_2=linear_sum % 2,
        general_even_formula_quadratic_sum_mod_2_level=quadratic_sum % (2 * QUOTIENT_LEVEL),
        general_even_formula_control_fails=even_control_fails,
        minimum_doubling_period=min_period,
        fixed_by_period_156=fixed_156,
        proper_period_divisors_fail=proper_fail,
        support_period_root_gcd_fp_star=support_gcd,
        ambient_period_root_gcd_fp_star=ambient_gcd,
        quotient_descent_ok=descent.row_ok,
        direct_closer=direct_closer,
        positive_payload=(
            "Y_507 is a Yang/Yu modular unit on X_1(507) with exact doubling "
            "period 156 and unique F_p^* root at the support period"
        ),
        first_missing_clause=(
            "no source theorem yet gives the finite-field value/divisor identity "
            "for Y_507 or extracts a DANGER3 triple"
        ),
        recommendation=(
            "treat Y_507 as the compact theorem target: a future hit must prove "
            "its value/divisor identity, not just its modular-unit admissibility"
        ),
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_yang_y507_modular_period_certificate()
    print("p25 KSY-y Yang Y_507 modular-period certificate gate")
    print(f"level={profile.level}")
    print(f"y507_exponents={profile.y507_exponents}")
    print("modularity")
    print(f"  exponent_sum_mod_12={profile.exponent_sum_mod_12}")
    print(f"  quadratic_sum_mod_level={profile.quadratic_sum_mod_level}")
    print(
        "  odd_level_modularity_congruences_ok="
        f"{int(profile.odd_level_modularity_congruences_ok)}"
    )
    print("orbit_condition")
    print(f"  signed_orbit_bad_counts={profile.signed_orbit_bad_counts}")
    print(f"  unsigned_orbit_bad_counts={profile.unsigned_orbit_bad_counts}")
    print(f"  signed_orbit_condition_ok={int(profile.signed_orbit_condition_ok)}")
    print(
        "  unsigned_orbit_condition_fails_as_control="
        f"{int(profile.unsigned_orbit_condition_fails_as_control)}"
    )
    print("controls")
    print(
        "  general_even_formula_linear_sum_mod_2="
        f"{profile.general_even_formula_linear_sum_mod_2}"
    )
    print(
        "  general_even_formula_quadratic_sum_mod_2_level="
        f"{profile.general_even_formula_quadratic_sum_mod_2_level}"
    )
    print(
        "  general_even_formula_control_fails="
        f"{int(profile.general_even_formula_control_fails)}"
    )
    print("period")
    print(f"  minimum_doubling_period={profile.minimum_doubling_period}")
    print(f"  fixed_by_period_156={int(profile.fixed_by_period_156)}")
    print(f"  proper_period_divisors_fail={int(profile.proper_period_divisors_fail)}")
    print(f"  support_period_root_gcd_Fp_star={profile.support_period_root_gcd_fp_star}")
    print(f"  ambient_period_root_gcd_Fp_star={profile.ambient_period_root_gcd_fp_star}")
    print("checks")
    print(f"  quotient_descent_ok={int(profile.quotient_descent_ok)}")
    print(f"  direct_closer={int(profile.direct_closer)}")
    print("interpretation")
    print("  Y_507_is_valid_X1_507_modular_unit=1")
    print("  Y_507_has_exact_doubling_period_156=1")
    print("  support_period_value_root_is_unique_in_Fp_star=1")
    print("  still_missing_value_or_divisor_theorem_and_DANGER3_extraction=1")
    print(
        "ksy_y_yang_y507_modular_period_certificate_rows="
        f"{int(profile.row_ok)}/1"
    )
    if not profile.row_ok:
        raise SystemExit("Yang Y_507 modular-period certificate regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
