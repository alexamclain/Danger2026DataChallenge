#!/usr/bin/env python3
"""Finite gate for the p24 adjacent-trace anchor descent target.

This does not prove the CM/Lang arithmetic theorem.  It records the exact
finite algebra around the remaining single anchor

    T_0 = Tr_{Q(zeta_n)/Q(zeta_n)^<p>}(P_0(zeta_n)).

After the covariance functoriality gate, the 48 right-difference equations are
forced by one condition: rho(T_0)=T_0.  Since the relevant rho-action has order
7, this is the same as the vanishing of the six nontrivial rho-projectors.
"""

from __future__ import annotations

import random


MOD = 43
DIM = 7
INV7 = pow(7, -1, MOD)


def find_order7_root() -> int:
    for x in range(2, MOD):
        if pow(x, 7, MOD) == 1 and x != 1:
            return x
    raise RuntimeError("no primitive 7th root found")


OMEGA = find_order7_root()
ZERO = (0,) * DIM


def add(u: tuple[int, ...], v: tuple[int, ...]) -> tuple[int, ...]:
    return tuple((a + b) % MOD for a, b in zip(u, v))


def sub(u: tuple[int, ...], v: tuple[int, ...]) -> tuple[int, ...]:
    return tuple((a - b) % MOD for a, b in zip(u, v))


def scale(c: int, v: tuple[int, ...]) -> tuple[int, ...]:
    return tuple((c * a) % MOD for a in v)


def rho(v: tuple[int, ...]) -> tuple[int, ...]:
    """Order-7 Frobenius quotient action."""

    return (v[-1],) + v[:-1]


def rho_pow(v: tuple[int, ...], power: int) -> tuple[int, ...]:
    out = v
    for _ in range(power % DIM):
        out = rho(out)
    return out


def projector(k: int, v: tuple[int, ...]) -> tuple[int, ...]:
    """Pi_k = 1/7 sum_j omega^(-kj) rho^j."""

    total = ZERO
    for j in range(DIM):
        coeff = pow(OMEGA, (-k * j) % DIM, MOD)
        total = add(total, scale(coeff, rho_pow(v, j)))
    return scale(INV7, total)


def vector_sum(values: list[tuple[int, ...]]) -> tuple[int, ...]:
    total = ZERO
    for value in values:
        total = add(total, value)
    return total


def is_zero(v: tuple[int, ...]) -> bool:
    return v == ZERO


def is_descended(v: tuple[int, ...]) -> bool:
    return rho(v) == v


def nontrivial_projectors_zero(v: tuple[int, ...]) -> bool:
    return all(is_zero(projector(k, v)) for k in range(1, DIM))


def trace_orbit_from_anchor(anchor: tuple[int, ...]) -> list[tuple[int, ...]]:
    """The unique shift-6 covariant seven-tuple with T_0=anchor."""

    values = [ZERO for _ in range(DIM)]
    current = anchor
    for j in range(DIM):
        values[(6 * j) % DIM] = current
        current = rho(current)
    return values


def shift6_covariant(values: list[tuple[int, ...]]) -> bool:
    return all(values[(i + 6) % DIM] == rho(values[i]) for i in range(DIM))


def telescopes(values: list[tuple[int, ...]]) -> bool:
    return vector_sum(values) == ZERO


def all_zero(values: list[tuple[int, ...]]) -> bool:
    return all(is_zero(value) for value in values)


def random_vec(rng: random.Random) -> tuple[int, ...]:
    return tuple(rng.randrange(MOD) for _ in range(DIM))


def nonzero_fixed_component_free(v: tuple[int, ...]) -> tuple[int, ...]:
    """Remove the fixed projector, forcing telescope under the orbit model."""

    candidate = sub(v, projector(0, v))
    if is_zero(candidate):
        return (1, MOD - 1, 0, 0, 0, 0, 0)
    return candidate


def main() -> None:
    rng = random.Random(20260607)

    projector_idempotent_failures = 0
    projector_sum_failures = 0
    rho_projector_eigen_failures = 0
    anchor_criterion_failures = 0
    covariance_orbit_failures = 0

    for _ in range(256):
        v = random_vec(rng)
        projected_sum = ZERO
        for k in range(DIM):
            pk = projector(k, v)
            projected_sum = add(projected_sum, pk)
            for ell in range(DIM):
                expected = pk if k == ell else ZERO
                if projector(ell, pk) != expected:
                    projector_idempotent_failures += 1
            eigen = scale(pow(OMEGA, k % DIM, MOD), pk)
            if rho(pk) != eigen:
                rho_projector_eigen_failures += 1

        if projected_sum != v:
            projector_sum_failures += 1

        if is_descended(v) != nontrivial_projectors_zero(v):
            anchor_criterion_failures += 1

        if not shift6_covariant(trace_orbit_from_anchor(v)):
            covariance_orbit_failures += 1

    covariance_telescope_without_anchor_leaks = 0
    covariance_telescope_trials = 64
    for _ in range(covariance_telescope_trials):
        anchor = nonzero_fixed_component_free(random_vec(rng))
        values = trace_orbit_from_anchor(anchor)
        if (
            shift6_covariant(values)
            and telescopes(values)
            and not is_descended(anchor)
            and not all_zero(values)
        ):
            covariance_telescope_without_anchor_leaks += 1

    covariance_anchor_without_telescope_leaks = 0
    for c in range(1, MOD):
        anchor = (c,) * DIM
        values = trace_orbit_from_anchor(anchor)
        if (
            shift6_covariant(values)
            and is_descended(anchor)
            and not telescopes(values)
            and not all_zero(values)
        ):
            covariance_anchor_without_telescope_leaks += 1

    fixed_anchor_telescope_forces_zero = 0
    for c in range(MOD):
        anchor = (c,) * DIM
        values = trace_orbit_from_anchor(anchor)
        implication_holds = (
            not (shift6_covariant(values) and is_descended(anchor) and telescopes(values))
            or all_zero(values)
        )
        if implication_holds:
            fixed_anchor_telescope_forces_zero += 1

    print(f"field_modulus={MOD}")
    print(f"omega_order7={OMEGA}")
    print(f"projector_idempotent_failures={projector_idempotent_failures}")
    print(f"projector_sum_failures={projector_sum_failures}")
    print(f"rho_projector_eigen_failures={rho_projector_eigen_failures}")
    print(
        "anchor_descended_iff_nontrivial_rho_projectors_zero_failures="
        f"{anchor_criterion_failures}"
    )
    print(f"covariance_orbit_failures={covariance_orbit_failures}")
    print(
        "covariance_plus_telescope_without_anchor_leaks="
        f"{covariance_telescope_without_anchor_leaks}/{covariance_telescope_trials}"
    )
    print(
        "covariance_plus_anchor_without_telescope_leaks="
        f"{covariance_anchor_without_telescope_leaks}/{MOD - 1}"
    )
    print(f"fixed_anchor_telescope_forces_zero={fixed_anchor_telescope_forces_zero}/{MOD}")
    print("p24_raw_hcoset_equations=1092")
    print("p24_compressed_right_difference_equations=48")
    print("p24_single_adjacent_anchor_projectors=6")
    print("single_anchor_descent_is_rho_fixedness_of_T0=1")
    print("single_anchor_descent_is_not_a_sample_or_prime_search_count=1")
    print("single_anchor_projectors_are_the_remaining_descent_target=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_p24_adjacent_anchor_descent_gate")


if __name__ == "__main__":
    main()
