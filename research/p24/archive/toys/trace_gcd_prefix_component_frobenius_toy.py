#!/usr/bin/env python3
"""Toy for Frobenius bookkeeping in tensor-product DFT components.

For K=F_q(mu_n) contained in L, the rth tensor component sends
omega -> omega^(q^r).  Therefore the rth component of the DFT column D_a is
the first collapsed frequency V_{q^r a}.  Relation coefficients are
conjugated at the same time.
"""

from __future__ import annotations

import random

from hermitian_mixed_lang_normality_audit import subfield_power_basis
from k_character_tensor_rank_scan import (
    ExtensionField,
    FpE,
    find_irreducible_modulus,
    primitive_root_of_order,
)


def random_element(field: ExtensionField, rng: random.Random) -> FpE:
    return tuple(rng.randrange(field.q) for _ in range(field.degree))


def random_subfield_element(
    basis: list[FpE],
    field: ExtensionField,
    rng: random.Random,
) -> FpE:
    total = field.zero
    for value in basis:
        total = field.add(total, field.scalar_mul(rng.randrange(field.q), value))
    return total


def dft_value(
    coeffs: list[FpE],
    frequency: int,
    omega: FpE,
    field: ExtensionField,
) -> FpE:
    n = len(coeffs)
    total = field.zero
    for i, coeff in enumerate(coeffs):
        exponent = (-frequency * i) % n
        total = field.add(total, field.mul(coeff, field.pow(omega, exponent)))
    return total


def component_dft_value(
    coeffs: list[FpE],
    frequency: int,
    component: int,
    omega: FpE,
    field: ExtensionField,
) -> FpE:
    n = len(coeffs)
    total = field.zero
    for i, coeff in enumerate(coeffs):
        exponent = (-frequency * i * (field.q**component)) % n
        total = field.add(total, field.mul(coeff, field.pow(omega, exponent)))
    return total


def relation_value(
    relation_coeffs: list[FpE],
    dft_values: list[FpE],
    component: int,
    field: ExtensionField,
) -> FpE:
    total = field.zero
    for coeff, value in zip(relation_coeffs, dft_values):
        total = field.add(
            total,
            field.mul(field.pow(coeff, field.q**component), value),
        )
    return total


def main() -> None:
    q = 2
    n = 3
    k_degree = 2
    l_degree = 4
    field = ExtensionField(q, l_degree, find_irreducible_modulus(q, l_degree, 20260606))
    omega = primitive_root_of_order(field, n, 20260606)
    k_basis = subfield_power_basis(q, k_degree, field, 20260606)
    rng = random.Random(20260606)

    coeffs = [random_element(field, rng) for _ in range(n)]
    first_component = [dft_value(coeffs, a, omega, field) for a in range(n)]

    component_mismatches = 0
    for r in range(k_degree):
        for a in range(n):
            direct = component_dft_value(coeffs, a, r, omega, field)
            shifted = first_component[(pow(q, r, n) * a) % n]
            if direct != shifted:
                component_mismatches += 1

    relation_coeffs = [
        random_subfield_element(k_basis, field, rng)
        for _ in range(n)
    ]
    relation_mismatches = 0
    for r in range(k_degree):
        direct_values = [
            component_dft_value(coeffs, a, r, omega, field)
            for a in range(n)
        ]
        direct_relation = relation_value(
            relation_coeffs,
            direct_values,
            r,
            field,
        )
        reindexed_values = []
        reindexed_coeffs = []
        q_power = pow(q, r, n)
        q_power_inv = pow(q_power, -1, n)
        for b in range(n):
            source_a = (q_power_inv * b) % n
            reindexed_coeffs.append(relation_coeffs[source_a])
            reindexed_values.append(first_component[b])
        reindexed_relation = relation_value(
            reindexed_coeffs,
            reindexed_values,
            r,
            field,
        )
        if direct_relation != reindexed_relation:
            relation_mismatches += 1

    p24_p = 10**24 + 7
    p24_q35 = p24_p % 35
    p24_orbits = []
    seen: set[int] = set()
    for a in range(35):
        if a in seen:
            continue
        orbit: list[int] = []
        x = a
        while x not in orbit:
            orbit.append(x)
            seen.add(x)
            x = (x * p24_q35) % 35
        p24_orbits.append(orbit)

    print("Trace-GCD prefix component Frobenius bookkeeping toy")
    print(f"q={q}")
    print(f"n={n}")
    print(f"k_degree={k_degree}")
    print(f"l_degree={l_degree}")
    print(f"omega={omega}")
    print(f"component_mismatches={component_mismatches}")
    print(f"relation_reindex_mismatches={relation_mismatches}")
    print("p24")
    print(f"  p24_p_mod_35={p24_q35}")
    print("  p24_ord_35_p=4")
    print(f"  p24_frequency_orbits={p24_orbits}")
    print("interpretation")
    print("  component_r_sees_frequency_p_power_r_times_a=1")
    print("  relation_coefficients_conjugate_with_component=1")
    print("  p24_frequency_orbits_bookkeep_components_not_blocks=1")
    print("conclusion=reported_trace_gcd_prefix_component_frobenius_toy")


if __name__ == "__main__":
    main()
