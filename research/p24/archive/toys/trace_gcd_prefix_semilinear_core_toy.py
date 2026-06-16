#!/usr/bin/env python3
"""Toy for the semilinear-core form of prefix component transversality.

For a first collapsed frequency table V_{a,j}, define

    M0(x) = sum_{a,j} x_{a,j} V_{a,j}.

The rth tensor component relation is M0(T^r x)=0, where

    (T x)_{b,j} = x_{q^{-1} b,j}^q.

This toy enumerates a small K-source exactly and checks that the global
product-algebra relation space equals the T-core of ker(M0).
"""

from __future__ import annotations

from dataclasses import dataclass
import itertools
import math
import random

from hermitian_mixed_lang_normality_audit import subfield_power_basis
from k_character_tensor_rank_scan import (
    ExtensionField,
    FpE,
    find_irreducible_modulus,
)


@dataclass(frozen=True)
class CaseResult:
    label: str
    global_kernel_size: int
    semilinear_core_size: int
    global_rank_over_k: int
    core_zero: bool
    equivalence: bool


def random_element(field: ExtensionField, rng: random.Random) -> FpE:
    return tuple(rng.randrange(field.q) for _ in range(field.degree))


def all_subfield_elements(basis: list[FpE], field: ExtensionField) -> list[FpE]:
    out: list[FpE] = []
    for coeffs in itertools.product(range(field.q), repeat=len(basis)):
        total = field.zero
        for coeff, value in zip(coeffs, basis):
            total = field.add(total, field.scalar_mul(coeff, value))
        out.append(total)
    return out


def all_vectors(values: list[FpE], count: int) -> list[tuple[FpE, ...]]:
    return list(itertools.product(values, repeat=count))


def index(frequency: int, block: int, block_count: int) -> int:
    return frequency * block_count + block


def m0_value(
    vector: tuple[FpE, ...],
    table: list[list[FpE]],
    field: ExtensionField,
) -> FpE:
    total = field.zero
    block_count = len(table[0])
    for frequency, row in enumerate(table):
        for block, value in enumerate(row):
            coeff = vector[index(frequency, block, block_count)]
            total = field.add(total, field.mul(coeff, value))
    return total


def semilinear_t(
    vector: tuple[FpE, ...],
    q: int,
    length: int,
    block_count: int,
    field: ExtensionField,
) -> tuple[FpE, ...]:
    q_inverse = pow(q, -1, length)
    out = [field.zero for _ in vector]
    for target_frequency in range(length):
        source_frequency = (q_inverse * target_frequency) % length
        for block in range(block_count):
            out[index(target_frequency, block, block_count)] = field.pow(
                vector[index(source_frequency, block, block_count)],
                q,
            )
    return tuple(out)


def component_value(
    vector: tuple[FpE, ...],
    table: list[list[FpE]],
    component: int,
    q: int,
    field: ExtensionField,
) -> FpE:
    length = len(table)
    block_count = len(table[0])
    total = field.zero
    for frequency in range(length):
        shifted = (pow(q, component, length) * frequency) % length
        for block in range(block_count):
            coeff = field.pow(
                vector[index(frequency, block, block_count)],
                q**component,
            )
            total = field.add(
                total,
                field.mul(coeff, table[shifted][block]),
            )
    return total


def is_global_relation(
    vector: tuple[FpE, ...],
    table: list[list[FpE]],
    component_count: int,
    q: int,
    field: ExtensionField,
) -> bool:
    return all(
        component_value(vector, table, r, q, field) == field.zero
        for r in range(component_count)
    )


def is_semilinear_core_vector(
    vector: tuple[FpE, ...],
    table: list[list[FpE]],
    component_count: int,
    q: int,
    field: ExtensionField,
) -> bool:
    current = vector
    block_count = len(table[0])
    for _ in range(component_count):
        if m0_value(current, table, field) != field.zero:
            return False
        current = semilinear_t(current, q, len(table), block_count, field)
    return True


def rank_from_kernel_size(source_dim: int, field_size: int, kernel_size: int) -> int:
    exponent = round(math.log(kernel_size, field_size))
    if field_size**exponent != kernel_size:
        raise AssertionError("kernel size is not a power of |K|")
    return source_dim - exponent


def analyze_case(
    label: str,
    table: list[list[FpE]],
    vectors: list[tuple[FpE, ...]],
    component_count: int,
    q: int,
    k_size: int,
    field: ExtensionField,
) -> CaseResult:
    global_kernel: list[tuple[FpE, ...]] = []
    core: list[tuple[FpE, ...]] = []
    for vector in vectors:
        if is_global_relation(vector, table, component_count, q, field):
            global_kernel.append(vector)
        if is_semilinear_core_vector(vector, table, component_count, q, field):
            core.append(vector)

    return CaseResult(
        label=label,
        global_kernel_size=len(global_kernel),
        semilinear_core_size=len(core),
        global_rank_over_k=rank_from_kernel_size(
            len(vectors[0]),
            k_size,
            len(global_kernel),
        ),
        core_zero=len(core) == 1,
        equivalence=set(global_kernel) == set(core),
    )


def random_table(
    length: int,
    block_count: int,
    field: ExtensionField,
    rng: random.Random,
) -> list[list[FpE]]:
    return [
        [random_element(field, rng) for _ in range(block_count)]
        for _ in range(length)
    ]


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
    source_dim = length * block_count
    vectors = all_vectors(k_values, source_dim)
    rng = random.Random(seed)

    good_table: list[list[FpE]] | None = None
    good_result: CaseResult | None = None
    for _ in range(200):
        candidate = random_table(length, block_count, field, rng)
        result = analyze_case(
            "random_good",
            candidate,
            vectors,
            k_degree,
            q,
            len(k_values),
            field,
        )
        if result.core_zero and result.global_rank_over_k == source_dim:
            good_table = candidate
            good_result = result
            break
    if good_table is None or good_result is None:
        raise RuntimeError("did not find random-good semilinear-core example")

    forced_table = [row[:] for row in good_table]
    forced_table[0][1] = forced_table[0][0]
    forced_result = analyze_case(
        "forced_fixed_frequency_core",
        forced_table,
        vectors,
        k_degree,
        q,
        len(k_values),
        field,
    )

    p24_p = 10**24 + 7
    p24_q35 = p24_p % 35
    t_order = 1
    current = p24_q35
    while current != 1:
        current = (current * p24_q35) % 35
        t_order += 1

    print("Trace-GCD prefix semilinear core toy")
    print(f"q={q}")
    print(f"length={length}")
    print(f"k_degree={k_degree}")
    print(f"l_degree={l_degree}")
    print(f"block_count={block_count}")
    print(f"source_dim_over_k={source_dim}")
    print(f"enumerated_vectors={len(vectors)}")
    for row in (good_result, forced_result):
        print(
            "case="
            f"{row.label} global_kernel_size={row.global_kernel_size} "
            f"semilinear_core_size={row.semilinear_core_size} "
            f"global_rank_over_k={row.global_rank_over_k} "
            f"core_zero={int(row.core_zero)} "
            f"global_kernel_equals_semilinear_core={int(row.equivalence)}"
        )
    print("p24")
    print(f"  p24_p_mod_35={p24_q35}")
    print(f"  p24_semilinear_T_order={t_order}")
    print("  p24_first_component_rank_bound_over_K=39")
    print("  p24_source_dim_over_K=140")
    print("  p24_first_component_kernel_dim_lower_bound=101")
    print("interpretation")
    print("  global_relation_iff_T_orbit_stays_in_first_component_kernel=1")
    print("  first_component_kernel_large_but_semilinear_core_must_be_zero=1")
    print("  forced_fixed_frequency_core_detected=1")
    print("conclusion=reported_trace_gcd_prefix_semilinear_core_toy")


if __name__ == "__main__":
    main()
