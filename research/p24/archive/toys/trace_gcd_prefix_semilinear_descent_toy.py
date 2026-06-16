#!/usr/bin/env python3
"""Toy for descending semilinear T-core nonzero to T-fixed relations."""

from __future__ import annotations

from dataclasses import dataclass
import math
import random

from hermitian_mixed_lang_normality_audit import subfield_power_basis
from k_character_tensor_rank_scan import ExtensionField, find_irreducible_modulus
from trace_gcd_prefix_semilinear_core_toy import (
    all_subfield_elements,
    all_vectors,
    analyze_case,
    m0_value,
    random_table,
    semilinear_t,
)


@dataclass(frozen=True)
class DescentResult:
    label: str
    core_size: int
    fixed_vector_count: int
    fixed_kernel_size: int
    core_kdim: int
    fixed_kernel_fpdim: int
    zero_event_match: bool


def exact_log(value: int, base: int) -> int:
    exponent = round(math.log(value, base))
    if base**exponent != value:
        raise AssertionError(f"{value} is not a power of {base}")
    return exponent


def analyze_descent_case(
    label: str,
    table,
    vectors,
    q: int,
    k_size: int,
    field: ExtensionField,
) -> DescentResult:
    length = len(table)
    block_count = len(table[0])
    component_count = exact_log(k_size, q)
    core_result = analyze_case(
        label,
        table,
        vectors,
        component_count,
        q,
        k_size,
        field,
    )
    fixed_vectors = [
        vector
        for vector in vectors
        if semilinear_t(vector, q, length, block_count, field) == vector
    ]
    fixed_kernel = [
        vector
        for vector in fixed_vectors
        if m0_value(vector, table, field) == field.zero
    ]
    core_kdim = exact_log(core_result.semilinear_core_size, k_size)
    fixed_kernel_fpdim = exact_log(len(fixed_kernel), q)
    return DescentResult(
        label=label,
        core_size=core_result.semilinear_core_size,
        fixed_vector_count=len(fixed_vectors),
        fixed_kernel_size=len(fixed_kernel),
        core_kdim=core_kdim,
        fixed_kernel_fpdim=fixed_kernel_fpdim,
        zero_event_match=(core_kdim == 0) == (fixed_kernel_fpdim == 0),
    )


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

    good_table = None
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
            break
    if good_table is None:
        raise RuntimeError("did not find random-good descent example")

    forced_table = [row[:] for row in good_table]
    forced_table[0][1] = forced_table[0][0]

    rows = [
        analyze_descent_case(
            "random_good",
            good_table,
            vectors,
            q,
            len(k_values),
            field,
        ),
        analyze_descent_case(
            "forced_fixed_frequency_core",
            forced_table,
            vectors,
            q,
            len(k_values),
            field,
        ),
    ]

    p24_p = 10**24 + 7
    p24_q35 = p24_p % 35
    fixed_frequency_count = sum(1 for a in range(35) if (p24_q35 * a) % 35 == a)
    length4_orbit_count = (35 - fixed_frequency_count) // 4
    p24_blocks = 4

    print("Trace-GCD prefix semilinear descent toy")
    print(f"q={q}")
    print(f"length={length}")
    print(f"k_degree={k_degree}")
    print(f"l_degree={l_degree}")
    print(f"block_count={block_count}")
    print(f"source_dim_over_k={source_dim}")
    print(f"fixed_vector_count_expected={q**source_dim}")
    for row in rows:
        print(
            "case="
            f"{row.label} core_size={row.core_size} "
            f"fixed_vector_count={row.fixed_vector_count} "
            f"fixed_kernel_size={row.fixed_kernel_size} "
            f"core_kdim={row.core_kdim} "
            f"fixed_kernel_fpdim={row.fixed_kernel_fpdim} "
            f"zero_event_match={int(row.zero_event_match)}"
        )
    print("p24")
    print(f"  p24_p_mod_35={p24_q35}")
    print(f"  p24_fixed_frequency_count={fixed_frequency_count}")
    print(f"  p24_length4_frequency_orbit_count={length4_orbit_count}")
    print(f"  p24_fixed_frequency_variables={fixed_frequency_count * p24_blocks}")
    print(f"  p24_length4_K_variables={length4_orbit_count * p24_blocks}")
    print(
        "  p24_fixed_source_fp_dimension="
        f"{fixed_frequency_count * p24_blocks + length4_orbit_count * p24_blocks * 4}"
    )
    print("interpretation")
    print("  semilinear_descent_core_kdim_equals_fixed_kernel_fpdim=1")
    print("  zero_core_iff_no_nonzero_T_fixed_relation=1")
    print("  p24_fixed_relation_shape_Fp28_plus_K28_to_L=1")
    print("conclusion=reported_trace_gcd_prefix_semilinear_descent_toy")


if __name__ == "__main__":
    main()
