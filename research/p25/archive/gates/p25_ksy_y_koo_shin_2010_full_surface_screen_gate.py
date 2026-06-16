#!/usr/bin/env python3
"""Full-surface Koo-Shin 2010 screen for the p25 KSY-y lane.

The supplied Koo-Shin 2010 paper has more useful structure than Theorem 5.2
alone.  This gate records the two pieces that matter for the p25 moonshot:

* Theorem 3.9 gives an orbit-sum integrality screen for prime-power
  Siegel-product components.  The live p25 packet passes this necessary screen.
* Theorem 6.2 gives complete one-axis X1(N) products.  The live p25 packet is a
  sparse mixed C3 x C169 graph / raw K-trace footprint, so this theorem is not
  a direct producer.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction
from math import gcd, lcm
from pathlib import Path

from p25_laneB_robert_ksy_theta2_kubert_lang_exponent_matrix_gate import source_packet
from p25_laneB_robert_ksy_theta2_normalized_y_product_gate import (
    normalized_y_product_footprint,
)
from p25_laneB_square_axis_bridge_raw_source_character_gate import (
    BASE_POINT,
    BRIDGE_SHIFT,
    C_ORDER,
    D_SHIFT,
    KERNEL_SHIFT,
    RIGHT_ORDER,
)


REPO = Path(__file__).resolve().parents[2]
TEXT_PATH = REPO / "incoming" / "extracted" / "s00209-008-0456-9.pdf.extract.txt"
QUOTIENT_RIGHT_ORDER = 3

Coord = tuple[int, int]
Ring = dict[Coord, int]


@dataclass(frozen=True)
class TextSurfaceScan:
    text_path: str
    has_theorem_3_9: bool
    has_theorem_5_2: bool
    has_theorem_6_2: bool
    has_theorem_8_1: bool
    has_theorem_8_3: bool
    has_theorem_9_8: bool
    has_theorem_9_10: bool
    has_theorem_9_11: bool
    row_ok: bool


@dataclass(frozen=True)
class OrbitSumScreen:
    name: str
    right_order: int
    c_order: int
    support: int
    coefficient_counts: tuple[tuple[int, int], ...]
    prime_power_terms: int
    composite_terms: int
    orbit_sums: tuple[tuple[int, Coord, int], ...]
    all_prime_power_orbit_sums_nonnegative: bool
    preserves_mixed_graph: bool
    theorem_3_9_use: str
    row_ok: bool


@dataclass(frozen=True)
class OneAxisMismatch:
    name: str
    right_order: int
    c_order: int
    support: int
    right_classes: int
    c_classes: int
    max_c_entries_per_right: int
    max_right_entries_per_c: int
    full_c_row_size: int
    full_right_row_size: int
    matches_complete_c_rows: bool
    matches_complete_right_rows: bool
    theorem_6_2_direct_producer: bool
    row_ok: bool


@dataclass(frozen=True)
class KooShin2010FullSurfaceScreen:
    text_scan: TextSurfaceScan
    source_packet_orbit_screen: OrbitSumScreen
    theta2_orbit_screen: OrbitSumScreen
    c_axis_projection_control: OrbitSumScreen
    source_packet_one_axis_mismatch: OneAxisMismatch
    theta2_one_axis_mismatch: OneAxisMismatch
    theorem_3_9_is_hygiene_not_selector: bool
    theorem_6_2_is_not_direct_producer: bool
    remaining_upgrade: str
    row_ok: bool


def coefficient_counts(ring: Ring) -> tuple[tuple[int, int], ...]:
    return tuple(sorted(Counter(ring.values()).items()))


def text_surface_scan() -> TextSurfaceScan:
    text = TEXT_PATH.read_text(encoding="utf-8", errors="ignore")
    has_3_9 = "Theorem 3.9 Let" in text and "for each orbit" in text
    has_5_2 = "Theorem 5.2 (1) For an odd prime p" in text
    has_6_2 = "Theorem 6.2 A product" in text and "is an element of K(X1(N))" in text
    has_8_1 = "Theorem 8.1 For N" in text and "K(X1(N)) = C" in text
    has_8_3 = "Theorem 8.3 For a prime p" in text
    has_9_8 = "Theorem 9.8 For N" in text
    has_9_10 = "Theorem 9.10 For N" in text
    has_9_11 = "Theorem 9.11 For a prime p" in text
    row_ok = all((has_3_9, has_5_2, has_6_2, has_8_1, has_8_3, has_9_8, has_9_10, has_9_11))
    return TextSurfaceScan(
        text_path=str(TEXT_PATH),
        has_theorem_3_9=has_3_9,
        has_theorem_5_2=has_5_2,
        has_theorem_6_2=has_6_2,
        has_theorem_8_1=has_8_1,
        has_theorem_8_3=has_8_3,
        has_theorem_9_8=has_9_8,
        has_theorem_9_10=has_9_10,
        has_theorem_9_11=has_9_11,
        row_ok=row_ok,
    )


def coordinate_order(value: int, modulus: int) -> int:
    value %= modulus
    if value == 0:
        return 1
    return modulus // gcd(value, modulus)


def prime_power_base(value: int) -> int | None:
    if value <= 1:
        return None
    remaining = value
    base = None
    divisor = 2
    while divisor * divisor <= remaining:
        if remaining % divisor == 0:
            if base is not None:
                return None
            base = divisor
            while remaining % divisor == 0:
                remaining //= divisor
        divisor += 1
    if remaining > 1:
        if base is not None:
            return None
        base = remaining
    return base


def numerator_mod_denominator(value: int, modulus: int, denominator: int) -> int:
    frac = Fraction(value % modulus, modulus)
    return (frac.numerator * (denominator // frac.denominator)) % denominator


def orbit_key(coord: Coord, right_order: int, c_order: int, denominator: int) -> Coord:
    x = numerator_mod_denominator(coord[0], right_order, denominator)
    y = numerator_mod_denominator(coord[1], c_order, denominator)
    images: list[Coord] = []
    for unit in range(1, denominator):
        if gcd(unit, denominator) != 1:
            continue
        images.append(((unit * x) % denominator, (unit * y) % denominator))
        images.append(((-unit * x) % denominator, (-unit * y) % denominator))
    return min(images)


def orbit_sum_screen(
    name: str,
    ring: Ring,
    right_order: int,
    c_order: int,
    preserves_mixed_graph: bool,
) -> OrbitSumScreen:
    orbit_sums: dict[tuple[int, Coord], int] = defaultdict(int)
    prime_power_terms = 0
    composite_terms = 0
    for coord, coefficient in ring.items():
        denominator = lcm(
            coordinate_order(coord[0], right_order),
            coordinate_order(coord[1], c_order),
        )
        if prime_power_base(denominator) is None:
            composite_terms += 1
            continue
        prime_power_terms += 1
        orbit_sums[(denominator, orbit_key(coord, right_order, c_order, denominator))] += coefficient

    sums = tuple(
        (denominator, key, value)
        for (denominator, key), value in sorted(orbit_sums.items())
    )
    all_nonnegative = all(value >= 0 for _denominator, _key, value in sums)
    row_ok = all_nonnegative and prime_power_terms > 0 and len(sums) == 1
    return OrbitSumScreen(
        name=name,
        right_order=right_order,
        c_order=c_order,
        support=len(ring),
        coefficient_counts=coefficient_counts(ring),
        prime_power_terms=prime_power_terms,
        composite_terms=composite_terms,
        orbit_sums=sums,
        all_prime_power_orbit_sums_nonnegative=all_nonnegative,
        preserves_mixed_graph=preserves_mixed_graph,
        theorem_3_9_use=(
            "necessary integrality/orbit-sum hygiene only; it certifies no exact "
            "P selector or DANGER3 extraction"
        ),
        row_ok=row_ok,
    )


def one_axis_mismatch(name: str, ring: Ring, right_order: int, c_order: int) -> OneAxisMismatch:
    by_right: dict[int, set[int]] = defaultdict(set)
    by_c: dict[int, set[int]] = defaultdict(set)
    for right, c_log in ring:
        by_right[right].add(c_log)
        by_c[c_log].add(right)

    max_c_per_right = max((len(values) for values in by_right.values()), default=0)
    max_right_per_c = max((len(values) for values in by_c.values()), default=0)
    matches_c_rows = bool(by_right) and all(len(values) == c_order for values in by_right.values())
    matches_right_rows = bool(by_c) and all(len(values) == right_order for values in by_c.values())
    theorem_6_2_direct = matches_c_rows or matches_right_rows
    row_ok = not theorem_6_2_direct
    return OneAxisMismatch(
        name=name,
        right_order=right_order,
        c_order=c_order,
        support=len(ring),
        right_classes=len(by_right),
        c_classes=len(by_c),
        max_c_entries_per_right=max_c_per_right,
        max_right_entries_per_c=max_right_per_c,
        full_c_row_size=c_order,
        full_right_row_size=right_order,
        matches_complete_c_rows=matches_c_rows,
        matches_complete_right_rows=matches_right_rows,
        theorem_6_2_direct_producer=theorem_6_2_direct,
        row_ok=row_ok,
    )


def c_axis_projection(packet: Ring) -> Ring:
    out: Ring = {}
    for (_right, c_log), coefficient in packet.items():
        coord = (0, c_log)
        out[coord] = out.get(coord, 0) + coefficient
        if out[coord] == 0:
            del out[coord]
    return dict(sorted(out.items()))


def profile_koo_shin_2010_full_surface_screen() -> KooShin2010FullSurfaceScreen:
    scan = text_surface_scan()
    packet = source_packet()
    theta2_inverse = normalized_y_product_footprint(
        BASE_POINT,
        KERNEL_SHIFT,
        D_SHIFT,
        BRIDGE_SHIFT,
    )
    projection = c_axis_projection(packet)

    packet_orbit = orbit_sum_screen(
        "source_packet_common_level_507",
        packet,
        QUOTIENT_RIGHT_ORDER,
        C_ORDER,
        preserves_mixed_graph=True,
    )
    theta2_orbit = orbit_sum_screen(
        "theta2_inverse_raw_level_12675",
        theta2_inverse,
        RIGHT_ORDER,
        C_ORDER,
        preserves_mixed_graph=True,
    )
    projection_orbit = orbit_sum_screen(
        "c_axis_projection_level_169_control",
        projection,
        1,
        C_ORDER,
        preserves_mixed_graph=False,
    )
    packet_axis = one_axis_mismatch(
        "source_packet_common_level_507",
        packet,
        QUOTIENT_RIGHT_ORDER,
        C_ORDER,
    )
    theta2_axis = one_axis_mismatch(
        "theta2_inverse_raw_level_12675",
        theta2_inverse,
        RIGHT_ORDER,
        C_ORDER,
    )

    theorem_3_9_is_hygiene = (
        packet_orbit.row_ok
        and theta2_orbit.row_ok
        and projection_orbit.row_ok
        and not projection_orbit.preserves_mixed_graph
    )
    theorem_6_2_not_direct = packet_axis.row_ok and theta2_axis.row_ok
    row_ok = (
        scan.row_ok
        and theorem_3_9_is_hygiene
        and theorem_6_2_not_direct
        and packet_orbit.prime_power_terms == 2
        and packet_orbit.composite_terms == 4
        and theta2_orbit.prime_power_terms == 4
        and theta2_orbit.composite_terms == 296
        and projection_orbit.prime_power_terms == 6
        and projection_orbit.composite_terms == 0
        and packet_axis.max_c_entries_per_right == 2
        and packet_axis.full_c_row_size == 169
        and theta2_axis.max_c_entries_per_right == 4
        and theta2_axis.full_c_row_size == 169
        and theta2_axis.max_right_entries_per_c == 25
        and theta2_axis.full_right_row_size == 75
    )
    return KooShin2010FullSurfaceScreen(
        text_scan=scan,
        source_packet_orbit_screen=packet_orbit,
        theta2_orbit_screen=theta2_orbit,
        c_axis_projection_control=projection_orbit,
        source_packet_one_axis_mismatch=packet_axis,
        theta2_one_axis_mismatch=theta2_axis,
        theorem_3_9_is_hygiene_not_selector=theorem_3_9_is_hygiene,
        theorem_6_2_is_not_direct_producer=theorem_6_2_not_direct,
        remaining_upgrade=(
            "a mixed-level theorem selecting exact P/theta2 with the C3 x C169 "
            "row graph, T edge, equal weights, and orientation"
        ),
        row_ok=row_ok,
    )


def print_orbit(row: OrbitSumScreen) -> None:
    print(
        "  "
        f"{row.name}: support={row.support} prime_power_terms={row.prime_power_terms} "
        f"composite_terms={row.composite_terms} orbit_sums={row.orbit_sums} "
        f"mixed={int(row.preserves_mixed_graph)} ok={int(row.row_ok)}"
    )


def print_axis(row: OneAxisMismatch) -> None:
    print(
        "  "
        f"{row.name}: support={row.support} right_classes={row.right_classes} "
        f"c_classes={row.c_classes} max_c_per_right={row.max_c_entries_per_right}/"
        f"{row.full_c_row_size} max_right_per_c={row.max_right_entries_per_c}/"
        f"{row.full_right_row_size} theorem6_2_direct={int(row.theorem_6_2_direct_producer)}"
    )


def main() -> int:
    profile = profile_koo_shin_2010_full_surface_screen()
    print("p25 KSY-y Koo-Shin 2010 full-surface screen gate")
    print("text_surfaces")
    print(f"  text_path={profile.text_scan.text_path}")
    print(f"  theorem_3_9={int(profile.text_scan.has_theorem_3_9)}")
    print(f"  theorem_5_2={int(profile.text_scan.has_theorem_5_2)}")
    print(f"  theorem_6_2={int(profile.text_scan.has_theorem_6_2)}")
    print(f"  theorem_8_1={int(profile.text_scan.has_theorem_8_1)}")
    print(f"  theorem_8_3={int(profile.text_scan.has_theorem_8_3)}")
    print(f"  theorem_9_8={int(profile.text_scan.has_theorem_9_8)}")
    print(f"  theorem_9_10={int(profile.text_scan.has_theorem_9_10)}")
    print(f"  theorem_9_11={int(profile.text_scan.has_theorem_9_11)}")
    print("theorem_3_9_orbit_sum_screens")
    print_orbit(profile.source_packet_orbit_screen)
    print_orbit(profile.theta2_orbit_screen)
    print_orbit(profile.c_axis_projection_control)
    print("theorem_6_2_one_axis_mismatch")
    print_axis(profile.source_packet_one_axis_mismatch)
    print_axis(profile.theta2_one_axis_mismatch)
    print("interpretation")
    print("  koo_shin_3_9_confirms_integrality_hygiene_not_exact_selector=1")
    print("  c_axis_projection_passing_3_9_is_insufficient_because_it_loses_mixed_graph=1")
    print("  koo_shin_6_2_complete_one_axis_rows_do_not_match_sparse_mixed_p25_payload=1")
    print(f"  remaining_upgrade={profile.remaining_upgrade}")
    print(f"ksy_y_koo_shin_2010_full_surface_screen_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("Koo-Shin 2010 full-surface screen regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
