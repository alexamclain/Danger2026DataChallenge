#!/usr/bin/env python3
"""Toy gate for product-component kernel transversality.

For A = K x K, global K-rank of vectors in A is the rank of the stacked
component matrices.  Component ranks alone are not enough: two maps can have
the same component rank profile but different global rank depending on how
their kernels intersect.
"""

from __future__ import annotations

from l1_axis_injectivity_scan import rank_mod_q


def rank(matrix: list[list[int]], q: int) -> int:
    return rank_mod_q(matrix, q)


def stack(components: list[list[list[int]]]) -> list[list[int]]:
    rows: list[list[int]] = []
    for matrix in components:
        rows.extend(matrix)
    return rows


def kernel_dim(source_dim: int, matrix: list[list[int]], q: int) -> int:
    return source_dim - rank(matrix, q)


def report_case(label: str, components: list[list[list[int]]], q: int) -> dict[str, int | str]:
    source_dim = len(components[0][0])
    component_ranks = [rank(matrix, q) for matrix in components]
    global_rank = rank(stack(components), q)
    global_kernel_dim = source_dim - global_rank
    component_kernel_dims = [
        kernel_dim(source_dim, matrix, q)
        for matrix in components
    ]
    print(
        f"case={label} component_ranks={component_ranks} "
        f"component_kernel_dims={component_kernel_dims} "
        f"global_rank={global_rank} global_kernel_dim={global_kernel_dim}"
    )
    return {
        "label": label,
        "component_rank_sum": sum(component_ranks),
        "global_rank": global_rank,
        "global_kernel_dim": global_kernel_dim,
    }


def main() -> None:
    q = 2
    source_dim = 2
    transverse = [
        [[1, 0]],
        [[0, 1]],
    ]
    aligned = [
        [[1, 0]],
        [[1, 0]],
    ]

    print("Trace-GCD prefix tensor-component rank toy")
    print(f"q={q}")
    print(f"source_dim={source_dim}")
    transverse_result = report_case("transverse_kernels", transverse, q)
    aligned_result = report_case("aligned_kernels", aligned, q)
    print("p24")
    print("  p24_tensor_components=4")
    print("  p24_component_dim_over_K=39")
    print("  p24_source_dim_over_K=140")
    print("  p24_component_rank_sum_needed_at_least=140")
    print("  p24_max_component_rank_sum=156")
    print("interpretation")
    print(
        "  same_component_rank_profile_different_global_rank="
        f"{int(transverse_result['component_rank_sum'] == aligned_result['component_rank_sum'] and transverse_result['global_rank'] != aligned_result['global_rank'])}"
    )
    print(
        "  global_full_rank_iff_component_kernel_intersection_zero="
        f"{int(transverse_result['global_kernel_dim'] == 0 and aligned_result['global_kernel_dim'] > 0)}"
    )
    print("  p24_prefix_tensor_components_require_kernel_transversality=1")
    print("conclusion=reported_trace_gcd_prefix_tensor_component_rank_toy")


if __name__ == "__main__":
    main()
