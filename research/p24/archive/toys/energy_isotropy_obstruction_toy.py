#!/usr/bin/env python3
"""Finite-field obstruction to deriving energy nonzero from content nonzero.

The relative-content certificate is exact: a packet is safe if its vector of
relative fibers is not the zero vector.  The scalar energy certificate is only
sufficient:

    E = sum_u P_u * conjugate(P_u).

This toy shows why the energy theorem cannot be a formal consequence of
content nonzero.  In the same quadratic packet field used by the D=-5000
calibration (`q=1259`, `f=X^2+36X+1`, so conjugation sends X to X^-1), the
Hermitian form already has nonzero isotropic vectors.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass


@dataclass(frozen=True)
class QuadField:
    q: int
    # Monic polynomial X^2 + a X + 1.
    a: int

    def add(self, x: tuple[int, int], y: tuple[int, int]) -> tuple[int, int]:
        return ((x[0] + y[0]) % self.q, (x[1] + y[1]) % self.q)

    def neg(self, x: tuple[int, int]) -> tuple[int, int]:
        return ((-x[0]) % self.q, (-x[1]) % self.q)

    def mul(self, x: tuple[int, int], y: tuple[int, int]) -> tuple[int, int]:
        # X^2 = -a X - 1.
        c0 = x[0] * y[0] - x[1] * y[1]
        c1 = x[0] * y[1] + x[1] * y[0] - self.a * x[1] * y[1]
        return (c0 % self.q, c1 % self.q)

    def conj(self, x: tuple[int, int]) -> tuple[int, int]:
        # If alpha is a root of X^2+aX+1, then alpha^-1 = -a-alpha.
        # c0 + c1*alpha maps to c0 + c1*alpha^-1.
        return ((x[0] - self.a * x[1]) % self.q, (-x[1]) % self.q)

    def norm(self, x: tuple[int, int]) -> int:
        product = self.mul(x, self.conj(x))
        if product[1] != 0:
            raise AssertionError(f"norm not in base field: {product}")
        return product[0] % self.q


def find_norm_value(field: QuadField, target: int) -> tuple[int, int] | None:
    target %= field.q
    for b in range(field.q):
        for c in range(field.q):
            x = (b, c)
            if x != (0, 0) and field.norm(x) == target:
                return x
    return None


def hermitian_energy(field: QuadField, vector: list[tuple[int, int]]) -> tuple[int, int]:
    total = (0, 0)
    for value in vector:
        total = field.add(total, field.mul(value, field.conj(value)))
    return total


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, default=1259)
    ap.add_argument("--a", type=int, default=36)
    args = ap.parse_args()

    field = QuadField(q=args.q, a=args.a)
    one = (1, 0)
    minus_one = (args.q - 1, 0)
    y = find_norm_value(field, args.q - 1)
    if y is None:
        raise RuntimeError("failed to find norm -1")
    vector = [one, y]
    energy = hermitian_energy(field, vector)
    span_det = (one[0] * y[1] - one[1] * y[0]) % field.q

    print("energy isotropy obstruction toy")
    print(f"q={field.q}")
    print(f"packet_factor=X^2 + {field.a}*X + 1")
    print(f"conjugation=X_to_X_inverse=1")
    print(f"norm_one={field.norm(one)}")
    print(f"norm_y={field.norm(y)}")
    print(f"y={y[0]} + {y[1]}*X")
    print(f"vector_nonzero={int(any(v != (0, 0) for v in vector))}")
    print(f"content_certificate_nonzero={int(vector[0] != (0, 0))}")
    print(f"maximal_base_field_span={int(span_det != 0)}")
    print(f"hermitian_energy={energy}")
    print(f"energy_zero={int(energy == (0, 0))}")
    print()
    print("interpretation")
    print("  nonzero_relative_content_does_not_force_energy_nonzero=1")
    print("  energy_certificate_requires_extra_arithmetic_not_linear_algebra=1")
    print("  p24_has_m=66254_coordinates_so_isotropy_is_no_formal_obstacle=1")
    print("conclusion=relative_energy_is_independent_sufficient_certificate")


if __name__ == "__main__":
    main()
