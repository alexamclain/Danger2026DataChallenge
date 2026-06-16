#!/usr/bin/env python3
"""Boundary for the tempting right-unit proof of order-7 augmentation.

The order-7 augmentation target would follow immediately from a very strong
symmetry:

    C(a,b) = C(a, eta*b)

for the centered mixed marginal, with eta acting trivially on the left
component and nontrivially on the right quotient.  Then every nontrivial
right quotient-character projection is both fixed and multiplied by a
nontrivial scalar, so it is zero.

This script records that finite implication and checks a pinned actual-CM
row.  The actual row is not p24-sized, but it has the same kind of mixed
Hermitian marginal packet and a nontrivial right quotient character.  It shows
that the multiplier symmetry is not a generic class-torsor automorphism.
"""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp
from cypari2 import Pari

from cycle_period_complexity_scan import find_full_cycle_prime
from hermitian_double_marginal_audit import (
    centered_double_marginal,
    double_marginal,
    kernel_matrix,
)
from hermitian_double_marginal_fourier_audit import dft_double_marginal, zeta_powers
from k_character_tensor_rank_scan import (
    ExtensionField,
    FpE,
    find_irreducible_modulus,
    primitive_root_of_order,
)
from packetized_relative_content_scan import packet_factors
from relative_moment_projection_scan import (
    find_splitting_primes,
    rotate,
    section_fiber_polynomials,
)


PINNED_D = -13319
PINNED_Q = 13463
PINNED_M = 28
LEFT = 4
RIGHT = 7
LEFT_U = 1
RIGHT_PRIMITIVE = 3
RIGHT_UNIT = 5  # 5 == 1 mod 4 and is nonsquare modulo 7.
SEED = 20260606


@dataclass(frozen=True)
class PinnedPacket:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    factor_degree: int
    centered: list[list[int]]
    dft: list[list[FpE]]
    field: ExtensionField


def right_log_table() -> dict[int, int]:
    value = 1
    logs: dict[int, int] = {}
    for exponent in range(RIGHT - 1):
        logs[value] = exponent
        value = value * RIGHT_PRIMITIVE % RIGHT
    if len(logs) != RIGHT - 1:
        raise RuntimeError("RIGHT_PRIMITIVE is not primitive")
    return logs


def quotient_character(value: int) -> int:
    # For RIGHT=7 and q=2 mod 7, the Frobenius subgroup is the square subgroup
    # {1,2,4}; the quotient has order two and the character is the Legendre
    # symbol.
    return 1 if right_log_table()[value] % 2 == 0 else -1


def load_pinned_packet() -> PinnedPacket:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    hilbert = pari.polclass(PINNED_D)
    h = int(pari.poldegree(hilbert))
    splits = find_splitting_primes(
        pari,
        hilbert,
        h,
        PINNED_Q,
        PINNED_Q + 1,
        1,
    )
    if not splits:
        raise RuntimeError("pinned splitting prime not found")
    q, roots = splits[0]
    full = find_full_cycle_prime(roots, PINNED_D, q)
    if full is None:
        raise RuntimeError("pinned full cycle not found")
    ell, cycle = full
    shifted = rotate(cycle, 0)
    n = h // PINNED_M
    factors = [factor for factor in packet_factors(n, q) if factor.degree() == 4]
    if not factors:
        raise RuntimeError("pinned degree-4 packet factor not found")
    factor = factors[0]

    residues = [
        fiber.rem(factor)
        for fiber in section_fiber_polynomials(shifted, q, PINNED_M, "complement")
    ]
    kernel = kernel_matrix(residues, factor, q)
    marginal = double_marginal(kernel, LEFT, RIGHT, q)
    centered = centered_double_marginal(marginal, q)

    extension_degree = int(sp.n_order(q % PINNED_M, PINNED_M))
    modulus = find_irreducible_modulus(q, extension_degree, SEED)
    field = ExtensionField(q, extension_degree, modulus)
    zeta = primitive_root_of_order(field, PINNED_M, SEED)
    powers = zeta_powers(zeta, PINNED_M, field)
    dft = dft_double_marginal(marginal, LEFT, RIGHT, powers, PINNED_M, field)
    return PinnedPacket(
        D=PINNED_D,
        q=q,
        ell=ell,
        h=h,
        m=PINNED_M,
        n=n,
        factor_degree=factor.degree(),
        centered=centered,
        dft=dft,
        field=field,
    )


def multiplier_invariance_failures(centered: list[list[int]], q: int) -> int:
    failures = 0
    # centered rows/cols omit the zero residue, so index residue x is x-1.
    for a in range(1, LEFT):
        for b in range(1, RIGHT):
            left_image = a  # RIGHT_UNIT == 1 mod LEFT.
            right_image = (RIGHT_UNIT * b) % RIGHT
            if centered[a - 1][b - 1] % q != centered[left_image - 1][right_image - 1] % q:
                failures += 1
    return failures


def character_projection(packet: PinnedPacket, left_u: int = LEFT_U) -> FpE:
    total = packet.field.zero
    row = packet.dft[left_u - 1]
    for v in range(1, RIGHT):
        weight = quotient_character(v)
        term = packet.field.scalar_mul(weight, row[v - 1])
        total = packet.field.add(total, term)
    return total


def finite_implication_demo() -> tuple[int, int]:
    # A synthetic centered table invariant under b -> RIGHT_UNIT*b has zero
    # nontrivial quotient-character projection row by row.
    q = 101
    centered = [[0 for _ in range(1, RIGHT)] for _ in range(1, LEFT)]
    for a in range(1, LEFT):
        for b in range(1, RIGHT):
            centered[a - 1][b - 1] = 17 * a % q
    invariant_failures = multiplier_invariance_failures(centered, q)
    projection_nonzeroes = 0
    for row in centered:
        projection = sum(quotient_character(v) * row[v - 1] for v in range(1, RIGHT)) % q
        projection_nonzeroes += int(projection != 0)
    return invariant_failures, projection_nonzeroes


def main() -> None:
    demo_invariance_failures, demo_projection_nonzeroes = finite_implication_demo()
    packet = load_pinned_packet()
    actual_invariance_failures = multiplier_invariance_failures(packet.centered, packet.q)
    projection = character_projection(packet)
    projection_nonzero = projection != packet.field.zero

    print("Trace-GCD fixed-frequency unit-symmetry boundary")
    print("finite_implication")
    print(f"  synthetic_multiplier_invariance_failures={demo_invariance_failures}")
    print(f"  synthetic_nontrivial_projection_nonzeroes={demo_projection_nonzeroes}")
    print("pinned_actual_cm_row")
    print(f"  D={packet.D}")
    print(f"  q={packet.q}")
    print(f"  h={packet.h}")
    print(f"  m={packet.m}")
    print(f"  n={packet.n}")
    print(f"  factor_degree={packet.factor_degree}")
    print(f"  left_component={LEFT}")
    print(f"  right_component={RIGHT}")
    print(f"  right_unit={RIGHT_UNIT}")
    print(f"  right_quotient_character={[quotient_character(v) for v in range(1, RIGHT)]}")
    print(f"  actual_multiplier_invariance_failures={actual_invariance_failures}")
    print(f"  actual_projection_for_left_u1={projection}")
    print(f"  actual_projection_nonzero={int(projection_nonzero)}")
    print("interpretation")
    print("  multiplier_invariance_would_force_character_projection_zero=1")
    print("  actual_cm_packet_refutes_generic_multiplier_invariance=1")
    print("  right_unit_action_is_not_a_free_class_torsor_automorphism=1")
    print("  p24_order7_vanishing_needs_specific_arithmetic_not_formal_diamond_symmetry=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_unit_symmetry_boundary")

    if demo_invariance_failures or demo_projection_nonzeroes:
        raise SystemExit(1)
    if actual_invariance_failures == 0 or not projection_nonzero:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
