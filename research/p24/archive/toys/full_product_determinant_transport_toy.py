#!/usr/bin/env python3
"""Full-product determinant transport toy for the p24 diamond theorem.

This is a theorem-shape guard for the remaining structural diamond proof.
It models one full right-product determinant-line object before projecting to
six nonzero right Frobenius factors.

For each edge O -> 2O, the toy constructs invertible source/target transports
dK,dT and block maps B_O satisfying

    B_2O dK = dT B_O.

Then

    det(B_2O) = det(dT) det(dK)^(-1) det(B_O),

so zero status and p-unitness propagate while literal determinant equality is
not expected.  The closing edge is allowed to return to the representative
after an internal Frobenius rotation, matching the p24 fact

    2^6 = p^17 mod 211.

No CM values are computed here.
"""

from __future__ import annotations

import argparse
import random

from block_cycle_determinant_line_invariance_toy import (
    det_mod,
    matmul,
    matrix_inverse,
    random_invertible,
)


P24 = 10**24 + 7
RIGHT = 211
UNIT = 2
P_MOD_RIGHT = P24 % RIGHT
ORBIT_LEN = 6
RIGHT_ORBIT_LEN = 35
TAIL_LEN = 16
FINAL_ROTATION_START = 17


def permutation_matrix(size: int, shift: int) -> list[list[int]]:
    return [
        [1 if row == (col + shift) % size else 0 for col in range(size)]
        for row in range(size)
    ]


def determinant_formula_holds(
    current: list[list[int]],
    nxt: list[list[int]],
    d_k: list[list[int]],
    d_t: list[list[int]],
    q: int,
) -> tuple[bool, bool, bool]:
    left = matmul(nxt, d_k, q)
    right = matmul(d_t, current, q)
    commutes = left == right
    det_current = det_mod(current, q)
    det_next = det_mod(nxt, q)
    det_dk = det_mod(d_k, q)
    det_dt = det_mod(d_t, q)
    expected = det_dt * pow(det_dk, -1, q) * det_current % q
    determinant_formula = det_next == expected
    zero_status_match = (det_current == 0) == (det_next == 0)
    return commutes, determinant_formula, zero_status_match


def run_invertible_trial(rng: random.Random, q: int, size: int) -> dict[str, int]:
    blocks: list[list[list[int]]] = [random_invertible(rng, q, size)]
    source_transports: list[list[list[int]]] = []
    target_transports: list[list[list[int]]] = []

    for _edge in range(ORBIT_LEN - 1):
        d_k = random_invertible(rng, q, size)
        d_t = random_invertible(rng, q, size)
        nxt = matmul(matmul(d_t, blocks[-1], q), matrix_inverse(d_k, q), q)
        source_transports.append(d_k)
        target_transports.append(d_t)
        blocks.append(nxt)

    source_rotation = permutation_matrix(size, FINAL_ROTATION_START % size)
    target_rotation = permutation_matrix(size, FINAL_ROTATION_START % size)
    final_rotated_representative = matmul(
        matmul(target_rotation, blocks[0], q),
        matrix_inverse(source_rotation, q),
        q,
    )
    closing_dk = random_invertible(rng, q, size)
    closing_dt = matmul(
        matmul(final_rotated_representative, closing_dk, q),
        matrix_inverse(blocks[-1], q),
        q,
    )
    source_transports.append(closing_dk)
    target_transports.append(closing_dt)

    commuting_failures = 0
    determinant_failures = 0
    zero_mismatches = 0
    literal_equal_edges = 0
    punit_edges = 0
    for edge in range(ORBIT_LEN):
        current = blocks[edge]
        nxt = (
            blocks[edge + 1]
            if edge + 1 < ORBIT_LEN
            else final_rotated_representative
        )
        commutes, det_ok, zero_ok = determinant_formula_holds(
            current,
            nxt,
            source_transports[edge],
            target_transports[edge],
            q,
        )
        commuting_failures += int(not commutes)
        determinant_failures += int(not det_ok)
        zero_mismatches += int(not zero_ok)
        literal_equal_edges += int(det_mod(current, q) == det_mod(nxt, q))
        punit_edges += int(det_mod(current, q) != 0 and det_mod(nxt, q) != 0)

    identified = matmul(
        matmul(matrix_inverse(target_rotation, q), final_rotated_representative, q),
        source_rotation,
        q,
    )
    return {
        "commuting_failures": commuting_failures,
        "determinant_failures": determinant_failures,
        "zero_mismatches": zero_mismatches,
        "literal_equal_edges": literal_equal_edges,
        "punit_edges": punit_edges,
        "final_identifies_to_representative": int(identified == blocks[0]),
        "rotation_det_punit": int(det_mod(source_rotation, q) != 0 and det_mod(target_rotation, q) != 0),
    }


def run_singular_trial(rng: random.Random, q: int, size: int) -> dict[str, int]:
    current = random_invertible(rng, q, size)
    current[-1] = current[0][:]
    zero_mismatches = 0
    determinant_failures = 0
    for _edge in range(ORBIT_LEN):
        d_k = random_invertible(rng, q, size)
        d_t = random_invertible(rng, q, size)
        nxt = matmul(matmul(d_t, current, q), matrix_inverse(d_k, q), q)
        _commutes, det_ok, zero_ok = determinant_formula_holds(current, nxt, d_k, d_t, q)
        determinant_failures += int(not det_ok)
        zero_mismatches += int(not zero_ok)
        current = nxt
    return {
        "singular_determinant_failures": determinant_failures,
        "singular_zero_mismatches": zero_mismatches,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=1009)
    parser.add_argument("--size", type=int, default=TAIL_LEN)
    parser.add_argument("--trials", type=int, default=80)
    parser.add_argument("--seed", type=int, default=20260606)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    totals = {
        "commuting_failures": 0,
        "determinant_failures": 0,
        "zero_mismatches": 0,
        "literal_equal_edges": 0,
        "punit_edges": 0,
        "final_identifications": 0,
        "rotation_det_punits": 0,
        "singular_determinant_failures": 0,
        "singular_zero_mismatches": 0,
    }
    for _trial in range(args.trials):
        inv = run_invertible_trial(rng, args.q, args.size)
        sing = run_singular_trial(rng, args.q, args.size)
        totals["commuting_failures"] += inv["commuting_failures"]
        totals["determinant_failures"] += inv["determinant_failures"]
        totals["zero_mismatches"] += inv["zero_mismatches"]
        totals["literal_equal_edges"] += inv["literal_equal_edges"]
        totals["punit_edges"] += inv["punit_edges"]
        totals["final_identifications"] += inv["final_identifies_to_representative"]
        totals["rotation_det_punits"] += inv["rotation_det_punit"]
        totals["singular_determinant_failures"] += sing["singular_determinant_failures"]
        totals["singular_zero_mismatches"] += sing["singular_zero_mismatches"]

    total_edges = args.trials * ORBIT_LEN
    rotation_identity = pow(UNIT, ORBIT_LEN, RIGHT) == pow(P_MOD_RIGHT, FINAL_ROTATION_START, RIGHT)
    print("full-product determinant transport toy")
    print(f"q={args.q}")
    print(f"block_size={args.size}")
    print(f"trials={args.trials}")
    print(f"orbit_len={ORBIT_LEN}")
    print(f"p24_unit={UNIT}")
    print(f"p24_p_mod_211={P_MOD_RIGHT}")
    print(f"p24_final_rotation_start={FINAL_ROTATION_START}")
    print(f"p24_unit6_equals_frobenius17={int(rotation_identity)}")
    print(f"commuting_square_failures={totals['commuting_failures']}")
    print(f"determinant_formula_failures={totals['determinant_failures']}")
    print(f"zero_status_mismatches={totals['zero_mismatches']}")
    print(f"literal_equal_edges={totals['literal_equal_edges']}/{total_edges}")
    print(f"punit_edges={totals['punit_edges']}/{total_edges}")
    print(f"final_identifies_to_representative={totals['final_identifications']}/{args.trials}")
    print(f"internal_rotation_det_punit={totals['rotation_det_punits']}/{args.trials}")
    print(f"singular_determinant_formula_failures={totals['singular_determinant_failures']}")
    print(f"singular_zero_status_mismatches={totals['singular_zero_mismatches']}")
    print("interpretation")
    print("  full_product_commuting_square_implies_determinant_line_transport=1")
    print("  internal_frobenius_rotation_closes_unit2_cycle_up_to_punit=1")
    print("  literal_printed_determinants_are_not_the_invariant=1")
    print("  toy_does_not_prove_cm_nonvanishing=1")
    print("conclusion=reported_full_product_determinant_transport_toy")

    if not rotation_identity:
        raise SystemExit(1)
    if totals["commuting_failures"] or totals["determinant_failures"]:
        raise SystemExit(1)
    if totals["zero_mismatches"] or totals["singular_zero_mismatches"]:
        raise SystemExit(1)
    if totals["punit_edges"] != total_edges:
        raise SystemExit(1)
    if totals["final_identifications"] != args.trials:
        raise SystemExit(1)
    if totals["rotation_det_punits"] != args.trials:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

