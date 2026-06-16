#!/usr/bin/env python3
"""Mine exact Lang/Moore pivot behavior under right-orbit orderings.

The p24 representative p-unit uses a leading ordered Moore minor: after
deleting one right Frobenius orbit, take full right blocks until the next block
would cross the left degree, then take the required tail coordinates.

This script tests that certificate shape on small actual-CM rows.  It does not
try to predict good minors; it checks exact rank and residual-norm behavior for
rule-defined orbit orderings.  A useful positive signal would be a stable
ordering rule whose leading minor is always full and whose residual products
are base-field p-unit candidates.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from itertools import islice, permutations
from math import factorial, gcd

import sympy as sp
from cypari2 import Pari

from crt_partial_moment_projection_scan import coprime_components
from cycle_period_complexity_scan import find_full_cycle_prime
from hermitian_double_marginal_audit import double_marginal, kernel_matrix
from hermitian_double_marginal_fourier_audit import dft_double_marginal, zeta_powers
from hermitian_mixed_frobenius_orbit_audit import q_orbits
from hermitian_mixed_lang_normality_audit import fq_rank
from hermitian_mixed_left_subfield_normality_audit import (
    transformed_coordinates_for_left_orbit,
)
from hermitian_mixed_subspace_polynomial_toy import (
    base_value_or_none,
    q_degree,
    qpoly_annihilator_profile,
    qpoly_extend_profile,
    relative_norm_to_base,
)
from k_character_tensor_rank_scan import (
    ExtensionField,
    FpE,
    find_irreducible_modulus,
    primitive_root_of_order,
)
from l1_axis_injectivity_scan import discriminants
from packetized_relative_content_scan import packet_factors
from relative_moment_projection_scan import (
    find_splitting_primes,
    quotient_sizes_any,
    rotate,
    section_fiber_polynomials,
)


@dataclass(frozen=True)
class OrderingSummary:
    omitted_orbit: int
    ordering_count: int
    leading_full_count: int
    full_block_full_count: int
    tail_full_count: int
    leading_norm_base_count: int
    prefix_norm_base_count: int
    tail_norm_base_count: int
    zero_leading_residual_norms: int
    zero_prefix_residual_norms: int
    zero_tail_residual_norms: int
    best_leading_rank: int
    worst_leading_rank: int
    best_tail_augmentation: int
    worst_tail_augmentation: int
    canonical_leading_full: bool
    canonical_full_block_full: bool
    canonical_tail_full: bool
    canonical_full_block_count: int
    canonical_tail_len: int
    canonical_pivot_prefix: tuple[int, ...]
    canonical_tail_pivot_prefix: tuple[int, ...]
    canonical_leading_norm_base: int | None
    canonical_prefix_norm_base: int | None
    canonical_tail_norm_base: int | None


@dataclass(frozen=True)
class PivotMinerRow:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    factor_degree: int
    extension_degree: int
    left: int
    right: int
    left_orbit_rep: int
    left_orbit_len: int
    right_orbit_count: int
    right_orbit_lengths: tuple[int, ...]
    transformed_count: int
    transformed_rank: int
    summaries: tuple[OrderingSummary, ...]


def product(values: list[FpE], field: ExtensionField) -> FpE:
    out = field.one
    for value in values:
        out = field.mul(out, value)
    return out


def norm_product_base(
    residuals: list[FpE],
    degree: int,
    field: ExtensionField,
) -> tuple[int | None, int]:
    value = field.one
    zero_count = 0
    for residual in residuals:
        norm = relative_norm_to_base(residual, degree, field)
        if norm == field.zero:
            zero_count += 1
        value = field.mul(value, norm)
    return base_value_or_none(value, field), zero_count


def ordered_values_from_blocks(
    blocks: list[list[FpE]],
    order: tuple[int, ...],
) -> list[FpE]:
    out: list[FpE] = []
    for index in order:
        out.extend(blocks[index])
    return out


def prefix_split(values: list[FpE], block_lengths: list[int], left_len: int) -> tuple[int, int]:
    prefix_len = 0
    block_count = 0
    for length in block_lengths:
        if prefix_len + length > left_len:
            break
        prefix_len += length
        block_count += 1
    return prefix_len, left_len - prefix_len


def evaluate_order(
    values: list[FpE],
    block_lengths: list[int],
    left_len: int,
    field: ExtensionField,
) -> dict[str, object]:
    leading = values[:left_len]
    leading_rank = fq_rank(leading, field.q)
    leading_ann, leading_pivots, leading_residuals = qpoly_annihilator_profile(
        leading, field
    )
    leading_norm, leading_zero_norms = norm_product_base(
        leading_residuals, left_len, field
    )

    prefix_len, tail_len = prefix_split(values, block_lengths, left_len)
    prefix = values[:prefix_len]
    tail = values[prefix_len:left_len]
    prefix_rank = fq_rank(prefix, field.q)
    prefix_ann, _prefix_pivots, prefix_residuals = qpoly_annihilator_profile(
        prefix, field
    )
    prefix_norm, prefix_zero_norms = norm_product_base(
        prefix_residuals, left_len, field
    )
    tail_ann, tail_pivots, tail_residuals = qpoly_extend_profile(
        prefix_ann, tail, field
    )
    tail_norm, tail_zero_norms = norm_product_base(tail_residuals, left_len, field)
    tail_augmentation = q_degree(tail_ann, field) - q_degree(prefix_ann, field)
    if tail_augmentation != leading_rank - prefix_rank:
        raise AssertionError("tail augmentation mismatch")

    return {
        "leading_rank": leading_rank,
        "prefix_rank": prefix_rank,
        "tail_augmentation": tail_augmentation,
        "prefix_len": prefix_len,
        "tail_len": tail_len,
        "leading_norm_base": leading_norm,
        "prefix_norm_base": prefix_norm,
        "tail_norm_base": tail_norm,
        "leading_zero_norms": leading_zero_norms,
        "prefix_zero_norms": prefix_zero_norms,
        "tail_zero_norms": tail_zero_norms,
        "leading_pivot_prefix": tuple(leading_pivots[:12]),
        "tail_pivot_prefix": tuple(tail_pivots[:12]),
    }


def orbit_orders(count: int, max_orderings: int) -> list[tuple[int, ...]]:
    all_count = factorial(count)
    if all_count <= max_orderings:
        return list(permutations(range(count)))
    return list(islice(permutations(range(count)), max_orderings))


def summarize_omission(
    omitted: int,
    blocks: list[list[FpE]],
    left_len: int,
    field: ExtensionField,
    max_orderings: int,
) -> OrderingSummary:
    kept_blocks = [block for index, block in enumerate(blocks) if index != omitted]
    orders = orbit_orders(len(kept_blocks), max_orderings)
    leading_full = 0
    prefix_full = 0
    tail_full = 0
    leading_norm_base = 0
    prefix_norm_base = 0
    tail_norm_base = 0
    zero_leading_norms = 0
    zero_prefix_norms = 0
    zero_tail_norms = 0
    leading_ranks: list[int] = []
    tail_augmentations: list[int] = []
    canonical: dict[str, object] | None = None
    for index, order in enumerate(orders):
        values = ordered_values_from_blocks(kept_blocks, order)
        block_lengths = [len(kept_blocks[i]) for i in order]
        result = evaluate_order(values, block_lengths, left_len, field)
        leading_rank = int(result["leading_rank"])
        prefix_rank = int(result["prefix_rank"])
        tail_aug = int(result["tail_augmentation"])
        prefix_len = int(result["prefix_len"])
        tail_len = int(result["tail_len"])
        leading_ranks.append(leading_rank)
        tail_augmentations.append(tail_aug)
        leading_full += int(leading_rank >= left_len)
        prefix_full += int(prefix_rank >= prefix_len)
        tail_full += int(tail_aug >= tail_len)
        leading_norm_base += int(result["leading_norm_base"] is not None)
        prefix_norm_base += int(result["prefix_norm_base"] is not None)
        tail_norm_base += int(result["tail_norm_base"] is not None)
        zero_leading_norms += int(result["leading_zero_norms"])
        zero_prefix_norms += int(result["prefix_zero_norms"])
        zero_tail_norms += int(result["tail_zero_norms"])
        if index == 0:
            canonical = result
    if canonical is None:
        raise AssertionError("no orbit orderings evaluated")
    canonical_prefix_len = int(canonical["prefix_len"])
    canonical_tail_len = int(canonical["tail_len"])
    block_count = 0
    consumed = 0
    for block in kept_blocks:
        if consumed + len(block) > left_len:
            break
        consumed += len(block)
        block_count += 1
    return OrderingSummary(
        omitted_orbit=omitted,
        ordering_count=len(orders),
        leading_full_count=leading_full,
        full_block_full_count=prefix_full,
        tail_full_count=tail_full,
        leading_norm_base_count=leading_norm_base,
        prefix_norm_base_count=prefix_norm_base,
        tail_norm_base_count=tail_norm_base,
        zero_leading_residual_norms=zero_leading_norms,
        zero_prefix_residual_norms=zero_prefix_norms,
        zero_tail_residual_norms=zero_tail_norms,
        best_leading_rank=max(leading_ranks),
        worst_leading_rank=min(leading_ranks),
        best_tail_augmentation=max(tail_augmentations),
        worst_tail_augmentation=min(tail_augmentations),
        canonical_leading_full=int(canonical["leading_rank"]) >= left_len,
        canonical_full_block_full=int(canonical["prefix_rank"]) >= canonical_prefix_len,
        canonical_tail_full=int(canonical["tail_augmentation"]) >= canonical_tail_len,
        canonical_full_block_count=block_count,
        canonical_tail_len=canonical_tail_len,
        canonical_pivot_prefix=tuple(canonical["leading_pivot_prefix"]),
        canonical_tail_pivot_prefix=tuple(canonical["tail_pivot_prefix"]),
        canonical_leading_norm_base=canonical["leading_norm_base"],  # type: ignore[arg-type]
        canonical_prefix_norm_base=canonical["prefix_norm_base"],  # type: ignore[arg-type]
        canonical_tail_norm_base=canonical["tail_norm_base"],  # type: ignore[arg-type]
    )


def audit_left_right(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    m: int,
    factor: sp.Poly,
    left: int,
    right: int,
    left_orbit: list[int],
    seed: int,
    max_orderings: int,
) -> PivotMinerRow | None:
    if factor.degree() % 2:
        return None
    h = len(cycle)
    n = h // m
    if pow(q, factor.degree() // 2, n) != n - 1:
        return None
    extension_degree = int(sp.n_order(q % m, m))
    modulus = find_irreducible_modulus(q, extension_degree, seed)
    field = ExtensionField(q, extension_degree, modulus)
    zeta = primitive_root_of_order(field, m, seed)
    powers = zeta_powers(zeta, m, field)
    residues = [
        fiber.rem(factor)
        for fiber in section_fiber_polynomials(cycle, q, m, "complement")
    ]
    kernel = kernel_matrix(residues, factor, q)
    marginal = double_marginal(kernel, left, right, q)
    dft_matrix = dft_double_marginal(marginal, left, right, powers, m, field)
    right_orbits = q_orbits(right, q)
    transformed = transformed_coordinates_for_left_orbit(
        dft_matrix,
        left,
        right,
        left_orbit,
        right_orbits,
        q,
        field,
        seed,
    )
    blocks: list[list[FpE]] = []
    offset = 0
    for orbit in right_orbits:
        blocks.append(transformed[offset : offset + len(orbit)])
        offset += len(orbit)
    summaries = tuple(
        summarize_omission(omitted, blocks, len(left_orbit), field, max_orderings)
        for omitted in range(len(blocks))
    )
    return PivotMinerRow(
        D=D,
        q=q,
        ell=ell,
        h=h,
        m=m,
        n=n,
        factor_degree=factor.degree(),
        extension_degree=extension_degree,
        left=left,
        right=right,
        left_orbit_rep=left_orbit[0],
        left_orbit_len=len(left_orbit),
        right_orbit_count=len(right_orbits),
        right_orbit_lengths=tuple(len(orbit) for orbit in right_orbits),
        transformed_count=len(transformed),
        transformed_rank=fq_rank(transformed, q),
        summaries=summaries,
    )


def scan(args: argparse.Namespace) -> PivotMinerRow | None:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
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
        quotient_sizes = [
            m
            for m in quotient_sizes
            if gcd(m, h // m) == 1
            and m <= args.max_m
            and (args.only_m is None or m == args.only_m)
            and len([component for component in coprime_components(m) if component > 2])
            >= 2
        ]
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
        case_had_cycle = False
        for q, roots in splits:
            if args.only_q is not None and q != args.only_q:
                continue
            full = find_full_cycle_prime(roots, D, q)
            if full is None:
                continue
            case_had_cycle = True
            ell, cycle = full
            shifted = rotate(cycle, args.origin_shift % h)
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
                    if factor.degree() < args.min_factor_degree:
                        continue
                    for left in coprime_components(m):
                        if left <= 2 or (args.only_left and left != args.only_left):
                            continue
                        for right in coprime_components(m):
                            if right <= 2 or (args.only_right and right != args.only_right):
                                continue
                            right_orbits = q_orbits(right, q)
                            if len(right_orbits) < args.min_right_orbits:
                                continue
                            if min(len(orbit) for orbit in right_orbits) < args.min_right_orbit_len:
                                continue
                            for left_orbit in q_orbits(left, q):
                                if len(left_orbit) < args.min_left_orbit_len:
                                    continue
                                row = audit_left_right(
                                    D,
                                    q,
                                    ell,
                                    shifted,
                                    m,
                                    factor,
                                    left,
                                    right,
                                    left_orbit,
                                    args.seed,
                                    args.max_orderings,
                                )
                                if row and row.transformed_rank >= row.left_orbit_len:
                                    return row
        if case_had_cycle:
            cases += 1
            if cases >= args.max_cases:
                break
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-cases", type=int, default=24)
    parser.add_argument("--min-h", type=int, default=12)
    parser.add_argument("--max-h", type=int, default=220)
    parser.add_argument("--max-abs-D", type=int, default=80000)
    parser.add_argument("--max-prime-quotients", type=int, default=12)
    parser.add_argument("--max-composite-quotients", type=int, default=24)
    parser.add_argument("--min-n", type=int, default=3)
    parser.add_argument("--max-n", type=int, default=220)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=600000)
    parser.add_argument("--max-splitting-primes", type=int, default=2)
    parser.add_argument("--max-m", type=int, default=120)
    parser.add_argument("--min-factor-degree", type=int, default=1)
    parser.add_argument("--max-factor-degree", type=int, default=12)
    parser.add_argument("--max-extension-degree", type=int, default=12)
    parser.add_argument("--min-left-orbit-len", type=int, default=2)
    parser.add_argument("--min-right-orbits", type=int, default=2)
    parser.add_argument("--min-right-orbit-len", type=int, default=1)
    parser.add_argument("--max-orderings", type=int, default=720)
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--origin-shift", type=int, default=0)
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--only-q", type=int)
    parser.add_argument("--only-m", type=int)
    parser.add_argument("--only-left", type=int)
    parser.add_argument("--only-right", type=int)
    parser.add_argument("--seed", type=int, default=20260605)
    args = parser.parse_args()

    row = scan(args)
    if row is None:
        raise SystemExit("no eligible full-span row found")

    print("Lang pivot-order miner")
    print(f"D={row.D}")
    print(f"q={row.q}")
    print(f"ell={row.ell}")
    print(f"h={row.h}")
    print(f"m={row.m}")
    print(f"n={row.n}")
    print(f"factor_degree={row.factor_degree}")
    print(f"extension_degree={row.extension_degree}")
    print(f"pair=({row.left},{row.right})")
    print(f"left_orbit_rep={row.left_orbit_rep}")
    print(f"left_orbit_len={row.left_orbit_len}")
    print(f"right_orbit_count={row.right_orbit_count}")
    print(f"right_orbit_lengths={list(row.right_orbit_lengths)}")
    print(f"transformed_count={row.transformed_count}")
    print(f"transformed_rank={row.transformed_rank}")
    print()
    for summary in row.summaries:
        print(f"omitted_orbit={summary.omitted_orbit}")
        print(f"  ordering_count={summary.ordering_count}")
        print(
            "  leading_full="
            f"{summary.leading_full_count}/{summary.ordering_count}"
        )
        print(
            "  full_block_full="
            f"{summary.full_block_full_count}/{summary.ordering_count}"
        )
        print(f"  tail_full={summary.tail_full_count}/{summary.ordering_count}")
        print(
            "  norm_base_counts="
            f"leading:{summary.leading_norm_base_count} "
            f"prefix:{summary.prefix_norm_base_count} "
            f"tail:{summary.tail_norm_base_count}"
        )
        print(
            "  zero_residual_norms="
            f"leading:{summary.zero_leading_residual_norms} "
            f"prefix:{summary.zero_prefix_residual_norms} "
            f"tail:{summary.zero_tail_residual_norms}"
        )
        print(
            "  leading_rank_range="
            f"{summary.worst_leading_rank}..{summary.best_leading_rank}"
        )
        print(
            "  tail_augmentation_range="
            f"{summary.worst_tail_augmentation}..{summary.best_tail_augmentation}"
        )
        print(
            "  canonical="
            f"leading:{int(summary.canonical_leading_full)} "
            f"prefix:{int(summary.canonical_full_block_full)} "
            f"tail:{int(summary.canonical_tail_full)} "
            f"full_blocks:{summary.canonical_full_block_count} "
            f"tail_len:{summary.canonical_tail_len}"
        )
        print(f"  canonical_pivots={list(summary.canonical_pivot_prefix)}")
        print(f"  canonical_tail_pivots={list(summary.canonical_tail_pivot_prefix)}")
        print(
            "  canonical_norms="
            f"leading:{summary.canonical_leading_norm_base} "
            f"prefix:{summary.canonical_prefix_norm_base} "
            f"tail:{summary.canonical_tail_norm_base}"
        )
    print()
    print("interpretation")
    print("  full_across_many_orderings_supports_order_robust_punit_search=1")
    print("  canonical_only_success_means_window_choice_is_arithmetic_data=1")
    print("  norm_base_counts_track_whether_residual_products_descend_to_Fq=1")
    print("conclusion=reported_lang_pivot_order_miner")


if __name__ == "__main__":
    main()
