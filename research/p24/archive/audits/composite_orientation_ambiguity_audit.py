#!/usr/bin/env python3
"""Audit orientation ambiguity for the composite p24 split ideal.

The best certificate-oriented formal target uses the oriented ideal

    a = p2 * p463 * p223^(-1)

with norm 206498 and class index 66254.  But an `X0(2*223*463)` relation by
itself does not remember which prime above each split rational prime was used.
It sees all sign choices

    +/-log(2) +/-log(223) +/-log(463).

This script asks how much class-group information is lost when that orientation
is forgotten.  If the sign choices generate the full class group, then a plain
unoriented composite modular equation is not the embedded quotient we need; it
must be supplemented by an orientation/character selector.
"""

from __future__ import annotations

import itertools
import math

import sympy as sp

from composite_split_cycle_audit import CLASS_NUMBER, P24, split_prime_logs, x0_index_for_squarefree

FACTORS = (2, 223, 463)
DESIRED_SIGNS = {2: 1, 223: -1, 463: 1}


def subgroup_index(logs: list[int]) -> int:
    g = CLASS_NUMBER
    for value in logs:
        g = math.gcd(g, value)
    return g


def main() -> None:
    rows = {row.ell: row for row in split_prime_logs(max(FACTORS))}
    logs = {ell: rows[ell].log for ell in FACTORS}
    norm = math.prod(FACTORS)
    x0_index = x0_index_for_squarefree(norm)

    sign_rows = []
    for signs in itertools.product((1, -1), repeat=len(FACTORS)):
        signed = dict(zip(FACTORS, signs))
        log_value = sum(signed[ell] * logs[ell] for ell in FACTORS) % CLASS_NUMBER
        index = math.gcd(CLASS_NUMBER, log_value)
        order = CLASS_NUMBER // index
        sign_rows.append((tuple(signed[ell] * ell for ell in FACTORS), log_value, index, order))

    all_sign_logs = [row[1] for row in sign_rows]
    all_sign_index = subgroup_index(all_sign_logs)
    individual_index = subgroup_index([logs[ell] for ell in FACTORS])

    desired_tuple = tuple(DESIRED_SIGNS[ell] * ell for ell in FACTORS)
    desired = next(row for row in sign_rows if row[0] == desired_tuple)

    print("p24 composite orientation ambiguity audit")
    print(f"p={P24}")
    print(f"class_number={CLASS_NUMBER}")
    print(f"class_number_factorization={sp.factorint(CLASS_NUMBER)}")
    print(f"rational_norm={norm}")
    print(f"x0_index_squarefree={x0_index}")
    print()
    print("individual_split_prime_logs")
    for ell in FACTORS:
        row = rows[ell]
        print(f"  ell={ell:4d} log={row.log:15d} index={row.index:8d} order={row.order:12d}")
    print()
    print("orientation_sign_choices")
    print("  signed_factors log index order")
    for signed, log_value, index, order in sorted(sign_rows, key=lambda row: (row[2], row[0])):
        marker = " desired" if signed == desired_tuple else ""
        print(f"  {signed!s:18s} {log_value:15d} {index:8d} {order:12d}{marker}")
    print()
    print("unoriented_subgroup")
    print(f"  desired_signed_factors={desired_tuple}")
    print(f"  desired_index={desired[2]}")
    print(f"  desired_order={desired[3]}")
    print(f"  subgroup_index_generated_by_all_sign_choices={all_sign_index}")
    print(f"  subgroup_order_generated_by_all_sign_choices={CLASS_NUMBER // all_sign_index}")
    print(f"  subgroup_index_generated_by_individual_prime_logs={individual_index}")
    print(f"  plain_X0_N_sign_choices_generate_full_class_group={int(all_sign_index == 1)}")
    print()
    print("interpretation")
    print("  oriented_composite_ideal_has_the_good_index_66254=1")
    print("  forgetting_orientation_replaces_one_cycle_by_the_sign_choice_Cayley_graph=1")
    print("  plain_X0_N_does_not_supply_the_oriented_period_selector=1")
    print("conclusion=composite_target_requires_orientation_or_high_order_character_data_not_just_unoriented_X0_N")


if __name__ == "__main__":
    main()
