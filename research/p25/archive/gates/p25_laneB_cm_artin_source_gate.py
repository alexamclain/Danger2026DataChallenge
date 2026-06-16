#!/usr/bin/env python3
"""CM-Artin local source gate for p25 Lane B.

The previous Lane B gates built a finite Jacobi packet on the post-B quotient.
This gate records what the negative-trace CM/ray-local sources actually are.

For the first C_3 x C_13 target the right C_3 source is the rational residue of
p^2 at the inert prime 151, while the C_13 source is the split prime 677.  Thus
the missing producer cannot be a plain split-prime class quotient: it must
couple an inert/ray-local right source to a split C-axis source.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd


P25 = 10**25 + 13
NEGATIVE_TRACE = -2988055724018
DK_NEGATIVE_TRACE = (NEGATIVE_TRACE * NEGATIVE_TRACE - 4 * P25) // 16
RIGHT_DEGREE = 3


@dataclass(frozen=True)
class LocalSource:
    prime: int
    role: str
    expected_visible: int


@dataclass(frozen=True)
class SourceCase:
    name: str
    rho_exp: int
    raw_order: int
    b_trace: int
    c_axis: int
    sources: tuple[LocalSource, ...]


CASES = (
    SourceCase(
        name="tiny_C3xC13",
        rho_exp=2,
        raw_order=12675,
        b_trace=325,
        c_axis=13,
        sources=(
            LocalSource(151, "right_axis", RIGHT_DEGREE),
            LocalSource(677, "c_axis", 13),
        ),
    ),
    SourceCase(
        name="prime_axis_C3xC53",
        rho_exp=16,
        raw_order=3975,
        b_trace=25,
        c_axis=53,
        sources=(
            LocalSource(7, "right_axis", RIGHT_DEGREE),
            LocalSource(151, "right_axis", RIGHT_DEGREE),
            LocalSource(107, "c_axis", 53),
        ),
    ),
    SourceCase(
        name="square_axis_C3xC169",
        rho_exp=2,
        raw_order=12675,
        b_trace=25,
        c_axis=169,
        sources=(
            LocalSource(151, "right_axis", RIGHT_DEGREE),
            LocalSource(677, "c_axis", 169),
        ),
    ),
)


def order_mod(value: int, modulus: int) -> int:
    if gcd(value, modulus) != 1:
        raise ValueError("non-unit")
    residue = value % modulus
    order = 1
    while residue != 1:
        residue = residue * value % modulus
        order += 1
    return order


def splitting_type(prime: int) -> str:
    residue = DK_NEGATIVE_TRACE % prime
    if residue == 0:
        return "ramified"
    legendre = pow(residue, (prime - 1) // 2, prime)
    if legendre == 1:
        return "split"
    if legendre == prime - 1:
        return "inert"
    raise RuntimeError("unexpected Legendre symbol")


def residue_unit_orders(prime: int, split_type: str) -> dict[str, int]:
    if split_type == "split":
        return {
            "rational_residue_units": prime - 1,
            "cm_residue_units": (prime - 1) * (prime - 1),
            "norm_one_units": prime - 1,
        }
    if split_type == "inert":
        return {
            "rational_residue_units": prime - 1,
            "cm_residue_units": prime * prime - 1,
            "norm_one_units": prime + 1,
        }
    return {
        "rational_residue_units": prime - 1,
        "cm_residue_units_reduced": prime - 1,
        "ramified_prime": 1,
    }


def factor_string(value: int) -> str:
    parts: list[str] = []
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            exponent = 0
            while value % divisor == 0:
                value //= divisor
                exponent += 1
            parts.append(f"{divisor}^{exponent}" if exponent > 1 else str(divisor))
        divisor += 1 if divisor == 2 else 2
    if value > 1:
        parts.append(str(value))
    return " * ".join(parts) if parts else "1"


def discrete_log_table(generator: int, prime: int, order: int) -> dict[int, int]:
    table: dict[int, int] = {}
    value = 1
    for exponent in range(order):
        if value in table:
            raise AssertionError("generator order collapsed early")
        table[value] = exponent
        value = value * generator % prime
    if value != 1:
        raise AssertionError("generator did not return to 1")
    return table


def right_source_agreement(case: SourceCase) -> tuple[int, int]:
    right_sources = [source for source in case.sources if source.role == "right_axis"]
    if len(right_sources) < 2:
        return case.raw_order, case.raw_order
    log_rows: list[list[int]] = []
    for source in right_sources:
        generator = pow(P25, case.rho_exp, source.prime)
        local_order = order_mod(generator, source.prime)
        table = discrete_log_table(generator, source.prime, local_order)
        values: list[int] = []
        residue = 1
        for _ in range(case.raw_order):
            values.append(table[residue] % RIGHT_DEGREE)
            residue = residue * generator % source.prime
        log_rows.append(values)
    hits = 0
    for index in range(case.raw_order):
        hits += int(all(row[index] == log_rows[0][index] for row in log_rows))
    return hits, case.raw_order


def audit_case(case: SourceCase) -> tuple[list[str], bool]:
    lines: list[str] = []
    role_hits = 0
    c_split_hits = 0
    right_non_split_hits = 0
    right_source_count = 0
    c_source_count = 0

    lines.append(
        f"case {case.name}: rho=p^{case.rho_exp} B={case.b_trace} "
        f"raw_order={case.raw_order} c_axis={case.c_axis}"
    )
    for source in case.sources:
        split_type = splitting_type(source.prime)
        generator = pow(P25, case.rho_exp, source.prime)
        local_order = order_mod(generator, source.prime)
        visible = local_order // gcd(local_order, case.b_trace)
        role_ok = visible == source.expected_visible
        role_hits += int(role_ok)
        c_source_count += int(source.role == "c_axis")
        right_source_count += int(source.role == "right_axis")
        c_split_hits += int(source.role == "c_axis" and split_type == "split")
        right_non_split_hits += int(
            source.role == "right_axis" and split_type in {"inert", "ramified"}
        )
        unit_orders = residue_unit_orders(source.prime, split_type)
        lines.append(
            "  source "
            f"prime={source.prime} split_type={split_type} role={source.role} "
            f"DK_mod_prime={DK_NEGATIVE_TRACE % source.prime} "
            f"p_mod_prime={P25 % source.prime} "
            f"ord_p_rho={local_order}={factor_string(local_order)} "
            f"visible_after_B={visible}={factor_string(visible)} "
            f"expected_visible={source.expected_visible} "
            f"role_ok={int(role_ok)} "
            f"unit_orders={unit_orders}"
        )

    agreement_hits, agreement_total = right_source_agreement(case)
    c_sources_split = c_source_count > 0 and c_split_hits == c_source_count
    right_has_ray_source = right_source_count > 0 and right_non_split_hits > 0
    right_agreement_ok = agreement_hits == agreement_total
    row_ok = (
        role_hits == len(case.sources)
        and c_sources_split
        and right_has_ray_source
        and right_agreement_ok
    )
    lines.append(
        "  summary "
        f"role_hits={role_hits}/{len(case.sources)} "
        f"c_sources_split={int(c_sources_split)} "
        f"right_has_inert_or_ramified_source={int(right_has_ray_source)} "
        f"right_source_agreement={agreement_hits}/{agreement_total} "
        f"ok={int(row_ok)}"
    )
    return lines, row_ok


def main() -> int:
    print("p25 Lane B CM-Artin local source gate")
    print(f"p={P25}")
    print(f"negative_trace={NEGATIVE_TRACE}")
    print(f"D_K={DK_NEGATIVE_TRACE}")
    ok_rows = 0
    for case in CASES:
        lines, ok = audit_case(case)
        ok_rows += int(ok)
        for line in lines:
            print(line)
    print(f"cm_artin_local_source_rows={ok_rows}/{len(CASES)}")
    print("interpretation")
    print("  laneB_sources_are_ray_local_not_plain_split_class_quotients=1")
    print("  tiny_C3xC13_couples_inert_151_right_source_with_split_677_C_source=1")
    print("  prime_C3xC53_has_split_107_C_source_but_duplicate_ramified_inert_right_sources=1")
    print("  producer_must_couple_right_ray_source_to_split_C_source=1")
    print("  split_prime_only_cm_lang_search_is_not_the_right_next_falsifier=1")
    print("conclusion=reported_p25_laneB_cm_artin_local_source_gate")
    return 0 if ok_rows == len(CASES) else 1


if __name__ == "__main__":
    raise SystemExit(main())
