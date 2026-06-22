#!/usr/bin/env python3
"""H90 local-solubility boundary for the Dplus U6 row bit.

The point-fiber probe found that row-bit fibers can be mixed over t alone, but
were uniform over rational E_h90 points.  This probe isolates the cheap
boundary statement:

    are t-fibers uniform exactly when Ktrace has a rational square root?

Here Ktrace = -(t^2+2t-1)(t^2-2t-1), the H90 elliptic coordinate satisfies
w^2 = Ktrace, and the row bit is chi(U6+2) on the reciprocal tower.

This is not a source law by itself.  It asks whether the right next theorem is
local solubility/Prym/theta over E_h90 rather than another visible character.
"""

from __future__ import annotations

import argparse
from collections import Counter

from p27_trace_norm_dplus_u6_rowbit_h90_pointfiber_probe import (
    chi,
    h90_values,
    parse_fields,
    row_signs_for_t,
    sign_name,
)


def normalize_signs(values: list[int]) -> int | None:
    signs = {value for value in values if value in (-1, 1)}
    if not signs:
        return None
    if len(signs) == 1:
        return signs.pop()
    return 0


def collect_field(q: int, materialization_filters: bool) -> Counter[str]:
    stats: Counter[str] = Counter()
    for t in range(1, q):
        signs = row_signs_for_t(t, q, materialization_filters)
        target = normalize_signs(signs)
        if target is None:
            stats["empty_t"] += 1
            continue

        _B, _C, _Fspin, Ktrace = h90_values(t, q)
        ksign = chi(Ktrace, q)
        klabel = sign_name(ksign)
        fiber_label = "mixed" if target == 0 else f"uniform_{sign_name(target)}"

        stats["active_t"] += 1
        stats[f"ktrace_{klabel}"] += 1
        stats[f"ktrace_{klabel}_{fiber_label}"] += 1
        stats[f"ktrace_{klabel}_rows"] += len(signs)
        stats[f"fiber_{fiber_label}"] += 1
        stats[f"fiber_size_{len(signs)}"] += 1

        if ksign != -1 and target == 0:
            stats["h90_soluble_mixed_failures"] += 1
        if ksign == -1 and target in (-1, 1):
            stats["h90_insoluble_uniform_failures"] += 1

        if target == 0:
            plus = sum(1 for sign in signs if sign == 1)
            minus = sum(1 for sign in signs if sign == -1)
            stats[f"mixed_plus_{plus}_minus_{minus}"] += 1

    active = stats["active_t"]
    stats["boundary_failures"] = stats["h90_soluble_mixed_failures"] + stats["h90_insoluble_uniform_failures"]
    stats["boundary_failure_x1000000"] = stats["boundary_failures"] * 1_000_000 // active if active else 0
    return stats


def print_counter(label: str, stats: Counter[str]) -> None:
    print(f"{label}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def run(fields: list[int], materialization_filters: bool) -> Counter[str]:
    aggregate: Counter[str] = Counter()
    print(f"materialization_filters = {int(materialization_filters)}")
    for q in fields:
        stats = collect_field(q, materialization_filters)
        aggregate.update(stats)
        print_counter(f"q{q}", stats)
    print_counter("aggregate", aggregate)
    return aggregate


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fields", default="71,167,199,263,607,1607,1847,2087")
    parser.add_argument("--include-bare", action="store_true")
    args = parser.parse_args()

    fields = parse_fields(args.fields)
    print("p27 trace/norm Dplus U6 row-bit H90 solubility-boundary probe")
    print("question = are row-bit t-fibers uniform exactly on H90-soluble Ktrace fibers?")
    print(f"fields = {','.join(str(q) for q in fields)}")

    aggregates = []
    for materialization_filters in ([True, False] if args.include_bare else [True]):
        aggregates.append(run(fields, materialization_filters))

    total_failures = sum(stats["boundary_failures"] for stats in aggregates)
    print("verdict:")
    print("  zero boundary failures supports a local-solubility/Prym/theta explanation")
    print("  any boundary failure kills the exact H90-solubility boundary formulation")
    print(f"total_boundary_failures = {total_failures}")
    print("p27_trace_norm_dplus_u6_rowbit_h90_solubility_boundary_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
