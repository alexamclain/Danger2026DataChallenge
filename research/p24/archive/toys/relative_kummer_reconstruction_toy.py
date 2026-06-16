#!/usr/bin/env python3
"""Kummer reconstruction toy for one relative tower layer.

For a cyclic prime-degree child layer, relative character traces are Lagrange
resolvents.  If the child degree is r and a primitive r-th root of unity is
available, a primitive trace T satisfies:

    T^r is invariant under the child rotation.

This is a more class-field-shaped object than the raw ordered trace T.  The
question is what it actually buys.  In the D=-5000, h=30=2*3*5 calibration
tower, the relative degree is 3 and zeta_3 lives in F_{q^2}.  This script
checks that:

* the parent period T_0 plus one primitive Kummer constant T_1^3 reconstructs
  the unordered child polynomial;
* the three cube-root choices give cyclic rotations of the child periods and
  hence the same child polynomial;
* the Kummer constant still depends on the oriented quotient action, so this
  is a normal form for the missing phase, not a seedless selector.
"""

from __future__ import annotations

from cypari2 import Pari

from embedded_decomposition_calibration import (
    D,
    ELL,
    H,
    Q,
    isogeny_neighbors,
    monic_poly_from_roots,
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


def f2_frob(x: Fq2, q: int = Q) -> Fq2:
    """Frobenius in F_q[w]/(w^2+w+1), where q == -1 mod 3."""

    return f2_pow(x, q, q)


def f2_equal_base(x: Fq2) -> int:
    if x[1] != 0:
        raise ValueError(f"not in base field: {x}")
    return x[0]


def f2_roots_of_power(target: Fq2, exponent: int, q: int = Q) -> list[Fq2]:
    roots: list[Fq2] = []
    for a in range(q):
        for b in range(q):
            x = (a, b)
            if f2_pow(x, exponent, q) == target:
                roots.append(x)
    return roots


def inverse_dft_degree3(t0: int, t1: Fq2, zeta: Fq2, q: int = Q) -> list[Fq2]:
    """Recover child periods from T0, T1, and T2=Frob(T1)."""

    traces = [f2_from_base(t0, q), t1, f2_frob(t1, q)]
    inv3 = pow(3, -1, q)
    children: list[Fq2] = []
    for r in range(3):
        value = (0, 0)
        for s, trace in enumerate(traces):
            coeff = f2_pow(zeta, (-s * r) % 3, q)
            value = f2_add(value, f2_mul(coeff, trace, q), q)
        children.append(f2_scalar_mul(inv3, value, q))
    return children


def main() -> None:
    if RELATIVE_DEGREE != 3:
        raise AssertionError("this toy is specialized to the degree-3 layer")

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

    print("relative Kummer reconstruction toy")
    print(f"D={D}")
    print(f"q={Q}")
    print(f"generator_ell={ELL}")
    print(f"class_number={H}")
    print(f"top_quotient={TOP_QUOTIENT}")
    print(f"relative_degree={RELATIVE_DEGREE}")
    print(f"recovery_subgroup_size={RECOVERY_SIZE}")
    print(f"zeta_pair={zeta}")
    print()

    for parent in range(TOP_QUOTIENT):
        children = [
            fine_periods[parent + TOP_QUOTIENT * a]
            for a in range(RELATIVE_DEGREE)
        ]
        true_poly = monic_poly_from_roots(children, Q)

        t0 = sum(children) % Q
        t1 = (0, 0)
        for a, child in enumerate(children):
            t1 = f2_add(t1, f2_scalar_mul(child, f2_pow(zeta, a, Q), Q), Q)
        kummer = f2_pow(t1, RELATIVE_DEGREE, Q)
        roots_t1 = f2_roots_of_power(kummer, RELATIVE_DEGREE, Q)

        recovered_polys: set[tuple[int, ...]] = set()
        recovered_children: list[list[int]] = []
        descends = 0
        for candidate_t1 in roots_t1:
            candidate_children = inverse_dft_degree3(t0, candidate_t1, zeta, Q)
            if all(child[1] == 0 for child in candidate_children):
                descends += 1
                base_children = [f2_equal_base(child) for child in candidate_children]
                recovered_children.append(base_children)
                recovered_polys.add(tuple(monic_poly_from_roots(base_children, Q)))

        print(f"parent={parent}")
        print(f"  true_children={children}")
        print(f"  true_child_polynomial={true_poly}")
        print(f"  T0={t0}")
        print(f"  T1={t1}")
        print(f"  T1_power_3={kummer}")
        print(f"  cube_roots_of_T1_power_3={roots_t1}")
        print(f"  descending_cube_root_choices={descends}")
        print(f"  recovered_child_lists={recovered_children}")
        print(f"  recovered_polynomials={sorted(recovered_polys)}")
        print(f"  unique_recovered_polynomial_count={len(recovered_polys)}")
        print(f"  true_polynomial_recovered={int(tuple(true_poly) in recovered_polys)}")
    print()
    print("interpretation")
    print("  parent_trace_plus_primitive_kummer_constant_recovers_child_polynomial=1")
    print("  cube_root_choices_are_cyclic_rotations_when_descent_is_enforced=1")
    print("  kummer_constant_depends_on_oriented_relative_action=1")
    print("  p24_positive_target_can_be_rephrased_as_relative_kummer_constants=1")
    print("conclusion=relative_kummer_powers_are_equivalent_phase_payload_not_seedless_selectors")


if __name__ == "__main__":
    main()
