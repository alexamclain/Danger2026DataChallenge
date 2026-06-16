#!/usr/bin/env python3
"""Cyclic-divisibility form of the adjacent-anchor descent target.

The adjacent-anchor descent gate states that one anchor

    T_0

must be fixed by the order-7 rho action.  If we write the rho-orbit coordinates
of T_0 as a polynomial

    A(y) = a_0 + a_1 y + ... + a_6 y^6,

then rho-fixedness is equivalent to all coefficients being equal, equivalently

    A(y) is a scalar multiple of Phi_7(y)=1+y+...+y^6.

Since deg A < 7, this is the same as the single cyclic divisibility condition

    A(y) == 0 mod Phi_7(y).

So the six nontrivial rho-projectors can be replaced by one base-field
polynomial remainder.  This is still finite algebra, not the CM/Lang producer,
but it is a tighter target for the selected adjacent-trace anchor theorem.
"""

from __future__ import annotations

import random


MOD = 43
ORDER = 7
SEED = 20260607
TRIALS = 512


Vector = tuple[int, ...]


def sub(left: Vector, right: Vector) -> Vector:
    return tuple((a - b) % MOD for a, b in zip(left, right))


def scale(c: int, value: Vector) -> Vector:
    return tuple((c * entry) % MOD for entry in value)


def rho(value: Vector) -> Vector:
    return (value[-1],) + value[:-1]


def is_fixed(value: Vector) -> bool:
    return rho(value) == value


def cyclic_remainder_mod_phi7(value: Vector) -> tuple[int, ...]:
    """Return A mod Phi_7 for deg(A)<7 as six coefficients.

    Since Phi_7(y)=1+...+y^6 is monic of degree 6, reduce

        a_0 + ... + a_6 y^6

    by replacing y^6 with -(1+...+y^5).
    """

    top = value[6]
    return tuple((value[index] - top) % MOD for index in range(6))


def is_divisible_by_phi7(value: Vector) -> bool:
    return all(entry == 0 for entry in cyclic_remainder_mod_phi7(value))


def find_order7_root() -> int:
    for candidate in range(2, MOD):
        if pow(candidate, ORDER, MOD) == 1 and candidate != 1:
            return candidate
    raise RuntimeError("no primitive order-7 root")


OMEGA = find_order7_root()
INV7 = pow(ORDER, -1, MOD)
ZERO = (0,) * ORDER


def add(left: Vector, right: Vector) -> Vector:
    return tuple((a + b) % MOD for a, b in zip(left, right))


def rho_pow(value: Vector, power: int) -> Vector:
    out = value
    for _step in range(power % ORDER):
        out = rho(out)
    return out


def projector(k: int, value: Vector) -> Vector:
    total = ZERO
    for j in range(ORDER):
        coeff = pow(OMEGA, (-k * j) % ORDER, MOD)
        total = add(total, scale(coeff, rho_pow(value, j)))
    return scale(INV7, total)


def nontrivial_projectors_zero(value: Vector) -> bool:
    return all(projector(k, value) == ZERO for k in range(1, ORDER))


def random_vector(rng: random.Random) -> Vector:
    return tuple(rng.randrange(MOD) for _ in range(ORDER))


def fixed_vector(c: int) -> Vector:
    return (c % MOD,) * ORDER


def main() -> None:
    rng = random.Random(SEED)

    fixed_divisibility_rows = 0
    projector_divisibility_rows = 0
    random_divisible = 0
    random_projector_zero = 0
    forced_fixed_rows = 0
    forced_nonfixed_rows = 0

    for _trial in range(TRIALS):
        value = random_vector(rng)
        fixed = is_fixed(value)
        divisible = is_divisible_by_phi7(value)
        projectors_zero = nontrivial_projectors_zero(value)
        fixed_divisibility_rows += int(fixed == divisible)
        projector_divisibility_rows += int(projectors_zero == divisible)
        random_divisible += int(divisible)
        random_projector_zero += int(projectors_zero)

        c = rng.randrange(MOD)
        forced = fixed_vector(c)
        forced_fixed_rows += int(is_fixed(forced) and is_divisible_by_phi7(forced))

        nonfixed = list(fixed_vector(c))
        nonfixed[0] = (nonfixed[0] + 1) % MOD
        forced_nonfixed_rows += int(
            not is_fixed(tuple(nonfixed))
            and not is_divisible_by_phi7(tuple(nonfixed))
        )

    print("Trace-GCD fixed-frequency p24 adjacent-anchor cyclic-divisibility gate")
    print(f"field_modulus={MOD}")
    print(f"rho_order={ORDER}")
    print(f"omega_order7={OMEGA}")
    print(f"random_trials={TRIALS}")
    print(f"fixed_iff_phi7_divisible_rows={fixed_divisibility_rows}/{TRIALS}")
    print(f"projectors_zero_iff_phi7_divisible_rows={projector_divisibility_rows}/{TRIALS}")
    print(f"random_phi7_divisible={random_divisible}/{TRIALS}")
    print(f"random_projector_zero={random_projector_zero}/{TRIALS}")
    print(f"forced_fixed_phi7_divisible_rows={forced_fixed_rows}/{TRIALS}")
    print(f"forced_nonfixed_not_phi7_divisible_rows={forced_nonfixed_rows}/{TRIALS}")
    print("p24_single_adjacent_anchor_projectors=6")
    print("p24_single_adjacent_anchor_cyclic_remainder_degree=6")
    print("single_anchor_descent_iff_phi7_divisibility=1")
    print("six_projectors_compress_to_one_cyclic_remainder_mod_phi7=1")
    print("adjacent_anchor_divisibility_is_finite_algebra_not_the_cm_lang_producer=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_p24_adjacent_anchor_cyclic_divisibility_gate")

    if fixed_divisibility_rows != TRIALS:
        raise SystemExit(1)
    if projector_divisibility_rows != TRIALS:
        raise SystemExit(1)
    if forced_fixed_rows != TRIALS or forced_nonfixed_rows != TRIALS:
        raise SystemExit(1)
    if random_divisible or random_projector_zero:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
