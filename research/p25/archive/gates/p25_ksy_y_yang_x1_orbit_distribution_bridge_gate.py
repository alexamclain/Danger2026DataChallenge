#!/usr/bin/env python3
"""Yang X_1(N) orbit-distribution bridge for the p25 K trace.

Yang's modular-unit paper records the one-dimensional Siegel-function
distribution relation

    prod_{k=0}^{n-1} E^{(N)}_{kM+a} = E^{(M)}_a,  N = nM.

For p25, the raw K trace has N=12675, M=507, n=25, and step M=507.
This exactly explains the 25-point right-kernel trace as a descent from the raw
level to the six-cell C3 x C169 quotient packet.  It is not a p25 closer by
itself: Yang's relation is for one-dimensional X_1(N) Siegel functions E_a, so
the remaining theorem debt is the exact six-cell mixed product/value identity
for the KSY normalized-y payload.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isqrt

from p25_laneB_robert_ksy_theta2_kubert_lang_exponent_matrix_gate import (
    QUOTIENT_LEVEL,
    QUOTIENT_RIGHT_ORDER,
    Ring,
    source_packet,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_row_labeled_pair_contract_gate import (
    TARGET_ROW_LABELED_PAIRS,
    profile_row_labeled_pair_candidate,
)
from p25_laneB_square_axis_bridge_raw_source_character_gate import (
    C_ORDER,
    KERNEL_SHIFT,
    RIGHT_ORDER,
    raw_source_mask,
)


Coord = tuple[int, int]

YANG_SOURCE_URL = "https://arxiv.org/pdf/0712.0629"
YANG_SOURCE_HANDLE = "Yifan Yang, Modular unit and cuspidal divisor class groups of X_1(N)"
YANG_LEMMA = "Lemma 5: prod_{k=0}^{n-1} E^{(N)}_{kM+a} = E^{(M)}_a for N=nM"
K_TRACE_LENGTH = 25
RAW_LEVEL = RIGHT_ORDER * C_ORDER


@dataclass(frozen=True)
class YangOrbitCell:
    quotient_coord: Coord
    residue_mod_507: int
    coefficient: int
    orbit_support: int
    raw_coords: tuple[Coord, ...]
    orbit_step_matches_kernel: bool
    ok: bool


@dataclass(frozen=True)
class YangX1OrbitDistributionBridge:
    source_url: str
    source_handle: str
    lemma_handle: str
    raw_level: int
    quotient_level: int
    trace_length: int
    orbit_step: int
    kernel_shift: Coord
    quotient_packet_support: int
    reconstructed_raw_support: int
    raw_source_support: int
    reconstructed_raw_equals_target: bool
    quotient_packet_equals_target: bool
    row_labeled_pair_contract_ok: bool
    quotient_prime_factors: tuple[int, ...]
    signed_orbit_bad_counts: tuple[tuple[int, int], ...]
    unsigned_orbit_bad_counts: tuple[tuple[int, int], ...]
    yang_yu_signed_orbit_condition_ok: bool
    unsigned_orbit_condition_fails_as_control: bool
    orbit_cells: tuple[YangOrbitCell, ...]
    direct_closer: bool
    first_positive_payload: str
    first_missing_clause: str
    recommendation: str
    row_ok: bool


def add_packet_entry(packet: Ring, coord: Coord, coefficient: int) -> None:
    packet[coord] = packet.get(coord, 0) + coefficient
    if packet[coord] == 0:
        del packet[coord]


def crt_row_c_to_level_507(row: int, c_log: int) -> int:
    """Return a mod 507 with a = row mod 3 and a = c_log mod 169."""
    lift = ((row - c_log) % QUOTIENT_RIGHT_ORDER)
    return (c_log + C_ORDER * lift) % QUOTIENT_LEVEL


def raw_coord_from_level_12675(residue: int) -> Coord:
    return (residue % RIGHT_ORDER, residue % C_ORDER)


def yang_orbit_raw_coords(residue_mod_507: int) -> tuple[Coord, ...]:
    return tuple(
        raw_coord_from_level_12675(residue_mod_507 + QUOTIENT_LEVEL * layer)
        for layer in range(K_TRACE_LENGTH)
    )


def orbit_cell(quotient_coord: Coord, coefficient: int) -> YangOrbitCell:
    residue = crt_row_c_to_level_507(*quotient_coord)
    raw_coords = yang_orbit_raw_coords(residue)
    expected_step = raw_coord_from_level_12675(QUOTIENT_LEVEL)
    step_ok = expected_step == KERNEL_SHIFT
    return YangOrbitCell(
        quotient_coord=quotient_coord,
        residue_mod_507=residue,
        coefficient=coefficient,
        orbit_support=len(set(raw_coords)),
        raw_coords=raw_coords,
        orbit_step_matches_kernel=step_ok,
        ok=len(set(raw_coords)) == K_TRACE_LENGTH and step_ok,
    )


def reconstruct_raw_from_yang_orbits(packet: Ring) -> Ring:
    out: Ring = {}
    for coord, coefficient in packet.items():
        for raw_coord in yang_orbit_raw_coords(crt_row_c_to_level_507(*coord)):
            add_packet_entry(out, raw_coord, coefficient)
    return dict(sorted(out.items()))


def prime_factors(value: int) -> tuple[int, ...]:
    out: list[int] = []
    remaining = value
    for divisor in range(2, isqrt(remaining) + 1):
        if remaining % divisor:
            continue
        out.append(divisor)
        while remaining % divisor == 0:
            remaining //= divisor
    if remaining > 1:
        out.append(remaining)
    return tuple(out)


def packet_residue_exponents(packet: Ring) -> dict[int, int]:
    out: dict[int, int] = {}
    for coord, coefficient in packet.items():
        residue = crt_row_c_to_level_507(*coord)
        out[residue] = out.get(residue, 0) + coefficient
        if out[residue] == 0:
            del out[residue]
    return dict(sorted(out.items()))


def orbit_bad_count(exponents: dict[int, int], prime: int, signed: bool) -> int:
    step = QUOTIENT_LEVEL // prime
    seen: set[tuple[int, ...]] = set()
    bad = 0
    for residue in range(QUOTIENT_LEVEL):
        orbit: set[int] = set()
        for layer in range(prime):
            point = (residue + layer * step) % QUOTIENT_LEVEL
            orbit.add(point)
            if signed:
                orbit.add((-point) % QUOTIENT_LEVEL)
        key = tuple(sorted(orbit))
        if key in seen:
            continue
        seen.add(key)
        if sum(exponents.get(point, 0) for point in key):
            bad += 1
    return bad


def profile_yang_x1_orbit_distribution_bridge() -> YangX1OrbitDistributionBridge:
    quotient_packet = source_packet()
    reconstructed_raw = reconstruct_raw_from_yang_orbits(quotient_packet)
    raw_target = raw_source_mask()
    exponents = packet_residue_exponents(quotient_packet)
    factors = prime_factors(QUOTIENT_LEVEL)
    signed_bad = tuple(
        (prime, orbit_bad_count(exponents, prime, signed=True))
        for prime in factors
    )
    unsigned_bad = tuple(
        (prime, orbit_bad_count(exponents, prime, signed=False))
        for prime in factors
    )
    signed_ok = all(count == 0 for _prime, count in signed_bad)
    unsigned_control = any(count > 0 for _prime, count in unsigned_bad)
    row_labeled = profile_row_labeled_pair_candidate(
        "yang_x1_orbit_distribution_quotient_packet",
        quotient_packet,
    )
    cells = tuple(
        orbit_cell(coord, coefficient)
        for coord, coefficient in sorted(quotient_packet.items())
    )
    direct_closer = False
    row_ok = (
        RAW_LEVEL == 12675
        and QUOTIENT_LEVEL == 507
        and K_TRACE_LENGTH == 25
        and RAW_LEVEL == K_TRACE_LENGTH * QUOTIENT_LEVEL
        and raw_coord_from_level_12675(QUOTIENT_LEVEL) == KERNEL_SHIFT
        and len(quotient_packet) == 6
        and reconstructed_raw == raw_target
        and len(reconstructed_raw) == 150
        and row_labeled.ok
        and row_labeled.row_labeled_pairs == TARGET_ROW_LABELED_PAIRS
        and factors == (3, 13)
        and signed_ok
        and unsigned_control
        and all(cell.ok for cell in cells)
        and not direct_closer
    )
    return YangX1OrbitDistributionBridge(
        source_url=YANG_SOURCE_URL,
        source_handle=YANG_SOURCE_HANDLE,
        lemma_handle=YANG_LEMMA,
        raw_level=RAW_LEVEL,
        quotient_level=QUOTIENT_LEVEL,
        trace_length=K_TRACE_LENGTH,
        orbit_step=QUOTIENT_LEVEL,
        kernel_shift=KERNEL_SHIFT,
        quotient_packet_support=len(quotient_packet),
        reconstructed_raw_support=len(reconstructed_raw),
        raw_source_support=len(raw_target),
        reconstructed_raw_equals_target=reconstructed_raw == raw_target,
        quotient_packet_equals_target=row_labeled.ok,
        row_labeled_pair_contract_ok=row_labeled.ok,
        quotient_prime_factors=factors,
        signed_orbit_bad_counts=signed_bad,
        unsigned_orbit_bad_counts=unsigned_bad,
        yang_yu_signed_orbit_condition_ok=signed_ok,
        unsigned_orbit_condition_fails_as_control=unsigned_control,
        orbit_cells=cells,
        direct_closer=direct_closer,
        first_positive_payload=(
            "the 25-point K trace is exactly the Yang X_1(N) orbit product "
            "from level 12675 to level 507"
        ),
        first_missing_clause=(
            "Yang's one-dimensional E_a relation does not prove the remaining "
            "six-cell KSY normalized-y product/value identity, period-156 "
            "context, or DANGER3 extraction"
        ),
        recommendation=(
            "keep as K-trace descent/provenance; use future theorem search on "
            "the six row-labeled quotient pairs rather than on the raw 150 "
            "K-trace factors"
        ),
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_yang_x1_orbit_distribution_bridge()
    print("p25 KSY-y Yang X1 orbit-distribution bridge gate")
    print(f"source={profile.source_url}")
    print(f"source_handle={profile.source_handle}")
    print(f"lemma_handle={profile.lemma_handle}")
    print("levels")
    print(f"  raw_level={profile.raw_level}")
    print(f"  quotient_level={profile.quotient_level}")
    print(f"  trace_length={profile.trace_length}")
    print(f"  orbit_step={profile.orbit_step}")
    print(f"  kernel_shift={profile.kernel_shift}")
    print("orbit_cells")
    for cell in profile.orbit_cells:
        print(
            "  "
            f"{cell.quotient_coord}: residue={cell.residue_mod_507} "
            f"coeff={cell.coefficient} support={cell.orbit_support} "
            f"kernel_step={int(cell.orbit_step_matches_kernel)}"
        )
    print("counts")
    print(f"  quotient_packet_support={profile.quotient_packet_support}")
    print(f"  reconstructed_raw_support={profile.reconstructed_raw_support}")
    print(f"  raw_source_support={profile.raw_source_support}")
    print(
        "  reconstructed_raw_equals_target="
        f"{int(profile.reconstructed_raw_equals_target)}"
    )
    print(f"  quotient_packet_equals_target={int(profile.quotient_packet_equals_target)}")
    print(f"  row_labeled_pair_contract_ok={int(profile.row_labeled_pair_contract_ok)}")
    print(f"  quotient_prime_factors={profile.quotient_prime_factors}")
    print(f"  signed_orbit_bad_counts={profile.signed_orbit_bad_counts}")
    print(f"  unsigned_orbit_bad_counts={profile.unsigned_orbit_bad_counts}")
    print(
        "  yang_yu_signed_orbit_condition_ok="
        f"{int(profile.yang_yu_signed_orbit_condition_ok)}"
    )
    print(
        "  unsigned_orbit_condition_fails_as_control="
        f"{int(profile.unsigned_orbit_condition_fails_as_control)}"
    )
    print(f"  direct_closer={int(profile.direct_closer)}")
    print("interpretation")
    print("  yang_orbit_relation_explains_the_25_point_K_trace_descent=1")
    print("  quotient_packet_passes_signed_orbit_condition_for_X1_507=1")
    print("  theorem_search_can_now_focus_on_the_six_cell_quotient_packet=1")
    print("  yang_x1_relation_is_not_the_missing_normalized_y_product_identity=1")
    print(
        "ksy_y_yang_x1_orbit_distribution_bridge_rows="
        f"{int(profile.row_ok)}/1"
    )
    if not profile.row_ok:
        raise SystemExit("Yang X1 orbit-distribution bridge regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
