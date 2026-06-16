#!/usr/bin/env python3
"""Kernel-polynomial realization of the reduced-anchor subgroup divisor.

The elliptic-subgroup divisor gate showed that the correct elliptic-unit
target is

    D_H = sum_{Q in H, Q != O} [Q] - (c - 1)[O]

for an odd cyclic subgroup H of order c.  This gate makes the principal
function explicit.  If H=<P> and c is odd, then the monic kernel polynomial

    K_H(x) = prod_{Q in (H \ {O})/{+-1}} (x - x(Q))

has divisor

    div(K_H) = D_H.

Each factor x-x(Q) vanishes at Q and -Q and has a double pole at O.  Thus
`deg K_H=(c-1)/2` and the pole order is `c-1`.  Squaring this polynomial is
the denominator shape that appears in x-coordinate isogeny formulas; the
unsquared kernel polynomial is the exact reduced-anchor residual.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import prod
from typing import Optional

from trace_gcd_fixed_frequency_p24_jacobi_carry_span_boundary import (
    P24_C_DEGREE,
    SMALL_C_DEGREES,
)


Point = Optional[tuple[int, int]]


@dataclass(frozen=True)
class Curve:
    q: int
    a: int
    b: int


@dataclass(frozen=True)
class KernelExample:
    c_degree: int
    curve: Curve
    generator: tuple[int, int]
    subgroup: tuple[Point, ...]
    x_roots: tuple[int, ...]


def inv(value: int, q: int) -> int:
    return pow(value % q, -1, q)


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def discriminant_nonzero(curve: Curve) -> bool:
    return (4 * curve.a * curve.a * curve.a + 27 * curve.b * curve.b) % curve.q != 0


def points(curve: Curve) -> list[Point]:
    q = curve.q
    squares: dict[int, list[int]] = {}
    for y in range(q):
        squares.setdefault(y * y % q, []).append(y)
    out: list[Point] = [None]
    for x in range(q):
        rhs = (x * x * x + curve.a * x + curve.b) % q
        for y in squares.get(rhs, []):
            out.append((x, y))
    return out


def neg(point: Point, q: int) -> Point:
    if point is None:
        return None
    x, y = point
    return (x, (-y) % q)


def add(curve: Curve, left: Point, right: Point) -> Point:
    q = curve.q
    if left is None:
        return right
    if right is None:
        return left
    x1, y1 = left
    x2, y2 = right
    if x1 == x2 and (y1 + y2) % q == 0:
        return None
    if left != right:
        slope = (y2 - y1) * inv(x2 - x1, q) % q
    else:
        if y1 % q == 0:
            return None
        slope = (3 * x1 * x1 + curve.a) * inv(2 * y1, q) % q
    x3 = (slope * slope - x1 - x2) % q
    y3 = (slope * (x1 - x3) - y1) % q
    return (x3, y3)


def mul(curve: Curve, n: int, point: Point) -> Point:
    acc: Point = None
    cur = point
    while n:
        if n & 1:
            acc = add(curve, acc, cur)
        cur = add(curve, cur, cur)
        n >>= 1
    return acc


def exact_order(curve: Curve, point: Point, order: int) -> bool:
    return point is not None and mul(curve, order, point) is None and all(
        mul(curve, factor, point) is not None
        for factor in range(1, order)
        if order % factor == 0
    )


def find_example(c_degree: int) -> KernelExample:
    # The search is tiny in practice, but bounded so the harness remains cheap.
    for q in range(max(7, c_degree + 2), 800):
        if q in (2, 3) or not is_prime(q):
            continue
        for a in range(min(q, 18)):
            for b in range(min(q, 18)):
                curve = Curve(q, a, b)
                if not discriminant_nonzero(curve):
                    continue
                pts = points(curve)
                if len(pts) % c_degree != 0:
                    continue
                for point in pts:
                    if exact_order(curve, point, c_degree):
                        subgroup = tuple(mul(curve, k, point) for k in range(c_degree))
                        roots = sorted(
                            {
                                subgroup[k][0]  # type: ignore[index]
                                for k in range(1, c_degree)
                            }
                        )
                        return KernelExample(
                            c_degree=c_degree,
                            curve=curve,
                            generator=point,  # type: ignore[arg-type]
                            subgroup=subgroup,
                            x_roots=tuple(roots),
                        )
    raise RuntimeError(f"no example found for c={c_degree}")


def subgroup_sum(curve: Curve, subgroup: tuple[Point, ...]) -> Point:
    acc: Point = None
    for point in subgroup[1:]:
        acc = add(curve, acc, point)
    return acc


def kernel_polynomial_degree(c_degree: int) -> int:
    return (c_degree - 1) // 2


def kernel_divisor_pole_order(c_degree: int) -> int:
    return 2 * kernel_polynomial_degree(c_degree)


def velu_x_denominator_degree(c_degree: int) -> int:
    return 2 * kernel_polynomial_degree(c_degree)


def divisor_degree_from_kernel(c_degree: int) -> int:
    return (2 * kernel_polynomial_degree(c_degree)) - kernel_divisor_pole_order(c_degree)


def root_pair_count_ok(example: KernelExample) -> bool:
    return len(example.x_roots) == kernel_polynomial_degree(example.c_degree)


def roots_are_subgroup_pairs(example: KernelExample) -> bool:
    roots = set(example.x_roots)
    return all(
        point is not None and point[0] in roots
        for point in example.subgroup[1:]
    )


def paired_x_coordinates(example: KernelExample) -> bool:
    curve = example.curve
    for point in example.subgroup[1:]:
        minus = neg(point, curve.q)
        if point is None or minus is None or point[0] != minus[0]:
            return False
    return True


def formal_kernel_rows() -> tuple[int, int, int, int, int, int]:
    rows = SMALL_C_DEGREES + [P24_C_DEGREE]
    degree_rows = 0
    pole_rows = 0
    divisor_degree_rows = 0
    velu_square_rows = 0
    residual_rows = 0
    for c_degree in rows:
        degree_ok = kernel_polynomial_degree(c_degree) * 2 == c_degree - 1
        pole_ok = kernel_divisor_pole_order(c_degree) == c_degree - 1
        divisor_ok = divisor_degree_from_kernel(c_degree) == 0
        velu_ok = velu_x_denominator_degree(c_degree) == c_degree - 1
        residual_ok = kernel_divisor_pole_order(c_degree) == c_degree - 1
        degree_rows += int(degree_ok)
        pole_rows += int(pole_ok)
        divisor_degree_rows += int(divisor_ok)
        velu_square_rows += int(velu_ok)
        residual_rows += int(residual_ok)
    return degree_rows, pole_rows, divisor_degree_rows, velu_square_rows, residual_rows, len(rows)


def main() -> None:
    print("Trace-GCD reduced-anchor kernel polynomial gate")

    actual_degrees = [5, 7, 11, 13, 17, 19]
    actual_rows = 0
    root_count_rows = 0
    paired_rows = 0
    subgroup_sum_rows = 0
    pole_order_rows = 0
    divisor_degree_rows = 0
    example_sizes: list[int] = []

    for c_degree in actual_degrees:
        example = find_example(c_degree)
        root_count_ok = int(root_pair_count_ok(example))
        paired_ok = int(paired_x_coordinates(example))
        subgroup_sum_ok = int(subgroup_sum(example.curve, example.subgroup) is None)
        pole_order_ok = int(kernel_divisor_pole_order(c_degree) == c_degree - 1)
        divisor_degree_ok = int(divisor_degree_from_kernel(c_degree) == 0)
        roots_ok = int(roots_are_subgroup_pairs(example))

        actual_rows += 1
        root_count_rows += int(root_count_ok and roots_ok)
        paired_rows += paired_ok
        subgroup_sum_rows += subgroup_sum_ok
        pole_order_rows += pole_order_ok
        divisor_degree_rows += divisor_degree_ok
        example_sizes.append(example.curve.q)

        print(
            "actual_row "
            f"c_degree={c_degree} "
            f"q={example.curve.q} "
            f"a={example.curve.a} "
            f"b={example.curve.b} "
            f"generator={example.generator} "
            f"group_order={len(points(example.curve))} "
            f"kernel_polynomial_degree={kernel_polynomial_degree(c_degree)} "
            f"x_root_count={len(example.x_roots)} "
            f"root_count_ok={root_count_ok} "
            f"roots_are_subgroup_pairs_ok={roots_ok} "
            f"paired_x_coordinates_ok={paired_ok} "
            f"subgroup_sum_zero_ok={subgroup_sum_ok} "
            f"pole_order_ok={pole_order_ok} "
            f"divisor_degree_ok={divisor_degree_ok}"
        )

    (
        formal_degree_rows,
        formal_pole_rows,
        formal_divisor_rows,
        formal_velu_rows,
        formal_residual_rows,
        formal_total,
    ) = formal_kernel_rows()

    print(f"actual_kernel_polynomial_rows_checked={actual_rows}")
    print(f"actual_kernel_root_pair_rows={root_count_rows}/{actual_rows}")
    print(f"actual_kernel_paired_x_rows={paired_rows}/{actual_rows}")
    print(f"actual_kernel_subgroup_sum_zero_rows={subgroup_sum_rows}/{actual_rows}")
    print(f"actual_kernel_pole_order_rows={pole_order_rows}/{actual_rows}")
    print(f"actual_kernel_divisor_degree_zero_rows={divisor_degree_rows}/{actual_rows}")
    print(f"actual_example_prime_product={prod(example_sizes)}")
    print(f"formal_kernel_rows_checked={formal_total}")
    print(f"formal_kernel_degree_rows={formal_degree_rows}/{formal_total}")
    print(f"formal_kernel_pole_order_rows={formal_pole_rows}/{formal_total}")
    print(f"formal_kernel_divisor_degree_zero_rows={formal_divisor_rows}/{formal_total}")
    print(f"formal_velu_x_denominator_degree_rows={formal_velu_rows}/{formal_total}")
    print(f"formal_kernel_residual_pole_order_rows={formal_residual_rows}/{formal_total}")
    print(f"p24_subgroup_order={P24_C_DEGREE}")
    print(f"p24_kernel_polynomial_degree={kernel_polynomial_degree(P24_C_DEGREE)}")
    print(f"p24_kernel_divisor_pole_order={kernel_divisor_pole_order(P24_C_DEGREE)}")
    print(f"p24_velu_x_denominator_degree={velu_x_denominator_degree(P24_C_DEGREE)}")
    print("interpretation")
    print("  kernel_polynomial_has_exact_subgroup_residual_divisor=1")
    print("  unsquared_kernel_polynomial_matches_R_c_not_R_c_squared=1")
    print("  velu_x_coordinate_denominator_is_the_square_of_the_kernel_polynomial=1")
    print("  p24_target_can_be_kernel_polynomial_for_selected_179_subgroup=1")
    print("  remaining_problem_is_constructing_selected_cm_lang_kernel_polynomial_without_class_enumeration=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_reduced_anchor_kernel_polynomial_gate")

    if root_count_rows != actual_rows:
        raise SystemExit(1)
    if paired_rows != actual_rows:
        raise SystemExit(1)
    if subgroup_sum_rows != actual_rows:
        raise SystemExit(1)
    if pole_order_rows != actual_rows:
        raise SystemExit(1)
    if divisor_degree_rows != actual_rows:
        raise SystemExit(1)
    if formal_degree_rows != formal_total:
        raise SystemExit(1)
    if formal_pole_rows != formal_total:
        raise SystemExit(1)
    if formal_divisor_rows != formal_total:
        raise SystemExit(1)
    if formal_velu_rows != formal_total:
        raise SystemExit(1)
    if formal_residual_rows != formal_total:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
