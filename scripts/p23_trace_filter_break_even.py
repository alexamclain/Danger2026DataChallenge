#!/usr/bin/env python3
"""Break-even costs for exact early odd trace-residue sidecar filters."""

from __future__ import annotations

import argparse
from functools import reduce

from x16_trace_residue_calibration import P23_TRACES


DEFAULT_ACTIVE_RATE_MPS = 0.108
DEFAULT_DIRECTY_RATE_MPS = 0.1175
DEFAULT_MEASURED_ELL3_US = 72.0


def target_residue_count(ell: int) -> int:
    return len({t % ell for t in P23_TRACES})


def product(values: list[float]) -> float:
    return reduce(lambda a, b: a * b, values, 1.0)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ells", type=int, nargs="+", default=[3, 5, 7, 11, 13, 17, 19])
    ap.add_argument("--active-rate-mps", type=float, default=DEFAULT_ACTIVE_RATE_MPS)
    ap.add_argument("--directy-rate-mps", type=float, default=DEFAULT_DIRECTY_RATE_MPS)
    ap.add_argument("--measured-ell3-us", type=float, default=DEFAULT_MEASURED_ELL3_US)
    args = ap.parse_args()

    active_us = 1.0 / args.active_rate_mps
    directy_us = 1.0 / args.directy_rate_mps

    print("p23 exact early trace-residue filter break-even")
    print(f"active_rate_Mps={args.active_rate_mps:.6f} active_cost_us={active_us:.6f}")
    print(f"directy_rate_Mps={args.directy_rate_mps:.6f} directy_cost_us={directy_us:.6f}")
    print(f"measured_ell3_exact_cost_us={args.measured_ell3_us:.3f}")
    print()
    print("prefix q_keep max_zero_cost_speedup active_break_even_us directy_break_even_us ell3_cost_over_active_break_even")

    qs: list[float] = []
    prefix: list[int] = []
    for ell in args.ells:
        prefix.append(ell)
        qs.append(target_residue_count(ell) / ell)
        q = product(qs)
        active_break_even = (1.0 - q) * active_us
        directy_break_even = (1.0 - q) * directy_us
        over = args.measured_ell3_us / active_break_even if active_break_even else float("inf")
        print(
            f"{','.join(str(x) for x in prefix):<20} "
            f"{q:.9f} {1.0 / q:.3f} "
            f"{active_break_even:.6f} {directy_break_even:.6f} {over:.2f}"
        )


if __name__ == "__main__":
    main()
