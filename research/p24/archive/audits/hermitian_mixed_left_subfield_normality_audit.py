#!/usr/bin/env python3
"""Audit left-subfield normality of Lang-trivialized mixed periods.

The Lang-normality target says that transformed mixed seed coordinates have
large F_q-span.  In the p24 mixed `157 x 211` block, the left and right
character degrees are coprime:

    ord_157(p)=156, ord_211(p)=35.

So after trivializing the right semilinear shift, the transformed coordinates
should lie in the left character field F_{p^156}.  The p24 target then becomes
an ordinary left-field normality statement:

    210 transformed coordinates span F_{p^156} over F_p.

This script checks the left-subfield landing and individual-coordinate
normality diagnostics on small CM rows.
"""

from __future__ import annotations

import argparse
import itertools
from dataclasses import dataclass
from math import gcd

import sympy as sp
from cypari2 import Pari

from crt_partial_moment_projection_scan import coprime_components
from cycle_period_complexity_scan import find_full_cycle_prime
from hermitian_double_marginal_audit import double_marginal, kernel_matrix
from hermitian_double_marginal_audit import centered_double_marginal
from hermitian_double_marginal_fourier_audit import (
    dft_double_marginal,
    zeta_powers,
)
from hermitian_mixed_frobenius_orbit_audit import q_orbits
from hermitian_mixed_lang_normality_audit import (
    fq_rank,
    lang_inverse_for_orbit,
    matrix_vector_mul,
    orbit_len_histogram,
    subfield_power_basis,
)
from hermitian_mixed_subspace_polynomial_toy import (
    base_value_or_none,
    full_field_annihilator,
    q_degree,
    qpoly_annihilator_profile,
    qpoly_extend_profile,
    qpoly_eval,
    relative_norm_to_base,
)
from k_character_tensor_rank_scan import (
    ExtensionField,
    FpE,
    find_irreducible_modulus,
    primitive_root_of_order,
)
from l1_axis_injectivity_scan import discriminants, rank_mod_q
from packetized_relative_content_scan import packet_factors
from relative_moment_projection_scan import (
    find_splitting_primes,
    quotient_sizes_any,
    rotate,
    section_fiber_polynomials,
)


@dataclass(frozen=True)
class LeftSubfieldTest:
    left: int
    right: int
    left_orbit_rep: int
    left_orbit_len: int
    right_orbit_count: int
    right_orbit_len_histogram: tuple[tuple[int, int], ...]
    right_lens_coprime_to_left: bool
    transformed_count: int
    transformed_fq_rank: int
    delete_one_min_transformed_rank: int
    delete_one_full_count: int
    delete_one_min_annihilator_q_degree: int
    delete_one_annihilator_degree_mismatches: int
    delete_one_annihilator_vanish_failures: int
    delete_one_full_field_annihilator_count: int
    delete_one_min_pivot_count: int
    delete_one_pivot_prefixes: tuple[tuple[int, ...], ...]
    delete_one_pivot_norm_products_base: tuple[int | None, ...]
    delete_one_zero_residual_norms: int
    delete_one_leading_min_rank: int
    delete_one_leading_full_count: int
    delete_one_leading_annihilator_degree_mismatches: int
    delete_one_leading_annihilator_vanish_failures: int
    delete_one_leading_full_field_annihilator_count: int
    delete_one_leading_norm_products_base: tuple[int | None, ...]
    delete_one_leading_zero_residual_norms: int
    delete_one_prefix_full_block_counts: tuple[int, ...]
    delete_one_prefix_tail_lengths: tuple[int, ...]
    delete_one_prefix_full_block_min_rank: int
    delete_one_prefix_full_block_full_count: int
    delete_one_prefix_tail_min_augmentation: int
    delete_one_prefix_tail_full_count: int
    delete_one_prefix_full_block_ann_degrees: tuple[int, ...]
    delete_one_prefix_full_block_norm_products_base: tuple[int | None, ...]
    delete_one_prefix_full_block_zero_residual_norms: int
    delete_one_prefix_tail_ann_degrees: tuple[int, ...]
    delete_one_prefix_tail_pivot_prefixes: tuple[tuple[int, ...], ...]
    delete_one_prefix_tail_norm_products_base: tuple[int | None, ...]
    delete_one_prefix_tail_zero_residual_norms: int
    left_subfield_failures: int
    max_single_normal_rank: int
    normal_coordinate_count: int
    annihilator_q_degree: int
    annihilator_degree_matches_rank: bool
    annihilator_vanish_failures: int
    full_field_annihilator: bool
    pivot_count: int
    pivot_prefix: tuple[int, ...]
    pivot_norm_product_base: int | None
    zero_residual_norms: int
    centered_right_profile_rank: int
    centered_profile_rank_match: bool
    centered_profile_subfield_failures: int
    centered_base_rank: int
    centered_base_rank_applicable: bool
    centered_base_profile_rank_match: bool
    centered_profile_stability_defect: int
    centered_profile_max_single_normal_rank: int
    centered_profile_normal_coordinate_count: int
    centered_trace_support_checked: bool
    centered_trace_lambda_count: int
    centered_trace_min_right_orbit_support: int
    centered_trace_zero_support_count: int
    centered_trace_one_support_count: int
    full_left_span: bool
    has_single_normal_coordinate: bool


@dataclass(frozen=True)
class LeftSubfieldRow:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    factor_degree: int
    extension_degree: int
    components: tuple[int, ...]
    tests: tuple[LeftSubfieldTest, ...]


def row_matches_filters(row: LeftSubfieldRow, args: argparse.Namespace) -> bool:
    tests = row.tests
    if args.min_left_orbit_len:
        tests = tuple(
            test for test in tests if test.left_orbit_len >= args.min_left_orbit_len
        )
    if args.require_coprime_lens:
        tests = tuple(test for test in tests if test.right_lens_coprime_to_left)
    if args.require_full_span:
        tests = tuple(test for test in tests if test.full_left_span)
    if args.min_pivot_count:
        tests = tuple(test for test in tests if test.pivot_count >= args.min_pivot_count)
    return bool(tests)


def quotient_m_can_match_filters(q: int, m: int, args: argparse.Namespace) -> bool:
    components = [component for component in coprime_components(m) if component > 2]
    for left in components:
        left_orbits = q_orbits(left, q)
        for right in components:
            right_orbits = q_orbits(right, q)
            for left_orbit in left_orbits:
                if args.min_left_orbit_len and len(left_orbit) < args.min_left_orbit_len:
                    continue
                if args.min_pivot_count and len(left_orbit) < args.min_pivot_count:
                    continue
                if args.require_coprime_lens and not all(
                    gcd(len(left_orbit), len(right_orbit)) == 1
                    for right_orbit in right_orbits
                ):
                    continue
                return True
    return False


def frobenius(value: FpE, power: int, field: ExtensionField) -> FpE:
    return field.pow(value, field.q**power)


def individual_normal_rank(value: FpE, degree: int, q: int, field: ExtensionField) -> int:
    conjugates = [frobenius(value, i, field) for i in range(degree)]
    return fq_rank(conjugates, q)


def transformed_coordinates_for_left_orbit(
    dft_matrix: list[list[FpE]],
    left: int,
    right: int,
    left_orbit: list[int],
    right_orbits: list[list[int]],
    q: int,
    field: ExtensionField,
    seed: int,
) -> list[FpE]:
    row_index = {u: u - 1 for u in range(1, left)}
    col_index = {v: v - 1 for v in range(1, right)}
    transformed: list[FpE] = []
    inverses: dict[int, list[list[FpE]]] = {}
    for right_orbit in right_orbits:
        orbit_len = len(right_orbit)
        if orbit_len not in inverses:
            inverses[orbit_len] = lang_inverse_for_orbit(q, orbit_len, field, seed)
        seed_vector = [
            dft_matrix[row_index[left_orbit[0]]][col_index[v]]
            for v in right_orbit
        ]
        transformed.extend(matrix_vector_mul(inverses[orbit_len], seed_vector, field))
    return transformed


def centered_right_profile_for_left_orbit(
    marginal: list[list[int]],
    left: int,
    right: int,
    left_orbit: list[int],
    m: int,
    zeta_pows,
    q: int,
    field: ExtensionField,
) -> list[FpE]:
    """Left-character transform of the centered right marginal.

    For fixed nonzero left frequency u0, set

        G_s = sum_a zeta_left^(u0*a) M(a,s).

    The nonzero right DFT values determine only the centered vector
    G_s - average_s G_s.  Its F_q-span should match the span of the
    trace-dual/Lang coordinates.
    """

    step_left = m // left
    u0 = left_orbit[0]
    values: list[FpE] = []
    for s in range(right):
        total = field.zero
        for a in range(left):
            weight = zeta_pows[(u0 * step_left * a) % m]
            total = field.add(
                total,
                field.mul(weight, field.embed(marginal[a][s])),
            )
        values.append(total)
    avg = field.scalar_mul(pow(right % q, -1, q), sum_field(values, field))
    return [field.sub(value, avg) for value in values]


def sum_field(values: list[FpE], field: ExtensionField) -> FpE:
    total = field.zero
    for value in values:
        total = field.add(total, value)
    return total


def trace_to_base(value: FpE, degree: int, field: ExtensionField) -> FpE:
    total = field.zero
    for i in range(degree):
        total = field.add(total, field.pow(value, field.q**i))
    return total


def right_fourier_coefficient(
    word: list[FpE],
    right_frequency: int,
    right: int,
    m: int,
    zeta_pows,
    field: ExtensionField,
) -> FpE:
    step_right = m // right
    total = field.zero
    for s, value in enumerate(word):
        weight = zeta_pows[(right_frequency * step_right * s) % m]
        total = field.add(total, field.mul(weight, value))
    return total


def centered_trace_right_orbit_support(
    centered_profile: list[FpE],
    right: int,
    right_orbits: list[list[int]],
    left_len: int,
    m: int,
    zeta_pows,
    q: int,
    field: ExtensionField,
    seed: int,
    max_lambda_enumeration: int,
) -> tuple[bool, int, int, int, int]:
    """Exhaustively test the cyclic-code obstruction at small left degree.

    For lambda in L=F_{q^left_len}, form

        f_lambda(s) = Tr_{L/F_q}(lambda * G_s^0).

    The support counted here is the number of nonzero right Frobenius-orbit
    Fourier components of this scalar word.  Support zero is exactly the
    original dual-kernel obstruction.  Support one falsifies the stronger
    delete-one/right-orbit separation candidate.
    """

    candidate_count = q**left_len - 1
    if candidate_count > max_lambda_enumeration:
        return False, candidate_count, 0, 0, 0

    left_basis = subfield_power_basis(q, left_len, field, seed + 157)
    min_support = len(right_orbits)
    zero_support = 0
    one_support = 0
    checked = 0
    for coeffs in itertools.product(range(q), repeat=left_len):
        if all(coeff == 0 for coeff in coeffs):
            continue
        lam = field.zero
        for coeff, basis_value in zip(coeffs, left_basis):
            lam = field.add(lam, field.scalar_mul(coeff, basis_value))
        word = [
            trace_to_base(field.mul(lam, value), left_len, field)
            for value in centered_profile
        ]
        support = 0
        for right_orbit in right_orbits:
            coeff = right_fourier_coefficient(
                word, right_orbit[0], right, m, zeta_pows, field
            )
            if coeff != field.zero:
                support += 1
        checked += 1
        min_support = min(min_support, support)
        if support == 0:
            zero_support += 1
        if support == 1:
            one_support += 1
    return True, checked, min_support, zero_support, one_support


def audit_left_orbit(
    marginal: list[list[int]],
    dft_matrix: list[list[FpE]],
    left: int,
    right: int,
    left_orbit: list[int],
    right_orbits: list[list[int]],
    m: int,
    zeta_pows,
    q: int,
    field: ExtensionField,
    seed: int,
    max_lambda_enumeration: int,
) -> LeftSubfieldTest:
    left_len = len(left_orbit)
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
    delete_one_ranks: list[int] = []
    delete_one_ann_degrees: list[int] = []
    delete_one_ann_mismatches = 0
    delete_one_ann_vanish_failures = 0
    delete_one_full_poly_count = 0
    delete_one_pivot_counts: list[int] = []
    delete_one_pivot_prefixes: list[tuple[int, ...]] = []
    delete_one_pivot_norm_products: list[int | None] = []
    delete_one_zero_residual_norms = 0
    delete_one_leading_ranks: list[int] = []
    delete_one_leading_ann_mismatches = 0
    delete_one_leading_ann_vanish_failures = 0
    delete_one_leading_full_poly_count = 0
    delete_one_leading_norm_products: list[int | None] = []
    delete_one_leading_zero_residual_norms = 0
    delete_one_prefix_full_block_counts: list[int] = []
    delete_one_prefix_tail_lengths: list[int] = []
    delete_one_prefix_full_block_ranks: list[int] = []
    delete_one_prefix_full_block_full = 0
    delete_one_prefix_tail_augmentations: list[int] = []
    delete_one_prefix_tail_full = 0
    delete_one_prefix_full_block_ann_degrees: list[int] = []
    delete_one_prefix_full_block_norm_products: list[int | None] = []
    delete_one_prefix_full_block_zero_residual_norms = 0
    delete_one_prefix_tail_ann_degrees: list[int] = []
    delete_one_prefix_tail_pivot_prefixes: list[tuple[int, ...]] = []
    delete_one_prefix_tail_norm_products: list[int | None] = []
    delete_one_prefix_tail_zero_residual_norms = 0
    for omitted in range(len(right_orbits)):
        kept = [
            right_orbit
            for index, right_orbit in enumerate(right_orbits)
            if index != omitted
        ]
        subset_transformed = transformed_coordinates_for_left_orbit(
            dft_matrix,
            left,
            right,
            left_orbit,
            kept,
            q,
            field,
            seed,
        )
        subset_rank = fq_rank(subset_transformed, q)
        subset_ann, subset_pivots, subset_residuals = qpoly_annihilator_profile(
            subset_transformed, field
        )
        subset_degree = q_degree(subset_ann, field)
        subset_vanish_failures = sum(
            1
            for value in subset_transformed
            if qpoly_eval(subset_ann, value, field) != field.zero
        )
        subset_norm_product = field.one
        for residual in subset_residuals:
            norm = relative_norm_to_base(residual, left_len, field)
            if norm == field.zero:
                delete_one_zero_residual_norms += 1
            subset_norm_product = field.mul(subset_norm_product, norm)
        leading_transformed = subset_transformed[:left_len]
        leading_rank = fq_rank(leading_transformed, q)
        leading_ann, _leading_pivots, leading_residuals = qpoly_annihilator_profile(
            leading_transformed, field
        )
        leading_degree = q_degree(leading_ann, field)
        leading_vanish_failures = sum(
            1
            for value in leading_transformed
            if qpoly_eval(leading_ann, value, field) != field.zero
        )
        leading_norm_product = field.one
        for residual in leading_residuals:
            norm = relative_norm_to_base(residual, left_len, field)
            if norm == field.zero:
                delete_one_leading_zero_residual_norms += 1
            leading_norm_product = field.mul(leading_norm_product, norm)
        full_prefix_len = 0
        full_block_count = 0
        for right_orbit in kept:
            orbit_len = len(right_orbit)
            if full_prefix_len + orbit_len > left_len:
                break
            full_prefix_len += orbit_len
            full_block_count += 1
        full_prefix_rank = fq_rank(subset_transformed[:full_prefix_len], q)
        tail_len = left_len - full_prefix_len
        tail_values = subset_transformed[full_prefix_len:left_len]
        tail_augmentation = leading_rank - full_prefix_rank
        full_prefix_ann, _full_prefix_pivots, full_prefix_residuals = (
            qpoly_annihilator_profile(subset_transformed[:full_prefix_len], field)
        )
        full_prefix_norm_product = field.one
        for residual in full_prefix_residuals:
            norm = relative_norm_to_base(residual, left_len, field)
            if norm == field.zero:
                delete_one_prefix_full_block_zero_residual_norms += 1
            full_prefix_norm_product = field.mul(full_prefix_norm_product, norm)
        tail_ann, tail_pivots, tail_residuals = qpoly_extend_profile(
            full_prefix_ann, tail_values, field
        )
        tail_norm_product = field.one
        for residual in tail_residuals:
            norm = relative_norm_to_base(residual, left_len, field)
            if norm == field.zero:
                delete_one_prefix_tail_zero_residual_norms += 1
            tail_norm_product = field.mul(tail_norm_product, norm)
        delete_one_ranks.append(subset_rank)
        delete_one_ann_degrees.append(subset_degree)
        if subset_degree != subset_rank:
            delete_one_ann_mismatches += 1
        delete_one_ann_vanish_failures += subset_vanish_failures
        if full_field_annihilator(left_len, subset_ann, field):
            delete_one_full_poly_count += 1
        delete_one_pivot_counts.append(len(subset_pivots))
        delete_one_pivot_prefixes.append(tuple(subset_pivots[:12]))
        delete_one_pivot_norm_products.append(
            base_value_or_none(subset_norm_product, field)
        )
        delete_one_leading_ranks.append(leading_rank)
        if leading_degree != leading_rank:
            delete_one_leading_ann_mismatches += 1
        delete_one_leading_ann_vanish_failures += leading_vanish_failures
        if full_field_annihilator(left_len, leading_ann, field):
            delete_one_leading_full_poly_count += 1
        delete_one_leading_norm_products.append(
            base_value_or_none(leading_norm_product, field)
        )
        delete_one_prefix_full_block_counts.append(full_block_count)
        delete_one_prefix_tail_lengths.append(tail_len)
        delete_one_prefix_full_block_ranks.append(full_prefix_rank)
        if full_prefix_rank == full_prefix_len:
            delete_one_prefix_full_block_full += 1
        delete_one_prefix_tail_augmentations.append(tail_augmentation)
        if tail_augmentation == tail_len:
            delete_one_prefix_tail_full += 1
        delete_one_prefix_full_block_ann_degrees.append(
            q_degree(full_prefix_ann, field)
        )
        delete_one_prefix_full_block_norm_products.append(
            base_value_or_none(full_prefix_norm_product, field)
        )
        delete_one_prefix_tail_ann_degrees.append(q_degree(tail_ann, field))
        delete_one_prefix_tail_pivot_prefixes.append(tuple(tail_pivots[:12]))
        delete_one_prefix_tail_norm_products.append(
            base_value_or_none(tail_norm_product, field)
        )
    subfield_failures = sum(
        1 for value in transformed if frobenius(value, left_len, field) != value
    )
    normal_ranks = [
        individual_normal_rank(value, left_len, q, field)
        for value in transformed
        if value != field.zero
    ]
    max_single = max(normal_ranks) if normal_ranks else 0
    normal_count = sum(1 for rank in normal_ranks if rank == left_len)
    transformed_rank = fq_rank(transformed, q)
    ann, pivot_indices, residuals = qpoly_annihilator_profile(transformed, field)
    ann_degree = q_degree(ann, field)
    ann_vanish_failures = sum(
        1 for value in transformed if qpoly_eval(ann, value, field) != field.zero
    )
    norm_product = field.one
    zero_residual_norms = 0
    for residual in residuals:
        norm = relative_norm_to_base(residual, left_len, field)
        if norm == field.zero:
            zero_residual_norms += 1
        norm_product = field.mul(norm_product, norm)
    centered_profile = centered_right_profile_for_left_orbit(
        marginal, left, right, left_orbit, m, zeta_pows, q, field
    )
    centered_profile_rank = fq_rank(centered_profile, q)
    centered_base_rank = rank_centered_base_for_left_orbit(
        marginal, left, right, left_orbit, q
    )
    centered_base_rank_applicable = len(left_orbit) == left - 1
    centered_profile_subfield_failures = sum(
        1 for value in centered_profile if frobenius(value, left_len, field) != value
    )
    centered_profile_frob = [
        frobenius(value, 1, field) for value in centered_profile
    ]
    centered_profile_stability_defect = (
        fq_rank(centered_profile + centered_profile_frob, q) - centered_profile_rank
    )
    centered_profile_normal_ranks = [
        individual_normal_rank(value, left_len, q, field)
        for value in centered_profile
        if value != field.zero
    ]
    centered_profile_max_single = (
        max(centered_profile_normal_ranks) if centered_profile_normal_ranks else 0
    )
    centered_profile_normal_count = sum(
        1 for rank in centered_profile_normal_ranks if rank == left_len
    )
    (
        trace_support_checked,
        trace_lambda_count,
        trace_min_support,
        trace_zero_support,
        trace_one_support,
    ) = centered_trace_right_orbit_support(
        centered_profile,
        right,
        right_orbits,
        left_len,
        m,
        zeta_pows,
        q,
        field,
        seed,
        max_lambda_enumeration,
    )
    return LeftSubfieldTest(
        left=left,
        right=right,
        left_orbit_rep=left_orbit[0],
        left_orbit_len=left_len,
        right_orbit_count=len(right_orbits),
        right_orbit_len_histogram=orbit_len_histogram(right_orbits),
        right_lens_coprime_to_left=all(
            gcd(left_len, len(right_orbit)) == 1 for right_orbit in right_orbits
        ),
        transformed_count=len(transformed),
        transformed_fq_rank=transformed_rank,
        delete_one_min_transformed_rank=(
            min(delete_one_ranks) if delete_one_ranks else transformed_rank
        ),
        delete_one_full_count=sum(
            1 for rank in delete_one_ranks if rank >= left_len
        ),
        delete_one_min_annihilator_q_degree=(
            min(delete_one_ann_degrees) if delete_one_ann_degrees else ann_degree
        ),
        delete_one_annihilator_degree_mismatches=delete_one_ann_mismatches,
        delete_one_annihilator_vanish_failures=delete_one_ann_vanish_failures,
        delete_one_full_field_annihilator_count=delete_one_full_poly_count,
        delete_one_min_pivot_count=(
            min(delete_one_pivot_counts) if delete_one_pivot_counts else len(pivot_indices)
        ),
        delete_one_pivot_prefixes=tuple(delete_one_pivot_prefixes),
        delete_one_pivot_norm_products_base=tuple(delete_one_pivot_norm_products),
        delete_one_zero_residual_norms=delete_one_zero_residual_norms,
        delete_one_leading_min_rank=(
            min(delete_one_leading_ranks) if delete_one_leading_ranks else transformed_rank
        ),
        delete_one_leading_full_count=sum(
            1 for rank in delete_one_leading_ranks if rank >= left_len
        ),
        delete_one_leading_annihilator_degree_mismatches=(
            delete_one_leading_ann_mismatches
        ),
        delete_one_leading_annihilator_vanish_failures=(
            delete_one_leading_ann_vanish_failures
        ),
        delete_one_leading_full_field_annihilator_count=(
            delete_one_leading_full_poly_count
        ),
        delete_one_leading_norm_products_base=tuple(delete_one_leading_norm_products),
        delete_one_leading_zero_residual_norms=delete_one_leading_zero_residual_norms,
        delete_one_prefix_full_block_counts=tuple(delete_one_prefix_full_block_counts),
        delete_one_prefix_tail_lengths=tuple(delete_one_prefix_tail_lengths),
        delete_one_prefix_full_block_min_rank=(
            min(delete_one_prefix_full_block_ranks)
            if delete_one_prefix_full_block_ranks
            else transformed_rank
        ),
        delete_one_prefix_full_block_full_count=delete_one_prefix_full_block_full,
        delete_one_prefix_tail_min_augmentation=(
            min(delete_one_prefix_tail_augmentations)
            if delete_one_prefix_tail_augmentations
            else 0
        ),
        delete_one_prefix_tail_full_count=delete_one_prefix_tail_full,
        delete_one_prefix_full_block_ann_degrees=tuple(
            delete_one_prefix_full_block_ann_degrees
        ),
        delete_one_prefix_full_block_norm_products_base=tuple(
            delete_one_prefix_full_block_norm_products
        ),
        delete_one_prefix_full_block_zero_residual_norms=(
            delete_one_prefix_full_block_zero_residual_norms
        ),
        delete_one_prefix_tail_ann_degrees=tuple(delete_one_prefix_tail_ann_degrees),
        delete_one_prefix_tail_pivot_prefixes=tuple(
            delete_one_prefix_tail_pivot_prefixes
        ),
        delete_one_prefix_tail_norm_products_base=tuple(
            delete_one_prefix_tail_norm_products
        ),
        delete_one_prefix_tail_zero_residual_norms=(
            delete_one_prefix_tail_zero_residual_norms
        ),
        left_subfield_failures=subfield_failures,
        max_single_normal_rank=max_single,
        normal_coordinate_count=normal_count,
        annihilator_q_degree=ann_degree,
        annihilator_degree_matches_rank=(ann_degree == transformed_rank),
        annihilator_vanish_failures=ann_vanish_failures,
        full_field_annihilator=full_field_annihilator(left_len, ann, field),
        pivot_count=len(pivot_indices),
        pivot_prefix=tuple(pivot_indices[:12]),
        pivot_norm_product_base=base_value_or_none(norm_product, field),
        zero_residual_norms=zero_residual_norms,
        centered_right_profile_rank=centered_profile_rank,
        centered_profile_rank_match=(centered_profile_rank == transformed_rank),
        centered_profile_subfield_failures=centered_profile_subfield_failures,
        centered_base_rank=centered_base_rank,
        centered_base_rank_applicable=centered_base_rank_applicable,
        centered_base_profile_rank_match=(
            centered_base_rank_applicable and centered_base_rank == centered_profile_rank
        ),
        centered_profile_stability_defect=centered_profile_stability_defect,
        centered_profile_max_single_normal_rank=centered_profile_max_single,
        centered_profile_normal_coordinate_count=centered_profile_normal_count,
        centered_trace_support_checked=trace_support_checked,
        centered_trace_lambda_count=trace_lambda_count,
        centered_trace_min_right_orbit_support=trace_min_support,
        centered_trace_zero_support_count=trace_zero_support,
        centered_trace_one_support_count=trace_one_support,
        full_left_span=(transformed_rank >= left_len),
        has_single_normal_coordinate=(normal_count > 0),
    )


def rank_centered_base_for_left_orbit(
    marginal: list[list[int]],
    left: int,
    right: int,
    left_orbit: list[int],
    q: int,
) -> int:
    """Rank of the centered marginal in the left-orbit quotient coordinates."""

    centered = centered_double_marginal(marginal, q)
    return rank_mod_q(centered, q)


def audit_packet(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    m: int,
    factor: sp.Poly,
    seed: int,
    max_lambda_enumeration: int,
) -> LeftSubfieldRow | None:
    if factor.degree() % 2:
        return None
    h = len(cycle)
    n = h // m
    if pow(q, factor.degree() // 2, n) != n - 1:
        return None

    components = coprime_components(m)
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
    tests: list[LeftSubfieldTest] = []
    for left in components:
        for right in components:
            if left == 2 or right == 2:
                continue
            marginal = double_marginal(kernel, left, right, q)
            dft_matrix = dft_double_marginal(marginal, left, right, powers, m, field)
            right_orbits = q_orbits(right, q)
            for left_orbit in q_orbits(left, q):
                tests.append(
                    audit_left_orbit(
                        marginal,
                        dft_matrix,
                        left,
                        right,
                        left_orbit,
                        right_orbits,
                        m,
                        powers,
                        q,
                        field,
                        seed,
                        max_lambda_enumeration,
                    )
                )

    if not tests:
        return None
    return LeftSubfieldRow(
        D=D,
        q=q,
        ell=ell,
        h=h,
        m=m,
        n=n,
        factor_degree=factor.degree(),
        extension_degree=extension_degree,
        components=components,
        tests=tuple(tests),
    )


def scan(args: argparse.Namespace) -> list[LeftSubfieldRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    rows: list[LeftSubfieldRow] = []
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
            if sp.gcd(m, h // m) == 1
            and m <= args.max_m
            and len([c for c in coprime_components(m) if c > 2]) >= 2
            and 1 + sum(c - 1 for c in coprime_components(m)) <= args.max_axis_dim
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
        if not splits:
            continue
        case_had_cycle = False
        for q, roots in splits:
            full = find_full_cycle_prime(roots, D, q)
            if full is None:
                continue
            case_had_cycle = True
            ell, cycle = full
            shifted = rotate(cycle, args.origin_shift % h)
            for m in quotient_sizes:
                if not quotient_m_can_match_filters(q, m, args):
                    continue
                extension_degree = int(sp.n_order(q % m, m))
                if extension_degree > args.max_extension_degree:
                    continue
                n = h // m
                axis_dim = 1 + sum(c - 1 for c in coprime_components(m))
                for factor in packet_factors(n, q):
                    if factor.degree() == 1 and not args.include_linear:
                        continue
                    if args.require_factor_degree_axis and factor.degree() < axis_dim:
                        continue
                    if factor.degree() < args.min_factor_degree:
                        continue
                    if factor.degree() > args.max_factor_degree:
                        continue
                    row = audit_packet(
                        D,
                        q,
                        ell,
                        shifted,
                        m,
                        factor,
                        args.seed,
                        args.max_lambda_enumeration,
                    )
                    if row is not None and row_matches_filters(row, args):
                        rows.append(row)
                        if len(rows) >= args.max_rows:
                            return rows
        if case_had_cycle:
            cases += 1
            if cases >= args.max_cases:
                break
    return rows


def p24_forecast() -> str:
    p = 10**24 + 7
    left = 157
    right = 211
    left_len = int(sp.n_order(p % left, left))
    right_len = int(sp.n_order(p % right, right))
    right_orbits = (right - 1) // right_len
    return (
        "p24_left_subfield_target: "
        f"left_degree={left_len} right_degree={right_len} "
        f"gcd={gcd(left_len, right_len)} transformed_count="
        f"{right_orbits * right_len} need_span={left_len}; "
        "need_156_independent_transformed_coordinates=1"
    )


def format_hist(histogram: tuple[tuple[int, int], ...]) -> str:
    return "{" + ",".join(f"{length}:{count}" for length, count in histogram) + "}"


def format_test(test: LeftSubfieldTest) -> str:
    return (
        f"({test.left},{test.right})[{test.left_orbit_rep}]"
        f":L{test.left_orbit_len}:right{test.right_orbit_count}"
        f":Rhist{format_hist(test.right_orbit_len_histogram)}"
        f":coprime{int(test.right_lens_coprime_to_left)}"
        f":count{test.transformed_count}"
        f":rank{test.transformed_fq_rank}"
        f":deleteone{test.delete_one_min_transformed_rank}"
        f":deletefull{test.delete_one_full_count}/{test.right_orbit_count}"
        f":deleteann{test.delete_one_min_annihilator_q_degree}"
        f":deleteannmis{test.delete_one_annihilator_degree_mismatches}"
        f":deleteannvanish{test.delete_one_annihilator_vanish_failures}"
        f":deletefullpoly{test.delete_one_full_field_annihilator_count}/{test.right_orbit_count}"
        f":deletepivots{test.delete_one_min_pivot_count}"
        f":deletepivotprefixes{[list(x) for x in test.delete_one_pivot_prefixes]}"
        f":deletepivotnorms{list(test.delete_one_pivot_norm_products_base)}"
        f":deletezeronorm{test.delete_one_zero_residual_norms}"
        f":leadmin{test.delete_one_leading_min_rank}"
        f":leadfull{test.delete_one_leading_full_count}/{test.right_orbit_count}"
        f":leadannmis{test.delete_one_leading_annihilator_degree_mismatches}"
        f":leadannvanish{test.delete_one_leading_annihilator_vanish_failures}"
        f":leadfullpoly{test.delete_one_leading_full_field_annihilator_count}/{test.right_orbit_count}"
        f":leadnorms{list(test.delete_one_leading_norm_products_base)}"
        f":leadzeronorm{test.delete_one_leading_zero_residual_norms}"
        f":fullblocks{list(test.delete_one_prefix_full_block_counts)}"
        f":taillens{list(test.delete_one_prefix_tail_lengths)}"
        f":fullblockrank{test.delete_one_prefix_full_block_min_rank}"
        f":fullblockfull{test.delete_one_prefix_full_block_full_count}/{test.right_orbit_count}"
        f":tailaug{test.delete_one_prefix_tail_min_augmentation}"
        f":tailfull{test.delete_one_prefix_tail_full_count}/{test.right_orbit_count}"
        f":fullblockann{list(test.delete_one_prefix_full_block_ann_degrees)}"
        f":fullblocknorms{list(test.delete_one_prefix_full_block_norm_products_base)}"
        f":fullblockzeronorm{test.delete_one_prefix_full_block_zero_residual_norms}"
        f":tailann{list(test.delete_one_prefix_tail_ann_degrees)}"
        f":tailpivots{[list(x) for x in test.delete_one_prefix_tail_pivot_prefixes]}"
        f":tailnorms{list(test.delete_one_prefix_tail_norm_products_base)}"
        f":tailzeronorm{test.delete_one_prefix_tail_zero_residual_norms}"
        f":ann{test.annihilator_q_degree}"
        f":annmatch{int(test.annihilator_degree_matches_rank)}"
        f":annvanish{test.annihilator_vanish_failures}"
        f":fullpoly{int(test.full_field_annihilator)}"
        f":pivots{test.pivot_count}"
        f":pivotprefix{list(test.pivot_prefix)}"
        f":pivotnorm{test.pivot_norm_product_base}"
        f":zeronorm{test.zero_residual_norms}"
        f":profile{test.centered_right_profile_rank}"
        f":profilematch{int(test.centered_profile_rank_match)}"
        f":profilesubfail{test.centered_profile_subfield_failures}"
        f":baserank{test.centered_base_rank}"
        f":baseapp{int(test.centered_base_rank_applicable)}"
        f":basematch{int(test.centered_base_profile_rank_match)}"
        f":profiledefect{test.centered_profile_stability_defect}"
        f":profilemaxsingle{test.centered_profile_max_single_normal_rank}"
        f":profilenormal{test.centered_profile_normal_coordinate_count}"
        f":tracesupport{int(test.centered_trace_support_checked)}"
        f":tracelambdas{test.centered_trace_lambda_count}"
        f":traceminorbit{test.centered_trace_min_right_orbit_support}"
        f":tracezero{test.centered_trace_zero_support_count}"
        f":traceone{test.centered_trace_one_support_count}"
        f":subfail{test.left_subfield_failures}"
        f":maxsingle{test.max_single_normal_rank}"
        f":normalcount{test.normal_coordinate_count}"
        f":full{int(test.full_left_span)}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-rows", type=int, default=20)
    parser.add_argument("--max-cases", type=int, default=80)
    parser.add_argument("--min-h", type=int, default=12)
    parser.add_argument("--max-h", type=int, default=500)
    parser.add_argument("--max-abs-D", type=int, default=500000)
    parser.add_argument("--max-prime-quotients", type=int, default=24)
    parser.add_argument("--max-composite-quotients", type=int, default=80)
    parser.add_argument("--min-n", type=int, default=3)
    parser.add_argument("--max-n", type=int, default=500)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=2_000_000)
    parser.add_argument("--max-splitting-primes", type=int, default=1)
    parser.add_argument("--max-axis-dim", type=int, default=160)
    parser.add_argument("--max-m", type=int, default=420)
    parser.add_argument("--max-factor-degree", type=int, default=120)
    parser.add_argument("--min-factor-degree", type=int, default=1)
    parser.add_argument("--require-factor-degree-axis", action="store_true")
    parser.add_argument("--max-extension-degree", type=int, default=8)
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--origin-shift", type=int, default=0)
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--min-left-orbit-len", type=int, default=0)
    parser.add_argument("--min-pivot-count", type=int, default=0)
    parser.add_argument("--require-coprime-lens", action="store_true")
    parser.add_argument("--require-full-span", action="store_true")
    parser.add_argument("--max-lambda-enumeration", type=int, default=50_000)
    parser.add_argument("--seed", type=int, default=20260605)
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args()

    rows = scan(args)
    tests = [test for row in rows for test in row.tests]
    coprime_tests = [test for test in tests if test.right_lens_coprime_to_left]
    subfield_failures = sum(test.left_subfield_failures for test in tests)
    ann_mismatches = [
        test for test in tests if not test.annihilator_degree_matches_rank
    ]
    ann_vanish_failures = sum(test.annihilator_vanish_failures for test in tests)
    zero_residual_norms = sum(test.zero_residual_norms for test in tests)
    profile_mismatches = [
        test for test in tests if not test.centered_profile_rank_match
    ]
    profile_subfield_failures = sum(
        test.centered_profile_subfield_failures for test in tests
    )
    profile_stable_tests = [
        test for test in tests if test.centered_profile_stability_defect == 0
    ]
    base_rank_applicable = [test for test in tests if test.centered_base_rank_applicable]
    base_rank_mismatches = [
        test for test in base_rank_applicable
        if not test.centered_base_profile_rank_match
    ]
    profile_normal_tests = [
        test for test in tests if test.centered_profile_normal_coordinate_count > 0
    ]
    missing_pivot_norms = [
        test for test in tests if test.pivot_norm_product_base is None
    ]
    normal_tests = [test for test in tests if test.has_single_normal_coordinate]
    full_tests = [test for test in tests if test.full_left_span]
    delete_one_full_tests = [
        test for test in tests
        if test.delete_one_min_transformed_rank >= test.left_orbit_len
    ]
    delete_one_ann_mismatches = sum(
        test.delete_one_annihilator_degree_mismatches for test in tests
    )
    delete_one_ann_vanish_failures = sum(
        test.delete_one_annihilator_vanish_failures for test in tests
    )
    delete_one_zero_residual_norms = sum(
        test.delete_one_zero_residual_norms for test in tests
    )
    delete_one_full_poly_all_tests = [
        test for test in tests
        if test.delete_one_full_field_annihilator_count == test.right_orbit_count
    ]
    delete_one_leading_full_tests = [
        test for test in tests
        if test.delete_one_leading_full_count == test.right_orbit_count
    ]
    delete_one_leading_ann_mismatches = sum(
        test.delete_one_leading_annihilator_degree_mismatches for test in tests
    )
    delete_one_leading_ann_vanish_failures = sum(
        test.delete_one_leading_annihilator_vanish_failures for test in tests
    )
    delete_one_leading_zero_residual_norms = sum(
        test.delete_one_leading_zero_residual_norms for test in tests
    )
    delete_one_leading_full_poly_all_tests = [
        test for test in tests
        if test.delete_one_leading_full_field_annihilator_count == test.right_orbit_count
    ]
    delete_one_full_block_all_tests = [
        test for test in tests
        if test.delete_one_prefix_full_block_full_count == test.right_orbit_count
    ]
    delete_one_tail_full_all_tests = [
        test for test in tests
        if test.delete_one_prefix_tail_full_count == test.right_orbit_count
    ]
    delete_one_prefix_tail_zero_residual_norms = sum(
        test.delete_one_prefix_tail_zero_residual_norms for test in tests
    )
    delete_one_prefix_full_block_zero_residual_norms = sum(
        test.delete_one_prefix_full_block_zero_residual_norms for test in tests
    )
    delete_one_prefix_full_block_norm_products_missing = sum(
        sum(
            1
            for value in test.delete_one_prefix_full_block_norm_products_base
            if value is None
        )
        for test in tests
    )
    delete_one_prefix_tail_norm_products_missing = sum(
        sum(1 for value in test.delete_one_prefix_tail_norm_products_base if value is None)
        for test in tests
    )
    full_poly_tests = [test for test in tests if test.full_field_annihilator]
    trace_support_checked = [
        test for test in tests if test.centered_trace_support_checked
    ]
    trace_zero_support = [
        test for test in trace_support_checked
        if test.centered_trace_zero_support_count
    ]
    trace_one_support = [
        test for test in trace_support_checked
        if test.centered_trace_one_support_count
    ]

    print("Hermitian mixed left-subfield normality audit")
    print(f"max_rows={args.max_rows}")
    print(f"max_h={args.max_h}")
    print(f"q_stop={args.q_stop}")
    print(f"max_axis_dim={args.max_axis_dim}")
    print(f"min_left_orbit_len={args.min_left_orbit_len}")
    print(f"require_coprime_lens={int(args.require_coprime_lens)}")
    print(f"require_full_span={int(args.require_full_span)}")
    print(f"max_lambda_enumeration={args.max_lambda_enumeration}")
    print(p24_forecast())
    print()
    if not args.summary_only:
        print(
            "columns: D q ell h m n deg ext comps "
            "tests=(c,d)[u0]:L:right:Rhist:coprime:count:rank:"
            "deleteone:deletefull:deleteann:deleteannmis:deleteannvanish:"
            "deletefullpoly:deletepivots:deletepivotprefixes:deletepivotnorms:"
            "deletezeronorm:leadmin:leadfull:leadannmis:leadannvanish:"
            "leadfullpoly:leadnorms:leadzeronorm:"
            "fullblocks:taillens:fullblockrank:fullblockfull:tailaug:tailfull:"
            "fullblockann:fullblocknorms:fullblockzeronorm:"
            "tailann:tailpivots:tailnorms:tailzeronorm:"
            "ann:annmatch:annvanish:fullpoly:pivots:pivotprefix:"
            "pivotnorm:zeronorm:profile:profilematch:profilesubfail:"
            "baserank:baseapp:basematch:profiledefect:"
            "profilemaxsingle:profilenormal:tracesupport:tracelambdas:"
            "traceminorbit:tracezero:traceone:subfail:"
            "maxsingle:normalcount:full"
        )
        for row in rows[:80]:
            formatted = ",".join(format_test(test) for test in row.tests)
            print(
                f"D={row.D:8d} q={row.q:8d} ell={row.ell:3d} "
                f"h={row.h:4d} m={row.m:4d} n={row.n:4d} "
                f"deg={row.factor_degree:4d} ext={row.extension_degree:2d} "
                f"comps={list(row.components)} tests={formatted}"
            )

    print()
    print("summary")
    print(f"  rows={len(rows)}")
    print(f"  tests={len(tests)}")
    print(f"  coprime_left_right_tests={len(coprime_tests)}")
    print(f"  left_subfield_failures={subfield_failures}")
    print(f"  annihilator_degree_mismatches={len(ann_mismatches)}")
    print(f"  annihilator_vanish_failures={ann_vanish_failures}")
    print(f"  zero_residual_norms={zero_residual_norms}")
    print(f"  centered_profile_rank_mismatches={len(profile_mismatches)}")
    print(f"  centered_profile_subfield_failures={profile_subfield_failures}")
    print(f"  centered_base_rank_applicable_tests={len(base_rank_applicable)}")
    print(f"  centered_base_profile_rank_mismatches={len(base_rank_mismatches)}")
    print(f"  centered_profile_stable_tests={len(profile_stable_tests)}")
    print(f"  centered_profile_normal_coordinate_tests={len(profile_normal_tests)}")
    print(f"  missing_pivot_norm_products={len(missing_pivot_norms)}")
    print(f"  full_left_span_tests={len(full_tests)}")
    print(f"  delete_one_full_left_span_tests={len(delete_one_full_tests)}")
    print(f"  delete_one_annihilator_degree_mismatches={delete_one_ann_mismatches}")
    print(f"  delete_one_annihilator_vanish_failures={delete_one_ann_vanish_failures}")
    print(f"  delete_one_zero_residual_norms={delete_one_zero_residual_norms}")
    print(
        "  delete_one_full_field_annihilator_all_tests="
        f"{len(delete_one_full_poly_all_tests)}"
    )
    print(f"  delete_one_leading_full_tests={len(delete_one_leading_full_tests)}")
    print(
        "  delete_one_leading_annihilator_degree_mismatches="
        f"{delete_one_leading_ann_mismatches}"
    )
    print(
        "  delete_one_leading_annihilator_vanish_failures="
        f"{delete_one_leading_ann_vanish_failures}"
    )
    print(
        "  delete_one_leading_zero_residual_norms="
        f"{delete_one_leading_zero_residual_norms}"
    )
    print(
        "  delete_one_leading_full_field_annihilator_all_tests="
        f"{len(delete_one_leading_full_poly_all_tests)}"
    )
    print(
        "  delete_one_prefix_full_block_full_all_tests="
        f"{len(delete_one_full_block_all_tests)}"
    )
    print(
        "  delete_one_prefix_tail_full_all_tests="
        f"{len(delete_one_tail_full_all_tests)}"
    )
    print(
        "  delete_one_prefix_full_block_zero_residual_norms="
        f"{delete_one_prefix_full_block_zero_residual_norms}"
    )
    print(
        "  delete_one_prefix_full_block_norm_products_missing="
        f"{delete_one_prefix_full_block_norm_products_missing}"
    )
    print(
        "  delete_one_prefix_tail_zero_residual_norms="
        f"{delete_one_prefix_tail_zero_residual_norms}"
    )
    print(
        "  delete_one_prefix_tail_norm_products_missing="
        f"{delete_one_prefix_tail_norm_products_missing}"
    )
    print(f"  full_field_annihilator_tests={len(full_poly_tests)}")
    print(f"  individual_normal_coordinate_tests_diagnostic={len(normal_tests)}")
    print(f"  centered_trace_support_checked_tests={len(trace_support_checked)}")
    print(f"  centered_trace_zero_support_tests={len(trace_zero_support)}")
    print(f"  centered_trace_one_support_tests={len(trace_one_support)}")
    if tests:
        print(f"  max_transformed_fq_rank={max(t.transformed_fq_rank for t in tests)}")
        print(
            "  max_delete_one_min_transformed_rank="
            f"{max(t.delete_one_min_transformed_rank for t in tests)}"
        )
        print(
            "  max_delete_one_min_annihilator_q_degree="
            f"{max(t.delete_one_min_annihilator_q_degree for t in tests)}"
        )
        print(
            "  max_delete_one_full_field_annihilator_count="
            f"{max(t.delete_one_full_field_annihilator_count for t in tests)}"
        )
        print(
            "  max_delete_one_leading_min_rank="
            f"{max(t.delete_one_leading_min_rank for t in tests)}"
        )
        print(
            "  max_delete_one_leading_full_count="
            f"{max(t.delete_one_leading_full_count for t in tests)}"
        )
        print(
            "  max_delete_one_prefix_full_block_count="
            f"{max(max(t.delete_one_prefix_full_block_counts) for t in tests)}"
        )
        print(
            "  max_delete_one_prefix_tail_length="
            f"{max(max(t.delete_one_prefix_tail_lengths) for t in tests)}"
        )
        print(
            "  max_delete_one_prefix_full_block_min_rank="
            f"{max(t.delete_one_prefix_full_block_min_rank for t in tests)}"
        )
        print(
            "  max_delete_one_prefix_tail_min_augmentation="
            f"{max(t.delete_one_prefix_tail_min_augmentation for t in tests)}"
        )
        print(
            "  max_delete_one_prefix_tail_ann_degree="
            f"{max(max(t.delete_one_prefix_tail_ann_degrees) for t in tests)}"
        )
        print(f"  max_annihilator_q_degree={max(t.annihilator_q_degree for t in tests)}")
        print(f"  max_pivot_count={max(t.pivot_count for t in tests)}")
        print(
            "  max_centered_right_profile_rank="
            f"{max(t.centered_right_profile_rank for t in tests)}"
        )
        print(f"  max_centered_base_rank={max(t.centered_base_rank for t in tests)}")
        print(
            "  max_centered_profile_stability_defect="
            f"{max(t.centered_profile_stability_defect for t in tests)}"
        )
        print(
            "  max_centered_profile_single_normal_rank="
            f"{max(t.centered_profile_max_single_normal_rank for t in tests)}"
        )
        print(
            "  max_individual_normal_rank_diagnostic="
            f"{max(t.max_single_normal_rank for t in tests)}"
        )
        print(f"  max_left_orbit_len={max(t.left_orbit_len for t in tests)}")
    if trace_support_checked:
        print(
            "  min_centered_trace_right_orbit_support="
            f"{min(t.centered_trace_min_right_orbit_support for t in trace_support_checked)}"
        )
        print(
            "  max_centered_trace_lambda_count="
            f"{max(t.centered_trace_lambda_count for t in trace_support_checked)}"
        )
    print()
    print("interpretation")
    print("  zero_subfield_failures_supports_left_subfield_landing=1")
    print("  zero_annihilator_mismatches_confirms_subspace_polynomial_degree=rank=1")
    print("  zero_profile_mismatches_confirms_centered_right_profile_equivalence=1")
    print("  base_rank_match_applies_when_left_orbit_is_all_nontrivial_characters=1")
    print("  delete_one_rank_tests_delsarte_right_orbit_support_candidate=1")
    print("  delete_one_annihilators_are_moore_punit_certificate_candidates=1")
    print("  delete_one_leading_prefix_tests_deterministic_minor_candidate=1")
    print("  leading_prefix_splits_into_full_right_blocks_plus_tail=1")
    print("  full_block_residual_norm_products_are_prefix_punit_candidates=1")
    print("  tail_residual_norm_products_are_quotient_punit_candidates=1")
    print("  profile_stability_defect_tests_galois_stable_normal_frame_candidate=1")
    print("  centered_trace_support_tests_cyclic_code_obstruction=1")
    print("  individual_normality_is_diagnostic_not_sufficient=1")
    print("  full_left_span_requires_enough_independent_transformed_coordinates=1")
    print("  p24_target_is_210_coordinate_span_not_one_normal_coordinate=1")
    print("conclusion=reported_hermitian_mixed_left_subfield_normality_audit")


if __name__ == "__main__":
    main()
