#!/usr/bin/env python3
"""Frame rigidity for the p25 square-axis no-borrow seed.

The seed-rigidity gate proves that the six-term seed has exactly three
3x3 AP-rectangle completions.  This gate classifies the frames of those
completions.

Every oriented presentation uses only the signed directions

    Y = 9,  X = 43,  X+Y = 52

on C_507.  The three rectangle completions are exactly the three two-direction
frames {Y, X+Y}, {Y, X}, and {X, X+Y}.  Thus the seed is not just contained in
some AP rectangles; the AP frames are forced by the same X/Y no-borrow
coordinates used by the group-ring normal form.
"""

from __future__ import annotations

from collections import Counter, defaultdict

from p25_laneB_square_axis_group_ring_normal_form_gate import X_STEP, Y_STEP
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER
from p25_laneB_square_axis_seed_rigidity_gate import (
    ap_rectangle_completions,
    seed_set,
)


SIGNED_FRAME_LABELS = {
    Y_STEP % QUOTIENT_ORDER: "+Y",
    (-Y_STEP) % QUOTIENT_ORDER: "-Y",
    X_STEP % QUOTIENT_ORDER: "+X",
    (-X_STEP) % QUOTIENT_ORDER: "-X",
    (X_STEP + Y_STEP) % QUOTIENT_ORDER: "+X+Y",
    (-(X_STEP + Y_STEP)) % QUOTIENT_ORDER: "-X-Y",
}

UNSIGNED_FRAME_LABELS = {
    Y_STEP % QUOTIENT_ORDER: "Y",
    (-Y_STEP) % QUOTIENT_ORDER: "Y",
    X_STEP % QUOTIENT_ORDER: "X",
    (-X_STEP) % QUOTIENT_ORDER: "X",
    (X_STEP + Y_STEP) % QUOTIENT_ORDER: "X+Y",
    (-(X_STEP + Y_STEP)) % QUOTIENT_ORDER: "X+Y",
}


def unsigned_label(step: int) -> str:
    return UNSIGNED_FRAME_LABELS[step % QUOTIENT_ORDER]


def normalized_pair(first_step: int, second_step: int) -> tuple[str, str]:
    return tuple(sorted((unsigned_label(first_step), unsigned_label(second_step))))


def seed_mask(base: int, first_step: int, second_step: int) -> tuple[tuple[int, ...], ...]:
    seed = seed_set()
    return tuple(
        tuple(
            int((base + row * first_step + column * second_step) % QUOTIENT_ORDER in seed)
            for column in range(3)
        )
        for row in range(3)
    )


def expected_frame_groups() -> dict[
    tuple[tuple[int, ...], tuple[int, ...]],
    tuple[tuple[str, str], int],
]:
    return {
        (
            (25, 34, 43, 77, 86, 95, 129, 138, 147),
            (25, 34, 77),
        ): (("X+Y", "Y"), 8),
        (
            (43, 52, 61, 86, 95, 104, 129, 138, 147),
            (52, 61, 104),
        ): (("X", "Y"), 8),
        (
            (43, 86, 95, 129, 138, 147, 181, 190, 233),
            (181, 190, 233),
        ): (("X", "X+Y"), 8),
    }


def triangular_masks() -> set[tuple[tuple[int, ...], ...]]:
    return {
        ((0, 0, 1), (0, 1, 1), (1, 1, 1)),
        ((1, 0, 0), (1, 1, 0), (1, 1, 1)),
        ((1, 1, 1), (0, 1, 1), (0, 0, 1)),
        ((1, 1, 1), (1, 1, 0), (1, 0, 0)),
    }


def main() -> int:
    print("p25 Lane B square-axis seed-frame-rigidity gate")
    print(f"quotient_order={QUOTIENT_ORDER} X={X_STEP} Y={Y_STEP} X_plus_Y={X_STEP + Y_STEP}")
    completions = ap_rectangle_completions()
    expected_groups = expected_frame_groups()
    allowed_steps = set(SIGNED_FRAME_LABELS)
    allowed_pair_counts: Counter[tuple[str, str]] = Counter()
    mask_counts: Counter[tuple[tuple[int, ...], ...]] = Counter()
    grouped: dict[tuple[tuple[int, ...], tuple[int, ...]], list[tuple[int, int, int]]] = defaultdict(list)

    canonical_step_hits = 0
    triangular_mask_hits = 0
    for base, first_step, second_step, rectangle, borrow in completions:
        if first_step in allowed_steps and second_step in allowed_steps:
            canonical_step_hits += 1
        pair = normalized_pair(first_step, second_step)
        allowed_pair_counts[pair] += 1
        mask = seed_mask(base, first_step, second_step)
        mask_counts[mask] += 1
        if mask in triangular_masks():
            triangular_mask_hits += 1
        grouped[(rectangle, borrow)].append((base, first_step, second_step))

    group_rows_ok = 0
    for key, (expected_pair, expected_count) in expected_groups.items():
        presentations = grouped.get(key, [])
        pairs = {normalized_pair(first_step, second_step) for _base, first_step, second_step in presentations}
        if len(presentations) == expected_count and pairs == {expected_pair}:
            group_rows_ok += 1

    expected_pair_counts = Counter(
        {
            ("X+Y", "Y"): 8,
            ("X", "Y"): 8,
            ("X", "X+Y"): 8,
        }
    )
    expected_mask_counts = Counter({mask: 6 for mask in triangular_masks()})
    row_ok = (
        len(completions) == 24
        and canonical_step_hits == 24
        and triangular_mask_hits == 24
        and allowed_pair_counts == expected_pair_counts
        and mask_counts == expected_mask_counts
        and group_rows_ok == 3
    )

    print(
        "seed_frame_rigidity: "
        f"completion_count={len(completions)}/24 "
        f"canonical_step_hits={canonical_step_hits}/24 "
        f"triangular_mask_hits={triangular_mask_hits}/24 "
        f"frame_group_rows={group_rows_ok}/3 "
        f"ok={int(row_ok)}"
    )
    print("signed_frame_labels")
    for step, label in sorted(SIGNED_FRAME_LABELS.items()):
        print(f"  {step}: {label}")
    print("pair_counts")
    for pair, count in sorted(allowed_pair_counts.items()):
        print(f"  pair={pair} count={count}")
    print("mask_counts")
    for mask, count in sorted(mask_counts.items()):
        print(f"  count={count} mask={mask}")
    print("completion_groups")
    for (rectangle, borrow), presentations in sorted(grouped.items()):
        pairs = sorted({normalized_pair(first_step, second_step) for _base, first_step, second_step in presentations})
        print(
            f"  pair={pairs} count={len(presentations)} "
            f"rectangle={list(rectangle)} borrow={list(borrow)}"
        )
        for base, first_step, second_step in presentations:
            print(
                f"    base={base} "
                f"steps=({first_step},{second_step}) "
                f"labels=({SIGNED_FRAME_LABELS[first_step]},{SIGNED_FRAME_LABELS[second_step]}) "
                f"mask={seed_mask(base, first_step, second_step)}"
            )
    print(f"square_axis_seed_frame_rigidity_rows={int(row_ok)}/1")
    print("interpretation")
    print("  every_seed_rectangle_completion_uses_only_signed_X_Y_XplusY_directions=1")
    print("  the_three_completion_groups_are_exactly_the_three_two_direction_frames=1")
    print("  every_orientation_is_a_triangular_no_borrow_mask=1")
    print("  producer_must_recover_the_X_Y_frame_not_an_arbitrary_AP_rectangle=1")
    print("conclusion=reported_p25_laneB_square_axis_seed_frame_rigidity_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
