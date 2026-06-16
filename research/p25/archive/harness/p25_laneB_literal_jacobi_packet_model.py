#!/usr/bin/env python3
"""Literal Jacobi-carry packet model for the p25 Lane B contract.

This is a quotient-level model of the missing selected packet Y[e].
It does not use p25 CM roots.  Instead it asks whether the exact p25 raw
packet contract is compatible with the reduced Jacobi-carry divisor model:

    theta_{u,v}(t) = [u t]_N + [v t]_N - [(u+v)t]_N

on N = 3*c, inflated to the raw rho cycle by distributing the post-B trace
uniformly over each B-block.  This is the additive/divisor analogue of the
literal Jacobi product-formula packet.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_selected_defect_value_gate import (
    RIGHT_DEGREE,
    c_row_sums_independent,
    c_zero_fiber_vanishes,
    inversion_constant_off_c_zero,
    selected_defect,
    split_prime_for,
    value_conditions_hold,
)


@dataclass(frozen=True)
class LiteralCase:
    name: str
    c_axis: int
    b_trace: int
    raw_order: int
    exhaustive: bool


CASES = (
    LiteralCase("tiny_C3xC13", 13, 325, 12675, True),
    LiteralCase("prime_axis_C3xC53", 53, 25, 3975, True),
    LiteralCase("square_axis_C3xC169", 169, 25, 12675, False),
)


def crt(right_index: int, c_index: int, c_degree: int) -> int:
    order = RIGHT_DEGREE * c_degree
    return (
        right_index * c_degree * pow(c_degree, -1, RIGHT_DEGREE)
        + c_index * RIGHT_DEGREE * pow(RIGHT_DEGREE, -1, c_degree)
    ) % order


def admissible_pairs(c_degree: int) -> list[tuple[int, int]]:
    order = RIGHT_DEGREE * c_degree
    pairs: list[tuple[int, int]] = []
    for c_axis_index in range(1, c_degree):
        u_value = RIGHT_DEGREE * c_axis_index
        for v_value in range(1, order):
            if (u_value + v_value) % order == 0:
                continue
            if v_value % c_degree == 0:
                continue
            if (u_value + v_value) % c_degree == 0:
                continue
            if v_value % RIGHT_DEGREE == 0:
                continue
            pairs.append((u_value, v_value))
    return pairs


def representative_pairs(c_degree: int) -> list[tuple[int, int]]:
    pairs = admissible_pairs(c_degree)
    canonical = (RIGHT_DEGREE, 1)
    indexes = {0, len(pairs) // 3, 2 * len(pairs) // 3, len(pairs) - 1}
    reps = [canonical]
    for index in sorted(indexes):
        if pairs[index] not in reps:
            reps.append(pairs[index])
    return reps


def carry_packet(c_degree: int, u_value: int, v_value: int, modulus: int) -> list[int]:
    order = RIGHT_DEGREE * c_degree
    uv_value = (u_value + v_value) % order
    out: list[int] = []
    for right in range(RIGHT_DEGREE):
        for c_index in range(c_degree):
            point = crt(right, c_index, c_degree)
            out.append(
                (
                    (u_value * point) % order
                    + (v_value * point) % order
                    - (uv_value * point) % order
                )
                % modulus
            )
    return out


def add_single_anchor(packet: list[int], modulus: int) -> list[int]:
    out = packet[:]
    out[0] = (out[0] - 1) % modulus
    return out


def raw_from_quotient_packet(
    quotient_packet: list[int], case: LiteralCase, modulus: int
) -> list[int]:
    inv_b = pow(case.b_trace % modulus, -1, modulus)
    raw = [0] * case.raw_order
    quotient_order = RIGHT_DEGREE * case.c_axis
    for r in range(RIGHT_DEGREE):
        for c in range(case.c_axis):
            value = quotient_packet[r * case.c_axis + c] * inv_b % modulus
            start = case.c_axis * r + RIGHT_DEGREE * c
            for j in range(case.b_trace):
                raw[(start + quotient_order * j) % case.raw_order] = value
    return raw


def trace_packet_from_raw(raw: list[int], case: LiteralCase, modulus: int) -> list[int]:
    quotient_order = RIGHT_DEGREE * case.c_axis
    out: list[int] = []
    for r in range(RIGHT_DEGREE):
        for c in range(case.c_axis):
            start = case.c_axis * r + RIGHT_DEGREE * c
            total = 0
            for j in range(case.b_trace):
                total = (total + raw[(start + quotient_order * j) % case.raw_order]) % modulus
            out.append(total)
    return out


def profile(row: list[int], c_degree: int, modulus: int) -> tuple[int, int, int, int]:
    return (
        int(c_zero_fiber_vanishes(row, c_degree, modulus)),
        int(c_row_sums_independent(row, c_degree, modulus)),
        int(inversion_constant_off_c_zero(row, c_degree, modulus)),
        int(value_conditions_hold(row, c_degree, modulus)),
    )


def audit_case(case: LiteralCase) -> tuple[list[str], bool]:
    modulus = split_prime_for(RIGHT_DEGREE * case.c_axis)
    pairs = admissible_pairs(case.c_axis) if case.exhaustive else representative_pairs(case.c_axis)
    carry_pass = 0
    reduced_pass = 0
    raw_trace_roundtrips = 0
    carry_profiles: dict[tuple[int, int, int, int], int] = {}
    reduced_profiles: dict[tuple[int, int, int, int], int] = {}
    examples: list[str] = []

    for index, (u_value, v_value) in enumerate(pairs):
        carry = carry_packet(case.c_axis, u_value, v_value, modulus)
        reduced = add_single_anchor(carry, modulus)

        raw_carry = raw_from_quotient_packet(carry, case, modulus)
        traced_carry = trace_packet_from_raw(raw_carry, case, modulus)
        raw_trace_roundtrips += int(traced_carry == carry)

        carry_defect = selected_defect(traced_carry, case.c_axis, modulus)
        reduced_defect = selected_defect(reduced, case.c_axis, modulus)
        carry_prof = profile(carry_defect, case.c_axis, modulus)
        reduced_prof = profile(reduced_defect, case.c_axis, modulus)
        carry_profiles[carry_prof] = carry_profiles.get(carry_prof, 0) + 1
        reduced_profiles[reduced_prof] = reduced_profiles.get(reduced_prof, 0) + 1
        carry_pass += carry_prof[3]
        reduced_pass += reduced_prof[3]

        if index < 3:
            examples.append(
                f"(u={u_value},v={v_value},carry={carry_prof},reduced={reduced_prof})"
            )

    ok = (
        raw_trace_roundtrips == len(pairs)
        and carry_pass == len(pairs)
        and reduced_pass == 0
    )
    lines = [
        (
            f"case {case.name}: c={case.c_axis} B={case.b_trace} "
            f"raw_order={case.raw_order} modulus={modulus} "
            f"pairs_checked={len(pairs)} exhaustive={int(case.exhaustive)} "
            f"raw_trace_roundtrips={raw_trace_roundtrips}/{len(pairs)} "
            f"carry_value_identity_hits={carry_pass}/{len(pairs)} "
            f"reduced_anchor_value_identity_hits={reduced_pass}/{len(pairs)} "
            f"ok={int(ok)}"
        ),
        f"  carry_profiles={carry_profiles}",
        f"  reduced_anchor_profiles={reduced_profiles}",
        f"  examples={examples}",
    ]
    return lines, ok


def main() -> int:
    print("p25 Lane B literal Jacobi packet model")
    print(f"right_degree={RIGHT_DEGREE}")
    ok_rows = 0
    for case in CASES:
        lines, ok = audit_case(case)
        ok_rows += int(ok)
        for line in lines:
            print(line)
    print(f"literal_packet_model_rows={ok_rows}/{len(CASES)}")
    print("interpretation")
    print("  Jacobi_carry_divisor_packets_roundtrip_through_the_exact_p25_Y_contract=1")
    print("  carry_packets_satisfy_the_selected_defect_value_identities=1")
    print("  naive_single_anchor_addition_is_not_itself_the_full_additive_packet=1")
    print("  p25_embedded_Y_should_model_the_reduced_product_formula_not_anchor_alone=1")
    print("conclusion=reported_p25_laneB_literal_jacobi_packet_model")
    return 0 if ok_rows == len(CASES) else 1


if __name__ == "__main__":
    raise SystemExit(main())
