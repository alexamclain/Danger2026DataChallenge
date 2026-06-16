#!/usr/bin/env python3
"""Fixed-frequency tail-in-prefix annihilator bridge.

The no-fixed-defect theorem has a local fixed-frequency form:

    tau_a in span(P_a).

For the CM trace pairing this is often easier to prove dually:

    every lambda that annihilates the four prefix values P_a
    also annihilates the tail value tau_a.

This toy records the exact finite equivalence and keeps two controls separate:
tail-in-prefix removes a fixed-frequency defect, while prefix full rank is the
ordinary Plucker p-unit condition.  The p24 fixed-frequency theorem needs both.
"""

from __future__ import annotations

from dataclasses import dataclass

from l1_axis_injectivity_scan import rank_mod_q
from trace_gcd_prefix_syndrome_resultant_bridge_toy import dot, nullspace_basis


Q = 101
AMBIENT_DIM = 6
PREFIX_COUNT = 4


@dataclass(frozen=True)
class FixedAnnihilatorCase:
    label: str
    prefix_rank: int
    prefix_full: bool
    rank_with_tail: int
    fixed_rank_jump: bool
    tail_in_prefix: bool
    annihilator_dim: int
    annihilator_kills_tail: bool
    annihilator_equivalence: bool
    fixed_ordinary_local_gate: bool


def e(index: int) -> list[int]:
    row = [0] * AMBIENT_DIM
    row[index] = 1
    return row


def add_scaled(terms: list[tuple[int, list[int]]]) -> list[int]:
    return [
        sum(scale * row[col] for scale, row in terms) % Q
        for col in range(AMBIENT_DIM)
    ]


def analyze_case(
    label: str,
    prefix_rows: list[list[int]],
    tail_row: list[int],
) -> FixedAnnihilatorCase:
    prefix_rank = rank_mod_q(prefix_rows, Q)
    rank_with_tail = rank_mod_q(prefix_rows + [tail_row], Q)
    annihilator = nullspace_basis(prefix_rows, Q, AMBIENT_DIM)
    annihilator_kills_tail = all(dot(tail_row, lam, Q) == 0 for lam in annihilator)
    tail_in_prefix = rank_with_tail == prefix_rank
    return FixedAnnihilatorCase(
        label=label,
        prefix_rank=prefix_rank,
        prefix_full=prefix_rank == PREFIX_COUNT,
        rank_with_tail=rank_with_tail,
        fixed_rank_jump=rank_with_tail == prefix_rank + 1,
        tail_in_prefix=tail_in_prefix,
        annihilator_dim=len(annihilator),
        annihilator_kills_tail=annihilator_kills_tail,
        annihilator_equivalence=tail_in_prefix == annihilator_kills_tail,
        fixed_ordinary_local_gate=(prefix_rank == PREFIX_COUNT and tail_in_prefix),
    )


def print_case(case: FixedAnnihilatorCase) -> None:
    print(
        f"case={case.label} prefix_rank={case.prefix_rank} "
        f"prefix_full={int(case.prefix_full)} "
        f"rank_with_tail={case.rank_with_tail} "
        f"fixed_rank_jump={int(case.fixed_rank_jump)} "
        f"tail_in_prefix={int(case.tail_in_prefix)} "
        f"annihilator_dim={case.annihilator_dim} "
        f"annihilator_kills_tail={int(case.annihilator_kills_tail)} "
        f"annihilator_equivalence={int(case.annihilator_equivalence)} "
        f"fixed_ordinary_local_gate={int(case.fixed_ordinary_local_gate)}"
    )


def main() -> None:
    basis = [e(i) for i in range(AMBIENT_DIM)]
    full_prefix = [basis[0], basis[1], basis[2], basis[3]]
    dependent_prefix = [basis[0], basis[1], basis[2], basis[2]]

    rows = [
        analyze_case(
            "prefix_full_tail_inside",
            full_prefix,
            add_scaled([(3, basis[0]), (5, basis[1]), (7, basis[3])]),
        ),
        analyze_case("prefix_full_tail_outside", full_prefix, basis[4]),
        analyze_case(
            "prefix_defect_tail_inside_control",
            dependent_prefix,
            add_scaled([(1, basis[0]), (2, basis[1])]),
        ),
        analyze_case("prefix_defect_tail_outside_control", dependent_prefix, basis[3]),
    ]

    print("Trace-GCD fixed-frequency annihilator bridge toy")
    print(f"q={Q}")
    print(f"ambient_dim={AMBIENT_DIM}")
    print(f"prefix_count={PREFIX_COUNT}")
    for row in rows:
        print_case(row)
    print("p24")
    print("  p24_fixed_frequency_count=7")
    print("  p24_fixed_prefix_values_per_frequency=4")
    print("  p24_fixed_tail_values_per_frequency=1")
    print("interpretation")
    print("  annihilator_inclusion_iff_tail_in_prefix=1")
    print("  fixed_tail_in_prefix_removes_fixed_defect_line=1")
    print("  prefix_plucker_unit_is_separate_from_tail_in_prefix=1")
    print("  p24_dual_target_is_fixed_prefix_annihilator_kills_tail=1")
    print("  p24_primal_target_is_seven_fixed_frequency_linear_relations=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_annihilator_bridge_toy")

    if not all(row.annihilator_equivalence for row in rows):
        raise SystemExit(1)
    if not rows[0].fixed_ordinary_local_gate:
        raise SystemExit(1)
    if rows[1].fixed_ordinary_local_gate or not rows[1].fixed_rank_jump:
        raise SystemExit(1)
    if rows[2].fixed_ordinary_local_gate or not rows[2].tail_in_prefix:
        raise SystemExit(1)
    if rows[3].tail_in_prefix or not rows[3].fixed_rank_jump:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
