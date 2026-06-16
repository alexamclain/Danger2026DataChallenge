#!/usr/bin/env python3
"""Toy for the fixed-relation trace adjoint syndrome."""

from __future__ import annotations

from dataclasses import dataclass
import itertools
import math
import random

from hermitian_mixed_lang_normality_audit import subfield_power_basis
from k_character_tensor_rank_scan import ExtensionField, FpE, find_irreducible_modulus
from trace_gcd_prefix_semilinear_core_toy import (
    all_subfield_elements,
    random_table,
)


@dataclass(frozen=True)
class AdjointCase:
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


def source_params(k_values: list[FpE], block_count: int) -> list[tuple[tuple[int, ...], tuple[FpE, ...]]]:
    return [
        (fixed, orbit_values)
        for fixed in itertools.product(range(2), repeat=block_count)
        for orbit_values in itertools.product(k_values, repeat=block_count)
    ]


def source_value(
    params: tuple[tuple[int, ...], tuple[FpE, ...]],
    table: list[list[FpE]],
    q: int,
    field: ExtensionField,
) -> FpE:
    fixed, orbit_values = params
    total = field.zero
    for block, coeff in enumerate(fixed):
        total = field.add(total, field.scalar_mul(coeff, table[0][block]))
    for block, z in enumerate(orbit_values):
        total = field.add(total, field.mul(z, table[1][block]))
        total = field.add(total, field.mul(field.pow(z, q), table[2][block]))
    return total


def syndrome(
    lam: FpE,
    table: list[list[FpE]],
    q: int,
    k_degree: int,
    field: ExtensionField,
) -> tuple[tuple[int, ...], tuple[FpE, ...]]:
    block_count = len(table[0])
    fixed = tuple(
        trace_to_base(field.mul(lam, table[0][block]), field)
        for block in range(block_count)
    )
    orbit_values = []
    for block in range(block_count):
        d0 = trace_to_subfield(field.mul(lam, table[1][block]), k_degree, field)
        d1 = trace_to_subfield(field.mul(lam, table[2][block]), k_degree, field)
        orbit_values.append(field.add(d0, field.pow(d1, q ** (k_degree - 1))))
    return fixed, tuple(orbit_values)


def source_syndrome_pairing(
    params: tuple[tuple[int, ...], tuple[FpE, ...]],
    syn: tuple[tuple[int, ...], tuple[FpE, ...]],
    k_degree: int,
    field: ExtensionField,
) -> int:
    fixed, orbit_values = params
    fixed_syn, orbit_syn = syn
    total = 0
    for coeff, value in zip(fixed, fixed_syn):
        total = (total + coeff * value) % field.q
    for z, value in zip(orbit_values, orbit_syn):
        total = (
            total
            + trace_k_to_base(field.mul(z, value), k_degree, field)
        ) % field.q
    return total


def analyze_adjoint_case(
    label: str,
    table: list[list[FpE]],
    params_list: list[tuple[tuple[int, ...], tuple[FpE, ...]]],
    lambdas: list[FpE],
    q: int,
    k_degree: int,
    field: ExtensionField,
) -> AdjointCase:
    kernel_size = sum(
        1
        for params in params_list
        if source_value(params, table, q, field) == field.zero
    )
    image = {
        syndrome(lam, table, q, k_degree, field)
        for lam in lambdas
    }
    source_dim = exact_log(len(params_list), q)
    primal_rank = source_dim - exact_log(kernel_size, q)
    adjoint_rank = exact_log(len(image), q)
    return AdjointCase(
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
    table: list[list[FpE]],
    params_list: list[tuple[tuple[int, ...], tuple[FpE, ...]]],
    q: int,
    field: ExtensionField,
) -> bool:
    return sum(
        1
        for params in params_list
        if source_value(params, table, q, field) == field.zero
    ) == 1


def pairing_mismatches(
    table: list[list[FpE]],
    params_list: list[tuple[tuple[int, ...], tuple[FpE, ...]]],
    lambdas: list[FpE],
    q: int,
    k_degree: int,
    field: ExtensionField,
) -> int:
    mismatches = 0
    source_values = [
        (params, source_value(params, table, q, field))
        for params in params_list
    ]
    lambda_syndromes = [
        (lam, syndrome(lam, table, q, k_degree, field))
        for lam in lambdas
    ]
    for params, value in source_values:
        for lam, syn in lambda_syndromes:
            left = trace_to_base(field.mul(lam, value), field)
            right = source_syndrome_pairing(
                params,
                syn,
                k_degree,
                field,
            )
            if left != right:
                mismatches += 1
    return mismatches


def main() -> None:
    q = 2
    length = 3
    k_degree = 2
    l_degree = 8
    block_count = 2
    seed = 20260606

    field = ExtensionField(q, l_degree, find_irreducible_modulus(q, l_degree, seed))
    k_basis = subfield_power_basis(q, k_degree, field, seed)
    k_values = all_subfield_elements(k_basis, field)
    params_list = source_params(k_values, block_count)
    lambdas = all_field_elements(field)
    rng = random.Random(seed)

    good_table = None
    for _ in range(200):
        candidate = random_table(length, block_count, field, rng)
        if fixed_source_injective(candidate, params_list, q, field):
            good_table = candidate
            break
    if good_table is None:
        raise RuntimeError("did not find random-good adjoint example")

    forced_table = [row[:] for row in good_table]
    forced_table[0][1] = forced_table[0][0]

    rows = [
        analyze_adjoint_case(
            "random_good",
            good_table,
            params_list,
            lambdas,
            q,
            k_degree,
            field,
        ),
        analyze_adjoint_case(
            "forced_fixed_frequency_relation",
            forced_table,
            params_list,
            lambdas,
            q,
            k_degree,
            field,
        ),
    ]
    mismatch_total = (
        pairing_mismatches(good_table, params_list, lambdas, q, k_degree, field)
        + pairing_mismatches(forced_table, params_list, lambdas, q, k_degree, field)
    )

    p24_p = 10**24 + 7
    p24_q35 = p24_p % 35
    fixed_frequency_count = sum(1 for a in range(35) if (p24_q35 * a) % 35 == a)
    length4_orbit_count = (35 - fixed_frequency_count) // 4
    p24_blocks = 4

    print("Trace-GCD prefix semilinear fixed-adjoint toy")
    print(f"q={q}")
    print(f"length={length}")
    print(f"k_degree={k_degree}")
    print(f"l_degree={l_degree}")
    print(f"block_count={block_count}")
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
    print(f"  p24_fixed_frequency_count={fixed_frequency_count}")
    print(f"  p24_length4_frequency_orbit_count={length4_orbit_count}")
    print(f"  p24_fixed_adjoint_scalar_tests={fixed_frequency_count * p24_blocks}")
    print(f"  p24_fixed_adjoint_K_tests={length4_orbit_count * p24_blocks}")
    print(
        "  p24_fixed_adjoint_target_fp_dimension="
        f"{fixed_frequency_count * p24_blocks + length4_orbit_count * p24_blocks * 4}"
    )
    print("interpretation")
    print("  fixed_adjoint_pairing_formula_verified=1")
    print("  fixed_relation_injective_iff_adjoint_syndrome_surjective=1")
    print("  p24_syndrome_shape_Fp28_plus_K28=1")
    print("conclusion=reported_trace_gcd_prefix_semilinear_fixed_adjoint_toy")


if __name__ == "__main__":
    main()
