#!/usr/bin/env python3
"""Toy model for Schubert determinant-line descent.

This is deliberately tiny.  It models the residue algebra of a decomposition
field at a split prime as a product of packet residue fields.

The useful lesson is:

* a fixed determinant expression has packet residues whose product is the
  packet norm;
* multiplying by a fixed unit expression preserves zero/nonzero;
* choosing row-reduction pivots separately in each packet can splice together
  different determinant sections and hide zeros of every fixed section.
"""

from __future__ import annotations

P = 101
PACKETS = [1, 2, 3, 4]


def mod(x: int) -> int:
    return x % P


def prod(values: list[int]) -> int:
    out = 1
    for value in values:
        out = mod(out * value)
    return out


def canonical_det(x: int) -> int:
    """det [[x+1, 2], [3, x+3]]."""
    return mod((x + 1) * (x + 3) - 6)


def unit(x: int) -> int:
    return mod(x + 7)


def col1_minor(x: int) -> int:
    """First fixed 1x1 minor of the row [x-1, x-2]."""
    return mod(x - 1)


def col2_minor(x: int) -> int:
    """Second fixed 1x1 minor of the row [x-1, x-2]."""
    return mod(x - 2)


def main() -> None:
    det_values = [canonical_det(x) for x in PACKETS]
    unit_values = [unit(x) for x in PACKETS]
    twisted_values = [mod(unit(x) * canonical_det(x)) for x in PACKETS]
    col1_values = [col1_minor(x) for x in PACKETS]
    col2_values = [col2_minor(x) for x in PACKETS]

    spliced_pivots = []
    spliced_columns = []
    for x in PACKETS:
        left = col1_minor(x)
        right = col2_minor(x)
        if left != 0:
            spliced_columns.append(1)
            spliced_pivots.append(left)
        else:
            spliced_columns.append(2)
            spliced_pivots.append(right)

    print("trace-frame Schubert descent toy")
    print(f"p={P}")
    print(f"packets={PACKETS}")
    print()
    print("canonical_fixed_determinant")
    print(f"  det_values={det_values}")
    print(f"  det_packet_norm={prod(det_values)}")
    print(f"  canonical_all_nonzero={int(all(value != 0 for value in det_values))}")
    print()
    print("unit_twisted_determinant")
    print(f"  unit_values={unit_values}")
    print(f"  twisted_values={twisted_values}")
    print(f"  twisted_packet_norm={prod(twisted_values)}")
    print(
        "  unit_twist_zero_compatible="
        f"{int([value == 0 for value in det_values] == [value == 0 for value in twisted_values])}"
    )
    print()
    print("noncanonical_packetwise_pivot_warning")
    print(f"  fixed_col1_values={col1_values}")
    print(f"  fixed_col2_values={col2_values}")
    print(f"  fixed_col1_packet_norm={prod(col1_values)}")
    print(f"  fixed_col2_packet_norm={prod(col2_values)}")
    print(f"  spliced_pivot_columns={spliced_columns}")
    print(f"  spliced_pivot_values={spliced_pivots}")
    print(f"  spliced_packet_product={prod(spliced_pivots)}")
    print(f"  spliced_all_nonzero={int(all(value != 0 for value in spliced_pivots))}")
    print(
        "  no_single_fixed_minor_nonzero="
        f"{int(not all(value != 0 for value in col1_values) and not all(value != 0 for value in col2_values))}"
    )
    print("conclusion=fixed_sections_descend_packetwise_pivots_do_not")


if __name__ == "__main__":
    main()
