#!/usr/bin/env python3
"""Right Gauss-sum reduction for the p24 obstruction polynomial.

For the right factor in the product-coboundary route,

    R_{chi,-a} = sum_v chi(v) T_{0,v,-a},

expand the class index as i = r + m*k with 0 <= r < m.  Since
m is divisible by 211, the additive right character only sees r mod 211.
The finite Gauss-sum identity gives

    sum_v chi(v) zeta_211^(v*r) =
      tau(chi) * chi^{-1}(r)    if r != 0 mod 211,
      0                         if r == 0 mod 211.

Thus, after dividing by the nonzero Gauss sum tau(chi), the right obstruction
is a single weighted relative polynomial

    G_chi(X) = sum_r w_chi(r) F_r(X),
    w_chi(r) = chi^{-1}(r mod 211),

evaluated at X = zeta_n^{-a}.  The remaining p24 theorem is therefore the
internal-character statement for this named weighted polynomial, not raw CM
periods and not termwise right-combo vanishing.
"""

from __future__ import annotations

import random


RIGHT = 211
RIGHT_GEN = 2
ORDER7 = 7
FIELD_Q = 8863  # 8863 - 1 = 6 * 211 * 7.
TOY_N = 31
TOY_INTERNAL_ORDER = 15
TOY_C_DEGREE = 5
TOY_B_OVER_C_DEGREE = 3
SEED = 20260606


def factor_distinct(value: int) -> set[int]:
    factors: set[int] = set()
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            factors.add(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor += 1
    if value > 1:
        factors.add(value)
    return factors


def primitive_root(q: int) -> int:
    factors = factor_distinct(q - 1)
    for candidate in range(2, q):
        if all(pow(candidate, (q - 1) // factor, q) != 1 for factor in factors):
            return candidate
    raise RuntimeError("no primitive root")


def log_table_mod_prime(modulus: int, generator: int) -> dict[int, int]:
    logs: dict[int, int] = {}
    value = 1
    for exponent in range(modulus - 1):
        logs[value] = exponent
        value = value * generator % modulus
    if len(logs) != modulus - 1:
        raise RuntimeError("bad generator")
    return logs


def character(value: int, zeta7: int, logs: dict[int, int], index: int) -> int:
    value %= RIGHT
    if value == 0:
        return 0
    return pow(zeta7, (index * logs[value]) % ORDER7, FIELD_Q)


def additive_gauss_sum(zeta211: int, zeta7: int, logs: dict[int, int], index: int) -> int:
    total = 0
    for v in range(1, RIGHT):
        total = (
            total
            + character(v, zeta7, logs, index) * pow(zeta211, v, FIELD_Q)
        ) % FIELD_Q
    return total


def gauss_additive_sum_for_residue(
    residue: int,
    zeta211: int,
    zeta7: int,
    logs: dict[int, int],
    index: int,
) -> int:
    total = 0
    for v in range(1, RIGHT):
        total = (
            total
            + character(v, zeta7, logs, index)
            * pow(zeta211, (v * residue) % RIGHT, FIELD_Q)
        ) % FIELD_Q
    return total


def polynomial_eval(coefficients: list[int], point: int) -> int:
    total = 0
    power = 1
    for coeff in coefficients:
        total = (total + coeff * power) % FIELD_Q
        power = power * point % FIELD_Q
    return total


def random_fibers(rng: random.Random) -> list[list[int]]:
    return [
        [rng.randrange(FIELD_Q) for _k in range(TOY_N)]
        for _r in range(RIGHT)
    ]


def right_resolvent_direct(
    fibers: list[list[int]],
    point: int,
    zeta211: int,
    zeta7: int,
    logs: dict[int, int],
    index: int,
) -> int:
    total = 0
    for v in range(1, RIGHT):
        coeff = character(v, zeta7, logs, index)
        inner = 0
        for residue, fiber in enumerate(fibers):
            inner = (
                inner
                + pow(zeta211, (v * residue) % RIGHT, FIELD_Q)
                * polynomial_eval(fiber, point)
            ) % FIELD_Q
        total = (total + coeff * inner) % FIELD_Q
    return total


def weighted_polynomial_coefficients(
    fibers: list[list[int]],
    zeta7: int,
    logs: dict[int, int],
    index: int,
) -> list[int]:
    coeffs = [0] * TOY_N
    for residue, fiber in enumerate(fibers):
        if residue == 0:
            continue
        weight = pow(character(residue, zeta7, logs, index), -1, FIELD_Q)
        for k, value in enumerate(fiber):
            coeffs[k] = (coeffs[k] + weight * value) % FIELD_Q
    return coeffs


def internal_subgroup_generator(zeta_n: int) -> int:
    # 2 has order 5 modulo 31; 3 has order 30, so 3^2 has order 15.
    exponent_generator = pow(3, 2, TOY_N)
    return exponent_generator


def internal_trace(coefficients: list[int], zeta_n: int, a: int, subgroup: list[int]) -> int:
    return sum(
        polynomial_eval(coefficients, pow(zeta_n, (a * exponent) % TOY_N, FIELD_Q))
        for exponent in subgroup
    ) % FIELD_Q


def force_internal_trace_zero(coefficients: list[int], zeta_n: int, a: int, subgroup: list[int]) -> list[int]:
    adjusted = coefficients[:]
    period_values = [
        sum(pow(zeta_n, (a * k * exponent) % TOY_N, FIELD_Q) for exponent in subgroup) % FIELD_Q
        for k in range(TOY_N)
    ]
    pivot = next(k for k in range(1, TOY_N) if period_values[k])
    current = internal_trace(adjusted, zeta_n, a, subgroup)
    adjusted[pivot] = (
        adjusted[pivot] - current * pow(period_values[pivot], -1, FIELD_Q)
    ) % FIELD_Q
    return adjusted


def main() -> None:
    root = primitive_root(FIELD_Q)
    zeta211 = pow(root, (FIELD_Q - 1) // RIGHT, FIELD_Q)
    zeta7 = pow(root, (FIELD_Q - 1) // ORDER7, FIELD_Q)
    zeta_n = pow(root, (FIELD_Q - 1) // TOY_N, FIELD_Q)
    logs = log_table_mod_prime(RIGHT, RIGHT_GEN)
    rng = random.Random(SEED)

    subgroup_generator = internal_subgroup_generator(zeta_n)
    subgroup: list[int] = []
    value = 1
    for _index in range(TOY_INTERNAL_ORDER):
        subgroup.append(value)
        value = value * subgroup_generator % TOY_N

    gauss_identity_failures = 0
    right_reduction_failures = 0
    random_internal_trace_nonzero = 0
    forced_internal_trace_zero = 0
    residue_zero_additive_sums = 0
    trials = 0

    for character_index in range(1, ORDER7):
        tau = additive_gauss_sum(zeta211, zeta7, logs, character_index)
        if tau == 0:
            raise RuntimeError("zero Gauss sum")
        for residue in range(RIGHT):
            additive = gauss_additive_sum_for_residue(
                residue,
                zeta211,
                zeta7,
                logs,
                character_index,
            )
            if residue == 0:
                residue_zero_additive_sums += int(additive == 0)
                expected = 0
            else:
                expected = tau * pow(character(residue, zeta7, logs, character_index), -1, FIELD_Q) % FIELD_Q
            gauss_identity_failures += int(additive != expected)

        for a in (1, 3):
            fibers = random_fibers(rng)
            point = pow(zeta_n, -a, FIELD_Q)
            direct = right_resolvent_direct(
                fibers,
                point,
                zeta211,
                zeta7,
                logs,
                character_index,
            )
            weighted = weighted_polynomial_coefficients(fibers, zeta7, logs, character_index)
            reduced = tau * polynomial_eval(weighted, point) % FIELD_Q
            right_reduction_failures += int(direct != reduced)
            random_internal_trace_nonzero += int(
                internal_trace(weighted, zeta_n, a, subgroup) != 0
            )
            forced = force_internal_trace_zero(weighted, zeta_n, a, subgroup)
            forced_internal_trace_zero += int(
                internal_trace(forced, zeta_n, a, subgroup) == 0
                and any(forced)
            )
            trials += 1

    print("Trace-GCD fixed-frequency p24 right Gauss weighted polynomial gate")
    print(f"field_q={FIELD_Q}")
    print(f"right={RIGHT}")
    print(f"right_primitive_root={RIGHT_GEN}")
    print(f"order7={ORDER7}")
    print(f"zeta211={zeta211}")
    print(f"zeta7={zeta7}")
    print(f"toy_n={TOY_N}")
    print(f"toy_zeta_n={zeta_n}")
    print(f"toy_internal_order={TOY_INTERNAL_ORDER}")
    print(f"toy_C_degree={TOY_C_DEGREE}")
    print(f"toy_B_over_C_degree={TOY_B_OVER_C_DEGREE}")
    print(f"toy_internal_subgroup={subgroup}")
    print(f"gauss_identity_failures={gauss_identity_failures}")
    print(f"residue_zero_additive_sums={residue_zero_additive_sums}/{ORDER7 - 1}")
    print(f"right_resolvent_to_weighted_polynomial_failures={right_reduction_failures}")
    print(f"random_weighted_polynomial_internal_trace_nonzero={random_internal_trace_nonzero}/{trials}")
    print(f"forced_weighted_polynomial_internal_trace_zero={forced_internal_trace_zero}/{trials}")
    print("interpretation")
    print("  right_obstruction_is_gauss_sum_times_weighted_relative_polynomial=1")
    print("  weights_are_inverse_right_order7_character_on_nonzero_residues=1")
    print("  residue_0_mod_211_drops_out_by_character_orthogonality=1")
    print("  weighted_polynomial_internal_trace_zero_is_not_formal=1")
    print("  remaining_theorem_is_internal_trace_zero_for_this_weighted_cm_polynomial=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_p24_right_gauss_weighted_polynomial_gate")

    if gauss_identity_failures:
        raise SystemExit(1)
    if residue_zero_additive_sums != ORDER7 - 1:
        raise SystemExit(1)
    if right_reduction_failures:
        raise SystemExit(1)
    if random_internal_trace_nonzero == 0:
        raise SystemExit(1)
    if forced_internal_trace_zero != trials:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
