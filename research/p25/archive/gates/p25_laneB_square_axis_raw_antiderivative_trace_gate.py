#!/usr/bin/env python3
"""Raw trace-degree gate for the diagonal anomaly antiderivative.

The quotient antiderivative-density gate rules out a local degree-zero
quotient-linear correction.  The next possible escape is raw: choose only one
C_25 kernel representative above each anomaly class.  That makes the raw
D-boundary a two-point edge, while still tracing to the same quotient edge.

This gate records the obstruction.  Every raw lift whose normalized trace is
the local anomaly has raw degree B*3 = 75.  Trace-zero kernel modes cannot
change that degree.  Adding a raw scalar to force degree zero makes the raw
support dense on all 12675 positions and the quotient trace dense on all 507
classes.  Thus the sparse raw section is useful diagnostically, but it is not
a degree-zero local correction.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_divisor_footprint_gate import primitive_root
from p25_laneB_square_axis_anomaly_orbit_balance_gate import anomaly_orbit
from p25_laneB_square_axis_antiderivative_density_gate import edge_vector
from p25_laneB_square_axis_group_ring_normal_form_gate import S_STEP
from p25_laneB_square_axis_trace_projection_lift_gate import (
    block_constant_count,
    kernel_mode_support,
    normalized_trace,
    square_axis_case,
)
from p25_selected_defect_value_gate import RIGHT_DEGREE, split_prime_for


@dataclass(frozen=True)
class RawLiftProfile:
    name: str
    raw_support: int
    raw_degree: int
    trace_support: int
    trace_degree: int
    boundary_raw_support: int
    boundary_trace_support: int
    boundary_trace_ok: bool
    block_constancy_hits: int
    kernel_modes: tuple[int, ...]
    mode0_count: int
    nontrivial_mode_counts: tuple[int, ...]
    ok: bool


def raw_boundary(raw: list[int], step: int, modulus: int) -> list[int]:
    out = [0] * len(raw)
    for index, value in enumerate(raw):
        if value % modulus == 0:
            continue
        out[index] = (out[index] + value) % modulus
        out[(index + step) % len(raw)] = (
            out[(index + step) % len(raw)] - value
        ) % modulus
    return out


def raw_support(raw: list[int], modulus: int) -> int:
    return sum(1 for value in raw if value % modulus)


def raw_degree(raw: list[int], modulus: int) -> int:
    return sum(raw) % modulus


def add_raw_scalar(raw: list[int], scalar: int, modulus: int) -> list[int]:
    return [(value + scalar) % modulus for value in raw]


def scalar_for_raw_degree_zero(raw: list[int], modulus: int) -> int:
    return (-raw_degree(raw, modulus) * pow(len(raw), -1, modulus)) % modulus


def make_antiderivative_lift(kind: str, modulus: int) -> list[int]:
    case = square_axis_case()
    quotient_order = RIGHT_DEGREE * case.c_axis
    raw = [0] * case.raw_order
    if kind == "block":
        for q_value in anomaly_orbit():
            for layer in range(case.b_trace):
                raw[q_value + quotient_order * layer] = 1
    elif kind == "sparse_section":
        for q_value in anomaly_orbit():
            raw[q_value] = case.b_trace % modulus
    else:
        raise AssertionError(f"unknown lift kind: {kind}")
    return raw


def profile_lift(
    name: str,
    raw: list[int],
    modulus: int,
    zeta25: int,
    expected_raw_support: int,
    expected_raw_degree: int,
    expected_trace_support: int,
    expected_trace_degree: int,
    expected_boundary_raw_support: int,
    expected_block_constancy_hits: int,
    expected_kernel_modes: tuple[int, ...],
    expected_mode0_count: int,
    expected_nontrivial_mode_counts: tuple[int, ...],
) -> RawLiftProfile:
    case = square_axis_case()
    quotient_order = RIGHT_DEGREE * case.c_axis
    trace = normalized_trace(raw, case, modulus)
    boundary = raw_boundary(raw, S_STEP, modulus)
    boundary_trace = normalized_trace(boundary, case, modulus)
    expected_edge = edge_vector(modulus)
    modes, mode_counts = kernel_mode_support(raw, case, modulus, zeta25)
    nontrivial_counts = tuple(mode_counts[1:])
    row_ok = (
        raw_support(raw, modulus) == expected_raw_support
        and raw_degree(raw, modulus) == expected_raw_degree % modulus
        and raw_support(trace, modulus) == expected_trace_support
        and raw_degree(trace, modulus) == expected_trace_degree % modulus
        and raw_support(boundary, modulus) == expected_boundary_raw_support
        and raw_support(boundary_trace, modulus) == 2
        and boundary_trace == expected_edge
        and block_constant_count(raw, case) == expected_block_constancy_hits
        and modes == expected_kernel_modes
        and mode_counts[0] == expected_mode0_count
        and nontrivial_counts == expected_nontrivial_mode_counts
        and quotient_order == 507
    )
    return RawLiftProfile(
        name=name,
        raw_support=raw_support(raw, modulus),
        raw_degree=raw_degree(raw, modulus),
        trace_support=raw_support(trace, modulus),
        trace_degree=raw_degree(trace, modulus),
        boundary_raw_support=raw_support(boundary, modulus),
        boundary_trace_support=raw_support(boundary_trace, modulus),
        boundary_trace_ok=boundary_trace == expected_edge,
        block_constancy_hits=block_constant_count(raw, case),
        kernel_modes=modes,
        mode0_count=mode_counts[0],
        nontrivial_mode_counts=nontrivial_counts,
        ok=row_ok,
    )


def main() -> int:
    case = square_axis_case()
    quotient_order = RIGHT_DEGREE * case.c_axis
    modulus = split_prime_for(case.raw_order)
    root = primitive_root(modulus)
    zeta25 = pow(root, (modulus - 1) // case.b_trace, modulus)
    block = make_antiderivative_lift("block", modulus)
    sparse = make_antiderivative_lift("sparse_section", modulus)
    block_scalar = scalar_for_raw_degree_zero(block, modulus)
    sparse_scalar = scalar_for_raw_degree_zero(sparse, modulus)
    block_dz = add_raw_scalar(block, block_scalar, modulus)
    sparse_dz = add_raw_scalar(sparse, sparse_scalar, modulus)
    full_modes = tuple(range(case.b_trace))

    print("p25 Lane B square-axis raw-antiderivative trace gate")
    print(
        f"case={case.name} raw_order={case.raw_order} quotient_order={quotient_order} "
        f"B={case.b_trace} modulus={modulus}"
    )
    profiles = [
        profile_lift(
            "block_antiderivative",
            block,
            modulus,
            zeta25,
            expected_raw_support=75,
            expected_raw_degree=75,
            expected_trace_support=3,
            expected_trace_degree=3,
            expected_boundary_raw_support=50,
            expected_block_constancy_hits=quotient_order,
            expected_kernel_modes=(0,),
            expected_mode0_count=3,
            expected_nontrivial_mode_counts=(0,) * (case.b_trace - 1),
        ),
        profile_lift(
            "sparse_section_antiderivative",
            sparse,
            modulus,
            zeta25,
            expected_raw_support=3,
            expected_raw_degree=75,
            expected_trace_support=3,
            expected_trace_degree=3,
            expected_boundary_raw_support=2,
            expected_block_constancy_hits=quotient_order - 3,
            expected_kernel_modes=full_modes,
            expected_mode0_count=3,
            expected_nontrivial_mode_counts=(3,) * (case.b_trace - 1),
        ),
        profile_lift(
            "block_degree_zero_scalar",
            block_dz,
            modulus,
            zeta25,
            expected_raw_support=case.raw_order,
            expected_raw_degree=0,
            expected_trace_support=quotient_order,
            expected_trace_degree=0,
            expected_boundary_raw_support=50,
            expected_block_constancy_hits=quotient_order,
            expected_kernel_modes=(0,),
            expected_mode0_count=quotient_order,
            expected_nontrivial_mode_counts=(0,) * (case.b_trace - 1),
        ),
        profile_lift(
            "sparse_degree_zero_scalar",
            sparse_dz,
            modulus,
            zeta25,
            expected_raw_support=case.raw_order,
            expected_raw_degree=0,
            expected_trace_support=quotient_order,
            expected_trace_degree=0,
            expected_boundary_raw_support=2,
            expected_block_constancy_hits=quotient_order - 3,
            expected_kernel_modes=full_modes,
            expected_mode0_count=quotient_order,
            expected_nontrivial_mode_counts=(3,) * (case.b_trace - 1),
        ),
    ]

    ok_rows = 0
    for row in profiles:
        ok_rows += int(row.ok)
        print(
            f"lift {row.name}: "
            f"raw_support={row.raw_support} "
            f"raw_degree={row.raw_degree} "
            f"trace_support={row.trace_support} "
            f"trace_degree={row.trace_degree} "
            f"boundary_raw_support={row.boundary_raw_support} "
            f"boundary_trace_support={row.boundary_trace_support} "
            f"boundary_trace_ok={int(row.boundary_trace_ok)} "
            f"block_constancy_hits={row.block_constancy_hits}/{quotient_order} "
            f"kernel_modes={list(row.kernel_modes)} "
            f"mode0_count={row.mode0_count} "
            f"nontrivial_mode_counts_first={list(row.nontrivial_mode_counts[:5])} "
            f"ok={int(row.ok)}"
        )

    trace_degree_formula_ok = (
        raw_degree(block, modulus) * pow(case.b_trace, -1, modulus) % modulus == 3
        and raw_degree(sparse, modulus) * pow(case.b_trace, -1, modulus) % modulus == 3
        and block_scalar == sparse_scalar
        and block_scalar not in (0, modulus - 1)
    )
    row_ok = ok_rows == len(profiles) and trace_degree_formula_ok
    print(
        "raw_trace_degree_law: "
        f"raw_degree=B*trace_degree=75 "
        f"degree_zero_scalar={block_scalar} "
        f"same_scalar_for_block_and_sparse={int(block_scalar == sparse_scalar)} "
        f"trace_degree_formula_ok={int(trace_degree_formula_ok)} "
        f"ok={int(row_ok)}"
    )
    print("interpretation")
    print("  sparse_raw_section_makes_the_D_boundary_two_points_but_keeps_degree_75=1")
    print("  trace_zero_kernel_modes_do_not_change_the_raw_trace_degree=1")
    print("  forcing_raw_degree_zero_makes_even_the_sparse_section_dense=1")
    print("  raw_escape_must_do_more_than_choose_a_sparse_C25_section=1")
    print(f"square_axis_raw_antiderivative_trace_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_raw_antiderivative_trace_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
