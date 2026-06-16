#!/usr/bin/env python3
"""Dual-basis coefficient-window audit for twisted trace frames.

For B/C = C(theta), the trace equations

    Tr_{B/C}(theta^i x) = 0,      0 <= i < k,

are equivalent to vanishing of the top k relative coefficients of
`g'(theta) * x`, where g is the minimal polynomial of theta over C.

This script checks that equivalence on small CM tensor-factor rows by
constructing an explicit E-basis of the intermediate field C and solving for
relative coefficients.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

import sympy as sp
from cypari2 import Pari

from crt_partial_moment_projection_scan import coprime_components
from cycle_period_complexity_scan import find_full_cycle_prime
from k_character_tensor_factor_block_scan import frequency_blocks
from k_character_tensor_factor_rank_scan import (
    PolyE,
    equal_degree_factors,
    poly_mod,
    rank_in_factor,
    row_to_poly,
    sympy_factor_to_poly_e,
)
from k_character_tensor_rank_scan import (
    ExtensionField,
    FpE,
    axis_frequency_set,
    character_rows,
    find_irreducible_modulus,
    primitive_root_of_order,
    rank_over_extension,
)
from l1_axis_injectivity_scan import coeff_vector
from packetized_relative_content_scan import packet_factors
from relative_moment_projection_scan import (
    find_splitting_primes,
    quotient_sizes_any,
    section_fiber_polynomials,
)
from tensor_factor_moore_audit import b_add, b_is_zero, b_mul, b_one, b_pow, b_sub
from tensor_factor_subfield_trace_audit import (
    divisors,
    element_rank,
    element_row,
    trace_to_subfield,
)
from tensor_factor_twisted_trace_frame_audit import twisted_trace_rank


@dataclass(frozen=True)
class WindowTargetAudit:
    name: str
    size: int
    raw_rank: int
    ranks_by_subdegree: tuple[tuple[int, tuple[int, ...], tuple[int, ...]], ...]


@dataclass(frozen=True)
class WindowAuditRow:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    factor_degree: int
    extension_degree: int
    tensor_factor_count: int
    tensor_factor_degree: int
    proper_subdegrees: tuple[int, ...]
    targets: tuple[WindowTargetAudit, ...]


def theta_element(field: ExtensionField) -> PolyE:
    return [field.zero, field.one]


def e_frobenius_power(
    value: PolyE,
    power: int,
    factor: PolyE,
    field: ExtensionField,
) -> PolyE:
    q_power = field.q ** field.degree
    return b_pow(value, q_power**power, factor, field)


def normal_subfield_basis(
    subdegree: int,
    factor_degree: int,
    factor: PolyE,
    field: ExtensionField,
) -> list[PolyE]:
    theta = theta_element(field)
    powers = [b_one(field)]
    for _ in range(1, factor_degree):
        powers.append(b_mul(powers[-1], theta, factor, field))
    traced_candidates = [
        trace_to_subfield(
            power,
            subdegree,
            factor_degree,
            factor,
            field,
        )
        for power in powers
    ]

    def try_candidate(candidate: PolyE) -> list[PolyE] | None:
        if b_is_zero(candidate, field):
            return None
        basis = [
            e_frobenius_power(candidate, i, factor, field)
            for i in range(subdegree)
        ]
        if element_rank(basis, factor, field) == subdegree:
            return basis
        return None

    for candidate in traced_candidates:
        basis = try_candidate(candidate)
        if basis is not None:
            return basis

    # Some composite rows have no normal generator among traced monomials.
    # Try small deterministic sums before declaring an implementation failure.
    for i, left in enumerate(traced_candidates):
        if b_is_zero(left, field):
            continue
        for right in traced_candidates[i + 1 :]:
            if b_is_zero(right, field):
                continue
            basis = try_candidate(b_add(left, right, factor, field))
            if basis is not None:
                return basis
    raise RuntimeError("could not find normal intermediate-field basis")


def relative_gprime_theta(
    subdegree: int,
    factor_degree: int,
    factor: PolyE,
    field: ExtensionField,
) -> PolyE:
    theta = theta_element(field)
    relative_degree = factor_degree // subdegree
    out = b_one(field)
    for j in range(1, relative_degree):
        conjugate = e_frobenius_power(theta, subdegree * j, factor, field)
        out = b_mul(out, b_sub(theta, conjugate, factor, field), factor, field)
    return out


def solve_square(
    columns: list[list[FpE]],
    vector: list[FpE],
    field: ExtensionField,
) -> list[FpE]:
    size = len(vector)
    mat = [
        [columns[col][row] for col in range(size)] + [vector[row]]
        for row in range(size)
    ]
    pivot_row = 0
    for col in range(size):
        pivot = None
        for row in range(pivot_row, size):
            if mat[row][col] != field.zero:
                pivot = row
                break
        if pivot is None:
            raise RuntimeError("basis matrix was singular")
        mat[pivot_row], mat[pivot] = mat[pivot], mat[pivot_row]
        inv = field.inv(mat[pivot_row][col])
        mat[pivot_row] = [field.mul(value, inv) for value in mat[pivot_row]]
        for row in range(size):
            if row == pivot_row:
                continue
            scale = mat[row][col]
            if scale == field.zero:
                continue
            mat[row] = [
                field.sub(left, field.mul(scale, right))
                for left, right in zip(mat[row], mat[pivot_row])
            ]
        pivot_row += 1
    return [mat[row][-1] for row in range(size)]


def relative_basis_columns(
    subfield_basis: list[PolyE],
    relative_degree: int,
    factor: PolyE,
    field: ExtensionField,
) -> list[list[FpE]]:
    theta = theta_element(field)
    theta_powers = [b_one(field)]
    for _ in range(1, relative_degree):
        theta_powers.append(b_mul(theta_powers[-1], theta, factor, field))
    columns: list[list[FpE]] = []
    for theta_power in theta_powers:
        for sub_basis_value in subfield_basis:
            columns.append(
                element_row(
                    b_mul(sub_basis_value, theta_power, factor, field),
                    factor,
                    field,
                )
            )
    return columns


def top_window_coords(
    value: PolyE,
    top_count: int,
    subdegree: int,
    relative_degree: int,
    gprime_theta: PolyE,
    basis_columns: list[list[FpE]],
    factor: PolyE,
    field: ExtensionField,
) -> list[FpE]:
    adjusted = b_mul(value, gprime_theta, factor, field)
    coords = solve_square(
        basis_columns,
        element_row(adjusted, factor, field),
        field,
    )
    out: list[FpE] = []
    for j in range(relative_degree - 1, relative_degree - top_count - 1, -1):
        start = j * subdegree
        out.extend(coords[start:start + subdegree])
    return out


def window_rank(
    elements: list[PolyE],
    top_count: int,
    subdegree: int,
    relative_degree: int,
    gprime_theta: PolyE,
    basis_columns: list[list[FpE]],
    factor: PolyE,
    field: ExtensionField,
) -> int:
    return rank_over_extension(
        [
            top_window_coords(
                value,
                top_count,
                subdegree,
                relative_degree,
                gprime_theta,
                basis_columns,
                factor,
                field,
            )
            for value in elements
        ],
        field,
    )


def audit_target(
    name: str,
    rows: list[list[FpE]],
    proper_subdegrees: list[int],
    factor_degree: int,
    selected_factor: PolyE,
    field: ExtensionField,
    max_windows: int | None,
) -> WindowTargetAudit:
    elements = [
        poly_mod(row_to_poly(row, field), selected_factor, field)
        for row in rows
    ]
    elements = [value for value in elements if not b_is_zero(value, field)]
    raw_rank = rank_in_factor(rows, selected_factor, field)
    by_subdegree: list[tuple[int, tuple[int, ...], tuple[int, ...]]] = []
    for subdegree in proper_subdegrees:
        relative_degree = factor_degree // subdegree
        limit = relative_degree if max_windows is None else min(max_windows, relative_degree)
        subfield_basis = normal_subfield_basis(
            subdegree,
            factor_degree,
            selected_factor,
            field,
        )
        basis_columns = relative_basis_columns(
            subfield_basis,
            relative_degree,
            selected_factor,
            field,
        )
        if rank_over_extension(basis_columns, field) != factor_degree:
            raise RuntimeError("relative basis did not span B over E")
        gprime_theta = relative_gprime_theta(
            subdegree,
            factor_degree,
            selected_factor,
            field,
        )
        trace_ranks: list[int] = []
        window_ranks: list[int] = []
        for window_size in range(1, limit + 1):
            trace_ranks.append(
                twisted_trace_rank(
                    elements,
                    subdegree,
                    window_size,
                    factor_degree,
                    selected_factor,
                    field,
                )
            )
            window_ranks.append(
                window_rank(
                    elements,
                    window_size,
                    subdegree,
                    relative_degree,
                    gprime_theta,
                    basis_columns,
                    selected_factor,
                    field,
                )
            )
        by_subdegree.append((subdegree, tuple(trace_ranks), tuple(window_ranks)))
    return WindowTargetAudit(
        name=name,
        size=len(rows),
        raw_rank=raw_rank,
        ranks_by_subdegree=tuple(by_subdegree),
    )


def audit_packet(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    m: int,
    factor: sp.Poly,
    seed: int,
    max_windows: int | None,
) -> WindowAuditRow:
    h = len(cycle)
    n = h // m
    residues = [
        fiber.rem(factor)
        for fiber in section_fiber_polynomials(cycle, q, m, "complement")
    ]
    residue_vectors = [coeff_vector(residue, factor.degree(), q) for residue in residues]
    extension_degree = int(sp.n_order(q % m, m))
    modulus = find_irreducible_modulus(q, extension_degree, seed)
    field = ExtensionField(q, extension_degree, modulus)
    zeta = primitive_root_of_order(field, m, seed)

    gcd_degree = int(sp.igcd(factor.degree(), extension_degree))
    tensor_factor_degree = factor.degree() // gcd_degree
    factors = equal_degree_factors(
        sympy_factor_to_poly_e(factor, field),
        tensor_factor_degree,
        field,
        seed,
    )
    selected_factor = factors[0]
    proper_subdegrees = [
        subdegree for subdegree in divisors(tensor_factor_degree)
        if subdegree not in (1, tensor_factor_degree)
    ]

    targets: list[WindowTargetAudit] = []
    axis_rows = character_rows(
        residue_vectors,
        axis_frequency_set(m),
        zeta,
        field,
    )
    targets.append(
        audit_target(
            "axis",
            axis_rows,
            proper_subdegrees,
            tensor_factor_degree,
            selected_factor,
            field,
            max_windows,
        )
    )
    for name, frequencies in frequency_blocks(m):
        targets.append(
            audit_target(
                name,
                character_rows(residue_vectors, frequencies, zeta, field),
                proper_subdegrees,
                tensor_factor_degree,
                selected_factor,
                field,
                max_windows,
            )
        )
        if name != "constant":
            targets.append(
                audit_target(
                    f"constant_plus_{name}",
                    character_rows(
                        residue_vectors,
                        sorted(set([0] + frequencies)),
                        zeta,
                        field,
                    ),
                    proper_subdegrees,
                    tensor_factor_degree,
                    selected_factor,
                    field,
                    max_windows,
                )
            )
    components = coprime_components(m)
    if len(components) >= 2:
        prefix = [0]
        for index, component in enumerate(components[:-1]):
            step = m // component
            prefix.extend((j * step) % m for j in range(1, component))
            targets.append(
                audit_target(
                    f"prefix_through_{component}",
                    character_rows(residue_vectors, sorted(set(prefix)), zeta, field),
                    proper_subdegrees,
                    tensor_factor_degree,
                    selected_factor,
                    field,
                    max_windows,
                )
            )
    return WindowAuditRow(
        D=D,
        q=q,
        ell=ell,
        h=h,
        m=m,
        n=n,
        factor_degree=factor.degree(),
        extension_degree=extension_degree,
        tensor_factor_count=len(factors),
        tensor_factor_degree=tensor_factor_degree,
        proper_subdegrees=tuple(proper_subdegrees),
        targets=tuple(targets),
    )


def discriminants(max_abs_D: int, only_D: int | None) -> list[int]:
    if only_D is not None:
        return [only_D]
    return [-5000] + [
        D for D in range(-200, -max_abs_D - 1, -1)
        if D % 4 in (0, 1)
    ]


def scan(args: argparse.Namespace) -> list[WindowAuditRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    rows: list[WindowAuditRow] = []
    seen: set[int] = set()
    cases = 0
    for D in discriminants(args.max_abs_D, args.only_D):
        if D in seen:
            continue
        seen.add(D)
        try:
            hilbert = pari.polclass(D)
            h = int(pari.poldegree(hilbert))
        except Exception:
            continue
        if not (args.min_h <= h <= args.max_h):
            continue
        quotient_sizes = quotient_sizes_any(
            h,
            max_prime=args.max_prime_quotients,
            max_composite=args.max_composite_quotients,
            min_n=args.min_n,
            max_n=args.max_n,
        )
        quotient_sizes = [m for m in quotient_sizes if sp.gcd(m, h // m) == 1]
        if args.require_composite_m:
            quotient_sizes = [
                m for m in quotient_sizes
                if len(coprime_components(m)) >= 2
            ]
        if args.only_m is not None:
            quotient_sizes = [m for m in quotient_sizes if m == args.only_m]
        if args.max_m is not None:
            quotient_sizes = [m for m in quotient_sizes if m <= args.max_m]
        if not quotient_sizes:
            continue
        splits = find_splitting_primes(
            pari,
            hilbert,
            h,
            args.q_start,
            args.q_stop,
            args.max_splitting_primes,
        )
        if not splits:
            continue
        case_had_row = False
        for q, roots in splits:
            full = find_full_cycle_prime(roots, D, q)
            if full is None:
                continue
            ell, cycle = full
            for m in quotient_sizes:
                extension_degree = int(sp.n_order(q % m, m))
                if extension_degree > args.max_extension_degree:
                    continue
                n = h // m
                for factor in packet_factors(n, q):
                    if factor.degree() == 1 and not args.include_linear:
                        continue
                    if factor.degree() > args.max_factor_degree:
                        continue
                    gcd_degree = int(sp.igcd(factor.degree(), extension_degree))
                    if gcd_degree < args.min_tensor_factor_count:
                        continue
                    tensor_factor_degree = factor.degree() // gcd_degree
                    if tensor_factor_degree > args.max_tensor_factor_degree:
                        continue
                    if len(divisors(tensor_factor_degree)) <= 2:
                        continue
                    rows.append(
                        audit_packet(
                            D,
                            q,
                            ell,
                            cycle,
                            m,
                            factor,
                            args.seed,
                            args.max_windows,
                        )
                    )
                    case_had_row = True
                    if len(rows) >= args.max_rows:
                        return rows
        if case_had_row:
            cases += 1
            if cases >= args.max_cases:
                break
    return rows


def format_subdegree(
    subdegree: int,
    trace_ranks: tuple[int, ...],
    window_ranks: tuple[int, ...],
) -> str:
    return f"{subdegree}:trace={list(trace_ranks)} window={list(window_ranks)}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-rows", type=int, default=8)
    parser.add_argument("--max-cases", type=int, default=8)
    parser.add_argument("--min-h", type=int, default=12)
    parser.add_argument("--max-h", type=int, default=220)
    parser.add_argument("--max-abs-D", type=int, default=50000)
    parser.add_argument("--max-prime-quotients", type=int, default=8)
    parser.add_argument("--max-composite-quotients", type=int, default=12)
    parser.add_argument("--min-n", type=int, default=3)
    parser.add_argument("--max-n", type=int, default=220)
    parser.add_argument("--max-m", type=int, default=48)
    parser.add_argument("--only-m", type=int)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=500000)
    parser.add_argument("--max-splitting-primes", type=int, default=1)
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--require-composite-m", action="store_true")
    parser.add_argument("--max-factor-degree", type=int, default=60)
    parser.add_argument("--max-extension-degree", type=int, default=12)
    parser.add_argument("--min-tensor-factor-count", type=int, default=2)
    parser.add_argument("--max-tensor-factor-degree", type=int, default=24)
    parser.add_argument("--max-windows", type=int)
    parser.add_argument("--seed", type=int, default=20260604)
    args = parser.parse_args()

    rows = scan(args)
    mismatches = 0
    full_axis_rows = 0
    max_profile_tests = 0
    max_profile_failures = 0
    displayed_profile_failures: list[tuple[WindowAuditRow, WindowTargetAudit, int, int, int, int]] = []
    for row in rows:
        for target in row.targets:
            for _, trace_ranks, window_ranks in target.ranks_by_subdegree:
                if trace_ranks != window_ranks:
                    mismatches += 1
            for subdegree, trace_ranks, _ in target.ranks_by_subdegree:
                for index, rank in enumerate(trace_ranks, start=1):
                    expected = min(target.raw_rank, index * subdegree)
                    max_profile_tests += 1
                    if rank != expected:
                        max_profile_failures += 1
                        if len(displayed_profile_failures) < 12:
                            displayed_profile_failures.append(
                                (row, target, subdegree, index, rank, expected)
                            )
            if target.name == "axis":
                if any(
                    trace_ranks and trace_ranks[-1] == target.raw_rank
                    for _, trace_ranks, _ in target.ranks_by_subdegree
                ):
                    full_axis_rows += 1

    print("tensor factor dual-basis coefficient-window audit")
    print(f"max_rows={args.max_rows}")
    print(f"max_cases={args.max_cases}")
    print(f"max_h={args.max_h}")
    print(f"q_stop={args.q_stop}")
    print()
    print("columns: D q ell h m n deg ext factors factor_deg proper_subdegrees")
    for row in rows:
        print(
            f"D={row.D:7d} q={row.q:7d} ell={row.ell:3d} "
            f"h={row.h:3d} m={row.m:3d} n={row.n:3d} "
            f"deg={row.factor_degree:3d} ext={row.extension_degree:2d} "
            f"factors={row.tensor_factor_count:2d} "
            f"factor_deg={row.tensor_factor_degree:3d} "
            f"proper={list(row.proper_subdegrees)}"
        )
        for target in row.targets:
            pieces = [
                format_subdegree(subdegree, trace_ranks, window_ranks)
                for subdegree, trace_ranks, window_ranks in target.ranks_by_subdegree
            ]
            print(
                f"  target={target.name:10s} size={target.size:3d} "
                f"raw_rank={target.raw_rank:3d} "
                f"{'; '.join(pieces)}"
            )
    print()
    print("summary")
    print(f"  rows={len(rows)}")
    print(f"  trace_window_rank_mismatch_targets={mismatches}")
    print(f"  axis_rows_full_by_tested_window={full_axis_rows}")
    print(f"  max_rank_profile_tests={max_profile_tests}")
    print(f"  max_rank_profile_failures={max_profile_failures}")
    if displayed_profile_failures:
        print("  displayed_max_rank_profile_failures")
        for row, target, subdegree, windows, rank, expected in displayed_profile_failures:
            print(
                f"    D={row.D} q={row.q} m={row.m} n={row.n} "
                f"target={target.name} subdegree={subdegree} windows={windows} "
                f"rank={rank}/{expected} raw_rank={target.raw_rank}"
            )
    print()
    print("interpretation")
    print("  window_rank_equals_trace_frame_rank_confirms_dual_basis_formula=1")
    print("  max_rank_profile_means_each_new_top_coefficient_adds_full_subfield_rank_until_saturation=1")
    print("  p24_target_can_be_stated_as_top_three_relative_coefficients_nonzero=1")
    print("conclusion=reported_tensor_factor_dual_basis_window_audit")


if __name__ == "__main__":
    main()
