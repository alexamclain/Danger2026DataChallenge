#!/usr/bin/env python3
"""Middle-trace genus alignment audit.

The middle strict p24 trace has very small split-cycle quotients, but those
quotients are genus-level information.  This script records the arithmetic in
a reproducible, low-cost form so it is visible beside the non-genus order-19
and third-trace composite targets.
"""

from __future__ import annotations

import math

import sympy as sp

P24 = 10**24 + 7
SQRT_P = math.isqrt(P24)
TRACE = -78903246840
D_K = -998443569409526507503607
CLASS_NUMBER = 833035208344
CLASS_GROUP_SHAPE = (208258802086, 2, 2)
PRIME_DISCRIMINANTS = (-7, -211, 4973929, -135907507341779)

ROWS = (
    {"ell": 2, "order": 208258802086, "index": 4, "x0_degree": 3},
    {"ell": 11, "order": 104129401043, "index": 8, "x0_degree": 12},
)


def signature(a: int) -> tuple[int, ...]:
    return tuple(int(sp.kronecker_symbol(d, a)) for d in PRIME_DISCRIMINANTS)


def main() -> None:
    print("middle trace genus/split alignment audit")
    print(f"p={P24}")
    print(f"sqrt_floor={SQRT_P}")
    print(f"trace={TRACE}")
    print(f"fundamental_D_K={D_K}")
    print(f"class_number={CLASS_NUMBER}")
    print(f"class_number_factorization={sp.factorint(CLASS_NUMBER)}")
    print(f"class_group_shape={CLASS_GROUP_SHAPE}")
    print(f"prime_discriminants={PRIME_DISCRIMINANTS}")
    print("redei_4_rank=0")
    print("genus_count=8")
    print(f"p_signature={signature(P24)}")
    print()

    print("split_prime_rows")
    print("  ell order index x0_degree seeded_proxy seeded_over_sqrt genus_signature")
    for row in ROWS:
        seeded = row["order"] * row["x0_degree"]
        print(
            f"  {row['ell']:3d} {row['order']:12d} {row['index']:5d} "
            f"{row['x0_degree']:9d} {seeded:13d} "
            f"{seeded / SQRT_P:16.6f} {signature(row['ell'])}"
        )
    print()

    print("interpretation")
    print("  ell_11_is_principal_genus_cycle=1")
    print("  ell_2_is_partial_genus_quotient=1")
    print("  p_splits_in_the_genus_field=1")
    print("  genus_data_does_not_select_a_j_root=1")
    print("  residual_recovery_degree_for_ell_11_is_104129401043=1")
    print("conclusion=middle_trace_quotient_is_easy_genus_data_but_not_a_certificate_selector")


if __name__ == "__main__":
    main()
