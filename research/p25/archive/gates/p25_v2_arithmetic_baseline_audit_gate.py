#!/usr/bin/env python3
"""Validate the p25 arithmetic baseline used by the wiki."""

from __future__ import annotations

from dataclasses import dataclass
from math import isqrt, prod


P = 10000000000000000000000013
K = 42
SQRT_FLOOR = 3162277660168


@dataclass(frozen=True)
class Factorization:
    factors: tuple[tuple[int, int], ...]

    def value(self) -> int:
        return prod(p**e for p, e in self.factors)

    def as_dict(self) -> dict[int, int]:
        return dict(self.factors)


@dataclass(frozen=True)
class TraceRow:
    t: int
    v2_order: int
    odd_part: int
    odd_part_factorization: Factorization
    discriminant: int
    discriminant_abs_factorization: Factorization
    fundamental_discriminant: int
    order_conductor: int
    order_class_number: int
    order_class_number_factorization: Factorization
    order_class_group: tuple[int, ...]
    row_ok: bool


@dataclass(frozen=True)
class ArithmeticBaseline:
    p_mod_8_ok: bool
    sqrt_floor_ok: bool
    k_ok: bool
    trace_rows: tuple[TraceRow, ...]
    pari_available: bool
    pari_class_groups_ok: bool
    row_ok: bool


TRACE_DATA = (
    {
        "t": 5808037298190,
        "v2_order": 42,
        "odd_part": 2273736754431,
        "odd_fac": ((3, 2), (601, 1), (420361759, 1)),
        "disc": -6266702742833805022723952,
        "disc_fac": ((2, 4), (7, 1), (1199351729, 1), (46652455412449, 1)),
        "fund_disc": -391668921427112813920247,
        "class_no": 907242623448,
        "class_fac": ((2, 3), (3, 1), (7, 1), (17, 2), (37, 1), (505027, 1)),
        "class_group": (226810655862, 2, 2),
    },
    {
        "t": 1409990787086,
        "v2_order": 50,
        "odd_part": 8881784197,
        "odd_fac": ((11, 1), (13, 1), (1543, 1), (40253, 1)),
        "disc": -38011925980332602215628656,
        "disc_fac": ((2, 4), (11, 1), (2465641, 1), (2910709, 1), (30093907049, 1)),
        "fund_disc": -2375745373770787638476791,
        "class_no": 2397272743184,
        "class_fac": ((2, 4), (11, 1), (13620867859, 1)),
        "class_group": (299659092898, 2, 2, 2),
    },
    {
        "t": -2988055724018,
        "v2_order": 42,
        "odd_part": 2273736754433,
        "odd_fac": ((17, 1), (5503, 1), (24304783, 1)),
        "disc": -31071522990163265817935728,
        "disc_fac": ((2, 4), (7, 1), (11, 1), (13, 1), (1493, 1), (1299417385618536931, 1)),
        "fund_disc": -1941970186885204113620983,
        "class_no": 999672108288,
        "class_fac": ((2, 8), (3, 1), (7, 1), (17, 1), (107, 1), (151, 1), (677, 1)),
        "class_group": (62479506768, 2, 2, 2, 2),
    },
)


def v2(n: int) -> int:
    count = 0
    while n % 2 == 0:
        count += 1
        n //= 2
    return count


def squarefree_part_from_factorization(factorization: Factorization) -> int:
    value = 1
    for prime, exponent in factorization.factors:
        if exponent % 2:
            value *= prime
    return value


def conductor_from_discriminant(discriminant: int, fundamental_discriminant: int) -> int:
    conductor_sq = abs(discriminant) // abs(fundamental_discriminant)
    conductor = isqrt(conductor_sq)
    return conductor if conductor * conductor == conductor_sq else -1


def pari_quadclassunit(discriminant: int) -> tuple[int, tuple[int, ...]] | None:
    try:
        from cypari2 import Pari
    except Exception:
        return None
    pari = Pari()
    result = pari(f"quadclassunit({discriminant})")
    class_number = int(result[0])
    group = tuple(int(x) for x in result[1])
    return class_number, group


def build_trace_row(raw: dict[str, object], pari_result: tuple[int, tuple[int, ...]] | None) -> TraceRow:
    t = int(raw["t"])
    order = P + 1 - t
    odd_fac = Factorization(tuple(raw["odd_fac"]))  # type: ignore[arg-type]
    disc_fac = Factorization(tuple(raw["disc_fac"]))  # type: ignore[arg-type]
    class_fac = Factorization(tuple(raw["class_fac"]))  # type: ignore[arg-type]
    discriminant = int(raw["disc"])
    fundamental_discriminant = int(raw["fund_disc"])
    class_number = int(raw["class_no"])
    class_group = tuple(raw["class_group"])  # type: ignore[arg-type]
    pari_ok = pari_result == (class_number, class_group)
    row_ok = (
        abs(t) <= 2 * isqrt(P) + 1
        and v2(order) == int(raw["v2_order"])
        and order >> int(raw["v2_order"]) == int(raw["odd_part"])
        and odd_fac.value() == int(raw["odd_part"])
        and t * t - 4 * P == discriminant
        and disc_fac.value() == abs(discriminant)
        and -squarefree_part_from_factorization(disc_fac) == fundamental_discriminant
        and conductor_from_discriminant(discriminant, fundamental_discriminant) == 4
        and class_fac.value() == class_number
        and pari_ok
    )
    return TraceRow(
        t=t,
        v2_order=int(raw["v2_order"]),
        odd_part=int(raw["odd_part"]),
        odd_part_factorization=odd_fac,
        discriminant=discriminant,
        discriminant_abs_factorization=disc_fac,
        fundamental_discriminant=fundamental_discriminant,
        order_conductor=4,
        order_class_number=class_number,
        order_class_number_factorization=class_fac,
        order_class_group=class_group,
        row_ok=row_ok,
    )


def build_baseline() -> ArithmeticBaseline:
    pari_results = [pari_quadclassunit(int(row["disc"])) for row in TRACE_DATA]
    pari_available = all(result is not None for result in pari_results)
    trace_rows = tuple(
        build_trace_row(raw, result) for raw, result in zip(TRACE_DATA, pari_results)
    )
    k_ok = min(row.v2_order for row in trace_rows) == K
    row_ok = (
        P % 8 == 5
        and isqrt(P) == SQRT_FLOOR
        and k_ok
        and pari_available
        and all(row.row_ok for row in trace_rows)
    )
    return ArithmeticBaseline(
        p_mod_8_ok=P % 8 == 5,
        sqrt_floor_ok=isqrt(P) == SQRT_FLOOR,
        k_ok=k_ok,
        trace_rows=trace_rows,
        pari_available=pari_available,
        pari_class_groups_ok=all(row.row_ok for row in trace_rows) if pari_available else False,
        row_ok=row_ok,
    )


def format_factorization(factorization: Factorization) -> str:
    return " * ".join(
        f"{prime}^{exponent}" if exponent != 1 else str(prime)
        for prime, exponent in factorization.factors
    )


def main() -> int:
    baseline = build_baseline()
    print("p25 v2 arithmetic baseline audit")
    print(f"p_mod_8_ok={int(baseline.p_mod_8_ok)}")
    print(f"sqrt_floor_ok={int(baseline.sqrt_floor_ok)}")
    print(f"k_ok={int(baseline.k_ok)}")
    print(f"pari_available={int(baseline.pari_available)}")
    for row in baseline.trace_rows:
        print(f"trace {row.t}")
        print(f"  v2_order={row.v2_order}")
        print(f"  odd_part={row.odd_part}")
        print(f"  odd_part_factorization={format_factorization(row.odd_part_factorization)}")
        print(f"  discriminant={row.discriminant}")
        print(f"  discriminant_abs_factorization={format_factorization(row.discriminant_abs_factorization)}")
        print(f"  fundamental_discriminant={row.fundamental_discriminant}")
        print(f"  order_conductor={row.order_conductor}")
        print(f"  order_class_number={row.order_class_number}")
        print(f"  order_class_number_factorization={format_factorization(row.order_class_number_factorization)}")
        print(f"  order_class_group={' x '.join('C_' + str(x) for x in row.order_class_group)}")
        print(f"  row_ok={int(row.row_ok)}")
    print(f"pari_class_groups_ok={int(baseline.pari_class_groups_ok)}")
    print(f"p25_v2_arithmetic_baseline_audit_rows={int(baseline.row_ok)}/1")
    return 0 if baseline.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
