#!/usr/bin/env python3
"""Actual-CM boundary for admissible Jacobi-carry span membership.

The p24 Jacobi route now asks for the selected weighted packet after B/C trace
to land in the termwise-safe admissible C-axis Jacobi-carry span.  This script
tests that stronger condition on the closest small actual-CM rows already used
as boundaries.

The test is deliberately quotient-level:

* D=-5000, q=3851, h=30 gives a raw projector/internal-character row with
  right quotient C_2 and C-analogue C_5.
* D=-13319, q=13463, h=140 gives the pinned right-combo/product row with
  right quotient C_2 and relative C_5.

Both are boundary rows, not p24 clones.  A failure here does not refute the p24
route; it prevents the false theorem "ordinary embedded CM projector/right-
combo packets are automatically admissible Jacobi combinations."
"""

from __future__ import annotations

from dataclasses import replace

from cypari2 import Pari

from embedded_decomposition_calibration import (
    D,
    ELL,
    H,
    isogeny_neighbors,
    pari_linear_roots,
    walk_cycle,
)
from k_character_tensor_rank_scan import ExtensionField, FpE, rank_over_extension
from trace_gcd_fixed_frequency_actual_cm_projector_internal_character_boundary import (
    Q as PROJECTOR_Q,
    TOY_C_DEGREE,
    TOP_QUOTIENT,
    nontrivial_top_projected_b_trace,
    rotate as rotate_list,
)
from trace_gcd_fixed_frequency_actual_cm_right_combo_anchor_boundary import (
    weighted_coefficients,
)
from trace_gcd_fixed_frequency_actual_cm_right_combo_boundary import (
    load_actual_packet as load_right_combo_packet,
    right_combo,
)
from relative_moment_projection_scan import rotate as rotate_tuple


def rank_mod(matrix: list[list[int]], modulus: int) -> int:
    mat = [row[:] for row in matrix if any(value % modulus for value in row)]
    rows = len(mat)
    cols = len(mat[0]) if rows else 0
    rank = 0
    for col in range(cols):
        pivot = None
        for row in range(rank, rows):
            if mat[row][col] % modulus:
                pivot = row
                break
        if pivot is None:
            continue
        mat[rank], mat[pivot] = mat[pivot], mat[rank]
        inv = pow(mat[rank][col] % modulus, -1, modulus)
        mat[rank] = [(value * inv) % modulus for value in mat[rank]]
        for row in range(rows):
            if row == rank:
                continue
            scale = mat[row][col] % modulus
            if scale:
                mat[row] = [
                    (left - scale * right) % modulus
                    for left, right in zip(mat[row], mat[rank])
                ]
        rank += 1
    return rank


def crt(right_index: int, c_index: int, right_degree: int, c_degree: int) -> int:
    order = right_degree * c_degree
    return (
        right_index * c_degree * pow(c_degree, -1, right_degree)
        + c_index * right_degree * pow(right_degree, -1, c_degree)
    ) % order


def carry_vector(
    right_degree: int,
    c_degree: int,
    modulus: int,
    u_value: int,
    v_value: int,
) -> list[int]:
    order = right_degree * c_degree
    uv_value = (u_value + v_value) % order
    points = [
        crt(right_index, c_index, right_degree, c_degree)
        for right_index in range(right_degree)
        for c_index in range(c_degree)
    ]
    return [
        ((u_value * point) % order + (v_value * point) % order - (uv_value * point) % order)
        % modulus
        for point in points
    ]


def c_axis_carry_rows(
    right_degree: int,
    c_degree: int,
    modulus: int,
    admissible: bool,
) -> list[list[int]]:
    order = right_degree * c_degree
    rows: list[list[int]] = []
    for c_axis_index in range(1, c_degree):
        u_value = right_degree * c_axis_index
        for v_value in range(1, order):
            if (u_value + v_value) % order == 0:
                continue
            if admissible:
                if v_value % c_degree == 0:
                    continue
                if (u_value + v_value) % c_degree == 0:
                    continue
            rows.append(carry_vector(right_degree, c_degree, modulus, u_value, v_value))
    return rows


def no_forbidden_int(
    row: list[int],
    right_degree: int,
    c_degree: int,
    modulus: int,
) -> bool:
    row_sums = [
        sum(row[right * c_degree : (right + 1) * c_degree]) % modulus
        for right in range(right_degree)
    ]
    return all(row_sum == row_sums[0] for row_sum in row_sums)


def no_forbidden_ext(
    row: list[FpE],
    right_degree: int,
    c_degree: int,
    field: ExtensionField,
) -> bool:
    row_sums: list[FpE] = []
    for right in range(right_degree):
        total = field.zero
        for value in row[right * c_degree : (right + 1) * c_degree]:
            total = field.add(total, value)
        row_sums.append(total)
    return all(row_sum == row_sums[0] for row_sum in row_sums)


def in_int_span(
    span_rows: list[list[int]],
    span_rank: int,
    target: list[int],
    modulus: int,
) -> bool:
    return rank_mod(span_rows + [target], modulus) == span_rank


def embed_rows(
    span_rows: list[list[int]],
    field: ExtensionField,
) -> list[list[FpE]]:
    return [[field.embed(value) for value in row] for row in span_rows]


def in_extension_span(
    embedded_span_rows: list[list[FpE]],
    span_rank: int,
    target: list[FpE],
    field: ExtensionField,
) -> bool:
    return rank_over_extension(embedded_span_rows + [target], field) == span_rank


def load_projector_cycle() -> list[int]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    roots = pari_linear_roots(pari.polclass(D), PROJECTOR_Q)
    graph = isogeny_neighbors(roots, ELL, PROJECTOR_Q)
    return walk_cycle(graph)


def projector_projected_distribution(cycle: list[int]) -> list[int]:
    projected = nontrivial_top_projected_b_trace(cycle)
    return projected + [(-value) % PROJECTOR_Q for value in projected]


def evaluate_projector_row() -> tuple[int, int, int, int, int]:
    right_degree = TOP_QUOTIENT
    c_degree = TOY_C_DEGREE
    broad_rows = c_axis_carry_rows(right_degree, c_degree, PROJECTOR_Q, admissible=False)
    admissible_rows = c_axis_carry_rows(
        right_degree, c_degree, PROJECTOR_Q, admissible=True
    )
    broad_rank = rank_mod(broad_rows, PROJECTOR_Q)
    admissible_rank = rank_mod(admissible_rows, PROJECTOR_Q)
    cycle = load_projector_cycle()

    no_forbidden = 0
    admissible_hits = 0
    broad_hits = 0
    broad_only_hits = 0
    for shift in range(H):
        shifted = rotate_list(cycle, shift)
        target = projector_projected_distribution(shifted)
        in_admissible = in_int_span(admissible_rows, admissible_rank, target, PROJECTOR_Q)
        in_broad = in_int_span(broad_rows, broad_rank, target, PROJECTOR_Q)
        no_forbidden += int(no_forbidden_int(target, right_degree, c_degree, PROJECTOR_Q))
        admissible_hits += int(in_admissible)
        broad_hits += int(in_broad)
        broad_only_hits += int(in_broad and not in_admissible)
    return (
        admissible_rank,
        broad_rank,
        no_forbidden,
        admissible_hits,
        broad_hits,
        broad_only_hits,
    )


def right_combo_projected_distribution(packet) -> list[FpE]:
    field = packet.field
    combos = [right_combo(packet, a_rel) for a_rel in range(packet.n)]
    return combos + [field.neg(value) for value in combos]


def coefficient_projected_distribution(coefficients: list[FpE], field) -> list[FpE]:
    return coefficients + [field.neg(value) for value in coefficients]


def defect_projected_distribution(coefficients: list[FpE], field) -> list[FpE]:
    base = coefficients[0]
    defects = [field.zero] + [field.sub(value, base) for value in coefficients[1:]]
    return defects + [field.neg(value) for value in defects]


def evaluate_right_combo_row() -> tuple[int, int, dict[str, tuple[int, int, int, int]], int]:
    packet = load_right_combo_packet()
    right_degree = 2
    c_degree = packet.n
    broad_rows = c_axis_carry_rows(right_degree, c_degree, packet.q, admissible=False)
    admissible_rows = c_axis_carry_rows(right_degree, c_degree, packet.q, admissible=True)
    broad_rank = rank_mod(broad_rows, packet.q)
    admissible_rank = rank_mod(admissible_rows, packet.q)
    broad_ext_rows = embed_rows(broad_rows, packet.field)
    admissible_ext_rows = embed_rows(admissible_rows, packet.field)

    profiles: dict[str, tuple[int, int, int, int]] = {
        "right_combo_resolvent": (0, 0, 0, 0),
        "weighted_coefficients": (0, 0, 0, 0),
        "selected_defect_coefficients": (0, 0, 0, 0),
    }
    rows_checked = 0
    for shift in range(packet.h):
        shifted = replace(packet, cycle=tuple(rotate_tuple(packet.cycle, shift)))
        coefficients = weighted_coefficients(shifted)
        targets = {
            "right_combo_resolvent": right_combo_projected_distribution(shifted),
            "weighted_coefficients": coefficient_projected_distribution(
                coefficients, packet.field
            ),
            "selected_defect_coefficients": defect_projected_distribution(
                coefficients, packet.field
            ),
        }
        for name, target in targets.items():
            no_forbidden, admissible_hits, broad_hits, broad_only_hits = profiles[name]
            in_admissible = in_extension_span(
                admissible_ext_rows, admissible_rank, target, packet.field
            )
            in_broad = in_extension_span(broad_ext_rows, broad_rank, target, packet.field)
            no_forbidden += int(
                no_forbidden_ext(target, right_degree, c_degree, packet.field)
            )
            admissible_hits += int(in_admissible)
            broad_hits += int(in_broad)
            broad_only_hits += int(in_broad and not in_admissible)
            profiles[name] = (
                no_forbidden,
                admissible_hits,
                broad_hits,
                broad_only_hits,
            )
        rows_checked += 1
    return admissible_rank, broad_rank, profiles, rows_checked


def main() -> None:
    (
        projector_admissible_rank,
        projector_broad_rank,
        projector_no_forbidden,
        projector_admissible_hits,
        projector_broad_hits,
        projector_broad_only_hits,
    ) = evaluate_projector_row()
    (
        right_combo_admissible_rank,
        right_combo_broad_rank,
        right_combo_profiles,
        right_combo_rows_checked,
    ) = evaluate_right_combo_row()

    print("Trace-GCD fixed-frequency actual-CM admissible Jacobi-span boundary")
    print("projector_row")
    print(f"  D={D}")
    print(f"  q={PROJECTOR_Q}")
    print(f"  h={H}")
    print(f"  right_degree={TOP_QUOTIENT}")
    print(f"  c_degree={TOY_C_DEGREE}")
    print(f"  admissible_rank={projector_admissible_rank}")
    print(f"  broad_rank={projector_broad_rank}")
    print(f"  no_forbidden_projected_origins={projector_no_forbidden}/{H}")
    print(f"  admissible_span_origins={projector_admissible_hits}/{H}")
    print(f"  broad_span_origins={projector_broad_hits}/{H}")
    print(f"  broad_only_origins={projector_broad_only_hits}/{H}")
    print("right_combo_row")
    print("  D=-13319")
    print("  q=13463")
    print(f"  h={right_combo_rows_checked}")
    print("  right_degree=2")
    print("  c_degree=5")
    print(f"  admissible_rank={right_combo_admissible_rank}")
    print(f"  broad_rank={right_combo_broad_rank}")
    for name, (
        no_forbidden,
        admissible_hits,
        broad_hits,
        broad_only_hits,
    ) in right_combo_profiles.items():
        print(f"  profile={name}")
        print(f"    no_forbidden_projected_origins={no_forbidden}/{right_combo_rows_checked}")
        print(f"    admissible_span_origins={admissible_hits}/{right_combo_rows_checked}")
        print(f"    broad_span_origins={broad_hits}/{right_combo_rows_checked}")
        print(f"    broad_only_origins={broad_only_hits}/{right_combo_rows_checked}")
    print("interpretation")
    print("  actual_cm_projector_packets_are_not_generically_admissible_jacobi=1")
    print("  actual_cm_right_combo_packets_are_not_generically_admissible_jacobi=1")
    print("  actual_cm_weighted_coefficient_packets_are_not_generically_admissible_jacobi=1")
    print("  actual_cm_selected_defect_packets_are_not_generically_admissible_jacobi=1")
    print("  broad_span_membership_without_no_forbidden_is_not_enough=1")
    print("  p24_still_needs_selected_weighted_packet_or_explicit_cm_lang_decomposition=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_actual_cm_admissible_jacobi_span_boundary")

    if projector_admissible_rank != 5 or projector_broad_rank != 6:
        raise SystemExit(1)
    if right_combo_admissible_rank != 5 or right_combo_broad_rank != 6:
        raise SystemExit(1)
    if projector_admissible_hits:
        raise SystemExit(1)
    if any(values[1] for values in right_combo_profiles.values()):
        raise SystemExit(1)
    if projector_no_forbidden:
        raise SystemExit(1)
    if any(values[0] for values in right_combo_profiles.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
