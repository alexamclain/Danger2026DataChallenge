#!/usr/bin/env python3
"""Fixed-frequency relation-section gate.

The no-fixed-defect theorem is local at the seven fixed frequencies
`a in 5Z/35Z`.  The annihilator bridge says it is enough to prove

    V_{a,1} in span(V_{a,2}, V_{a,3}, V_{a,5}, V_{a,6})

for all seven fixed frequencies.  Since `p24 = 1 mod 7`, those frequencies
are base-rational in the 7-part.  A class-set-free proof should therefore
produce four base cyclic coefficient sections

    c_2(y), c_3(y), c_5(y), c_6(y) in F_p[y]/(y^7 - 1)

such that, at each seventh root y=omega^a,

    V_{a,1} = c_2(y)V_{a,2}+c_3(y)V_{a,3}+c_5(y)V_{a,5}+c_6(y)V_{a,6}.

This toy records the finite implication and controls.  The coefficient section
is a certificate surface only when constructed intrinsically from the CM/Lang
data; arbitrary interpolation after seeing the seven relations is still
post-fit evidence.
"""

from __future__ import annotations

from dataclasses import dataclass
import random

from l1_axis_injectivity_scan import rank_mod_q
from trace_gcd_prefix_syndrome_resultant_bridge_toy import dot, nullspace_basis


Q = 43
FIXED_COUNT = 7
PREFIX_COUNT = 4
AMBIENT_DIM = 6


@dataclass(frozen=True)
class RelationSectionCase:
    label: str
    fixed_count: int
    relation_zeroes: int
    prefix_full_frequencies: int
    tail_in_prefix_frequencies: int
    annihilator_inclusions: int
    fixed_defect_frequencies: int
    fixed_ordinary_gate_frequencies: int
    relation_section_valid: bool
    no_fixed_defects: bool


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
    raise RuntimeError("no primitive root found")


def poly_eval(coeffs: list[int], x: int, q: int) -> int:
    total = 0
    power = 1
    for coeff in coeffs:
        total = (total + coeff * power) % q
        power = power * x % q
    return total


def add_scaled(terms: list[tuple[int, list[int]]], q: int) -> list[int]:
    return [
        sum(scale * row[col] for scale, row in terms) % q
        for col in range(AMBIENT_DIM)
    ]


def random_vector(q: int, rng: random.Random) -> list[int]:
    return [rng.randrange(q) for _ in range(AMBIENT_DIM)]


def random_full_prefix(q: int, rng: random.Random) -> list[list[int]]:
    for _ in range(1000):
        rows = [random_vector(q, rng) for _ in range(PREFIX_COUNT)]
        if rank_mod_q(rows, q) == PREFIX_COUNT:
            return rows
    raise RuntimeError("failed to find full prefix")


def relation_tail(
    prefix_rows: list[list[int]],
    coeff_sections: list[list[int]],
    root: int,
    q: int,
) -> list[int]:
    coeffs = [poly_eval(section, root, q) for section in coeff_sections]
    return add_scaled(list(zip(coeffs, prefix_rows)), q)


def vector_sub(left: list[int], right: list[int], q: int) -> list[int]:
    return [(a - b) % q for a, b in zip(left, right)]


def annihilator_kills_tail(prefix_rows: list[list[int]], tail: list[int], q: int) -> bool:
    annihilator = nullspace_basis(prefix_rows, q, AMBIENT_DIM)
    return all(dot(tail, lam, q) == 0 for lam in annihilator)


def analyze_case(
    label: str,
    prefix_by_frequency: list[list[list[int]]],
    tail_by_frequency: list[list[int]],
    coeff_sections: list[list[int]],
    roots: list[int],
) -> RelationSectionCase:
    relation_zeroes = 0
    prefix_full = 0
    tail_inside = 0
    annihilator_ok = 0
    fixed_defects = 0
    ordinary = 0
    for prefix_rows, tail, root in zip(prefix_by_frequency, tail_by_frequency, roots):
        expected = relation_tail(prefix_rows, coeff_sections, root, Q)
        relation_ok = vector_sub(tail, expected, Q) == [0] * AMBIENT_DIM
        relation_zeroes += int(relation_ok)
        prefix_rank = rank_mod_q(prefix_rows, Q)
        rank_with_tail = rank_mod_q(prefix_rows + [tail], Q)
        prefix_full += int(prefix_rank == PREFIX_COUNT)
        inside = rank_with_tail == prefix_rank
        tail_inside += int(inside)
        annihilator_ok += int(annihilator_kills_tail(prefix_rows, tail, Q))
        fixed_defects += int(rank_with_tail == prefix_rank + 1)
        ordinary += int(prefix_rank == PREFIX_COUNT and inside)
    return RelationSectionCase(
        label=label,
        fixed_count=len(roots),
        relation_zeroes=relation_zeroes,
        prefix_full_frequencies=prefix_full,
        tail_in_prefix_frequencies=tail_inside,
        annihilator_inclusions=annihilator_ok,
        fixed_defect_frequencies=fixed_defects,
        fixed_ordinary_gate_frequencies=ordinary,
        relation_section_valid=relation_zeroes == len(roots),
        no_fixed_defects=fixed_defects == 0,
    )


def print_case(case: RelationSectionCase) -> None:
    print(
        f"case={case.label} fixed_count={case.fixed_count} "
        f"relation_zeroes={case.relation_zeroes}/{case.fixed_count} "
        f"prefix_full_frequencies={case.prefix_full_frequencies}/{case.fixed_count} "
        f"tail_in_prefix_frequencies={case.tail_in_prefix_frequencies}/{case.fixed_count} "
        f"annihilator_inclusions={case.annihilator_inclusions}/{case.fixed_count} "
        f"fixed_defect_frequencies={case.fixed_defect_frequencies} "
        "fixed_ordinary_gate_frequencies="
        f"{case.fixed_ordinary_gate_frequencies}/{case.fixed_count} "
        f"relation_section_valid={int(case.relation_section_valid)} "
        f"no_fixed_defects={int(case.no_fixed_defects)}"
    )


def main() -> None:
    rng = random.Random(20260606)
    root = primitive_root(Q)
    omega7 = pow(root, (Q - 1) // FIXED_COUNT, Q)
    roots = [pow(omega7, index, Q) for index in range(FIXED_COUNT)]
    coeff_sections = [
        [rng.randrange(Q) for _ in range(FIXED_COUNT)]
        for _ in range(PREFIX_COUNT)
    ]
    good_prefix = [random_full_prefix(Q, rng) for _ in range(FIXED_COUNT)]
    good_tail = [
        relation_tail(prefix_rows, coeff_sections, root_value, Q)
        for prefix_rows, root_value in zip(good_prefix, roots)
    ]

    corrupted_tail = [row[:] for row in good_tail]
    corrupted_tail[3] = vector_sub(corrupted_tail[3], [0, 0, 0, 0, 1, 0], Q)

    prefix_defect = [[row[:] for row in prefix] for prefix in good_prefix]
    prefix_defect[2][-1] = prefix_defect[2][0][:]
    prefix_defect_tail = [
        relation_tail(prefix_rows, coeff_sections, root_value, Q)
        for prefix_rows, root_value in zip(prefix_defect, roots)
    ]

    cases = [
        analyze_case("valid_relation_section", good_prefix, good_tail, coeff_sections, roots),
        analyze_case("one_bad_fixed_relation_control", good_prefix, corrupted_tail, coeff_sections, roots),
        analyze_case(
            "prefix_plucker_failure_control",
            prefix_defect,
            prefix_defect_tail,
            coeff_sections,
            roots,
        ),
    ]

    print("Trace-GCD fixed-frequency relation-section toy")
    print(f"q={Q}")
    print(f"fixed_frequency_count={FIXED_COUNT}")
    print(f"prefix_count={PREFIX_COUNT}")
    print(f"relation_section_coefficients={PREFIX_COUNT * FIXED_COUNT}")
    for case in cases:
        print_case(case)
    print("interpretation")
    print("  relation_section_implies_tail_in_prefix_at_all_fixed_frequencies=1")
    print("  valid_relation_section_removes_all_fixed_defects=1")
    print("  corrupted_fixed_relation_creates_fixed_defect=1")
    print("  prefix_plucker_unit_remains_separate_from_relation_section=1")
    print("  p24_relation_section_target_has_28_base_coefficients=1")
    print("  relation_section_must_be_constructed_intrinsically_not_postfit=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_relation_section_toy")

    good, corrupted, prefix_bad = cases
    if not good.relation_section_valid or not good.no_fixed_defects:
        raise SystemExit(1)
    if corrupted.relation_section_valid or corrupted.fixed_defect_frequencies != 1:
        raise SystemExit(1)
    if not prefix_bad.relation_section_valid or prefix_bad.fixed_ordinary_gate_frequencies == FIXED_COUNT:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
