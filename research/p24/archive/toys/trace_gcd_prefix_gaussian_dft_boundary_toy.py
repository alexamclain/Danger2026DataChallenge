#!/usr/bin/env python3
"""Boundary toy for Gaussian DFT scalar extension.

The p24 Gaussian-period basis invites a length-35 DFT over K=F_p(mu_35).
That DFT is safe in L tensor_Fp K.  It is not safe to multiply the K
coefficients into L and reason about the resulting F_p-rank in L.

This tiny F_4/F_2 example shows the pitfall:

    [1, 1, 0] has collapsed F_2-rank 1,
    its length-3 DFT over F_4 collapses to [0, omega^2, omega],
    which has F_2-rank 2.

In the tensor product, both families have K-rank 1, as they should.
"""

from __future__ import annotations

from k_character_tensor_rank_scan import (
    ExtensionField,
    find_irreducible_modulus,
    primitive_root_of_order,
    rank_over_extension,
)
from l1_axis_injectivity_scan import rank_mod_q


def tensor_vector_over_k(
    value: tuple[int, ...],
    kfield: ExtensionField,
) -> list[tuple[int, ...]]:
    return [kfield.embed(coord) for coord in value]


def dft_collapsed(
    values: list[tuple[int, ...]],
    omega: tuple[int, ...],
    field: ExtensionField,
) -> list[tuple[int, ...]]:
    out: list[tuple[int, ...]] = []
    n = len(values)
    for a in range(n):
        total = field.zero
        for i, value in enumerate(values):
            total = field.add(total, field.mul(field.pow(omega, a * i), value))
        out.append(total)
    return out


def dft_tensor_rows(
    values: list[tuple[int, ...]],
    omega: tuple[int, ...],
    kfield: ExtensionField,
) -> list[list[tuple[int, ...]]]:
    rows: list[list[tuple[int, ...]]] = []
    n = len(values)
    for a in range(n):
        row = [kfield.zero for _ in range(kfield.degree)]
        for i, value in enumerate(values):
            coeff = kfield.pow(omega, a * i)
            tensor = tensor_vector_over_k(value, kfield)
            row = [
                kfield.add(left, kfield.mul(coeff, right))
                for left, right in zip(row, tensor)
            ]
        rows.append(row)
    return rows


def main() -> None:
    q = 2
    degree = 2
    field = ExtensionField(q, degree, find_irreducible_modulus(q, degree, 20260606))
    omega = primitive_root_of_order(field, 3, 20260606)

    values = [field.one, field.one, field.zero]
    collapsed_dft = dft_collapsed(values, omega, field)

    original_collapsed_rank = rank_mod_q([list(value) for value in values], q)
    dft_collapsed_rank = rank_mod_q([list(value) for value in collapsed_dft], q)

    original_tensor_rank = rank_over_extension(
        [tensor_vector_over_k(value, field) for value in values],
        field,
    )
    dft_tensor_rank = rank_over_extension(
        dft_tensor_rows(values, omega, field),
        field,
    )

    print("Trace-GCD prefix Gaussian DFT scalar-extension boundary toy")
    print(f"q={q}")
    print(f"degree={degree}")
    print(f"omega={omega}")
    print(f"values={values}")
    print(f"collapsed_dft={collapsed_dft}")
    print(f"original_collapsed_fp_rank={original_collapsed_rank}")
    print(f"dft_collapsed_fp_rank={dft_collapsed_rank}")
    print(f"original_tensor_k_rank={original_tensor_rank}")
    print(f"dft_tensor_k_rank={dft_tensor_rank}")
    print("interpretation")
    print(
        "  collapsed_extension_coefficient_dft_can_change_base_rank="
        f"{int(original_collapsed_rank != dft_collapsed_rank)}"
    )
    print(
        "  tensor_product_dft_preserves_scalar_extended_rank="
        f"{int(original_tensor_rank == dft_tensor_rank)}"
    )
    print("  p24_gaussian_dft_must_stay_in_L_tensor_K=1")
    print("conclusion=reported_trace_gcd_prefix_gaussian_dft_boundary_toy")


if __name__ == "__main__":
    main()
