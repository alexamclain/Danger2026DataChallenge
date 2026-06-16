#!/usr/bin/env python3
"""Dimension accounting for the p24 top-coefficient trace-frame theorem."""

from __future__ import annotations

import math

SUBFIELD_DEGREE = 179
RELATIVE_DEGREE = 31

BLOCKS = {
    "constant": 1,
    "2": 1,
    "157": 156,
    "211": 210,
}

TARGETS = {
    "constant+2+157": BLOCKS["constant"] + BLOCKS["2"] + BLOCKS["157"],
    "211": BLOCKS["211"],
    "full_axis": sum(BLOCKS.values()),
}


def main() -> None:
    print("p24 top-coefficient capacity accounting")
    print(f"subfield_degree_over_E={SUBFIELD_DEGREE}")
    print(f"relative_degree_B_over_C={RELATIVE_DEGREE}")
    print()
    print("blocks")
    for name, dim in BLOCKS.items():
        print(f"  {name}: dim={dim} windows_needed={math.ceil(dim / SUBFIELD_DEGREE)}")
    print()
    print("targets")
    for name, dim in TARGETS.items():
        windows = math.ceil(dim / SUBFIELD_DEGREE)
        print(
            f"  {name}: dim={dim} windows_needed={windows} "
            f"capacity={windows * SUBFIELD_DEGREE}"
        )
    print()
    print("proposed_window_targets")
    print("  top_1 coefficient should certify constant+2+157 block")
    print("  top_2 coefficients should certify 211 block")
    print("  top_3 coefficients should certify the full axis direct sum")
    print("conclusion=reported_tensor_factor_top_coefficient_capacity")


if __name__ == "__main__":
    main()
