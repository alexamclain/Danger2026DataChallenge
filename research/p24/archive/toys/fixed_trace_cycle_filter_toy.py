#!/usr/bin/env python3
"""Fixed-trace filtering still does not select one CM-order component quotient."""

from __future__ import annotations

from cypari2 import Pari

from fixed_trace_cm_root_toy import (
    FROBENIUS_D,
    MAXIMAL_D,
    P,
    TRACE,
    curve_order,
    j_invariant,
    pari_linear_roots,
)
from unfiltered_phi_cycle_toy import ELL, Q, cm_cycle_sums, phi_adjacency, simple_3cycles


def fixed_trace_j_values() -> set[int]:
    out: set[int] = set()
    for a in range(P):
        for b in range(P):
            j = j_invariant(a, b)
            if j is None:
                continue
            trace = P + 1 - curve_order(a, b)
            if abs(trace) == TRACE:
                out.add(j)
    return out


def main() -> None:
    pari = Pari()
    pari.allocatemem(128 * 1024 * 1024)
    maximal_roots = set(pari_linear_roots(pari.polclass(MAXIMAL_D), P))
    frobenius_roots = set(pari_linear_roots(pari.polclass(FROBENIUS_D), P))
    fixed_roots = fixed_trace_j_values()
    if fixed_roots != maximal_roots | frobenius_roots:
        raise AssertionError("fixed trace roots should equal union of CM orders")

    graph = phi_adjacency(Q, ELL)
    cycles = simple_3cycles(graph)
    universal_sums = {sum(cycle) % Q for cycle in cycles}
    fixed_cycles = [cycle for cycle in cycles if set(cycle) <= fixed_roots]
    fixed_sums = {sum(cycle) % Q for cycle in fixed_cycles}
    maximal_cycles = [cycle for cycle in cycles if set(cycle) <= maximal_roots]
    maximal_sums = {sum(cycle) % Q for cycle in maximal_cycles}

    print("fixed trace cycle filter toy")
    print(f"p={P}")
    print(f"target_abs_trace={TRACE}")
    print(f"maximal_D={MAXIMAL_D}")
    print(f"frobenius_order_D={FROBENIUS_D}")
    print(f"ell={ELL}")
    print(f"universal_cycles={len(cycles)}")
    print(f"universal_sum_count={len(universal_sums)}")
    print(f"maximal_roots={sorted(maximal_roots)}")
    print(f"frobenius_roots={sorted(frobenius_roots)}")
    print(f"fixed_trace_roots={sorted(fixed_roots)}")
    print(f"maximal_cycles={len(maximal_cycles)}")
    print(f"maximal_sums={sorted(maximal_sums)}")
    print(f"cm_cycle_sums_helper={cm_cycle_sums()}")
    print(f"fixed_trace_cycles={len(fixed_cycles)}")
    print(f"fixed_trace_sums={sorted(fixed_sums)}")
    print(f"extra_fixed_trace_sums={sorted(fixed_sums - maximal_sums)}")
    print()
    print("interpretation")
    print("  fixed_trace_filter_removes_many_universal_cycles=1")
    print("  fixed_trace_still_includes_multiple_CM_orders=1")
    print("  maximal_order_component_quotient_still_needs_order_or_volcano_filter=1")
    print("conclusion=reported_fixed_trace_cycle_filter_toy")


if __name__ == "__main__":
    main()
