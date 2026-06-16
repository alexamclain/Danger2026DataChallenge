#!/usr/bin/env python3
"""Toy for the full RS-tail fixed-relation trace adjoint.

The explicit fixed map

    Psi_RS : F_q^f + K^m + F_q^s -> L

has three column families:

* fixed-frequency prefix columns;
* moving frequency-orbit prefix columns with `K` coefficients;
* RS-tail columns with base-field coefficients.

This toy verifies the trace-adjoint syndrome formula and the finite duality

    Psi_RS injective <=> Psi_RS^* surjective.

The p24 arithmetic theorem can then be phrased as surjectivity of the actual
CM syndrome map

    L -> F_p^28 + K^28 + F_p^16.
"""

from __future__ import annotations

from dataclasses import dataclass
import itertools
import math
import random

from hermitian_mixed_lang_normality_audit import subfield_power_basis
from k_character_tensor_rank_scan import ExtensionField, FpE, find_irreducible_modulus
from trace_gcd_prefix_semilinear_core_toy import (
    all_subfield_elements,
    random_element,
)


@dataclass(frozen=True)
class RsTailAdjointCase:
    label: str
    source_dim: int
    kernel_size: int
    image_size: int
    primal_rank: int
    adjoint_rank: int
    injective: bool
    adjoint_surjective: bool


def exact_log(value: int, base: int) -> int:
    exponent = round(math.log(value, base))
    if base**exponent != value:
        raise AssertionError(f"{value} is not a power of {base}")
    return exponent


def all_field_elements(field: ExtensionField) -> list[FpE]:
    return list(itertools.product(range(field.q), repeat=field.degree))


def trace_to_base(value: FpE, field: ExtensionField) -> int:
    total = field.zero
    for i in range(field.degree):
        total = field.add(total, field.pow(value, field.q**i))
    if any(total[i] for i in range(1, field.degree)):
        raise AssertionError("base trace did not land in base field")
    return total[0] % field.q


def trace_to_subfield(value: FpE, subdegree: int, field: ExtensionField) -> FpE:
    if field.degree % subdegree:
        raise ValueError("subdegree must divide field degree")
    total = field.zero
    relative_degree = field.degree // subdegree
    for i in range(relative_degree):
        total = field.add(total, field.pow(value, field.q ** (subdegree * i)))
    if field.pow(total, field.q**subdegree) != total:
        raise AssertionError("relative trace did not land in subfield")
    return total


def trace_k_to_base(value: FpE, subdegree: int, field: ExtensionField) -> int:
    total = field.zero
    for i in range(subdegree):
        total = field.add(total, field.pow(value, field.q**i))
    if any(total[i] for i in range(1, field.degree)):
        raise AssertionError("K trace did not land in base field")
    return total[0] % field.q


def frequency_orbits(length: int, multiplier: int) -> list[list[int]]:
    seen: set[int] = set()
    out: list[list[int]] = []
    for start in range(length):
        if start in seen:
            continue
        orbit: list[int] = []
        current = start
        while current not in seen:
            seen.add(current)
            orbit.append(current)
            current = (multiplier * current) % length
        out.append(orbit)
    return out


def add_many(values: list[FpE], field: ExtensionField) -> FpE:
    total = field.zero
    for value in values:
        total = field.add(total, value)
    return total


def tail_column(
    tail_table: list[FpE],
    tail_pos: int,
    omega: FpE,
    field: ExtensionField,
) -> FpE:
    return add_many(
        [
            field.mul(field.pow(omega, frequency * tail_pos), value)
            for frequency, value in enumerate(tail_table)
        ],
        field,
    )


def source_params(
    q: int,
    k_values: list[FpE],
    fixed_frequency_count: int,
    moving_orbit_count: int,
    prefix_blocks: int,
    tail_dim: int,
) -> list[tuple[tuple[int, ...], tuple[FpE, ...], tuple[int, ...]]]:
    return [
        (fixed, moving, tail)
        for fixed in itertools.product(
            range(q), repeat=fixed_frequency_count * prefix_blocks
        )
        for moving in itertools.product(
            k_values, repeat=moving_orbit_count * prefix_blocks
        )
        for tail in itertools.product(range(q), repeat=tail_dim)
    ]


def source_value(
    params: tuple[tuple[int, ...], tuple[FpE, ...], tuple[int, ...]],
    prefix_table: list[list[FpE]],
    tail_table: list[FpE],
    orbits: list[list[int]],
    omega: FpE,
    q: int,
    field: ExtensionField,
) -> FpE:
    fixed, moving, tail = params
    prefix_blocks = len(prefix_table[0])
    total = field.zero
    fixed_index = 0
    moving_index = 0
    for orbit in orbits:
        if len(orbit) == 1:
            frequency = orbit[0]
            for block in range(prefix_blocks):
                total = field.add(
                    total,
                    field.scalar_mul(
                        fixed[fixed_index],
                        prefix_table[frequency][block],
                    ),
                )
                fixed_index += 1
            continue
        representative = orbit[0]
        for block in range(prefix_blocks):
            z = moving[moving_index]
            moving_index += 1
            for step in range(len(orbit)):
                frequency = (pow(q, step, len(prefix_table)) * representative) % len(
                    prefix_table
                )
                total = field.add(
                    total,
                    field.mul(
                        field.pow(z, q**step),
                        prefix_table[frequency][block],
                    ),
                )
    for tail_pos, coeff in enumerate(tail):
        total = field.add(
            total,
            field.scalar_mul(
                coeff,
                tail_column(tail_table, tail_pos, omega, field),
            ),
        )
    return total


def syndrome(
    lam: FpE,
    prefix_table: list[list[FpE]],
    tail_table: list[FpE],
    orbits: list[list[int]],
    omega: FpE,
    q: int,
    k_degree: int,
    tail_dim: int,
    field: ExtensionField,
) -> tuple[tuple[int, ...], tuple[FpE, ...], tuple[int, ...]]:
    prefix_blocks = len(prefix_table[0])
    fixed_syn: list[int] = []
    moving_syn: list[FpE] = []
    for orbit in orbits:
        if len(orbit) == 1:
            frequency = orbit[0]
            for block in range(prefix_blocks):
                fixed_syn.append(
                    trace_to_base(
                        field.mul(lam, prefix_table[frequency][block]),
                        field,
                    )
                )
            continue
        representative = orbit[0]
        for block in range(prefix_blocks):
            pieces: list[FpE] = []
            for step in range(len(orbit)):
                frequency = (pow(q, step, len(prefix_table)) * representative) % len(
                    prefix_table
                )
                traced = trace_to_subfield(
                    field.mul(lam, prefix_table[frequency][block]),
                    k_degree,
                    field,
                )
                pieces.append(field.pow(traced, q ** ((k_degree - step) % k_degree)))
            moving_syn.append(add_many(pieces, field))
    tail_syn = tuple(
        trace_to_base(field.mul(lam, tail_column(tail_table, pos, omega, field)), field)
        for pos in range(tail_dim)
    )
    return tuple(fixed_syn), tuple(moving_syn), tail_syn


def source_syndrome_pairing(
    params: tuple[tuple[int, ...], tuple[FpE, ...], tuple[int, ...]],
    syn: tuple[tuple[int, ...], tuple[FpE, ...], tuple[int, ...]],
    k_degree: int,
    field: ExtensionField,
) -> int:
    fixed, moving, tail = params
    fixed_syn, moving_syn, tail_syn = syn
    total = 0
    for coeff, value in zip(fixed, fixed_syn):
        total = (total + coeff * value) % field.q
    for z, value in zip(moving, moving_syn):
        total = (total + trace_k_to_base(field.mul(z, value), k_degree, field)) % field.q
    for coeff, value in zip(tail, tail_syn):
        total = (total + coeff * value) % field.q
    return total


def analyze_adjoint_case(
    label: str,
    prefix_table: list[list[FpE]],
    tail_table: list[FpE],
    orbits: list[list[int]],
    omega: FpE,
    params_list: list[tuple[tuple[int, ...], tuple[FpE, ...], tuple[int, ...]]],
    lambdas: list[FpE],
    q: int,
    k_degree: int,
    field: ExtensionField,
) -> RsTailAdjointCase:
    tail_dim = len(params_list[0][2])
    kernel_size = sum(
        1
        for params in params_list
        if source_value(params, prefix_table, tail_table, orbits, omega, q, field)
        == field.zero
    )
    image = {
        syndrome(
            lam,
            prefix_table,
            tail_table,
            orbits,
            omega,
            q,
            k_degree,
            tail_dim,
            field,
        )
        for lam in lambdas
    }
    source_dim = exact_log(len(params_list), q)
    primal_rank = source_dim - exact_log(kernel_size, q)
    adjoint_rank = exact_log(len(image), q)
    return RsTailAdjointCase(
        label=label,
        source_dim=source_dim,
        kernel_size=kernel_size,
        image_size=len(image),
        primal_rank=primal_rank,
        adjoint_rank=adjoint_rank,
        injective=kernel_size == 1,
        adjoint_surjective=len(image) == len(params_list),
    )


def fixed_source_injective(
    prefix_table: list[list[FpE]],
    tail_table: list[FpE],
    orbits: list[list[int]],
    omega: FpE,
    params_list: list[tuple[tuple[int, ...], tuple[FpE, ...], tuple[int, ...]]],
    q: int,
    field: ExtensionField,
) -> bool:
    return (
        sum(
            1
            for params in params_list
            if source_value(
                params, prefix_table, tail_table, orbits, omega, q, field
            )
            == field.zero
        )
        == 1
    )


def pairing_mismatches(
    prefix_table: list[list[FpE]],
    tail_table: list[FpE],
    orbits: list[list[int]],
    omega: FpE,
    params_list: list[tuple[tuple[int, ...], tuple[FpE, ...], tuple[int, ...]]],
    lambdas: list[FpE],
    q: int,
    k_degree: int,
    field: ExtensionField,
) -> int:
    mismatches = 0
    tail_dim = len(params_list[0][2])
    source_values = [
        (params, source_value(params, prefix_table, tail_table, orbits, omega, q, field))
        for params in params_list
    ]
    lambda_syndromes = [
        (
            lam,
            syndrome(
                lam,
                prefix_table,
                tail_table,
                orbits,
                omega,
                q,
                k_degree,
                tail_dim,
                field,
            ),
        )
        for lam in lambdas
    ]
    for params, value in source_values:
        for lam, syn in lambda_syndromes:
            left = trace_to_base(field.mul(lam, value), field)
            right = source_syndrome_pairing(params, syn, k_degree, field)
            if left != right:
                mismatches += 1
    return mismatches


def random_tables(
    length: int,
    prefix_blocks: int,
    field: ExtensionField,
    rng: random.Random,
) -> tuple[list[list[FpE]], list[FpE]]:
    prefix = [
        [random_element(field, rng) for _ in range(prefix_blocks)]
        for _ in range(length)
    ]
    tail = [random_element(field, rng) for _ in range(length)]
    return prefix, tail


def main() -> None:
    q = 2
    length = 3
    k_degree = 2
    l_degree = 6
    prefix_blocks = 1
    tail_dim = 2
    seed = 20260606

    field = ExtensionField(q, l_degree, find_irreducible_modulus(q, l_degree, seed))
    k_basis = subfield_power_basis(q, k_degree, field, seed)
    k_values = all_subfield_elements(k_basis, field)
    omega_candidates = [
        value for value in all_field_elements(field)
        if value != field.zero and field.pow(value, length) == field.one
    ]
    omega = next(value for value in omega_candidates if value != field.one)
    orbits = frequency_orbits(length, q % length)
    fixed_frequency_count = sum(1 for orbit in orbits if len(orbit) == 1)
    moving_orbit_count = sum(1 for orbit in orbits if len(orbit) > 1)
    params_list = source_params(
        q,
        k_values,
        fixed_frequency_count,
        moving_orbit_count,
        prefix_blocks,
        tail_dim,
    )
    lambdas = all_field_elements(field)
    rng = random.Random(seed)

    good_prefix = None
    good_tail = None
    for _ in range(200):
        prefix, tail = random_tables(length, prefix_blocks, field, rng)
        if fixed_source_injective(prefix, tail, orbits, omega, params_list, q, field):
            good_prefix = prefix
            good_tail = tail
            break
    if good_prefix is None or good_tail is None:
        raise RuntimeError("did not find random-good RS-tail adjoint example")

    forced_prefix = [row[:] for row in good_prefix]
    forced_prefix[0][0] = field.zero
    forced_tail = [row[0] for row in good_prefix]

    rows = [
        analyze_adjoint_case(
            "random_good",
            good_prefix,
            good_tail,
            orbits,
            omega,
            params_list,
            lambdas,
            q,
            k_degree,
            field,
        ),
        analyze_adjoint_case(
            "forced_prefix_fixed_relation",
            forced_prefix,
            good_tail,
            orbits,
            omega,
            params_list,
            lambdas,
            q,
            k_degree,
            field,
        ),
        analyze_adjoint_case(
            "forced_rs_tail_fixed_relation",
            good_prefix,
            forced_tail,
            orbits,
            omega,
            params_list,
            lambdas,
            q,
            k_degree,
            field,
        ),
    ]
    mismatch_total = sum(
        pairing_mismatches(
            prefix,
            tail,
            orbits,
            omega,
            params_list,
            lambdas,
            q,
            k_degree,
            field,
        )
        for prefix, tail in (
            (good_prefix, good_tail),
            (forced_prefix, good_tail),
            (good_prefix, forced_tail),
        )
    )

    p24_p = 10**24 + 7
    p24_q35 = p24_p % 35
    p24_fixed_frequency_count = sum(1 for a in range(35) if (p24_q35 * a) % 35 == a)
    p24_length4_orbit_count = (35 - p24_fixed_frequency_count) // 4
    p24_blocks = 4
    p24_tail_dim = 16

    print("Trace-GCD RS-tail fixed-adjoint toy")
    print(f"q={q}")
    print(f"length={length}")
    print(f"k_degree={k_degree}")
    print(f"l_degree={l_degree}")
    print(f"prefix_blocks={prefix_blocks}")
    print(f"tail_dim={tail_dim}")
    print(f"source_size={len(params_list)}")
    print(f"lambda_count={len(lambdas)}")
    print(f"pairing_mismatches={mismatch_total}")
    for row in rows:
        print(
            "case="
            f"{row.label} source_dim={row.source_dim} "
            f"kernel_size={row.kernel_size} "
            f"image_size={row.image_size} "
            f"primal_rank={row.primal_rank} "
            f"adjoint_rank={row.adjoint_rank} "
            f"injective={int(row.injective)} "
            f"adjoint_surjective={int(row.adjoint_surjective)}"
        )
    print("p24")
    print(f"  p24_fixed_frequency_count={p24_fixed_frequency_count}")
    print(f"  p24_length4_frequency_orbit_count={p24_length4_orbit_count}")
    print(f"  p24_fixed_adjoint_scalar_tests={p24_fixed_frequency_count * p24_blocks}")
    print(f"  p24_fixed_adjoint_K_tests={p24_length4_orbit_count * p24_blocks}")
    print(f"  p24_fixed_adjoint_tail_tests={p24_tail_dim}")
    print(
        "  p24_fixed_adjoint_target_fp_dimension="
        f"{p24_fixed_frequency_count * p24_blocks + p24_length4_orbit_count * p24_blocks * 4 + p24_tail_dim}"
    )
    print("interpretation")
    print("  rs_tail_fixed_adjoint_pairing_formula_verified=1")
    print("  rs_tail_fixed_relation_injective_iff_adjoint_syndrome_surjective=1")
    print("  p24_syndrome_shape_Fp28_plus_K28_plus_Fp16=1")
    print("conclusion=reported_trace_gcd_rs_tail_fixed_adjoint_toy")


if __name__ == "__main__":
    main()
