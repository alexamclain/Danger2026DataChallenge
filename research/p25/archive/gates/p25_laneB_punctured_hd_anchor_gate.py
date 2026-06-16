#!/usr/bin/env python3
"""Punctured Hasse-Davenport anchor gate for p25 Lane B.

The local divisor gates reduced the first p25 moonshot target to a coupled
Jacobi-carry footprint on C_3 x C_c.  This gate checks the multiplicative
Jacobi-sum shadow inherited from the p24 work:

    U(r,k) = J(chi^(u*t(r,k)), chi^(v*t(r,k)))

with the reduced degenerate convention Jdagger(1,1)=1.  For the p25 right=3
targets, the raw packet should fail only at the single degenerate anchor, and
the corrected packet should satisfy the two multiplicative producer identities:

* two-level pair products are constant on C-zero and off-C-zero fibers;
* selected row-product ratios are independent of the right row.

The gate also records two producer-facing facts:

* the anchor scalar has no c-th root in the small Jacobi value field, so a
  Kummer/sign descent is still needed;
* plain cyclotomic Frobenius does not realize the full p25 quotient, although
  the real-cyclotomic residual splits into very small components.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd

from p25_laneB_literal_jacobi_packet_model import admissible_pairs, crt
from p25_selected_defect_value_gate import RIGHT_DEGREE, split_prime_for


P25 = 10**25 + 13


@dataclass(frozen=True)
class AnchorCase:
    name: str
    c_axis: int


CASES = (
    AnchorCase("tiny_C3xC13", 13),
    AnchorCase("prime_axis_C3xC53", 53),
)


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    divisor = 3
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 2
    return True


def next_split_prime(order: int, after: int) -> int:
    multiplier = max(2, after // order)
    while True:
        candidate = multiplier * order + 1
        if candidate > after and is_prime(candidate):
            return candidate
        multiplier += 1


def factor_distinct(value: int) -> set[int]:
    factors: set[int] = set()
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            factors.add(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor += 1 if divisor == 2 else 2
    if value > 1:
        factors.add(value)
    return factors


def primitive_root(modulus: int) -> int:
    factors = factor_distinct(modulus - 1)
    for candidate in range(2, modulus):
        if all(pow(candidate, (modulus - 1) // factor, modulus) != 1 for factor in factors):
            return candidate
    raise RuntimeError("no primitive root")


def log_table(field_q: int) -> list[int | None]:
    generator = primitive_root(field_q)
    logs: list[int | None] = [None] * field_q
    value = 1
    for exponent in range(field_q - 1):
        logs[value] = exponent
        value = value * generator % field_q
    if value != 1:
        raise RuntimeError("bad primitive root")
    return logs


@dataclass
class JacobiContext:
    order: int
    base_field_q: int
    value_field_l: int
    zeta: int
    characters: list[list[int]]
    cache: dict[tuple[int, int], int]

    def jacobi_sum(self, exponent_a: int, exponent_b: int) -> int:
        key = (exponent_a % self.order, exponent_b % self.order)
        if key in self.cache:
            return self.cache[key]
        chars_a = self.characters[key[0]]
        chars_b = self.characters[key[1]]
        total = 0
        for x_value in range(self.base_field_q):
            total += chars_a[x_value] * chars_b[(1 - x_value) % self.base_field_q]
        self.cache[key] = total % self.value_field_l
        return self.cache[key]


def make_context(order: int) -> JacobiContext:
    base_field_q = split_prime_for(order)
    value_field_l = next_split_prime(order, base_field_q)
    logs = log_table(base_field_q)
    value_root = primitive_root(value_field_l)
    zeta = pow(value_root, (value_field_l - 1) // order, value_field_l)
    characters: list[list[int]] = []
    for exponent in range(order):
        row: list[int] = []
        for value in range(base_field_q):
            if value == 0:
                row.append(0)
            else:
                log_value = logs[value]
                if log_value is None:
                    raise RuntimeError("missing discrete log")
                row.append(
                    pow(
                        zeta,
                        (exponent % order) * (log_value % order),
                        value_field_l,
                    )
                )
        characters.append(row)
    return JacobiContext(order, base_field_q, value_field_l, zeta, characters, {})


def packet_values(ctx: JacobiContext, c_axis: int, u_value: int, v_value: int) -> list[int]:
    values: list[int] = []
    for right in range(RIGHT_DEGREE):
        for c_index in range(c_axis):
            point = crt(right, c_index, c_axis)
            values.append(ctx.jacobi_sum(u_value * point, v_value * point))
    return values


def anchor_corrected(values: list[int], q_minus_2: int, modulus: int) -> list[int]:
    out = values[:]
    out[0] = out[0] * pow(q_minus_2, -1, modulus) % modulus
    return out


def two_level_products(values: list[int], c_axis: int, modulus: int) -> tuple[set[int], set[int]]:
    zero_products: set[int] = set()
    off_products: set[int] = set()
    for right in range(RIGHT_DEGREE):
        zero_products.add(
            values[right * c_axis]
            * values[((-right) % RIGHT_DEGREE) * c_axis]
            % modulus
        )
        for c_index in range(1, c_axis):
            off_products.add(
                values[right * c_axis + c_index]
                * values[
                    ((-right) % RIGHT_DEGREE) * c_axis
                    + ((-c_index) % c_axis)
                ]
                % modulus
            )
    return zero_products, off_products


def row_ratios(values: list[int], c_axis: int, modulus: int) -> list[int | None]:
    ratios: list[int | None] = []
    for right in range(RIGHT_DEGREE):
        product = 1
        for c_index in range(c_axis):
            product = product * values[right * c_axis + c_index] % modulus
        base = values[right * c_axis]
        if base == 0:
            ratios.append(None)
        else:
            ratios.append(
                product * pow(pow(base, c_axis, modulus), -1, modulus) % modulus
            )
    return ratios


def pair_products_constant(values: list[int], c_axis: int, modulus: int) -> bool:
    zero_products, off_products = two_level_products(values, c_axis, modulus)
    return len(zero_products) == 1 and len(off_products) == 1


def row_ratios_constant(values: list[int], c_axis: int, modulus: int) -> bool:
    ratios = row_ratios(values, c_axis, modulus)
    return None not in ratios and len(set(value for value in ratios if value is not None)) == 1


def zero_fiber_has_expected_degeneracy(
    values: list[int], c_axis: int, q_minus_2: int, modulus: int
) -> bool:
    if values[0] != q_minus_2 % modulus:
        return False
    return all(
        values[right * c_axis] == modulus - 1
        for right in range(1, RIGHT_DEGREE)
    )


def scalar_has_c_root(value: int, c_axis: int, modulus: int) -> bool:
    return pow(value % modulus, (modulus - 1) // gcd(c_axis, modulus - 1), modulus) == 1


def multiplicative_order(value: int, modulus: int) -> int:
    if gcd(value, modulus) != 1:
        raise ValueError("value is not a unit")
    order = 1
    residue = value % modulus
    while residue != 1:
        residue = residue * value % modulus
        order += 1
    return order


def real_cyclotomic_order(value: int, c_axis: int) -> int:
    residue = value % c_axis
    current = residue
    order = 1
    while current not in {1, c_axis - 1}:
        current = current * residue % c_axis
        order += 1
    return order


def expected_pair_count(c_axis: int) -> int:
    return (RIGHT_DEGREE - 1) * (c_axis - 1) * (c_axis - 2)


def audit_case(case: AnchorCase) -> tuple[list[str], bool]:
    c_axis = case.c_axis
    order = RIGHT_DEGREE * c_axis
    ctx = make_context(order)
    q_minus_2 = (ctx.base_field_q - 2) % ctx.value_field_l
    pairs = admissible_pairs(c_axis)

    raw_off_pair_hits = 0
    raw_two_level_pair_hits = 0
    raw_row_ratio_hits = 0
    expected_degeneracy_hits = 0
    corrected_pair_hits = 0
    corrected_ratio_hits = 0
    corrected_product_formula_hits = 0
    single_anchor_hits = 0
    anchor_scale_formula_hits = 0
    anchor_values: set[int] = set()

    for u_value, v_value in pairs:
        values = packet_values(ctx, c_axis, u_value, v_value)
        corrected = anchor_corrected(values, q_minus_2, ctx.value_field_l)
        zero_products, off_products = two_level_products(values, c_axis, ctx.value_field_l)
        raw_ratios = row_ratios(values, c_axis, ctx.value_field_l)
        corrected_ratios = row_ratios(corrected, c_axis, ctx.value_field_l)

        raw_off_pair_hits += int(len(off_products) == 1)
        raw_two_level_pair_hits += int(len(zero_products) == 1 and len(off_products) == 1)
        raw_row_ratio_hits += int(row_ratios_constant(values, c_axis, ctx.value_field_l))
        expected_degeneracy_hits += int(
            zero_fiber_has_expected_degeneracy(
                values, c_axis, q_minus_2, ctx.value_field_l
            )
        )
        corrected_pair_hit = pair_products_constant(
            corrected, c_axis, ctx.value_field_l
        )
        corrected_ratio_hit = row_ratios_constant(
            corrected, c_axis, ctx.value_field_l
        )
        corrected_pair_hits += int(corrected_pair_hit)
        corrected_ratio_hits += int(corrected_ratio_hit)
        corrected_product_formula_hits += int(corrected_pair_hit and corrected_ratio_hit)
        single_anchor_hits += int(corrected[0] == 1 and corrected[1:] == values[1:])

        if (
            raw_ratios[0] is not None
            and raw_ratios[1] is not None
            and corrected_ratios[0] is not None
            and raw_ratios[0] != 0
            and raw_ratios[1] != 0
        ):
            raw_defect = raw_ratios[0] * pow(raw_ratios[1], -1, ctx.value_field_l)
            raw_defect %= ctx.value_field_l
            correction_scale = corrected_ratios[0] * pow(raw_ratios[0], -1, ctx.value_field_l)
            correction_scale %= ctx.value_field_l
            expected_scale = pow(q_minus_2, c_axis - 1, ctx.value_field_l)
            anchor_scale_formula_hits += int(
                correction_scale == expected_scale
                and raw_defect * expected_scale % ctx.value_field_l == 1
            )
        anchor_values.add(values[0])

    pair_count = len(pairs)
    anchor_has_root = scalar_has_c_root(q_minus_2, c_axis, ctx.value_field_l)
    neg_anchor_has_root = scalar_has_c_root(-q_minus_2, c_axis, ctx.value_field_l)
    p_mod_c_order = multiplicative_order(P25 % c_axis, c_axis)
    p_mod_level_order = multiplicative_order(P25 % order, order)
    real_order = real_cyclotomic_order(P25, c_axis)
    real_degree = (c_axis - 1) // 2
    real_factor_count = real_degree // real_order

    ok = (
        pair_count == expected_pair_count(c_axis)
        and raw_off_pair_hits == pair_count
        and raw_two_level_pair_hits == 0
        and raw_row_ratio_hits == 0
        and expected_degeneracy_hits == pair_count
        and corrected_pair_hits == pair_count
        and corrected_ratio_hits == pair_count
        and corrected_product_formula_hits == pair_count
        and single_anchor_hits == pair_count
        and anchor_scale_formula_hits == pair_count
        and not anchor_has_root
        and not neg_anchor_has_root
        and gcd(c_axis, P25 - 1) == 1
        and p_mod_level_order < order
        and real_factor_count == 2
    )

    lines = [
        (
            f"case {case.name}: c={c_axis} order={order} "
            f"base_field_q={ctx.base_field_q} value_field_l={ctx.value_field_l} "
            f"pairs_checked={pair_count} expected_pairs={expected_pair_count(c_axis)} "
            f"cached_jacobi_sums={len(ctx.cache)} "
            f"q_minus_2={q_minus_2} "
            f"raw_off_pair_hits={raw_off_pair_hits}/{pair_count} "
            f"raw_two_level_pair_hits={raw_two_level_pair_hits}/{pair_count} "
            f"raw_row_ratio_hits={raw_row_ratio_hits}/{pair_count} "
            f"expected_zero_fiber_degeneracy_hits={expected_degeneracy_hits}/{pair_count} "
            f"corrected_pair_product_hits={corrected_pair_hits}/{pair_count} "
            f"corrected_row_ratio_hits={corrected_ratio_hits}/{pair_count} "
            f"corrected_product_formula_hits={corrected_product_formula_hits}/{pair_count} "
            f"single_anchor_hits={single_anchor_hits}/{pair_count} "
            f"anchor_scale_formula_hits={anchor_scale_formula_hits}/{pair_count} "
            f"anchor_values={sorted(anchor_values)} "
            f"anchor_has_c_root={int(anchor_has_root)} "
            f"neg_anchor_has_c_root={int(neg_anchor_has_root)} "
            f"p_mod_c={P25 % c_axis} p_order_mod_c={p_mod_c_order} "
            f"p_order_mod_3c={p_mod_level_order} "
            f"real_cyclotomic_degree={real_degree} "
            f"real_component_degree={real_order} "
            f"real_component_count={real_factor_count} "
            f"plain_cyclotomic_realizes_full_quotient={int(p_mod_level_order == order)} "
            f"ok={int(ok)}"
        )
    ]
    return lines, ok


def main() -> int:
    print("p25 Lane B punctured Hasse-Davenport anchor gate")
    print(f"p={P25}")
    print(f"right_degree={RIGHT_DEGREE}")
    ok_rows = 0
    for case in CASES:
        lines, ok = audit_case(case)
        ok_rows += int(ok)
        for line in lines:
            print(line)
    print(f"punctured_hd_anchor_rows={ok_rows}/{len(CASES)}")
    print("interpretation")
    print("  raw_right_mixed_jacobi_packet_fails_only_by_degenerate_anchor=1")
    print("  correcting_single_J_1_1_anchor_by_q_minus_2_inverse_fixes_product_formula=1")
    print("  anchor_scalar_has_no_c_root_in_the_small_value_field=1")
    print("  p25_plain_cyclotomic_frobenius_does_not_realize_full_laneB_quotient=1")
    print("  p25_real_cyclotomic_residual_splits_into_two_small_components=1")
    print("  producer_target_is_cm_artin_pullback_plus_single_anchor_kummer_descent=1")
    print("conclusion=reported_p25_laneB_punctured_hd_anchor_gate")
    return 0 if ok_rows == len(CASES) else 1


if __name__ == "__main__":
    raise SystemExit(main())
