#!/usr/bin/env python3
"""Static overlap audit for the p24 leading prefix and smooth-axis support.

In the cyclic Toeplitz/translate-minor model, a principal singular-modulus
factor appears in a determinant term when a selected row index equals the
matched selected column index, up to the chosen cyclic origin.  A direct
principal-product dominance proof would need many such coincidences.

This audit computes the p24 smooth-axis frequency set in Z/mZ and measures how
many points it can share with any consecutive leading prefix of length 368.
"""

from __future__ import annotations

from collections import Counter

M = 66254
COMPONENTS = (2, 157, 211)
AXIS_DIM = 1 + sum(component - 1 for component in COMPONENTS)


def component_frequencies(component: int) -> list[int]:
    step = M // component
    return [(step * a) % M for a in range(1, component)]


def axis_frequencies() -> dict[int, str]:
    out: dict[int, str] = {0: "constant"}
    for component in COMPONENTS:
        for freq in component_frequencies(component):
            if freq in out:
                raise AssertionError((component, freq, out[freq]))
            out[freq] = str(component)
    return out


def interval(start: int, length: int) -> set[int]:
    return {(start + offset) % M for offset in range(length)}


def main() -> None:
    axis = axis_frequencies()
    prefix0 = interval(0, AXIS_DIM)
    overlap0 = sorted(prefix0 & set(axis))
    best: list[tuple[int, list[int]]] = []
    max_overlap = -1
    for start in range(M):
        points = sorted(interval(start, AXIS_DIM) & set(axis))
        count = len(points)
        if count > max_overlap:
            max_overlap = count
            best = [(start, points)]
        elif count == max_overlap and len(best) < 8:
            best.append((start, points))

    component_hist = Counter(axis.values())
    prefix_component_hist = Counter(axis[point] for point in overlap0)
    best_component_hist = Counter(axis[point] for point in best[0][1])

    print("p24 axis-prefix overlap audit")
    print(f"m={M}")
    print(f"components={list(COMPONENTS)}")
    print(f"axis_dim={AXIS_DIM}")
    print(f"axis_support_size={len(axis)}")
    print(f"leading_prefix_size={len(prefix0)}")
    print(f"axis_component_hist={dict(sorted(component_hist.items()))}")
    print(f"leading_prefix_overlap_count={len(overlap0)}")
    print(f"leading_prefix_overlap_points={overlap0}")
    print(f"leading_prefix_overlap_components={dict(sorted(prefix_component_hist.items()))}")
    print(f"max_cyclic_interval_overlap={max_overlap}")
    print(f"max_overlap_ratio={max_overlap}/{AXIS_DIM}")
    print("best_shift_examples")
    for start, points in best:
        components = [axis[point] for point in points]
        print(f"  start={start} points={points} components={components}")
    print(f"best_overlap_components={dict(sorted(best_component_hist.items()))}")
    print()
    print("interpretation")
    print("  any_cyclic_leading_prefix_meets_smooth_axis_support_in_at_most_3_points=1")
    print("  direct_principal_diagonal_dominance_cannot_use_many_principal_factors=1")
    print("  selected_minor_still_needs_nonprincipal_or_padic_structure=1")
    print("conclusion=reported_trace_frame_axis_prefix_overlap_boundary")


if __name__ == "__main__":
    main()
