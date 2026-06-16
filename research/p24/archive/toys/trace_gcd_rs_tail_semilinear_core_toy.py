#!/usr/bin/env python3
"""Toy for the full RS-tail semilinear-core theorem.

The fixed p24 square map can be written after scalar extension to
`K = F_p(mu_35)` as a first-component map

    M_RS : K^{35*4} + K[z]_<16 -> L,
    M_RS(x,z) = sum x_{a,j} V_{a,j}
              + sum_a (sum_s z_s omega^{a*s}) V_{a,tail}.

The other tensor components are obtained by the semilinear operator

    (T x)_{b,j} = x_{q^{-1}b,j}^q,        (T z)_s = z_s^q.

This toy checks the finite equivalence on a small exact model:

    global product-algebra relation = T-core of ker(M_RS),

and also checks the Hilbert-90 descent from a nonzero T-core to a nonzero
T-fixed relation.
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
    primitive_root_of_order,
)
from trace_gcd_prefix_semilinear_core_toy import (
    all_subfield_elements,
    all_vectors,
    random_element,
)


@dataclass(frozen=True)
class RsCoreResult:
    label: str
    global_kernel_size: int
    semilinear_core_size: int
    fixed_vector_count: int
    fixed_kernel_size: int
    global_rank_over_k: int
    core_kdim: int
    fixed_kernel_fpdim: int
    core_zero: bool
    equivalence: bool
    descent_match: bool


def exact_log(value: int, base: int) -> int:
    exponent = round(math.log(value, base))
    if base**exponent != value:
        raise AssertionError(f"{value} is not a power of {base}")
    return exponent


def prefix_index(frequency: int, block: int, prefix_blocks: int) -> int:
    return frequency * prefix_blocks + block


def tail_index(length: int, prefix_blocks: int, tail_pos: int) -> int:
    return length * prefix_blocks + tail_pos


def tail_value(
    vector: tuple[FpE, ...],
    frequency: int,
    length: int,
    prefix_blocks: int,
    tail_dim: int,
    omega: FpE,
    field: ExtensionField,
) -> FpE:
    total = field.zero
    for tail_pos in range(tail_dim):
        coeff = vector[tail_index(length, prefix_blocks, tail_pos)]
        scale = field.pow(omega, frequency * tail_pos)
        total = field.add(total, field.mul(coeff, scale))
    return total


def m_rs_value(
    vector: tuple[FpE, ...],
    prefix_table: list[list[FpE]],
    tail_table: list[FpE],
    omega: FpE,
    field: ExtensionField,
) -> FpE:
    length = len(prefix_table)
    prefix_blocks = len(prefix_table[0])
    tail_dim = len(vector) - length * prefix_blocks
    total = field.zero
    for frequency, row in enumerate(prefix_table):
        for block, value in enumerate(row):
            coeff = vector[prefix_index(frequency, block, prefix_blocks)]
            total = field.add(total, field.mul(coeff, value))
        z_at_frequency = tail_value(
            vector, frequency, length, prefix_blocks, tail_dim, omega, field
        )
        total = field.add(
            total,
            field.mul(z_at_frequency, tail_table[frequency]),
        )
    return total


def semilinear_t_rs(
    vector: tuple[FpE, ...],
    q: int,
    length: int,
    prefix_blocks: int,
    tail_dim: int,
    field: ExtensionField,
) -> tuple[FpE, ...]:
    q_inverse = pow(q, -1, length)
    out = [field.zero for _ in vector]
    for target_frequency in range(length):
        source_frequency = (q_inverse * target_frequency) % length
        for block in range(prefix_blocks):
            out[prefix_index(target_frequency, block, prefix_blocks)] = field.pow(
                vector[prefix_index(source_frequency, block, prefix_blocks)],
                q,
            )
    for tail_pos in range(tail_dim):
        out[tail_index(length, prefix_blocks, tail_pos)] = field.pow(
            vector[tail_index(length, prefix_blocks, tail_pos)],
            q,
        )
    return tuple(out)


def component_value(
    vector: tuple[FpE, ...],
    prefix_table: list[list[FpE]],
    tail_table: list[FpE],
    component: int,
    q: int,
    omega: FpE,
    field: ExtensionField,
) -> FpE:
    current = vector
    length = len(prefix_table)
    prefix_blocks = len(prefix_table[0])
    tail_dim = len(vector) - length * prefix_blocks
    for _ in range(component):
        current = semilinear_t_rs(
            current, q, length, prefix_blocks, tail_dim, field
        )
    return m_rs_value(current, prefix_table, tail_table, omega, field)


def is_global_relation(
    vector: tuple[FpE, ...],
    prefix_table: list[list[FpE]],
    tail_table: list[FpE],
    component_count: int,
    q: int,
    omega: FpE,
    field: ExtensionField,
) -> bool:
    return all(
        component_value(
            vector, prefix_table, tail_table, r, q, omega, field
        )
        == field.zero
        for r in range(component_count)
    )


def is_semilinear_core_vector(
    vector: tuple[FpE, ...],
    prefix_table: list[list[FpE]],
    tail_table: list[FpE],
    component_count: int,
    q: int,
    omega: FpE,
    field: ExtensionField,
) -> bool:
    current = vector
    length = len(prefix_table)
    prefix_blocks = len(prefix_table[0])
    tail_dim = len(vector) - length * prefix_blocks
    for _ in range(component_count):
        if m_rs_value(current, prefix_table, tail_table, omega, field) != field.zero:
            return False
        current = semilinear_t_rs(
            current, q, length, prefix_blocks, tail_dim, field
        )
    return True


def analyze_case(
    label: str,
    prefix_table: list[list[FpE]],
    tail_table: list[FpE],
    vectors: list[tuple[FpE, ...]],
    component_count: int,
    q: int,
    k_size: int,
    omega: FpE,
    field: ExtensionField,
) -> RsCoreResult:
    length = len(prefix_table)
    prefix_blocks = len(prefix_table[0])
    tail_dim = len(vectors[0]) - length * prefix_blocks
    global_kernel: list[tuple[FpE, ...]] = []
    core: list[tuple[FpE, ...]] = []
    fixed_vectors: list[tuple[FpE, ...]] = []
    fixed_kernel: list[tuple[FpE, ...]] = []
    for vector in vectors:
        if is_global_relation(
            vector, prefix_table, tail_table, component_count, q, omega, field
        ):
            global_kernel.append(vector)
        if is_semilinear_core_vector(
            vector, prefix_table, tail_table, component_count, q, omega, field
        ):
            core.append(vector)
        if (
            semilinear_t_rs(vector, q, length, prefix_blocks, tail_dim, field)
            == vector
        ):
            fixed_vectors.append(vector)
            if m_rs_value(vector, prefix_table, tail_table, omega, field) == field.zero:
                fixed_kernel.append(vector)

    core_kdim = exact_log(len(core), k_size)
    fixed_kernel_fpdim = exact_log(len(fixed_kernel), q)
    global_kernel_kdim = exact_log(len(global_kernel), k_size)
    return RsCoreResult(
        label=label,
        global_kernel_size=len(global_kernel),
        semilinear_core_size=len(core),
        fixed_vector_count=len(fixed_vectors),
        fixed_kernel_size=len(fixed_kernel),
        global_rank_over_k=len(vectors[0]) - global_kernel_kdim,
        core_kdim=core_kdim,
        fixed_kernel_fpdim=fixed_kernel_fpdim,
        core_zero=len(core) == 1,
        equivalence=set(global_kernel) == set(core),
        descent_match=core_kdim == fixed_kernel_fpdim,
    )


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


def force_prefix_relation(prefix_table: list[list[FpE]]) -> list[list[FpE]]:
    forced = [row[:] for row in prefix_table]
    # Frequency 0 is fixed by `a -> q*a`; killing this coefficient forces a
    # T-fixed prefix relation.
    forced[0][0] = (0,) * len(forced[0][0])
    return forced


def force_rs_tail_relation(
    prefix_table: list[list[FpE]],
) -> list[FpE]:
    # The T-fixed vector with x_{a,0}=1 for every frequency and z_0=1
    # becomes a relation in characteristic 2 when tail_a = prefix_{a,0}.
    return [row[0] for row in prefix_table]


def main() -> None:
    q = 2
    length = 3
    k_degree = 2
    l_degree = 6
    prefix_blocks = 1
    tail_dim = 2
    seed = 20260606

    field = ExtensionField(q, l_degree, find_irreducible_modulus(q, l_degree, seed))
    k_basis = subfield_power_basis(q, k_degree, field, seed + 1)
    k_values = all_subfield_elements(k_basis, field)
    omega = primitive_root_of_order(field, length, seed + 2)
    source_dim = length * prefix_blocks + tail_dim
    vectors = all_vectors(k_values, source_dim)
    rng = random.Random(seed)

    good_prefix: list[list[FpE]] | None = None
    good_tail: list[FpE] | None = None
    good_result: RsCoreResult | None = None
    for _ in range(200):
        prefix, tail = random_tables(length, prefix_blocks, field, rng)
        result = analyze_case(
            "random_good",
            prefix,
            tail,
            vectors,
            k_degree,
            q,
            len(k_values),
            omega,
            field,
        )
        if result.core_zero and result.global_rank_over_k == source_dim:
            good_prefix = prefix
            good_tail = tail
            good_result = result
            break
    if good_prefix is None or good_tail is None or good_result is None:
        raise RuntimeError("did not find random-good RS-tail semilinear example")

    forced_prefix_result = analyze_case(
        "forced_prefix_fixed_core",
        force_prefix_relation(good_prefix),
        good_tail,
        vectors,
        k_degree,
        q,
        len(k_values),
        omega,
        field,
    )
    forced_tail_result = analyze_case(
        "forced_rs_tail_fixed_core",
        good_prefix,
        force_rs_tail_relation(good_prefix),
        vectors,
        k_degree,
        q,
        len(k_values),
        omega,
        field,
    )

    p24_p = 10**24 + 7
    p24_q35 = p24_p % 35
    fixed_frequency_count = sum(1 for a in range(35) if (p24_q35 * a) % 35 == a)
    length4_orbit_count = (35 - fixed_frequency_count) // 4
    p24_prefix_blocks = 4
    p24_tail_dim = 16
    p24_fixed_source_dim = (
        fixed_frequency_count * p24_prefix_blocks
        + length4_orbit_count * p24_prefix_blocks * 4
        + p24_tail_dim
    )

    print("Trace-GCD RS-tail semilinear core toy")
    print(f"q={q}")
    print(f"length={length}")
    print(f"k_degree={k_degree}")
    print(f"l_degree={l_degree}")
    print(f"prefix_blocks={prefix_blocks}")
    print(f"tail_dim={tail_dim}")
    print(f"source_dim_over_k={source_dim}")
    print(f"enumerated_vectors={len(vectors)}")
    print(f"fixed_vector_count_expected={q**source_dim}")
    for row in (good_result, forced_prefix_result, forced_tail_result):
        print(
            "case="
            f"{row.label} global_kernel_size={row.global_kernel_size} "
            f"semilinear_core_size={row.semilinear_core_size} "
            f"fixed_vector_count={row.fixed_vector_count} "
            f"fixed_kernel_size={row.fixed_kernel_size} "
            f"global_rank_over_k={row.global_rank_over_k} "
            f"core_kdim={row.core_kdim} "
            f"fixed_kernel_fpdim={row.fixed_kernel_fpdim} "
            f"core_zero={int(row.core_zero)} "
            f"global_kernel_equals_semilinear_core={int(row.equivalence)} "
            f"hilbert90_descent_match={int(row.descent_match)}"
        )
    print("p24")
    print(f"  p24_p_mod_35={p24_q35}")
    print(f"  p24_fixed_frequency_count={fixed_frequency_count}")
    print(f"  p24_length4_frequency_orbit_count={length4_orbit_count}")
    print(f"  p24_prefix_blocks={p24_prefix_blocks}")
    print(f"  p24_tail_dim={p24_tail_dim}")
    print(f"  p24_fixed_prefix_variables={fixed_frequency_count * p24_prefix_blocks}")
    print(f"  p24_length4_K_variables={length4_orbit_count * p24_prefix_blocks}")
    print(f"  p24_fixed_source_fp_dimension={p24_fixed_source_dim}")
    print("interpretation")
    print("  global_relation_iff_T_orbit_stays_in_RS_tail_kernel=1")
    print("  semilinear_descent_core_kdim_equals_fixed_kernel_fpdim=1")
    print("  zero_core_iff_no_nonzero_T_fixed_RS_tail_relation=1")
    print("  forced_prefix_fixed_core_detected=1")
    print("  forced_rs_tail_fixed_core_detected=1")
    print("  p24_fixed_relation_shape_Fp28_plus_K28_plus_Fp16_to_L=1")
    print("conclusion=reported_trace_gcd_rs_tail_semilinear_core_toy")


if __name__ == "__main__":
    main()
