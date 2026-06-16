#!/usr/bin/env python3
"""Static accounting for the p24 trace-frame sum-rank erasure theorem."""

from __future__ import annotations

import math

P = 10**24 + 7
E_DEGREE = 5460
BLOCKS = 31
BLOCK_DIM = 179
AXIS_DIM = 368
KEEP_BLOCKS = 3


def main() -> None:
    kept_dim = KEEP_BLOCKS * BLOCK_DIM
    erased_blocks = BLOCKS - KEEP_BLOCKS
    erased_dim = erased_blocks * BLOCK_DIM
    ambient_dim = BLOCKS * BLOCK_DIM
    singleton_distance = ambient_dim - AXIS_DIM + 1
    needed_distance = erased_dim + 1
    subset_count = math.comb(BLOCKS, KEEP_BLOCKS)
    log10_q = E_DEGREE * math.log10(P)
    codim_margin = kept_dim - AXIS_DIM + 1
    one_projection_log10_failure = -codim_margin * log10_q
    union_log10_failure = math.log10(subset_count) + one_projection_log10_failure

    print("p24 trace-frame sum-rank erasure accounting")
    print(f"p={P}")
    print(f"E_degree={E_DEGREE}")
    print(f"log10_Q={log10_q:.6f}")
    print(f"relative_blocks={BLOCKS}")
    print(f"block_dimension_over_E={BLOCK_DIM}")
    print(f"axis_dimension={AXIS_DIM}")
    print(f"keep_blocks={KEEP_BLOCKS}")
    print(f"kept_dimension={kept_dim}")
    print(f"erased_blocks={erased_blocks}")
    print(f"erased_dimension={erased_dim}")
    print(f"ambient_dimension={ambient_dim}")
    print(f"three_block_subset_count={subset_count}")
    print()
    print("distance_accounting")
    print(f"  singleton_distance=ambient_dim-axis_dim+1={singleton_distance}")
    print(f"  needed_distance=erased_dimension+1={needed_distance}")
    print(f"  msrd_distance_suffices={int(singleton_distance >= needed_distance)}")
    print(f"  distance_slack={singleton_distance - needed_distance}")
    print()
    print("random_subspace_model")
    print("  one_projection_failure ~= Q^-(kept_dimension-axis_dimension+1)")
    print(f"  codim_margin={codim_margin}")
    print(f"  log10_one_projection_failure~={one_projection_log10_failure:.6e}")
    print(f"  log10_union_bound_all_3blocks~={union_log10_failure:.6e}")
    print()
    print("certificate_surface")
    print("  top_three_certificate_needs_one_injective_projection=1")
    print(f"  all_three_block_erasure_theorem_has_projection_count={subset_count}")
    print("  stronger_erasure_theorem_is_better_as_a_proof_import_than_as_finite_data=1")
    print("conclusion=reported_trace_frame_sum_rank_erasure_accounting")


if __name__ == "__main__":
    main()
