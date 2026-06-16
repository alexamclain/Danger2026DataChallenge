#!/usr/bin/env python3
"""Actual-CM boundary for right-axis covariance plus anchor descent.

The p24 fixed-frequency theorem is now concentrated on a right-axis statement:
after internal tracing, Frobenius covariance moves the right quotient cosets,
and one descended anchor coset would force all quotient-character projections
to vanish.

This script tests that exact *shape* on a small actual-CM row with the same
right-axis geometry:

    D = -6719, q = 6863, h = 105, m = 21 = 3 * 7, n = 5.

Here rho = Frob_q^2 fixes the left component 3 and has order 3 on the right
quotient of (Z/7Z)^*.  The internal generator q^6 fixes the right axis and
has order 2 on the relative n-layer.  We compute the actual additive right
resolvents, trace over that internal relative subgroup, and check:

* formal additive-resolvent covariance holds;
* Gauss-normalized quotient projections are rho-fixed;
* those fixed normalized projections are nevertheless nonzero.

So covariance plus Gauss normalization is still not enough.  The extra p24
input really is anchor descent / equal H-coset sums for the internally traced
profile, not just formal CM Frobenius covariance.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd, lcm

import sympy as sp
from cypari2 import Pari

from cycle_period_complexity_scan import find_full_cycle_prime
from k_character_tensor_rank_scan import (
    ExtensionField,
    FpE,
    find_irreducible_modulus,
    primitive_root_of_order,
)
from relative_moment_projection_scan import find_splitting_primes


D = -6719
Q = 6863
M = 21
N = 5
LEFT = 3
RIGHT = 7
RIGHT_GEN = 3
RHO_EXPONENT = 2
INTERNAL_EXPONENT = 6
QUOTIENT_ORDER = 3
SEED = 20260606


@dataclass(frozen=True)
class ActualCycle:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    cycle: tuple[int, ...]
    field: ExtensionField
    zeta_right: FpE
    zeta_rel: FpE
    zeta_quotient: FpE


def log_table_mod_prime(modulus: int, generator: int) -> dict[int, int]:
    logs: dict[int, int] = {}
    value = 1
    for exponent in range(modulus - 1):
        logs[value] = exponent
        value = value * generator % modulus
    if len(logs) != modulus - 1:
        raise RuntimeError("bad right primitive root")
    return logs


def subgroup_generated(modulus: int, generator: int) -> list[int]:
    values: list[int] = []
    value = 1
    while value not in values:
        values.append(value)
        value = value * generator % modulus
    return values


def cosets_by_log_residue(
    modulus: int,
    generator: int,
    quotient_order: int,
) -> list[list[int]]:
    logs = log_table_mod_prime(modulus, generator)
    return [
        sorted(
            [value for value in range(1, modulus) if logs[value] % quotient_order == residue],
            key=logs.__getitem__,
        )
        for residue in range(quotient_order)
    ]


def load_actual_cycle() -> ActualCycle:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    hilbert = pari.polclass(D)
    h = int(pari.poldegree(hilbert))
    splits = find_splitting_primes(pari, hilbert, h, Q, Q + 1, 1)
    if not splits:
        raise RuntimeError("pinned splitting prime not found")
    q, roots = splits[0]
    full = find_full_cycle_prime(roots, D, q)
    if full is None:
        raise RuntimeError("pinned full cycle not found")
    ell, cycle = full

    root_order = lcm(RIGHT, N, QUOTIENT_ORDER)
    extension_degree = int(sp.n_order(q % root_order, root_order))
    modulus = find_irreducible_modulus(q, extension_degree, SEED)
    field = ExtensionField(q, extension_degree, modulus)
    zeta = primitive_root_of_order(field, root_order, SEED)
    return ActualCycle(
        D=D,
        q=q,
        ell=ell,
        h=h,
        m=M,
        n=N,
        cycle=tuple(cycle),
        field=field,
        zeta_right=field.pow(zeta, root_order // RIGHT),
        zeta_rel=field.pow(zeta, root_order // N),
        zeta_quotient=field.pow(zeta, root_order // QUOTIENT_ORDER),
    )


def frobenius_power(value: FpE, field: ExtensionField, exponent: int) -> FpE:
    return field.pow(value, field.q**exponent)


def quotient_character(
    residue: int,
    logs: dict[int, int],
    zeta_quotient: FpE,
    field: ExtensionField,
    index: int,
) -> FpE:
    return field.pow(zeta_quotient, (index * logs[residue]) % QUOTIENT_ORDER)


def additive_resolvent(cycle: ActualCycle, right_frequency: int, rel_frequency: int) -> FpE:
    total = cycle.field.zero
    for index, j_value in enumerate(cycle.cycle):
        r = index % cycle.m
        k = index // cycle.m
        right_weight = cycle.field.pow(
            cycle.zeta_right,
            (right_frequency * (r % RIGHT)) % RIGHT,
        )
        rel_weight = cycle.field.pow(
            cycle.zeta_rel,
            (rel_frequency * k) % cycle.n,
        )
        total = cycle.field.add(
            total,
            cycle.field.mul(
                cycle.field.mul(right_weight, rel_weight),
                cycle.field.embed(j_value),
            ),
        )
    return total


def internally_traced_profile(cycle: ActualCycle, rel_coset_rep: int) -> list[FpE]:
    internal = subgroup_generated(cycle.n, pow(cycle.q, INTERNAL_EXPONENT, cycle.n))
    profile = [cycle.field.zero for _ in range(RIGHT)]
    for right_frequency in range(1, RIGHT):
        total = cycle.field.zero
        for rel_multiplier in internal:
            total = cycle.field.add(
                total,
                additive_resolvent(
                    cycle,
                    right_frequency,
                    (rel_coset_rep * rel_multiplier) % cycle.n,
                ),
            )
        profile[right_frequency] = total
    return profile


def h_coset_sums(profile: list[FpE], cosets: list[list[int]], field: ExtensionField) -> list[FpE]:
    sums: list[FpE] = []
    for coset in cosets:
        total = field.zero
        for residue in coset:
            total = field.add(total, profile[residue])
        sums.append(total)
    return sums


def quotient_projection(
    profile: list[FpE],
    logs: dict[int, int],
    zeta_quotient: FpE,
    field: ExtensionField,
    index: int,
) -> FpE:
    total = field.zero
    for residue in range(1, RIGHT):
        total = field.add(
            total,
            field.mul(
                quotient_character(residue, logs, zeta_quotient, field, index),
                profile[residue],
            ),
        )
    return total


def right_gauss_sum(
    cycle: ActualCycle,
    logs: dict[int, int],
    index: int,
) -> FpE:
    total = cycle.field.zero
    for residue in range(1, RIGHT):
        total = cycle.field.add(
            total,
            cycle.field.mul(
                quotient_character(
                    residue,
                    logs,
                    cycle.zeta_quotient,
                    cycle.field,
                    index,
                ),
                cycle.field.pow(cycle.zeta_right, residue),
            ),
        )
    return total


def main() -> None:
    cycle = load_actual_cycle()
    logs = log_table_mod_prime(RIGHT, RIGHT_GEN)
    rho_right = pow(cycle.q, RHO_EXPONENT, RIGHT)
    internal_right = pow(cycle.q, INTERNAL_EXPONENT, RIGHT)
    rho_left = pow(cycle.q, RHO_EXPONENT, LEFT)
    internal_rel = pow(cycle.q, INTERNAL_EXPONENT, cycle.n)
    internal = subgroup_generated(cycle.n, internal_rel)
    rel_cosets = []
    seen: set[int] = set()
    for start in range(1, cycle.n):
        if start in seen:
            continue
        coset = sorted((start * value) % cycle.n for value in internal)
        seen.update(coset)
        rel_cosets.append(coset)
    h_cosets = cosets_by_log_residue(RIGHT, RIGHT_GEN, QUOTIENT_ORDER)

    covariance_failures = 0
    anchor_descended = 0
    equal_h_coset_sums = 0
    nonzero_normalized_projections = 0
    normalized_projection_fixed = 0
    checked_projections = 0
    coset_sum_rows: list[list[FpE]] = []
    normalized_values: list[FpE] = []

    for rel_coset in rel_cosets:
        profile = internally_traced_profile(cycle, rel_coset[0])
        for right_frequency in range(1, RIGHT):
            expected = profile[(rho_right * right_frequency) % RIGHT]
            actual = frobenius_power(profile[right_frequency], cycle.field, RHO_EXPONENT)
            covariance_failures += int(actual != expected)

        sums = h_coset_sums(profile, h_cosets, cycle.field)
        coset_sum_rows.append(sums)
        equal_h_coset_sums += int(len(set(sums)) == 1)
        anchor_descended += int(
            frobenius_power(sums[0], cycle.field, RHO_EXPONENT) == sums[0]
        )

        for character_index in range(1, QUOTIENT_ORDER):
            tau = right_gauss_sum(cycle, logs, character_index)
            projection = quotient_projection(
                profile,
                logs,
                cycle.zeta_quotient,
                cycle.field,
                character_index,
            )
            normalized = cycle.field.div(projection, tau)
            normalized_values.append(normalized)
            nonzero_normalized_projections += int(normalized != cycle.field.zero)
            normalized_projection_fixed += int(
                frobenius_power(normalized, cycle.field, RHO_EXPONENT) == normalized
            )
            checked_projections += 1

    print("Trace-GCD fixed-frequency actual-CM right-axis covariance boundary")
    print(f"D={cycle.D}")
    print(f"q={cycle.q}")
    print(f"ell={cycle.ell}")
    print(f"h={cycle.h}")
    print(f"m={cycle.m}")
    print(f"n={cycle.n}")
    print(f"left={LEFT}")
    print(f"right={RIGHT}")
    print(f"right_primitive_root={RIGHT_GEN}")
    print(f"quotient_order={QUOTIENT_ORDER}")
    print(f"field_degree_for_mu_right_mu_n={cycle.field.degree}")
    print(f"rho_exponent={RHO_EXPONENT}")
    print(f"rho_left_mod_left={rho_left}")
    print(f"rho_right_mod_right={rho_right}")
    print(f"rho_right_log_mod_quotient={logs[rho_right] % QUOTIENT_ORDER}")
    print(f"internal_exponent={INTERNAL_EXPONENT}")
    print(f"internal_right_mod_right={internal_right}")
    print(f"internal_rel_mod_n={internal_rel}")
    print(f"internal_rel_subgroup={internal}")
    print(f"relative_internal_cosets={rel_cosets}")
    print(f"right_H_cosets={h_cosets}")
    print(f"additive_resolvent_covariance_failures={covariance_failures}")
    print(f"anchor_coset_descended={anchor_descended}/{len(rel_cosets)}")
    print(f"equal_H_coset_sums={equal_h_coset_sums}/{len(rel_cosets)}")
    print(
        "gauss_normalized_nonzero_projections="
        f"{nonzero_normalized_projections}/{checked_projections}"
    )
    print(
        "gauss_normalized_projection_rho_fixed="
        f"{normalized_projection_fixed}/{checked_projections}"
    )
    print(f"H_coset_sum_rows={coset_sum_rows}")
    print(f"gauss_normalized_projection_values={normalized_values}")
    print("interpretation")
    print("  actual_cm_additive_resolvent_covariance_holds=1")
    print("  gauss_normalized_projection_can_be_rho_fixed_and_nonzero=1")
    print("  covariance_plus_gauss_normalization_does_not_imply_anchor_descent=1")
    print("  p24_still_needs_section_aware_anchor_descent_or_equal_H_coset_sums=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_actual_cm_right_axis_covariance_boundary")

    if (cycle.h, cycle.m, cycle.n) != (105, M, N):
        raise SystemExit(1)
    if rho_left != 1:
        raise SystemExit(1)
    if logs[rho_right] % QUOTIENT_ORDER == 0:
        raise SystemExit(1)
    if internal_right != 1:
        raise SystemExit(1)
    if gcd(cycle.q, cycle.n) != 1 or len(internal) != 2:
        raise SystemExit(1)
    if covariance_failures:
        raise SystemExit(1)
    if normalized_projection_fixed != checked_projections:
        raise SystemExit(1)
    if nonzero_normalized_projections != checked_projections:
        raise SystemExit(1)
    if anchor_descended or equal_h_coset_sums:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
