#!/usr/bin/env python3
"""Fast factor-level support audit for centered plateau subspaces.

The Fourier/Lang transform is invertible on each Frobenius orbit block.  To
measure how a plateau bad subspace touches those blocks, it is enough to reduce
the plateau basis polynomials modulo each irreducible factor of Y^right - 1
over F_q.  This avoids constructing extension-field DFT matrices.

For p24 shape we can take a small carrier field such as q=5, since
ord_211(5)=35 matches ord_211(p24)=35.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

import sympy as sp
from cypari2 import Pari

from l1_axis_injectivity_scan import coeff_vector, rank_mod_q
from packetized_relative_content_scan import poly_from_coeffs

X = sp.symbols("X")


@dataclass(frozen=True)
class FactorBlock:
    factor_degree: int
    factor_label: str
    block_rank: int


def right_factors(right: int, q: int) -> list[sp.Poly]:
    pari = Pari()
    fac = pari(f"factor(Mod(1,{q})*(x^{right}-1))")
    out: list[sp.Poly] = []
    for i in range(len(fac[0])):
        factor = fac[0][i]
        exp = int(fac[1][i])
        if exp != 1:
            raise ValueError("right polynomial factor was not squarefree")
        degree = int(pari.poldegree(factor))
        coeffs = [int(pari.polcoef(factor, j)) % q for j in range(degree + 1)]
        out.append(poly_from_coeffs(coeffs, q))
    return sorted(out, key=lambda f: (f.degree(), str(f.as_expr())))


def plateau_basis_polys(right: int, left: int, start: int, zero_position: int, q: int) -> list[sp.Poly]:
    plateau = {(start + offset) % right for offset in range(left)}
    zero = zero_position % right
    polys: list[sp.Poly] = []
    if zero not in plateau:
        expr = sum(X**index for index in plateau)
        polys.append(sp.Poly(expr, X, modulus=q))
    for index in range(right):
        if index in plateau or index == zero:
            continue
        polys.append(sp.Poly(X**index, X, modulus=q))
    return polys


def factor_label(factor: sp.Poly) -> str:
    if factor.degree() == 1:
        root = (-int(factor.coeff_monomial(X**0))) % int(factor.get_modulus())
        return f"linear_root_{root}"
    return f"deg{factor.degree()}:{sp.srepr(factor.as_expr())[:48]}"


def audit(right: int, left: int, start: int, zero_position: int, q: int) -> tuple[int, list[FactorBlock]]:
    basis = plateau_basis_polys(right, left, start, zero_position, q)
    blocks: list[FactorBlock] = []
    for factor in right_factors(right, q):
        vectors = [coeff_vector(poly.rem(factor), factor.degree(), q) for poly in basis]
        blocks.append(
            FactorBlock(
                factor_degree=factor.degree(),
                factor_label=factor_label(factor),
                block_rank=rank_mod_q(vectors, q),
            )
        )
    return len(basis), blocks


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, required=True)
    parser.add_argument("--right", type=int, required=True)
    parser.add_argument("--left", type=int, required=True)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--zero-position", type=int, default=0)
    args = parser.parse_args()

    dim, blocks = audit(args.right, args.left, args.start, args.zero_position, args.q)
    nonzero_blocks = [block for block in blocks if block.block_rank]
    print("Centered plateau factor-support audit")
    print(f"q={args.q}")
    print(f"right={args.right}")
    print(f"left_plateau_length={args.left}")
    print(f"start={args.start}")
    print(f"zero_position={args.zero_position % args.right}")
    print(f"ord_right_q={int(sp.n_order(args.q % args.right, args.right))}")
    print(f"plateau_subspace_dim={dim}")
    print(f"factor_count={len(blocks)}")
    print(f"nonzero_factor_blocks={len(nonzero_blocks)}/{len(blocks)}")
    print("block_rank_profile")
    for block in blocks:
        print(
            f"  degree={block.factor_degree:3d} "
            f"rank={block.block_rank:3d} label={block.factor_label}"
        )
    print()
    print("interpretation")
    print("  lang_block_rank_equals_residue_rank_mod_right_factor=1")
    print("  all_blocks_nonzero_means_no_small_block_support_shortcut=1")
    print("conclusion=reported_centered_plateau_factor_support_audit")


if __name__ == "__main__":
    main()
