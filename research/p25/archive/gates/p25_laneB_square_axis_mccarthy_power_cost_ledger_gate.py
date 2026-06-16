#!/usr/bin/env python3
"""Cost ledger for the powered McCarthy quotient route.

The powered-transport gate closes the finite raw-Y payload conditional on an
arithmetic producer for

    (R(q)^2029 - 1) / (zeta_39^5 - 1).

This gate prices that remaining move against the p25 sub-sqrt target.  It is
not a proof that the powered quotient is an allowed arithmetic object.  It
records that the 2029th power and the determined scalar normalization are not
themselves a size obstruction under conservative finite-payload accounting.

Even the intentionally pessimistic bound

    2029 * raw_order(C_3 x C_169 x B_25)

is only 25,717,575, far below sqrt(10^25+13).
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isqrt

from p25_laneB_square_axis_gross_koblitz_projector_raw_y_gate import projector_raw_y_profile
from p25_laneB_square_axis_mccarthy_power_transport_raw_y_gate import (
    mccarthy_power_transport_raw_y_profile,
)
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER


P25 = 10**25 + 13
SQRT_FLOOR = 3_162_277_660_168
POWER_EXPONENT = 2029
RAW_ORDER = 12675
S_TRACE_SUPPORT = 3


@dataclass(frozen=True)
class McCarthyPowerCostLedgerProfile:
    p: int
    sqrt_floor: int
    power_exponent: int
    exponent_bit_length: int
    exponent_popcount: int
    binary_power_multiplications: int
    s_trace_power_bound: int
    quotient_packet_support: int
    quotient_packet_power_bound: int
    twist_dense_power_bound: int
    raw_y_nonzero: int
    raw_y_power_bound: int
    raw_order: int
    raw_order_power_bound: int
    worst_bound: int
    worst_margin_to_sqrt: int
    transport_normalized_closes: bool
    unnormalized_control_fails: bool
    coefficient_inverse: int
    finite_cost_below_sqrt: bool
    binary_power_tiny: bool
    scalar_normalization_determined: bool
    remaining_debt_is_arithmetic_not_size: bool


def popcount(value: int) -> int:
    return bin(value).count("1")


def mccarthy_power_cost_ledger_profile() -> McCarthyPowerCostLedgerProfile:
    transport = mccarthy_power_transport_raw_y_profile()
    raw_y = projector_raw_y_profile()
    bit_length = len(bin(POWER_EXPONENT)) - 2
    pop = popcount(POWER_EXPONENT)
    binary_ops = bit_length - 1 + pop - 1
    s_bound = POWER_EXPONENT * S_TRACE_SUPPORT
    quotient_bound = POWER_EXPONENT * raw_y.quotient_support
    twist_bound = POWER_EXPONENT * QUOTIENT_ORDER
    raw_y_bound = POWER_EXPONENT * transport.normalized_attempt.raw_y_nonzero
    raw_order_bound = POWER_EXPONENT * RAW_ORDER
    worst = max(s_bound, quotient_bound, twist_bound, raw_y_bound, raw_order_bound)
    return McCarthyPowerCostLedgerProfile(
        p=P25,
        sqrt_floor=SQRT_FLOOR,
        power_exponent=POWER_EXPONENT,
        exponent_bit_length=bit_length,
        exponent_popcount=pop,
        binary_power_multiplications=binary_ops,
        s_trace_power_bound=s_bound,
        quotient_packet_support=raw_y.quotient_support,
        quotient_packet_power_bound=quotient_bound,
        twist_dense_power_bound=twist_bound,
        raw_y_nonzero=transport.normalized_attempt.raw_y_nonzero,
        raw_y_power_bound=raw_y_bound,
        raw_order=RAW_ORDER,
        raw_order_power_bound=raw_order_bound,
        worst_bound=worst,
        worst_margin_to_sqrt=SQRT_FLOOR // worst,
        transport_normalized_closes=transport.normalized_raw_y_closes,
        unnormalized_control_fails=transport.unnormalized_control_fails_exact_packet,
        coefficient_inverse=transport.transported_minus_one_inverse,
        finite_cost_below_sqrt=worst < SQRT_FLOOR,
        binary_power_tiny=binary_ops < 64,
        scalar_normalization_determined=transport.transported_minus_one_inverse == 636,
        remaining_debt_is_arithmetic_not_size=(
            worst < SQRT_FLOOR
            and transport.normalized_raw_y_closes
            and transport.unnormalized_control_fails_exact_packet
        ),
    )


def main() -> int:
    print("p25 Lane B McCarthy power-cost ledger gate")
    profile = mccarthy_power_cost_ledger_profile()
    row_ok = (
        profile.p == P25
        and profile.sqrt_floor == isqrt(P25)
        and profile.sqrt_floor == SQRT_FLOOR
        and profile.power_exponent == 2029
        and profile.exponent_bit_length == 11
        and profile.exponent_popcount == 9
        and profile.binary_power_multiplications == 18
        and profile.s_trace_power_bound == 6087
        and profile.quotient_packet_support == 252
        and profile.quotient_packet_power_bound == 511308
        and profile.twist_dense_power_bound == 1028703
        and profile.raw_y_nonzero == 6300
        and profile.raw_y_power_bound == 12782700
        and profile.raw_order == 12675
        and profile.raw_order_power_bound == 25717575
        and profile.worst_bound == 25717575
        and profile.worst_margin_to_sqrt == 122961
        and profile.transport_normalized_closes
        and profile.unnormalized_control_fails
        and profile.coefficient_inverse == 636
        and profile.finite_cost_below_sqrt
        and profile.binary_power_tiny
        and profile.scalar_normalization_determined
        and profile.remaining_debt_is_arithmetic_not_size
    )

    print(f"mccarthy_power_cost_ledger_profile={profile}")
    print("cost_ledger_laws")
    print("  binary_exponentiation_for_2029_needs_18_multiplications=1")
    print("  2029_times_S_trace_support_is_6087=1")
    print("  2029_times_quotient_packet_support_is_511308=1")
    print("  2029_times_dense_C507_twist_space_is_1028703=1")
    print("  2029_times_raw_Y_support_is_12782700=1")
    print("  2029_times_full_raw_order_is_25717575=1")
    print("  worst_conservative_bound_is_below_sqrt_by_factor_122961=1")
    print("interpretation")
    print("  powered_mccarthy_route_is_not_killed_by_subsqrt_size_accounting=1")
    print("  remaining_debt_is_arithmetic_legitimacy_of_power_and_scaling=1")
    print(f"square_axis_mccarthy_power_cost_ledger_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_mccarthy_power_cost_ledger_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
