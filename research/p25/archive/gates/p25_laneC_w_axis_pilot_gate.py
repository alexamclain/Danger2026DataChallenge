#!/usr/bin/env python3
"""Lane C W_axis pilot gate for the p25 moonshot.

Lane C is not a practical producer yet; it is a theorem microscope.  The p25
handoff records three sub-sqrt W_axis rank surfaces and names the negative
trace's bundled axis n=2031 as the first falsifiable target.  This gate makes
that accounting executable and records the bounded p24 analogue scan that was
run as the first falsifier.

The analogue scan found no injectivity failures in the eligible small cases,
so the p25 n=2031 side quest is not killed by the first finite test.  The
largest-prime-only n=677 shortcut remains killed by the dimension guardrail.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isqrt


P = 10**25 + 13
SQRT_FLOOR = 3162277660168


@dataclass(frozen=True)
class Factorization:
    factors: tuple[tuple[int, int], ...]

    def value(self) -> int:
        result = 1
        for prime, exponent in self.factors:
            result *= prime**exponent
        return result

    def phi(self) -> int:
        result = self.value()
        for prime, _ in self.factors:
            result = result // prime * (prime - 1)
        return result


@dataclass(frozen=True)
class WAxisSurface:
    name: str
    trace: int
    odd_part: int
    odd_part_factorization: Factorization
    selected_chain_slots: int
    selected_chain_below_sqrt: bool
    recovery_n: int
    recovery_factorization: Factorization
    w_axis_dim: int
    ord_n_p: int
    ord_ge_dim: bool
    packet_count: int
    rank_surface: int
    rank_surface_below_sqrt: bool


@dataclass(frozen=True)
class GuardrailProfile:
    name: str
    n: int
    factorization: Factorization
    w_axis_dim: int
    ord_n_p: int
    ord_ge_dim: bool
    killed: bool


@dataclass(frozen=True)
class AnalogueScanProfile:
    command_max_cases: int
    command_max_h: int
    command_max_abs_d: int
    command_max_n: int
    command_q_stop: int
    packet_rows: int
    nonzero_rows: int
    dimension_bound_rows: int
    injective_possible_rows: int
    injective_rows: int
    injective_failures: int
    full_k_injective_possible_rows: int
    full_k_injective_rows: int
    full_k_injective_failure_rows: int
    rank_defect_histogram: tuple[tuple[int, int], ...]
    injective_pivot_prefix_min: int
    injective_pivot_prefix_max: int
    passed_first_falsifier: bool


@dataclass(frozen=True)
class LaneCWAxisProfile:
    p: int
    sqrt_floor: int
    surfaces: tuple[WAxisSurface, ...]
    negative_prime_only_guardrail: GuardrailProfile
    analogue_scan: AnalogueScanProfile
    best_surface_name: str
    best_surface_rank_surface: int
    all_surfaces_below_sqrt: bool


def distinct_prime_factors(value: int) -> tuple[int, ...]:
    factors: list[int] = []
    n = value
    candidate = 2
    while candidate * candidate <= n:
        if n % candidate == 0:
            factors.append(candidate)
            while n % candidate == 0:
                n //= candidate
        candidate += 1 if candidate == 2 else 2
    if n > 1:
        factors.append(n)
    return tuple(factors)


def multiplicative_order_mod_p(modulus: int, phi_value: int) -> int:
    order = phi_value
    for prime in distinct_prime_factors(phi_value):
        while order % prime == 0 and pow(P, order // prime, modulus) == 1:
            order //= prime
    return order


def surface(
    name: str,
    trace: int,
    odd_part_factorization: Factorization,
    selected_chain_slots: int,
    recovery_factorization: Factorization,
    w_axis_dim: int,
    packet_count: int,
) -> WAxisSurface:
    odd_part = odd_part_factorization.value()
    recovery_n = recovery_factorization.value()
    phi_n = recovery_factorization.phi()
    ord_n_p = multiplicative_order_mod_p(recovery_n, phi_n)
    rank_surface = phi_n * w_axis_dim
    return WAxisSurface(
        name=name,
        trace=trace,
        odd_part=odd_part,
        odd_part_factorization=odd_part_factorization,
        selected_chain_slots=selected_chain_slots,
        selected_chain_below_sqrt=selected_chain_slots < SQRT_FLOOR,
        recovery_n=recovery_n,
        recovery_factorization=recovery_factorization,
        w_axis_dim=w_axis_dim,
        ord_n_p=ord_n_p,
        ord_ge_dim=ord_n_p >= w_axis_dim,
        packet_count=packet_count,
        rank_surface=rank_surface,
        rank_surface_below_sqrt=rank_surface < SQRT_FLOOR,
    )


def lane_c_profile() -> LaneCWAxisProfile:
    surfaces = (
        surface(
            "positive_trace",
            5808037298190,
            Factorization(((3, 2), (601, 1), (420361759, 1))),
            505371,
            Factorization(((505027, 1),)),
            336,
            2,
        ),
        surface(
            "middle_trace",
            1409990787086,
            Factorization(((11, 1), (13, 1), (1543, 1), (40253, 1))),
            13620867886,
            Factorization(((13620867859, 1),)),
            15,
            2,
        ),
        surface(
            "negative_trace",
            -2988055724018,
            Factorization(((17, 1), (5503, 1), (24304783, 1))),
            1218,
            Factorization(((3, 1), (677, 1))),
            298,
            4,
        ),
    )
    guardrail_n = Factorization(((677, 1),))
    guardrail_ord = multiplicative_order_mod_p(guardrail_n.value(), guardrail_n.phi())
    guardrail = GuardrailProfile(
        name="negative_trace_prime_only_677",
        n=guardrail_n.value(),
        factorization=guardrail_n,
        w_axis_dim=298,
        ord_n_p=guardrail_ord,
        ord_ge_dim=guardrail_ord >= 298,
        killed=guardrail_ord < 298,
    )
    analogue = AnalogueScanProfile(
        command_max_cases=40,
        command_max_h=1200,
        command_max_abs_d=200000,
        command_max_n=2031,
        command_q_stop=500000,
        packet_rows=126,
        nonzero_rows=126,
        dimension_bound_rows=0,
        injective_possible_rows=126,
        injective_rows=126,
        injective_failures=0,
        full_k_injective_possible_rows=124,
        full_k_injective_rows=124,
        full_k_injective_failure_rows=0,
        rank_defect_histogram=((0, 126),),
        injective_pivot_prefix_min=2,
        injective_pivot_prefix_max=4,
        passed_first_falsifier=True,
    )
    best = min(surfaces, key=lambda row: row.rank_surface)
    return LaneCWAxisProfile(
        p=P,
        sqrt_floor=SQRT_FLOOR,
        surfaces=surfaces,
        negative_prime_only_guardrail=guardrail,
        analogue_scan=analogue,
        best_surface_name=best.name,
        best_surface_rank_surface=best.rank_surface,
        all_surfaces_below_sqrt=all(row.rank_surface_below_sqrt and row.selected_chain_below_sqrt for row in surfaces),
    )


def main() -> int:
    print("p25 Lane C W_axis pilot gate")
    profile = lane_c_profile()
    expected = LaneCWAxisProfile(
        p=P,
        sqrt_floor=isqrt(P),
        surfaces=(
            WAxisSurface("positive_trace", 5808037298190, 2273736754431, Factorization(((3, 2), (601, 1), (420361759, 1))), 505371, True, 505027, Factorization(((505027, 1),)), 336, 252513, True, 2, 169688736, True),
            WAxisSurface("middle_trace", 1409990787086, 8881784197, Factorization(((11, 1), (13, 1), (1543, 1), (40253, 1))), 13620867886, True, 13620867859, Factorization(((13620867859, 1),)), 15, 6810433929, True, 2, 204313017870, True),
            WAxisSurface("negative_trace", -2988055724018, 2273736754433, Factorization(((17, 1), (5503, 1), (24304783, 1))), 1218, True, 2031, Factorization(((3, 1), (677, 1))), 298, 338, True, 4, 402896, True),
        ),
        negative_prime_only_guardrail=GuardrailProfile("negative_trace_prime_only_677", 677, Factorization(((677, 1),)), 298, 169, False, True),
        analogue_scan=AnalogueScanProfile(40, 1200, 200000, 2031, 500000, 126, 126, 0, 126, 126, 0, 124, 124, 0, ((0, 126),), 2, 4, True),
        best_surface_name="negative_trace",
        best_surface_rank_surface=402896,
        all_surfaces_below_sqrt=True,
    )
    row_ok = profile == expected and profile.sqrt_floor == SQRT_FLOOR

    print(f"p={profile.p} sqrt_floor={profile.sqrt_floor}")
    print("w_axis_surfaces")
    for row in profile.surfaces:
        print(f"  {row}")
    print(f"negative_prime_only_guardrail={profile.negative_prime_only_guardrail}")
    print(f"analogue_scan_profile={profile.analogue_scan}")
    print("lane_c_laws")
    print("  all three selected-chain and W_axis rank surfaces are below sqrt(p)")
    print("  negative trace n=2031 is the smallest rank surface and passes ord_n(p) >= dim(W_axis)")
    print("  negative trace n=677 alone fails the dimension guardrail: ord_677(p)=169 < 298")
    print("  bounded small analogue axis-injectivity scan found zero injectivity failures")
    print("interpretation")
    print("  laneC_is_not_killed_by_payload_size=1")
    print("  laneC_prime_only_677_shortcut_is_killed=1")
    print("  laneC_first_axis_injectivity_falsifier_passed=1")
    print("  laneC_still_requires_a_p25_moore_or_p_unit_nonvanishing_theorem=1")
    print(f"laneC_w_axis_pilot_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneC_w_axis_pilot_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
