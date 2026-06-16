#!/usr/bin/env python3
"""Finite gate for the full Gaussian-DFT plus truncated-tail form.

In the p24 square coinvariant target the four full right blocks have length
35, but the tail contributes only the first 16 right Lang coordinates.  After
scalar extension to `K = F_p(mu_35)`, the full blocks are diagonalized by the
length-35 DFT.  The truncated tail is not diagonal: it becomes the
Reed-Solomon/Vandermonde subspace of degree `<16` polynomials evaluated on the
35 frequency points.

This toy checks the finite identity in a small field:

* F_q-rank of the original time-domain columns equals K-rank after faithful
  scalar extension;
* DFT of the full prefix blocks is an invertible source change;
* the first `tail_dim` time-domain tail columns are reconstructed from the
  full tail spectrum by the corresponding Vandermonde rows.

The arithmetic p24 theorem would have to prove p-unitness for the actual CM
Gaussian/RS-tail determinant, not just this linear algebra.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import random

import sympy as sp

from hermitian_mixed_lang_normality_audit import subfield_power_basis
from k_character_tensor_rank_scan import (
    ExtensionField,
    FpE,
    find_irreducible_modulus,
    primitive_root_of_order,
)
from l1_axis_injectivity_scan import rank_mod_q


@dataclass(frozen=True)
class GaussianRsTailRow:
    label: str
    q: int
    right_len: int
    k_degree: int
    left_degree: int
    prefix_blocks: int
    tail_dim: int
    source_dim: int
    time_rank: int
    diagonal_k_rank: int
    spectral_k_rank: int
    diagonal_fq_rank: int
    spectral_fq_rank: int
    tail_reconstruction_failures: int
    rank_match: bool
    full_rank: bool


def random_element(field: ExtensionField, rng: random.Random) -> FpE:
    return tuple(rng.randrange(field.q) for _ in range(field.degree))


def product_vector_to_fq(vector: tuple[FpE, ...]) -> list[int]:
    coords: list[int] = []
    for component in vector:
        coords.extend(component)
    return coords


def product_k_rank(
    vectors: list[tuple[FpE, ...]],
    k_basis: list[FpE],
    field: ExtensionField,
) -> tuple[int, int]:
    if not vectors:
        return 0, 0
    rows: list[list[int]] = []
    for vector in vectors:
        for kappa in k_basis:
            scaled_components: list[FpE] = []
            for component_index, component in enumerate(vector):
                embedded = field.pow(kappa, field.q**component_index)
                scaled_components.append(field.mul(embedded, component))
            rows.append(product_vector_to_fq(tuple(scaled_components)))
    fq_rank = rank_mod_q(rows, field.q)
    if fq_rank % len(k_basis):
        raise AssertionError("faithful K-span F_q-rank was not divisible by [K:F_q]")
    return fq_rank // len(k_basis), fq_rank


def diagonal_product_vector(value: FpE, k_degree: int) -> tuple[FpE, ...]:
    return tuple(value for _ in range(k_degree))


def spectral_component(
    values: list[FpE],
    frequency: int,
    component_index: int,
    omega: FpE,
    field: ExtensionField,
) -> FpE:
    omega_component = field.pow(omega, field.q**component_index)
    total = field.zero
    for time_index, value in enumerate(values):
        exponent = (-frequency * time_index) % (field.q ** field.degree - 1)
        coeff = field.pow(omega_component, exponent)
        total = field.add(total, field.mul(coeff, value))
    return total


def spectral_vector(
    values: list[FpE],
    frequency: int,
    k_degree: int,
    omega: FpE,
    field: ExtensionField,
) -> tuple[FpE, ...]:
    return tuple(
        spectral_component(values, frequency, component_index, omega, field)
        for component_index in range(k_degree)
    )


def tail_rs_vector(
    tail_spectrum: list[tuple[FpE, ...]],
    tail_index: int,
    right_len: int,
    omega: FpE,
    field: ExtensionField,
) -> tuple[FpE, ...]:
    inv_right = pow(right_len % field.q, -1, field.q)
    components: list[FpE] = []
    for component_index in range(len(tail_spectrum[0])):
        omega_component = field.pow(omega, field.q**component_index)
        total = field.zero
        for frequency, spectrum_value in enumerate(tail_spectrum):
            coeff = field.pow(omega_component, frequency * tail_index)
            total = field.add(
                total,
                field.mul(coeff, spectrum_value[component_index]),
            )
        components.append(field.scalar_mul(inv_right, total))
    return tuple(components)


def audit_tuple(
    label: str,
    prefix_values: list[list[FpE]],
    tail_values: list[FpE],
    tail_dim: int,
    k_basis: list[FpE],
    omega: FpE,
    field: ExtensionField,
) -> GaussianRsTailRow:
    right_len = len(tail_values)
    k_degree = len(k_basis)
    time_columns = [
        value for block in prefix_values for value in block
    ] + tail_values[:tail_dim]
    time_rank = rank_mod_q([list(value) for value in time_columns], field.q)

    diagonal_vectors = [
        diagonal_product_vector(value, k_degree) for value in time_columns
    ]
    diagonal_k_rank, diagonal_fq_rank = product_k_rank(
        diagonal_vectors, k_basis, field
    )

    spectral_vectors: list[tuple[FpE, ...]] = []
    for block in prefix_values:
        for frequency in range(right_len):
            spectral_vectors.append(
                spectral_vector(block, frequency, k_degree, omega, field)
            )
    tail_spectrum = [
        spectral_vector(tail_values, frequency, k_degree, omega, field)
        for frequency in range(right_len)
    ]
    tail_rs_vectors = [
        tail_rs_vector(tail_spectrum, tail_index, right_len, omega, field)
        for tail_index in range(tail_dim)
    ]
    spectral_vectors.extend(tail_rs_vectors)
    spectral_k_rank, spectral_fq_rank = product_k_rank(
        spectral_vectors, k_basis, field
    )

    tail_reconstruction_failures = sum(
        tail_rs_vectors[index] != diagonal_product_vector(tail_values[index], k_degree)
        for index in range(tail_dim)
    )
    source_dim = len(time_columns)
    return GaussianRsTailRow(
        label=label,
        q=field.q,
        right_len=right_len,
        k_degree=k_degree,
        left_degree=field.degree,
        prefix_blocks=len(prefix_values),
        tail_dim=tail_dim,
        source_dim=source_dim,
        time_rank=time_rank,
        diagonal_k_rank=diagonal_k_rank,
        spectral_k_rank=spectral_k_rank,
        diagonal_fq_rank=diagonal_fq_rank,
        spectral_fq_rank=spectral_fq_rank,
        tail_reconstruction_failures=tail_reconstruction_failures,
        rank_match=(
            time_rank == diagonal_k_rank == spectral_k_rank
            and diagonal_fq_rank == spectral_fq_rank
        ),
        full_rank=(time_rank == source_dim),
    )


def find_full_rank_data(
    prefix_blocks: int,
    right_len: int,
    tail_dim: int,
    k_basis: list[FpE],
    omega: FpE,
    field: ExtensionField,
    rng: random.Random,
    attempts: int,
) -> tuple[list[list[FpE]], list[FpE]]:
    for _ in range(attempts):
        prefix = [
            [random_element(field, rng) for _ in range(right_len)]
            for _ in range(prefix_blocks)
        ]
        tail = [random_element(field, rng) for _ in range(right_len)]
        row = audit_tuple("candidate", prefix, tail, tail_dim, k_basis, omega, field)
        if row.full_rank and row.rank_match:
            return prefix, tail
    raise RuntimeError("could not find a full-rank toy row")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=2)
    parser.add_argument("--right-len", type=int, default=5)
    parser.add_argument("--left-degree", type=int, default=12)
    parser.add_argument("--prefix-blocks", type=int, default=2)
    parser.add_argument("--tail-dim", type=int, default=2)
    parser.add_argument("--attempts", type=int, default=400)
    parser.add_argument("--seed", type=int, default=20260606)
    args = parser.parse_args()

    k_degree = int(sp.n_order(args.q % args.right_len, args.right_len))
    if args.left_degree % k_degree:
        raise SystemExit("left-degree must be divisible by ord_right(q)")
    if args.prefix_blocks * args.right_len + args.tail_dim > args.left_degree:
        raise SystemExit("source dimension must fit into the toy left field")
    field = ExtensionField(
        args.q,
        args.left_degree,
        find_irreducible_modulus(args.q, args.left_degree, args.seed),
    )
    k_basis = subfield_power_basis(args.q, k_degree, field, args.seed + 1)
    omega = primitive_root_of_order(field, args.right_len, args.seed + 2)
    rng = random.Random(args.seed)

    prefix, tail = find_full_rank_data(
        args.prefix_blocks,
        args.right_len,
        args.tail_dim,
        k_basis,
        omega,
        field,
        rng,
        args.attempts,
    )
    rows = [
        audit_tuple("random_full_rank", prefix, tail, args.tail_dim, k_basis, omega, field)
    ]

    prefix_dependent = [block[:] for block in prefix]
    prefix_dependent[1][0] = prefix_dependent[0][0]
    rows.append(
        audit_tuple(
            "forced_prefix_dependence",
            prefix_dependent,
            tail,
            args.tail_dim,
            k_basis,
            omega,
            field,
        )
    )

    tail_dependent = tail[:]
    tail_dependent[0] = prefix[0][0]
    rows.append(
        audit_tuple(
            "forced_tail_dependence",
            prefix,
            tail_dependent,
            args.tail_dim,
            k_basis,
            omega,
            field,
        )
    )

    print("Trace-GCD full Gaussian DFT / RS-tail toy")
    print(
        "columns: label q right_len k_degree left_degree prefix_blocks tail_dim "
        "source_dim time_rank diagonal_k_rank spectral_k_rank diagonal_fq_rank "
        "spectral_fq_rank tail_reconstruction_failures rank_match full_rank"
    )
    for row in rows:
        print(
            f"row label={row.label} q={row.q} right_len={row.right_len} "
            f"k_degree={row.k_degree} left_degree={row.left_degree} "
            f"prefix_blocks={row.prefix_blocks} tail_dim={row.tail_dim} "
            f"source_dim={row.source_dim} time_rank={row.time_rank} "
            f"diagonal_k_rank={row.diagonal_k_rank} "
            f"spectral_k_rank={row.spectral_k_rank} "
            f"diagonal_fq_rank={row.diagonal_fq_rank} "
            f"spectral_fq_rank={row.spectral_fq_rank} "
            f"tail_reconstruction_failures={row.tail_reconstruction_failures} "
            f"rank_match={int(row.rank_match)} full_rank={int(row.full_rank)}"
        )
    rank_failures = [row for row in rows if not row.rank_match]
    reconstruction_failures = sum(row.tail_reconstruction_failures for row in rows)
    full_rows = [row for row in rows if row.full_rank]
    low_rank_controls = [row for row in rows if not row.full_rank]
    print("totals")
    print(f"  rows={len(rows)}")
    print(f"  rank_mismatches={len(rank_failures)}")
    print(f"  tail_reconstruction_failures={reconstruction_failures}")
    print(f"  full_rank_rows={len(full_rows)}")
    print(f"  low_rank_controls={len(low_rank_controls)}")
    print("interpretation")
    print("  full_prefix_blocks_diagonalize_after_faithful_K_scalar_extension=1")
    print("  truncated_tail_becomes_degree_lt_tail_dim_RS_subspace=1")
    print("  p24_full_coinvariant_gaussian_rs_tail_shape=4x35_plus_16_to_156=1")
    print("conclusion=reported_trace_gcd_full_gaussian_rs_tail_toy")

    if rank_failures or reconstruction_failures or not full_rows or not low_rank_controls:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
