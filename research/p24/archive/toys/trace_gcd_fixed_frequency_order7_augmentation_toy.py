#!/usr/bin/env python3
"""Order-7 augmentation route for the fixed-frequency syzygy.

The symmetry boundary shows that ordinary right centering only proves the
trivial fixed frequency.  This toy isolates a stronger theorem candidate.

Let R7 = F_p[y]/(y^7-1).  If the six right-orbit sections satisfy

    T + P2 + P3 + P4 + P5 + P6 = 0

after order-7 projection, and the omitted -1 orbit satisfies the sign
covariance

    P4 = y^(-2) T,

then

    (1 + y^(-2)) T = -(P2 + P3 + P5 + P6).

Since 1 + y^(-2) is a unit in R7, this gives the required fixed-frequency
tail-in-prefix syzygy without pointwise interpolation.
"""

from __future__ import annotations

from dataclasses import dataclass
import random


Q = 29
N = 7
AMBIENT_DIM = 4

Poly = list[int]
Section = list[Poly]


@dataclass(frozen=True)
class AugmentationCase:
    label: str
    one_plus_yminus2_unit: bool
    augmentation_identity: bool
    negation_covariance: bool
    explicit_syzygy: bool
    centering_at_y1: bool
    nontrivial_augmentation_zeroes: int


def primitive_root(q: int) -> int:
    factors: set[int] = set()
    value = q - 1
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            factors.add(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor += 1
    if value > 1:
        factors.add(value)
    for candidate in range(2, q):
        if all(pow(candidate, (q - 1) // factor, q) != 1 for factor in factors):
            return candidate
    raise RuntimeError("no primitive root")


def roots_of_order_7() -> list[int]:
    root = primitive_root(Q)
    omega = pow(root, (Q - 1) // N, Q)
    return [pow(omega, index, Q) for index in range(N)]


def cyclic_add(left: Poly, right: Poly) -> Poly:
    return [(a + b) % Q for a, b in zip(left, right)]


def cyclic_neg(poly: Poly) -> Poly:
    return [(-value) % Q for value in poly]


def cyclic_sub(left: Poly, right: Poly) -> Poly:
    return cyclic_add(left, cyclic_neg(right))


def cyclic_mul(left: Poly, right: Poly) -> Poly:
    out = [0] * N
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            index = (i + j) % N
            out[index] = (out[index] + a * b) % Q
    return out


def monomial(power: int, coeff: int = 1) -> Poly:
    out = [0] * N
    out[power % N] = coeff % Q
    return out


def poly_eval(poly: Poly, value: int) -> int:
    return sum(coeff * pow(value, power, Q) for power, coeff in enumerate(poly)) % Q


def rref(matrix: list[list[int]]) -> tuple[list[list[int]], list[int]]:
    rows = [[value % Q for value in row] for row in matrix if any(value % Q for value in row)]
    width = len(rows[0]) if rows else 0
    pivots: list[int] = []
    pivot_row = 0
    for col in range(width):
        pivot = next((row for row in range(pivot_row, len(rows)) if rows[row][col] % Q), None)
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        inv = pow(rows[pivot_row][col] % Q, -1, Q)
        rows[pivot_row] = [value * inv % Q for value in rows[pivot_row]]
        for row in range(len(rows)):
            if row == pivot_row:
                continue
            scale = rows[row][col] % Q
            if scale:
                rows[row] = [
                    (value - scale * pivot_value) % Q
                    for value, pivot_value in zip(rows[row], rows[pivot_row])
                ]
        pivots.append(col)
        pivot_row += 1
    return rows, pivots


def invert_unit(poly: Poly) -> Poly | None:
    columns = []
    for col in range(N):
        basis = monomial(col)
        columns.append(cyclic_mul(poly, basis))
    matrix = [[columns[col][row] for col in range(N)] for row in range(N)]
    target = monomial(0)
    reduced, pivots = rref([row + [target[index]] for index, row in enumerate(matrix)])
    if pivots[:N] != list(range(N)):
        return None
    return [reduced[row][-1] % Q for row in range(N)]


def random_poly(rng: random.Random) -> Poly:
    return [rng.randrange(Q) for _ in range(N)]


def random_section(rng: random.Random) -> Section:
    return [random_poly(rng) for _ in range(AMBIENT_DIM)]


def section_add(left: Section, right: Section) -> Section:
    return [cyclic_add(a, b) for a, b in zip(left, right)]


def section_neg(section: Section) -> Section:
    return [cyclic_neg(poly) for poly in section]


def section_sub(left: Section, right: Section) -> Section:
    return section_add(left, section_neg(right))


def section_scale(poly: Poly, section: Section) -> Section:
    return [cyclic_mul(poly, coord) for coord in section]


def section_sum(sections: list[Section]) -> Section:
    out = [[0] * N for _ in range(AMBIENT_DIM)]
    for section in sections:
        out = section_add(out, section)
    return out


def zero_section(section: Section) -> bool:
    return all(all(value % Q == 0 for value in poly) for poly in section)


def section_eval(section: Section, value: int) -> list[int]:
    return [poly_eval(poly, value) for poly in section]


def force_y1_centering(sections: list[Section], roots: list[int]) -> list[Section]:
    """Alter P6 by a constant vector so the augmentation vanishes at y=1."""

    adjusted = [[poly[:] for poly in section] for section in sections]
    total_at_one = section_eval(section_sum(adjusted), roots[0])
    for coord, value in enumerate(total_at_one):
        adjusted[-1][coord][0] = (adjusted[-1][coord][0] - value) % Q
    return adjusted


def analyze_case(label: str, sections: list[Section], yminus2: Poly, unit_inv: Poly | None) -> AugmentationCase:
    tail, p2, p3, p4, p5, p6 = sections
    augmentation = section_sum(sections)
    selected_sum = section_sum([p2, p3, p5, p6])
    explicit = False
    if unit_inv is not None:
        reconstructed = section_scale(cyclic_neg(unit_inv), selected_sum)
        explicit = zero_section(section_sub(tail, reconstructed))
    roots = roots_of_order_7()
    augmentation_values = [section_eval(augmentation, root) for root in roots]
    return AugmentationCase(
        label=label,
        one_plus_yminus2_unit=unit_inv is not None,
        augmentation_identity=zero_section(augmentation),
        negation_covariance=zero_section(section_sub(p4, section_scale(yminus2, tail))),
        explicit_syzygy=explicit,
        centering_at_y1=all(value == 0 for value in augmentation_values[0]),
        nontrivial_augmentation_zeroes=sum(
            int(all(value == 0 for value in values))
            for values in augmentation_values[1:]
        ),
    )


def print_case(case: AugmentationCase) -> None:
    print(
        f"case={case.label} "
        f"one_plus_yminus2_unit={int(case.one_plus_yminus2_unit)} "
        f"augmentation_identity={int(case.augmentation_identity)} "
        f"negation_covariance={int(case.negation_covariance)} "
        f"explicit_syzygy={int(case.explicit_syzygy)} "
        f"centering_at_y1={int(case.centering_at_y1)} "
        f"nontrivial_augmentation_zeroes={case.nontrivial_augmentation_zeroes}/6"
    )


def main() -> None:
    rng = random.Random(20260606)
    yminus2 = monomial(-2)
    denominator = cyclic_add(monomial(0), yminus2)
    unit_inv = invert_unit(denominator)

    tail = random_section(rng)
    p2 = random_section(rng)
    p3 = random_section(rng)
    p5 = random_section(rng)
    p4 = section_scale(yminus2, tail)
    p6 = section_neg(section_sum([tail, p2, p3, p4, p5]))
    good = [tail, p2, p3, p4, p5, p6]

    centered_only = force_y1_centering(
        [random_section(rng) for _ in range(6)],
        roots_of_order_7(),
    )

    corrupted_p4 = section_add(p4, random_section(rng))
    corrupted_p6 = section_neg(section_sum([tail, p2, p3, corrupted_p4, p5]))
    corrupted = [tail, p2, p3, corrupted_p4, p5, corrupted_p6]

    cases = [
        analyze_case("order7_augmentation_plus_negation", good, yminus2, unit_inv),
        analyze_case("ordinary_centering_only_control", centered_only, yminus2, unit_inv),
        analyze_case("augmentation_without_negation_control", corrupted, yminus2, unit_inv),
    ]

    print("Trace-GCD fixed-frequency order-7 augmentation toy")
    print(f"q={Q}")
    print(f"ring=F_q[y]/(y^{N}-1)")
    print(f"yminus2={yminus2}")
    print(f"one_plus_yminus2_inverse_exists={int(unit_inv is not None)}")
    for case in cases:
        print_case(case)
    print("interpretation")
    print("  order7_augmentation_plus_negation_gives_explicit_syzygy=1")
    print("  one_plus_yminus2_is_unit_in_R7=1")
    print("  centering_only_does_not_control_nontrivial_order7=1")
    print("  augmentation_without_negation_covariance_does_not_give_formula=1")
    print("  p24_next_theorem_can_be_order7_augmentation_vanishing=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_order7_augmentation_toy")

    good_case, centered_case, corrupted_case = cases
    if not good_case.explicit_syzygy:
        raise SystemExit(1)
    if centered_case.nontrivial_augmentation_zeroes != 0 or centered_case.explicit_syzygy:
        raise SystemExit(1)
    if corrupted_case.negation_covariance or corrupted_case.explicit_syzygy:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
