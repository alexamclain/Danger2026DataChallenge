#!/usr/bin/env python3
"""Probe actual Jacobi-sum product identities behind admissible carries.

The current p24 theorem target is product-formula shaped:

    U(r,0)U(-r,0) constant,
    U(r,c)U(-r,-c) constant for c != 0,
    prod_c U(r,c)/U(r,0)^c_degree constant in r.

The admissible carry algebra proves the logarithmic/divisor version.  This
probe asks whether the same identities are visible for honest finite-field
Jacobi sums

    U_t = J(chi^(u*t), chi^(v*t))

for small N=7*c.  Degenerate characters are included, because the C-zero fiber
is exactly where one character can become trivial.

Result preview: raw Jacobi sums have the right off-zero pair-product
complement, but the C-zero/trivial-character constants and row-product ratios
do not automatically match the p24 selected-defect target.  This isolates the
extra normalization needed from a CM/Lang product formula.
"""

from __future__ import annotations

from dataclasses import dataclass

from trace_gcd_fixed_frequency_p24_jacobi_carry_span_boundary import (
    RIGHT_DEGREE,
    SMALL_C_DEGREES,
    crt,
    split_prime_for,
)
from trace_gcd_fixed_frequency_p24_jacobi_carry_c_centering_gate import primitive_root


def next_split_prime(order: int, after: int) -> int:
    multiplier = max(2, after // order)
    while True:
        candidate = multiplier * order + 1
        if candidate > after and is_prime(candidate):
            return candidate
        multiplier += 1


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


def log_table(field_q: int) -> tuple[int, list[int | None]]:
    generator = primitive_root(field_q)
    logs: list[int | None] = [None] * field_q
    value = 1
    for exponent in range(field_q - 1):
        logs[value] = exponent
        value = value * generator % field_q
    return generator, logs


@dataclass(frozen=True)
class JacobiContext:
    order: int
    base_field_q: int
    value_field_l: int
    zeta: int
    logs: list[int | None]

    def character(self, exponent: int, value: int) -> int:
        if value % self.base_field_q == 0:
            return 0
        log_value = self.logs[value]
        if log_value is None:
            raise RuntimeError("missing discrete log")
        return pow(self.zeta, (exponent % self.order) * (log_value % self.order), self.value_field_l)

    def jacobi_sum(self, exponent_a: int, exponent_b: int) -> int:
        total = 0
        for x_value in range(self.base_field_q):
            total += self.character(exponent_a, x_value) * self.character(
                exponent_b, (1 - x_value) % self.base_field_q
            )
        return total % self.value_field_l


def make_context(order: int) -> JacobiContext:
    base_field_q = split_prime_for(order)
    value_field_l = next_split_prime(order, base_field_q)
    _, logs = log_table(base_field_q)
    value_root = primitive_root(value_field_l)
    zeta = pow(value_root, (value_field_l - 1) // order, value_field_l)
    if pow(zeta, order, value_field_l) != 1 or zeta == 1:
        raise RuntimeError("bad cyclotomic value root")
    return JacobiContext(order, base_field_q, value_field_l, zeta, logs)


def packet_values(ctx: JacobiContext, c_degree: int, u_value: int, v_value: int) -> list[int]:
    values: list[int] = []
    for right in range(RIGHT_DEGREE):
        for c_index in range(c_degree):
            point = crt(right, c_index, c_degree)
            values.append(ctx.jacobi_sum(u_value * point, v_value * point))
    return values


def two_level_products(
    values: list[int], c_degree: int, modulus: int
) -> tuple[set[int], set[int]]:
    zero_products: set[int] = set()
    off_products: set[int] = set()
    for right in range(RIGHT_DEGREE):
        zero_products.add(
            values[right * c_degree]
            * values[((-right) % RIGHT_DEGREE) * c_degree]
            % modulus
        )
        for c_index in range(1, c_degree):
            off_products.add(
                values[right * c_degree + c_index]
                * values[((-right) % RIGHT_DEGREE) * c_degree + ((-c_index) % c_degree)]
                % modulus
            )
    return zero_products, off_products


def row_ratios(values: list[int], c_degree: int, modulus: int) -> list[int | None]:
    ratios: list[int | None] = []
    for right in range(RIGHT_DEGREE):
        product = 1
        for c_index in range(c_degree):
            product = product * values[right * c_degree + c_index] % modulus
        base = values[right * c_degree]
        if base == 0:
            ratios.append(None)
        else:
            ratios.append(product * pow(pow(base, c_degree, modulus), -1, modulus) % modulus)
    return ratios


def normalize_c_zero(values: list[int], c_degree: int, modulus: int) -> list[int]:
    """Force the C-zero fiber to 1 to mimic selected-defect normalization."""
    out = values[:]
    for right in range(RIGHT_DEGREE):
        base = out[right * c_degree]
        if base:
            inv = pow(base, -1, modulus)
            for c_index in range(c_degree):
                out[right * c_degree + c_index] = out[right * c_degree + c_index] * inv % modulus
    return out


def admissible_sample_pairs(c_degree: int) -> list[tuple[int, int]]:
    order = RIGHT_DEGREE * c_degree
    out: list[tuple[int, int]] = []
    for c_axis_index in range(1, min(c_degree, 4)):
        u_value = RIGHT_DEGREE * c_axis_index
        for v_value in range(1, order):
            if (u_value + v_value) % order == 0:
                continue
            if v_value % c_degree == 0:
                continue
            if (u_value + v_value) % c_degree == 0:
                continue
            out.append((u_value, v_value))
            if len(out) >= 8:
                return out
    return out


def main() -> None:
    print("Trace-GCD fixed-frequency Jacobi-sum product-formula probe")
    print(f"right_degree={RIGHT_DEGREE}")

    rows_checked = 0
    raw_off_pair_rows = 0
    raw_full_pair_rows = 0
    raw_ratio_rows = 0
    normalized_ratio_rows = 0
    mixed_no_ratio_rows = 0
    mixed_no_normalized_ratio_rows = 0

    for c_degree in SMALL_C_DEGREES[:3]:
        order = RIGHT_DEGREE * c_degree
        ctx = make_context(order)
        pairs = admissible_sample_pairs(c_degree)
        row_raw_off = 0
        row_raw_full = 0
        row_raw_ratio = 0
        row_norm_ratio = 0
        row_mixed_raw_ratio = 0
        row_mixed_norm_ratio = 0
        mixed_pair_count = 0
        raw_ratio_hit_pairs: list[tuple[int, int]] = []
        normalized_ratio_hit_pairs: list[tuple[int, int]] = []

        for u_value, v_value in pairs:
            is_right_mixed = v_value % RIGHT_DEGREE != 0
            mixed_pair_count += int(is_right_mixed)
            values = packet_values(ctx, c_degree, u_value, v_value)
            zero_products, off_products = two_level_products(
                values, c_degree, ctx.value_field_l
            )
            ratios = row_ratios(values, c_degree, ctx.value_field_l)
            normalized = normalize_c_zero(values, c_degree, ctx.value_field_l)
            normalized_ratios = row_ratios(normalized, c_degree, ctx.value_field_l)

            row_raw_off += int(len(off_products) == 1)
            row_raw_full += int(len(zero_products) == 1 and len(off_products) == 1)
            raw_ratio_hit = (
                None not in ratios and len(set(value for value in ratios if value is not None)) == 1
            )
            normalized_ratio_hit = (
                None not in normalized_ratios
                and len(set(value for value in normalized_ratios if value is not None)) == 1
            )
            row_raw_ratio += int(raw_ratio_hit)
            row_norm_ratio += int(normalized_ratio_hit)
            if raw_ratio_hit:
                raw_ratio_hit_pairs.append((u_value, v_value))
            if normalized_ratio_hit:
                normalized_ratio_hit_pairs.append((u_value, v_value))
            if is_right_mixed:
                row_mixed_raw_ratio += int(raw_ratio_hit)
                row_mixed_norm_ratio += int(normalized_ratio_hit)

        raw_off_ok = int(row_raw_off == len(pairs))
        raw_full_ok = int(row_raw_full == len(pairs))
        raw_ratio_ok = int(row_raw_ratio == len(pairs))
        norm_ratio_ok = int(row_norm_ratio == len(pairs))
        mixed_ratio_ok = int(mixed_pair_count > 0 and row_mixed_raw_ratio == 0)
        mixed_norm_ratio_ok = int(mixed_pair_count > 0 and row_mixed_norm_ratio == 0)
        raw_off_pair_rows += raw_off_ok
        raw_full_pair_rows += raw_full_ok
        raw_ratio_rows += raw_ratio_ok
        normalized_ratio_rows += norm_ratio_ok
        mixed_no_ratio_rows += mixed_ratio_ok
        mixed_no_normalized_ratio_rows += mixed_norm_ratio_ok
        rows_checked += 1

        print(
            "row "
            f"c_degree={c_degree} order={order} "
            f"base_field_q={ctx.base_field_q} value_field_l={ctx.value_field_l} "
            f"sample_pairs={len(pairs)} "
            f"raw_off_c_pair_products_constant={row_raw_off}/{len(pairs)} "
            f"raw_two_level_pair_products_constant={row_raw_full}/{len(pairs)} "
            f"raw_row_ratios_constant={row_raw_ratio}/{len(pairs)} "
            f"c_zero_normalized_row_ratios_constant={row_norm_ratio}/{len(pairs)} "
            f"right_mixed_raw_row_ratios_constant={row_mixed_raw_ratio}/{mixed_pair_count} "
            f"right_mixed_normalized_row_ratios_constant={row_mixed_norm_ratio}/{mixed_pair_count} "
            f"raw_ratio_hit_pairs={raw_ratio_hit_pairs} "
            f"normalized_ratio_hit_pairs={normalized_ratio_hit_pairs} "
            f"raw_off_pair_ok={raw_off_ok} raw_full_pair_ok={raw_full_ok} "
            f"raw_ratio_ok={raw_ratio_ok} normalized_ratio_ok={norm_ratio_ok} "
            f"mixed_ratio_none_ok={mixed_ratio_ok} "
            f"mixed_normalized_ratio_none_ok={mixed_norm_ratio_ok}"
        )

    print(f"raw_off_c_pair_product_rows={raw_off_pair_rows}/{rows_checked}")
    print(f"raw_two_level_pair_product_rows={raw_full_pair_rows}/{rows_checked}")
    print(f"raw_row_ratio_rows={raw_ratio_rows}/{rows_checked}")
    print(f"c_zero_normalized_row_ratio_rows={normalized_ratio_rows}/{rows_checked}")
    print(f"right_mixed_no_row_ratio_rows={mixed_no_ratio_rows}/{rows_checked}")
    print(
        "right_mixed_no_c_zero_normalized_row_ratio_rows="
        f"{mixed_no_normalized_ratio_rows}/{rows_checked}"
    )
    print("interpretation")
    print("  honest_jacobi_sums_supply_off_c_inversion_product_complement=1")
    print("  degenerate_c_zero_fiber_needs_selected_normalization=1")
    print("  row_product_ratio_is_not_automatic_for_raw_jacobi_sums=1")
    print("  product_formula_target_needs_extra_distribution_or_selected_ratio=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_jacobi_sum_product_formula_probe")

    if raw_off_pair_rows != rows_checked:
        raise SystemExit(1)
    if raw_ratio_rows == rows_checked and normalized_ratio_rows == rows_checked:
        raise SystemExit("probe unexpectedly found automatic row-ratio theorem")
    if mixed_no_ratio_rows != rows_checked:
        raise SystemExit("right-mixed Jacobi sums unexpectedly supplied row ratios")


if __name__ == "__main__":
    main()
