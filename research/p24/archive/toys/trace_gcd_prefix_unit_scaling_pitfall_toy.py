#!/usr/bin/env python3
"""Toy showing target-algebra unit scaling is not rank-safe.

In the Gaussian DFT form, D_{a,j}=G_a*U_{a,j}.  Each G_a is a unit in the
target algebra, but it is not a base-field scalar.  Multiplying different
columns by different target units can change base-field linear independence.

This F_4/F_2 toy is the minimal example:

    1 and alpha are F_2-independent,
    multiplying alpha by alpha^{-1} gives 1 and 1, dependent.
"""

from __future__ import annotations

from k_character_tensor_rank_scan import ExtensionField, find_irreducible_modulus
from l1_axis_injectivity_scan import rank_mod_q


def main() -> None:
    q = 2
    field = ExtensionField(q, 2, find_irreducible_modulus(q, 2, 20260606))
    alpha = (0, 1)
    if alpha == field.zero:
        raise AssertionError("bad alpha")
    alpha_inv = field.inv(alpha)

    original = [field.one, alpha]
    scaled = [field.one, field.mul(alpha_inv, alpha)]
    base_scaled = [field.one, field.scalar_mul(1, alpha)]

    original_rank = rank_mod_q([list(value) for value in original], q)
    scaled_rank = rank_mod_q([list(value) for value in scaled], q)
    base_scaled_rank = rank_mod_q([list(value) for value in base_scaled], q)

    print("Trace-GCD prefix target-unit scaling pitfall toy")
    print(f"q={q}")
    print(f"field_degree={field.degree}")
    print(f"alpha={alpha}")
    print(f"alpha_inv={alpha_inv}")
    print(f"original={original}")
    print(f"scaled_by_target_unit={scaled}")
    print(f"scaled_by_base_scalar={base_scaled}")
    print(f"original_fp_rank={original_rank}")
    print(f"target_unit_scaled_fp_rank={scaled_rank}")
    print(f"base_scalar_scaled_fp_rank={base_scaled_rank}")
    print("interpretation")
    print(
        "  target_unit_column_scaling_can_change_base_rank="
        f"{int(original_rank != scaled_rank)}"
    )
    print(
        "  base_scalar_column_scaling_preserves_base_rank="
        f"{int(original_rank == base_scaled_rank)}"
    )
    print("  gaussian_Ga_units_are_not_individually_divisible_for_full_rank=1")
    print("conclusion=reported_trace_gcd_prefix_unit_scaling_pitfall_toy")


if __name__ == "__main__":
    main()
