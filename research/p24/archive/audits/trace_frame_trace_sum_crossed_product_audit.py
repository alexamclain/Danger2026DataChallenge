#!/usr/bin/env python3
"""Block/crossed-product audit for trace-frame beta resultants.

The cyclic-resultant audit proves

    prod_beta D_beta = det(mul_f on B[Y]/(Y^n - 1)).

This script refines that finite identity by splitting `Y^n - 1` into
Frobenius-orbit factors over E.  For a beta orbit O, let

    phi_O(Y) = prod_{beta in O} (Y - theta^(-beta)) in E[Y].

Then the orbit product should equal the B-linear block determinant

    det(mul_f on B[Y]/phi_O) = prod_{beta in O} D_beta.

This is the concrete commutative shadow of the semilinear/crossed-product
fixed algebra.  The same run also checks the tempting but false ordinary-norm
collapse `prod_O D_beta = D_rep^|O|`.
"""

from __future__ import annotations

import argparse
from collections import defaultdict

import sympy as sp

from k_character_tensor_factor_rank_scan import (
    equal_degree_factors,
    sympy_factor_to_poly_e,
    trim,
)
from k_character_tensor_rank_scan import ExtensionField, FpE, find_irreducible_modulus
from tensor_factor_dual_basis_window_audit import theta_element
from tensor_factor_moore_audit import (
    b_add,
    b_is_zero,
    b_mul,
    b_one,
    b_pow,
    b_sub,
)
from trace_frame_beta_product_resultant_audit import (
    PolyB,
    b_det,
    b_embed,
    b_equal,
    beta_orbits,
    cyclic_interpolation_coeffs,
    e_product,
    find_case,
    norm_base,
)
from trace_frame_residual_tail_origin_action_audit import (
    OriginTailRow,
    determinant,
    rows_for_case,
)


def b_neg(value: PolyB, modulus: PolyB, field: ExtensionField) -> PolyB:
    return b_sub([field.zero], value, modulus, field)


def y_poly_mul(
    left: list[PolyB],
    right: list[PolyB],
    modulus: PolyB,
    field: ExtensionField,
) -> list[PolyB]:
    out = [[field.zero] for _ in range(len(left) + len(right) - 1)]
    for i, a in enumerate(left):
        if b_is_zero(a, field):
            continue
        for j, b in enumerate(right):
            if b_is_zero(b, field):
                continue
            out[i + j] = b_add(out[i + j], b_mul(a, b, modulus, field), modulus, field)
    return y_trim(out, field)


def y_trim(poly: list[PolyB], field: ExtensionField) -> list[PolyB]:
    out = [trim(coeff, field) for coeff in poly]
    while len(out) > 1 and b_is_zero(out[-1], field):
        out.pop()
    return out


def orbit_factor(roots: list[PolyB], modulus: PolyB, field: ExtensionField) -> list[PolyB]:
    poly = [b_one(field)]
    for root in roots:
        poly = y_poly_mul([b_neg(root, modulus, field), b_one(field)], poly, modulus, field)
    return y_trim(poly, field)


def y_mod(poly: list[PolyB], divisor: list[PolyB], modulus: PolyB, field: ExtensionField) -> list[PolyB]:
    poly = y_trim(poly[:], field)
    divisor = y_trim(divisor, field)
    degree = len(divisor) - 1
    if degree <= 0 or not b_equal(divisor[-1], b_one(field), field):
        raise ValueError("monic positive-degree divisor expected")
    while len(poly) >= len(divisor):
        lead = poly[-1]
        if not b_is_zero(lead, field):
            shift = len(poly) - len(divisor)
            for i, coeff in enumerate(divisor[:-1]):
                poly[shift + i] = b_sub(
                    poly[shift + i],
                    b_mul(lead, coeff, modulus, field),
                    modulus,
                    field,
                )
        poly.pop()
        poly = y_trim(poly, field)
    while len(poly) < degree:
        poly.append([field.zero])
    return poly[:degree]


def y_mul_mod(
    left: list[PolyB],
    right: list[PolyB],
    divisor: list[PolyB],
    modulus: PolyB,
    field: ExtensionField,
) -> list[PolyB]:
    return y_mod(y_poly_mul(left, right, modulus, field), divisor, modulus, field)


def block_determinant(
    coeffs: list[PolyB],
    divisor: list[PolyB],
    modulus: PolyB,
    field: ExtensionField,
) -> PolyB:
    degree = len(divisor) - 1
    reduced = y_mod(coeffs, divisor, modulus, field)
    matrix: list[list[PolyB]] = []
    for row in range(degree):
        matrix_row: list[PolyB] = []
        for col in range(degree):
            basis = [[field.zero] for _ in range(col)] + [b_one(field)]
            product = y_mul_mod(reduced, basis, divisor, modulus, field)
            matrix_row.append(product[row])
        matrix.append(matrix_row)
    return b_det(matrix, modulus, field)


def e_pow(value: FpE, exponent: int, field: ExtensionField) -> FpE:
    out = field.one
    base = value
    n = exponent
    while n:
        if n & 1:
            out = field.mul(out, base)
        base = field.mul(base, base)
        n >>= 1
    return out


def weighted_shift_det(values: list[FpE], field: ExtensionField) -> FpE:
    """Determinant of e_r -> values[r] e_{r+1}."""

    degree = len(values)
    matrix = [[field.zero for _ in range(degree)] for _ in range(degree)]
    for col, value in enumerate(values):
        matrix[(col + 1) % degree][col] = value
    return determinant(matrix, field)


def summarize_group(
    group_rows: list[OriginTailRow],
    selected_factor: PolyB,
    factor_degree: int,
    field: ExtensionField,
    determinant_kind: str,
) -> list[dict[str, object]]:
    n = group_rows[0].n
    by_beta: dict[int, FpE] = {}
    for row in group_rows:
        if row.alpha != 0:
            continue
        value = row.full_det if determinant_kind == "full" else row.tail_det
        if value is None:
            continue
        by_beta[row.beta] = value
    if len(by_beta) != n:
        return []

    values = [by_beta[beta] for beta in range(n)]
    theta = theta_element(field)
    theta_inv = b_pow(theta, n - 1, selected_factor, field)
    coeffs = cyclic_interpolation_coeffs(values, theta_inv, theta, selected_factor, field)
    Q_mod_n = pow(field.q, field.degree, n)
    orbits = beta_orbits(n, Q_mod_n)

    theta_inv_powers = [b_one(field)]
    for _ in range(1, n):
        theta_inv_powers.append(
            b_mul(theta_inv_powers[-1], theta_inv, selected_factor, field)
        )

    out: list[dict[str, object]] = []
    first = group_rows[0]
    for orbit_index, orbit in enumerate(orbits):
        roots = [theta_inv_powers[beta] for beta in orbit]
        phi = orbit_factor(roots, selected_factor, field)
        phi_e_coeffs = sum(1 for coeff in phi if len(trim(coeff, field)) == 1)
        orbit_values = [values[beta] for beta in orbit]
        direct_e = e_product(orbit_values, field)
        direct_b = b_embed(direct_e)
        block_det = block_determinant(coeffs, phi, selected_factor, field)
        shift_det = weighted_shift_det(orbit_values, field)
        signed_direct = direct_e if len(orbit) % 2 == 1 else field.neg(direct_e)
        representative = values[orbit[0]]
        ordinary_power = e_pow(representative, len(orbit), field)
        out.append(
            {
                "D": first.D,
                "q": first.q,
                "h": first.h,
                "m": first.m,
                "n": first.n,
                "target": first.target,
                "subdegree": first.subdegree,
                "kind": determinant_kind,
                "raw_rank": first.raw_rank,
                "top_count": first.top_count,
                "residual_dim": first.residual_dim,
                "orbit_index": orbit_index,
                "orbit_len": len(orbit),
                "orbit_rep": orbit[0],
                "value_constant": len({values[beta] for beta in orbit}) == 1,
                "phi_degree": len(phi) - 1,
                "phi_e_coeffs": phi_e_coeffs,
                "block_det_match": b_equal(block_det, direct_b, field),
                "block_det_in_E": len(trim(block_det, field)) == 1,
                "block_det_zero": b_is_zero(block_det, field),
                "block_det_norm": norm_base(direct_e, field),
                "weighted_shift_match": shift_det == signed_direct,
                "ordinary_power_match": ordinary_power == direct_e,
            }
        )
    return out


def audit(args: argparse.Namespace) -> list[dict[str, object]]:
    case = find_case(args)
    if case is None:
        raise SystemExit("no eligible case found")
    D, q, ell, cycle, m, factor = case
    extension_degree = int(sp.n_order(q % m, m))
    modulus = find_irreducible_modulus(q, extension_degree, args.seed)
    field = ExtensionField(q, extension_degree, modulus)
    factor_degree = factor.degree() // int(sp.igcd(factor.degree(), extension_degree))
    selected_factor = equal_degree_factors(
        sympy_factor_to_poly_e(factor, field),
        factor_degree,
        field,
        args.seed,
    )[0]

    rows = rows_for_case(
        D,
        q,
        ell,
        cycle,
        m,
        factor,
        args.target or ["axis"],
        args.seed,
        args.max_top_count,
    )
    groups: dict[tuple[str, int], list[OriginTailRow]] = defaultdict(list)
    for row in rows:
        groups[(row.target, row.subdegree)].append(row)

    out: list[dict[str, object]] = []
    for group in groups.values():
        out.extend(summarize_group(group, selected_factor, factor_degree, field, "full"))
        if all(row.tail_det is not None for row in group):
            out.extend(summarize_group(group, selected_factor, factor_degree, field, "tail"))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-abs-D", type=int, default=20000)
    ap.add_argument("--only-D", type=int, default=None)
    ap.add_argument("--min-h", type=int, default=1)
    ap.add_argument("--max-h", type=int, default=240)
    ap.add_argument("--min-n", type=int, default=2)
    ap.add_argument("--max-n", type=int, default=240)
    ap.add_argument("--max-m", type=int, default=48)
    ap.add_argument("--only-m", type=int, default=None)
    ap.add_argument("--q-start", type=int, default=101)
    ap.add_argument("--q-stop", type=int, default=20000)
    ap.add_argument("--max-splitting-primes", type=int, default=1)
    ap.add_argument("--max-prime-quotients", type=int, default=48)
    ap.add_argument("--max-composite-quotients", type=int, default=48)
    ap.add_argument("--max-factor-degree", type=int, default=24)
    ap.add_argument("--max-extension-degree", type=int, default=8)
    ap.add_argument("--max-tensor-factor-degree", type=int, default=14)
    ap.add_argument("--min-tensor-factor-count", type=int, default=1)
    ap.add_argument("--max-top-count", type=int, default=4)
    ap.add_argument("--max-cases", type=int, default=4)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--include-linear", action="store_true")
    ap.add_argument("--require-composite-m", action="store_true")
    ap.add_argument("--target", action="append")
    args = ap.parse_args()

    rows = audit(args)
    print("trace-frame trace-sum crossed-product block audit")
    print(f"rows={len(rows)}")
    print(
        "columns: D q h m n target subdeg kind raw top residual_dim "
        "orbit rep len constant phi_degree phi_E_coeffs "
        "block_det_match block_det_in_E block_det_zero block_det_norm "
        "weighted_shift_match ordinary_power_match"
    )
    for row in rows:
        print(
            f"D={row['D']} q={row['q']} h={row['h']} m={row['m']} n={row['n']} "
            f"target={row['target']} subdeg={row['subdegree']} kind={row['kind']} "
            f"raw={row['raw_rank']} top={row['top_count']} "
            f"residual_dim={row['residual_dim']} "
            f"orbit={row['orbit_index']} rep={row['orbit_rep']} len={row['orbit_len']} "
            f"constant={int(row['value_constant'])} "
            f"phi_degree={row['phi_degree']} phi_E_coeffs={row['phi_e_coeffs']} "
            f"block_det_match={int(row['block_det_match'])} "
            f"block_det_in_E={int(row['block_det_in_E'])} "
            f"block_det_zero={int(row['block_det_zero'])} "
            f"block_det_norm={row['block_det_norm'] if row['block_det_norm'] is not None else 'NA'} "
            f"weighted_shift_match={int(row['weighted_shift_match'])} "
            f"ordinary_power_match={int(row['ordinary_power_match'])}"
        )
    print()
    print("interpretation")
    print("  block_det_match=1 is the Frobenius-orbit factor identity.")
    print("  weighted_shift_match=1 is the crossed-product weighted-cycle norm identity.")
    print("  phi_E_coeffs=phi_degree+1 confirms each block is defined over E.")
    print("  ordinary_power_match=0 on nonconstant orbits rules out ordinary norm collapse.")
    print("  p24 analogue has one degree-1 block and 560 degree-5549 blocks.")
    print("conclusion=reported_trace_sum_crossed_product_block_audit")


if __name__ == "__main__":
    main()
