#!/usr/bin/env python3
"""Audit direct inverse witnesses for the full beta-algebra determinant.

If `delta_all` is a unit in the full beta algebra, a literal certificate could
carry its inverse.  This is usually the wrong surface: in the cyclic
interpolation model, the inverse is obtained by interpolating the pointwise
inverse beta sequence, and it may be just as dense as the determinant itself.

This script checks compact CM trace-frame rows and measures whether the
interpolant for `D_beta` or `1/D_beta` has sparse support, subfield descent, or
an unexpectedly small coefficient-orbit support.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass

import sympy as sp

from k_character_tensor_factor_rank_scan import (
    equal_degree_factors,
    sympy_factor_to_poly_e,
)
from k_character_tensor_rank_scan import ExtensionField, FpE, find_irreducible_modulus
from trace_frame_beta_product_resultant_audit import (
    PolyB,
    b_equal,
    b_lands_in_E,
    b_subfield_degree,
    beta_orbits,
    cyclic_interpolation_coeffs,
    find_case,
)
from tensor_factor_dual_basis_window_audit import theta_element
from tensor_factor_moore_audit import b_add, b_is_zero, b_mul, b_one, b_pow
from tensor_factor_subfield_trace_audit import divisors
from trace_frame_residual_tail_origin_action_audit import OriginTailRow, rows_for_case


@dataclass(frozen=True)
class InverseWitnessRow:
    D: int
    q: int
    h: int
    m: int
    n: int
    target: str
    subdegree: int
    determinant_kind: str
    raw_rank: int
    top_count: int
    residual_dim: int
    value_zero_count: int
    value_distinct: int
    interpolant_support: int
    inverse_support: int
    interpolant_e_coeffs: int
    inverse_e_coeffs: int
    interpolant_subfield_hist: tuple[tuple[int, int], ...]
    inverse_subfield_hist: tuple[tuple[int, int], ...]
    coefficient_orbit_count: int
    interpolant_orbit_support: int
    inverse_orbit_support: int
    inverse_identity_holds: bool


def cyclic_convolution(
    left: list[PolyB],
    right: list[PolyB],
    modulus: PolyB,
    field: ExtensionField,
) -> list[PolyB]:
    n = len(left)
    out = [[field.zero] for _ in range(n)]
    for i, a in enumerate(left):
        if b_is_zero(a, field):
            continue
        for j, b in enumerate(right):
            if b_is_zero(b, field):
                continue
            k = (i + j) % n
            out[k] = b_add(out[k], b_mul(a, b, modulus, field), modulus, field)
    return out


def support(coeffs: list[PolyB], field: ExtensionField) -> int:
    return sum(1 for coeff in coeffs if not b_is_zero(coeff, field))


def e_coeffs(coeffs: list[PolyB], field: ExtensionField) -> int:
    return sum(1 for coeff in coeffs if b_lands_in_E(coeff, field))


def subfield_hist(
    coeffs: list[PolyB],
    factor_degree: int,
    modulus: PolyB,
    field: ExtensionField,
) -> tuple[tuple[int, int], ...]:
    hist = Counter(
        b_subfield_degree(coeff, factor_degree, modulus, field)
        for coeff in coeffs
        if not b_is_zero(coeff, field)
    )
    return tuple(sorted(hist.items()))


def orbit_support(
    coeffs: list[PolyB],
    multiplier: int,
    field: ExtensionField,
) -> int:
    return sum(
        1 for orbit in beta_orbits(len(coeffs), multiplier)
        if not b_is_zero(coeffs[orbit[0]], field)
    )


def summarize_group(
    group_rows: list[OriginTailRow],
    selected_factor: PolyB,
    factor_degree: int,
    field: ExtensionField,
    determinant_kind: str,
) -> InverseWitnessRow | None:
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
        return None

    values = [by_beta[beta] for beta in range(n)]
    zero_count = sum(1 for value in values if value == field.zero)
    if zero_count:
        return None

    # `theta_element(field)` is the class of X; theta^(n-1) is theta^-1
    # because theta has order n in the selected packet factor.
    theta = theta_element(field)
    theta_inv = b_pow(theta, n - 1, selected_factor, field)
    coeffs = cyclic_interpolation_coeffs(
        values,
        theta_inv,
        theta,
        selected_factor,
        field,
    )
    inverse_values = [field.inv(value) for value in values]
    inverse_coeffs = cyclic_interpolation_coeffs(
        inverse_values,
        theta_inv,
        theta,
        selected_factor,
        field,
    )

    product = cyclic_convolution(coeffs, inverse_coeffs, selected_factor, field)
    identity = [b_one(field)] + [[field.zero] for _ in range(n - 1)]
    Q_mod_n = pow(field.q, field.degree, n)
    first = group_rows[0]
    return InverseWitnessRow(
        D=first.D,
        q=first.q,
        h=first.h,
        m=first.m,
        n=first.n,
        target=first.target,
        subdegree=first.subdegree,
        determinant_kind=determinant_kind,
        raw_rank=first.raw_rank,
        top_count=first.top_count,
        residual_dim=first.residual_dim,
        value_zero_count=zero_count,
        value_distinct=len(set(values)),
        interpolant_support=support(coeffs, field),
        inverse_support=support(inverse_coeffs, field),
        interpolant_e_coeffs=e_coeffs(coeffs, field),
        inverse_e_coeffs=e_coeffs(inverse_coeffs, field),
        interpolant_subfield_hist=subfield_hist(
            coeffs, factor_degree, selected_factor, field
        ),
        inverse_subfield_hist=subfield_hist(
            inverse_coeffs, factor_degree, selected_factor, field
        ),
        coefficient_orbit_count=len(beta_orbits(n, Q_mod_n)),
        interpolant_orbit_support=orbit_support(coeffs, Q_mod_n, field),
        inverse_orbit_support=orbit_support(inverse_coeffs, Q_mod_n, field),
        inverse_identity_holds=all(
            b_equal(left, right, field)
            for left, right in zip(product, identity)
        ),
    )


def fmt_hist(hist: tuple[tuple[int, int], ...]) -> str:
    return "[" + ",".join(f"{degree}:{count}" for degree, count in hist) + "]"


def audit(args: argparse.Namespace) -> list[InverseWitnessRow]:
    case = find_case(args)
    if case is None:
        raise SystemExit("no eligible case found")
    D, q, ell, cycle, m, factor = case
    extension_degree = int(sp.n_order(q % m, m))
    modulus = find_irreducible_modulus(q, extension_degree, args.seed)
    field = ExtensionField(q, extension_degree, modulus)
    tensor_factor_degree = factor.degree() // int(sp.igcd(factor.degree(), extension_degree))
    selected_factor = equal_degree_factors(
        sympy_factor_to_poly_e(factor, field),
        tensor_factor_degree,
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

    out: list[InverseWitnessRow] = []
    for group in groups.values():
        full = summarize_group(
            group, selected_factor, tensor_factor_degree, field, "full"
        )
        if full is not None:
            out.append(full)
        if all(row.tail_det is not None for row in group):
            tail = summarize_group(
                group, selected_factor, tensor_factor_degree, field, "tail"
            )
            if tail is not None:
                out.append(tail)
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
    print("trace-frame beta inverse-witness audit")
    print(f"rows={len(rows)}")
    print(
        "columns: D q h m n target subdeg kind raw top residual_dim "
        "distinct zeros support inv_support E_coeffs inv_E_coeffs "
        "subfield_hist inv_subfield_hist coeff_orbits orbit_support "
        "inv_orbit_support inverse_identity"
    )
    for row in rows:
        print(
            f"D={row.D} q={row.q} h={row.h} m={row.m} n={row.n} "
            f"target={row.target} subdeg={row.subdegree} "
            f"kind={row.determinant_kind} raw={row.raw_rank} "
            f"top={row.top_count} residual_dim={row.residual_dim} "
            f"distinct={row.value_distinct} zeros={row.value_zero_count} "
            f"support={row.interpolant_support} "
            f"inv_support={row.inverse_support} "
            f"E_coeffs={row.interpolant_e_coeffs} "
            f"inv_E_coeffs={row.inverse_e_coeffs} "
            f"subfield_hist={fmt_hist(row.interpolant_subfield_hist)} "
            f"inv_subfield_hist={fmt_hist(row.inverse_subfield_hist)} "
            f"coeff_orbits={row.coefficient_orbit_count} "
            f"orbit_support={row.interpolant_orbit_support} "
            f"inv_orbit_support={row.inverse_orbit_support} "
            f"inverse_identity={int(row.inverse_identity_holds)}"
        )
    print()
    print("interpretation")
    print("  inv_support_equal_n_means_literal_inverse_is_dense_in_beta.")
    print("  inv_orbit_support_equal_orbits_means no orbit-sparse inverse witness.")
    print("  inv_E_coeffs_less_than_n means inverse does not descend to E[Y].")
    print("  inverse_identity=1 checks f*g=1 in B[Y]/(Y^n-1).")
    print("conclusion=reported_trace_frame_beta_inverse_witness_audit")


if __name__ == "__main__":
    main()
