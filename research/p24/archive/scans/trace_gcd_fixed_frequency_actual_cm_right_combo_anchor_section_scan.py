#!/usr/bin/env python3
"""Origin-section scan for the actual-CM right-combo anchor boundary.

The pinned right-combo anchor boundary checks one origin for the small
actual-CM analogue

    D=-13319, q=13463, h=140, m=28=4*7, n=5.

Here the recombined relative quotient has only one nonzero coset, so the
recombined balance is exactly the anchor equation

    sum_{k != 0} c_k = (n - 1) c_0.

This scan rotates the embedded CM cycle through all global origin/section
choices.  It tests the natural loophole "maybe the right-combo anchor is true
after choosing the correct embedded child section."  For this actual-CM row it
is not: every rotated section has a nonzero anchor defect.
"""

from __future__ import annotations

from dataclasses import replace

from trace_gcd_fixed_frequency_actual_cm_right_combo_anchor_boundary import (
    weighted_coefficients,
)
from trace_gcd_fixed_frequency_actual_cm_right_combo_boundary import (
    load_actual_packet,
)


def rotate_tuple(values: tuple[int, ...], shift: int) -> tuple[int, ...]:
    shift %= len(values)
    return values[shift:] + values[:shift]


def anchor_defect(packet) -> tuple[int, ...]:
    coeffs = weighted_coefficients(packet)
    total = packet.field.zero
    for coeff in coeffs[1:]:
        total = packet.field.add(total, coeff)
    target = packet.field.scalar_mul(packet.n - 1, coeffs[0])
    return packet.field.sub(total, target)


def main() -> None:
    base = load_actual_packet()
    defects: list[tuple[int, ...]] = []
    zero_shifts: list[int] = []

    for shift in range(base.h):
        packet = replace(base, cycle=rotate_tuple(base.cycle, shift))
        defect = anchor_defect(packet)
        defects.append(defect)
        if defect == packet.field.zero:
            zero_shifts.append(shift)

    nonzero_count = sum(defect != base.field.zero for defect in defects)
    distinct_defects = len(set(defects))
    first_defects = defects[: min(8, len(defects))]

    print("Trace-GCD fixed-frequency actual-CM right-combo anchor section scan")
    print(f"D={base.D}")
    print(f"q={base.q}")
    print(f"ell={base.ell}")
    print(f"h={base.h}")
    print(f"m={base.m}")
    print(f"n={base.n}")
    print(f"origin_sections_checked={base.h}")
    print(f"anchor_zero_sections={len(zero_shifts)}/{base.h}")
    print(f"anchor_nonzero_sections={nonzero_count}/{base.h}")
    print(f"distinct_anchor_defects={distinct_defects}")
    print(f"zero_section_shifts={zero_shifts}")
    print(f"first_anchor_defects={first_defects}")
    print("interpretation")
    print("  actual_cm_right_combo_anchor_not_rescued_by_origin_section=1")
    print("  selected_section_choice_alone_does_not_prove_anchor_balance=1")
    print("  p24_anchor_still_needs_specific_weighted_G_chi_or_explicit_potential=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_actual_cm_right_combo_anchor_section_scan")

    if (base.D, base.q, base.h, base.m, base.n) != (-13319, 13463, 140, 28, 5):
        raise SystemExit(1)
    if zero_shifts:
        raise SystemExit(1)
    if nonzero_count != base.h:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
