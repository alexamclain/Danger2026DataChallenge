#!/usr/bin/env python3
"""Toy warning for scalar-extension rank in K-character language.

Full K-normality is F_p-linear independence of packet-field elements
`beta_r in A`.  After adjoining K roots of unity, the correct operation is
scalar extension:

    A_E = A tensor_{F_p} E.

It is *not* the same as choosing one embedding A -> E and then treating the
images as scalars over E.  The latter collapses every nonzero set to rank at
most one.

This tiny F_2/F_4 toy shows the distinction.  The elements 1 and alpha are
F_2-independent in F_4.  Under scalar extension to F_4,

    F_4 tensor_{F_2} F_4 ~= F_4 x F_4,

they remain independent.  Under a single embedding into F_4, they are just two
scalars and have F_4-rank one.
"""

from __future__ import annotations


def add(x: int, y: int) -> int:
    return x ^ y


def mul(x: int, y: int) -> int:
    """Multiply in F_4 = F_2[a]/(a^2+a+1), encoded 0,1,a,a+1."""
    out = 0
    for i in range(2):
        if (y >> i) & 1:
            out ^= x << i
    # reduce a^2 = a + 1
    if out & 0b100:
        out ^= 0b100
        out ^= 0b011
    return out & 0b11


def determinant_2x2(matrix: list[list[int]]) -> int:
    return add(mul(matrix[0][0], matrix[1][1]), mul(matrix[0][1], matrix[1][0]))


def rank_2x2(matrix: list[list[int]]) -> int:
    if determinant_2x2(matrix):
        return 2
    if any(value for row in matrix for value in row):
        return 1
    return 0


def frobenius(x: int) -> int:
    return mul(x, x)


def main() -> None:
    one = 1
    alpha = 2
    alpha_frob = frobenius(alpha)

    # Single embedding A -> E: columns are scalars in one E-line.
    single_embedding_rank = 1

    # Tensor decomposition F4 tensor_F2 F4 ~= F4 x F4 sends
    # x -> (x, x^2).  Columns (1, alpha) are independent over F4 because the
    # Moore/Frobenius matrix has nonzero determinant.
    tensor_matrix = [
        [one, alpha],
        [frobenius(one), alpha_frob],
    ]
    tensor_rank = rank_2x2(tensor_matrix)

    print("scalar-extension rank pitfall toy")
    print("field=F2, packet=A=F4, splitting=E=F4")
    print("basis_elements=[1,alpha]")
    print(f"alpha_square={alpha_frob}  # encoded alpha+1")
    print(f"single_embedding_rank_over_E={single_embedding_rank}")
    print(f"tensor_extension_moore_matrix={tensor_matrix}")
    print(f"tensor_extension_rank_over_E={tensor_rank}")
    print(f"moore_determinant={determinant_2x2(tensor_matrix)}")
    print()
    print("interpretation")
    print("  single_embedding_rank_collapses_to_one=1")
    print("  scalar_extension_tensor_rank_preserves_F2_independence=1")
    print("  K_character_rank_must_mean_tensor_scalar_extension=1")
    print("conclusion=reported_scalar_extension_rank_pitfall_toy")


if __name__ == "__main__":
    main()
