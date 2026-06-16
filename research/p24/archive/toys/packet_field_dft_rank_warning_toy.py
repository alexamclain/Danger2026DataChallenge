#!/usr/bin/env python3
"""Toy warning for packet-field coordinate transforms.

An invertible DFT matrix whose entries live in the packet field does not
automatically preserve the F_p-span of the coordinate entries.

This matters for the p24 211-axis discussion.  Since the 211st roots of unity
already lie in the H-packet field, the 211-axis can be diagonalized there.
That is useful structure, but it is not a formal replacement for a
base-field/Moore rank statement.

The tiny model is F_4/F_2.  The matrix

    [[0, 1],
     [1, alpha]]

is invertible over F_4.  It sends the coordinate vector (0,1), whose entries
span a one-dimensional F_2-space, to (1,alpha), whose entries span a
two-dimensional F_2-space.
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
    if out & 0b100:
        out ^= 0b100
        out ^= 0b011
    return out & 0b11


def determinant_2x2(matrix: list[list[int]]) -> int:
    return add(mul(matrix[0][0], matrix[1][1]), mul(matrix[0][1], matrix[1][0]))


def mat_vec(matrix: list[list[int]], vector: list[int]) -> list[int]:
    return [
        add(mul(row[0], vector[0]), mul(row[1], vector[1]))
        for row in matrix
    ]


def fp2_span_rank(elements: list[int]) -> int:
    """Rank of F_4 elements as vectors over F_2."""
    basis = [0, 0]
    rank = 0
    for value in elements:
        x = value
        while x:
            pivot = x.bit_length() - 1
            if basis[pivot]:
                x ^= basis[pivot]
                continue
            basis[pivot] = x
            rank += 1
            break
    return rank


def main() -> None:
    alpha = 2
    matrix = [[0, 1], [1, alpha]]
    before = [0, 1]
    after = mat_vec(matrix, before)

    print("packet-field DFT rank warning toy")
    print("base_field=F2")
    print("packet_field=F4")
    print("alpha_encoding=2")
    print(f"matrix={matrix}")
    print(f"determinant={determinant_2x2(matrix)}")
    print(f"matrix_invertible_over_packet_field={int(determinant_2x2(matrix) != 0)}")
    print(f"before_vector={before}")
    print(f"after_vector={after}")
    print(f"before_coordinate_F2_span_rank={fp2_span_rank(before)}")
    print(f"after_coordinate_F2_span_rank={fp2_span_rank(after)}")
    print()
    print("interpretation")
    print("  packet_field_invertible_coordinate_transform=1")
    print("  base_field_coordinate_span_preserved=0")
    print("  packet_field_diagonalization_is_not_a_rank_certificate_by_itself=1")
    print("conclusion=reported_packet_field_dft_rank_warning_toy")


if __name__ == "__main__":
    main()
