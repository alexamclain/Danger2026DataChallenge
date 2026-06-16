#!/usr/bin/env python3
"""Kummer nonvanishing bridge for a cyclic relative layer.

This uses the D=-5000, h=30=2*3*5 calibration tower.  For one degree-3
relative layer above a parent, the child periods y_0,y_1,y_2 form a cyclic
vector.  Its Fourier evaluations

    T_s = sum_u zeta^(s*u) y_u

are relative character traces.  The primitive Kummer powers K_s = T_s^3 are
invariant under cyclic relabeling.  For nonvanishing/p-unit purposes, K_s != 0
is enough to prove T_s != 0, even though K_s alone does not select the child
ordering.

This is the finite bridge the p24 trace-GCD route would use if f_trace can be
expressed in relative Kummer/resolvent coordinates.
"""

from __future__ import annotations

from cypari2 import Pari

from embedded_decomposition_calibration import (
    D,
    ELL,
    H,
    Q,
    isogeny_neighbors,
    pari_linear_roots,
    walk_cycle,
)
from relative_tower_character_toy import (
    FINE_QUOTIENT,
    RECOVERY_SIZE,
    RELATIVE_DEGREE,
    TOP_QUOTIENT,
    f2_add,
    f2_from_base,
    f2_mul,
    f2_pow,
    f2_scalar_mul,
)


Fq2 = tuple[int, int]


def f2_is_zero(x: Fq2) -> bool:
    return x == (0, 0)


def f2_is_base(x: Fq2) -> bool:
    return x[1] == 0


def relative_traces(children: list[int], zeta: Fq2) -> list[Fq2]:
    traces: list[Fq2] = []
    for s in range(RELATIVE_DEGREE):
        value = (0, 0)
        for u, child in enumerate(children):
            coeff = f2_pow(zeta, s * u, Q)
            value = f2_add(value, f2_scalar_mul(child, coeff, Q), Q)
        traces.append(value)
    return traces


def product(values: list[Fq2]) -> Fq2:
    out = (1, 0)
    for value in values:
        out = f2_mul(out, value, Q)
    return out


def direct_cyclic_values(children: list[int], zeta: Fq2) -> list[Fq2]:
    """Evaluate f(Y)=sum_u children[u] Y^u at 1,zeta,zeta^2."""

    values: list[Fq2] = []
    for s in range(RELATIVE_DEGREE):
        value = (0, 0)
        point = f2_pow(zeta, s, Q)
        for u, child in enumerate(children):
            value = f2_add(
                value,
                f2_scalar_mul(child, f2_pow(point, u, Q), Q),
                Q,
            )
        values.append(value)
    return values


def main() -> None:
    if RELATIVE_DEGREE != 3:
        raise AssertionError("toy specialized to the degree-3 layer")

    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    roots = pari_linear_roots(pari.polclass(D), Q)
    graph = isogeny_neighbors(roots, ELL, Q)
    cycle = walk_cycle(graph)

    fine_periods = [
        sum(cycle[(r + FINE_QUOTIENT * k) % H] for k in range(RECOVERY_SIZE)) % Q
        for r in range(FINE_QUOTIENT)
    ]
    zeta = (0, 1)

    print("relative Kummer nonvanishing bridge toy")
    print(f"D={D}")
    print(f"q={Q}")
    print(f"generator_ell={ELL}")
    print(f"class_number={H}")
    print(f"top_quotient={TOP_QUOTIENT}")
    print(f"relative_degree={RELATIVE_DEGREE}")
    print(f"recovery_subgroup_size={RECOVERY_SIZE}")
    print(f"zeta_pair={zeta}")
    print()

    failures = 0
    for parent in range(TOP_QUOTIENT):
        children = [
            fine_periods[parent + TOP_QUOTIENT * a]
            for a in range(RELATIVE_DEGREE)
        ]
        traces = relative_traces(children, zeta)
        direct = direct_cyclic_values(children, zeta)
        kummer = [f2_pow(trace, RELATIVE_DEGREE, Q) for trace in traces]
        norm_from_traces = product(traces)
        norm_from_direct = product(direct)
        all_traces_nonzero = all(not f2_is_zero(trace) for trace in traces)
        all_kummer_nonzero = all(not f2_is_zero(value) for value in kummer)
        bridge_ok = all_traces_nonzero == all_kummer_nonzero
        direct_match = traces == direct
        norm_match = norm_from_traces == norm_from_direct
        norm_base = f2_is_base(norm_from_traces)
        failures += int(not (bridge_ok and direct_match and norm_match and norm_base))

        print(f"parent={parent}")
        print(f"  children={children}")
        print(f"  traces={traces}")
        print(f"  direct_values={direct}")
        print(f"  kummer_powers={kummer}")
        print(f"  norm_from_traces={norm_from_traces}")
        print(f"  norm_from_direct={norm_from_direct}")
        print(f"  norm_in_base_field={int(norm_base)}")
        print(f"  direct_values_match_traces={int(direct_match)}")
        print(f"  all_traces_nonzero={int(all_traces_nonzero)}")
        print(f"  all_kummer_powers_nonzero={int(all_kummer_nonzero)}")
        print(f"  nonvanishing_bridge_ok={int(bridge_ok)}")

    zero_children = [1, 1, 1]
    zero_traces = relative_traces(zero_children, zeta)
    zero_kummer = [f2_pow(trace, RELATIVE_DEGREE, Q) for trace in zero_traces]
    forced_zero_detected = any(f2_is_zero(value) for value in zero_kummer[1:])
    print()
    print("synthetic_zero_control")
    print(f"  children={zero_children}")
    print(f"  traces={zero_traces}")
    print(f"  kummer_powers={zero_kummer}")
    print(f"  primitive_kummer_zero_detected={int(forced_zero_detected)}")
    failures += int(not forced_zero_detected)

    print()
    print("interpretation")
    print("  cyclic_values_equal_relative_character_traces=1")
    print("  primitive_kummer_power_nonzero_certifies_trace_nonzero=1")
    print("  this_is_nonvanishing_data_not_selected_child_ordering=1")
    print("  p24_needs_f_trace_as_determinant_in_relative_resolvent_coordinates=1")
    print(f"failures={failures}")
    print("conclusion=reported_relative_kummer_nonvanishing_bridge_toy")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
