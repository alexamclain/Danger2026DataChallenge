#!/usr/bin/env python3
"""Linear-span obstruction for the p25 GK half-orbit projector.

The half-orbit interaction gate found the exact anomaly projector:

    O * (1 - E)

where O and E are the odd and even Frobenius p^2 half-orbit averages.  This
gate checks that the product/resonance is genuinely needed at the finite
screening level: the anomaly indicator is not in the rational linear span of
the constant vector, Lucas/no-borrow selected support, O, and E.

Adding a product term closes the span immediately:

    anomaly = O - O*E = selected*O.

So a literature hit that only supplies additive half-orbit averages is still
too weak.  A hit that supplies a multiplicative unit quotient, Barnes delta,
or equivalent interaction remains alive.
"""

from __future__ import annotations

from fractions import Fraction

from p25_laneB_square_axis_gross_koblitz_half_orbit_interaction_gate import (
    interaction_profile,
)


Vector = tuple[int, ...]


def column_rank(vectors: tuple[Vector, ...]) -> int:
    if not vectors:
        return 0
    rows = len(vectors[0])
    matrix = [
        [Fraction(vector[row]) for vector in vectors]
        for row in range(rows)
    ]
    rank = 0
    column_count = len(vectors)
    for column in range(column_count):
        pivot = None
        for row in range(rank, rows):
            if matrix[row][column]:
                pivot = row
                break
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        pivot_value = matrix[rank][column]
        matrix[rank] = [value / pivot_value for value in matrix[rank]]
        for row in range(rows):
            if row == rank or not matrix[row][column]:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                value - factor * pivot_entry
                for value, pivot_entry in zip(matrix[row], matrix[rank])
            ]
        rank += 1
        if rank == rows:
            break
    return rank


def in_span(basis: tuple[Vector, ...], target: Vector) -> bool:
    return column_rank(basis) == column_rank(basis + (target,))


def vector(values: list[int]) -> Vector:
    return tuple(values)


def main() -> int:
    print("p25 Lane B square-axis Gross-Koblitz half-orbit linear-span obstruction gate")
    profile = interaction_profile()
    cells = profile.cells
    coords = tuple((cell.h_value, cell.t_value) for cell in cells)

    one = vector([1 for _cell in cells])
    selected = vector([int(cell.selected) for cell in cells])
    odd = vector([cell.odd_avg for cell in cells])
    even = vector([cell.even_avg for cell in cells])
    odd_even_product = vector([cell.odd_avg * cell.even_avg for cell in cells])
    odd_not_even = vector([cell.odd_avg * (1 - cell.even_avg) for cell in cells])
    selected_odd = vector([int(cell.selected) * cell.odd_avg for cell in cells])
    anomaly = vector([int(cell.anomaly) for cell in cells])
    binomial_defect = vector([
        (cell.corrected_payload_value is not None)
        and (1 if cell.anomaly else 0)
        for cell in cells
    ])

    additive_basis = (one, selected, odd, even)
    product_basis = additive_basis + (odd_even_product,)
    direct_interaction_basis = additive_basis + (odd_not_even,)
    selected_product_basis = additive_basis + (selected_odd,)

    additive_rank = column_rank(additive_basis)
    additive_with_target_rank = column_rank(additive_basis + (anomaly,))
    product_rank = column_rank(product_basis)
    direct_interaction_rank = column_rank(direct_interaction_basis)
    selected_product_rank = column_rank(selected_product_basis)

    row_ok = (
        coords
        == (
            (0, 0),
            (0, 1),
            (0, 2),
            (1, 0),
            (1, 1),
            (1, 2),
            (2, 0),
            (2, 1),
            (2, 2),
        )
        and not in_span(additive_basis, anomaly)
        and in_span(product_basis, anomaly)
        and in_span(direct_interaction_basis, anomaly)
        and in_span(selected_product_basis, anomaly)
        and odd_not_even == anomaly
        and selected_odd == anomaly
        and binomial_defect == anomaly
    )

    print(f"coords={coords}")
    print(f"one={one}")
    print(f"selected={selected}")
    print(f"odd={odd}")
    print(f"even={even}")
    print(f"odd_even_product={odd_even_product}")
    print(f"odd_not_even={odd_not_even}")
    print("span_laws")
    print(f"  additive_rank={additive_rank}")
    print(f"  additive_with_target_rank={additive_with_target_rank}")
    print(f"  product_rank={product_rank}")
    print(f"  direct_interaction_rank={direct_interaction_rank}")
    print(f"  selected_product_rank={selected_product_rank}")
    print(f"  anomaly_in_additive_half_orbit_span={int(in_span(additive_basis, anomaly))}")
    print(f"  anomaly_in_product_half_orbit_span={int(in_span(product_basis, anomaly))}")
    print(f"  anomaly_equals_odd_not_even={int(odd_not_even == anomaly)}")
    print(f"  anomaly_equals_selected_odd={int(selected_odd == anomaly)}")
    print("interpretation")
    print("  additive_half_orbit_averages_are_too_weak=1")
    print("  multiplicative_or_delta_interaction_is_required=1")
    print(f"square_axis_gross_koblitz_half_orbit_linear_span_obstruction_rows={int(row_ok)}/1")
    print(
        "conclusion=reported_p25_laneB_square_axis_gross_koblitz_half_orbit_linear_span_obstruction_gate"
    )
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
