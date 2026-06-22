#!/usr/bin/env python3
"""Emit the narrowed CAS handoff for the p27 B-line gamma class.

The visible screens have reduced the live B-line question to the class

    gamma^2 = v + 2

over the f3-plus reduced layer.  This packet freezes the guard-field rows for
the staged transition

    A = B^2 - 2
    H^2 = u + 2
    F_A(u,v) = (v^2 - 4)^2 - 4*u*(v^2 - 4)*(v + A)
               + 16*(v + A)^2 = 0
    gamma^2 = v + 2

The materialization root rho^2=v^2-4 is recorded as orientation data, but the
class to extract first is gamma on the generic transition: chi(v+2) is already
constant on all four generic v-roots in the guard fields.
"""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
from typing import Any, Optional

from p27_b_line_gamma_h90_quotient_probe import inv, sqrt_mod_square
from p27_b_line_transition_closure_probe import (
    DEFAULT_FIRST,
    collect_actual_edges,
    load_field,
    transition_roots,
    transition_value,
)
from p27_kline_reverse_z_relation_probe import parse_ints
from p27_label2_alpha_branch_recurrence_probe import legendre


def sign_label(sign: int) -> str:
    if sign == 1:
        return "plus"
    if sign == -1:
        return "minus"
    if sign == 0:
        return "zero"
    return f"bad_{sign}"


def product(values: list[int], p: int) -> int:
    out = 1
    for value in values:
        out = out * (value % p) % p
    return out


def maybe_div(num: int, den: int, p: int) -> Optional[int]:
    iden = inv(den, p)
    if iden is None:
        return None
    return num % p * iden % p


def h90_payload(actual: list[int], u: int, q: int) -> tuple[dict[str, Any], Counter]:
    stats: Counter = Counter()
    if len(actual) != 2:
        stats["h90_bad_actual_count"] += 1
        return {}, stats

    v0, v1 = actual
    g0 = (v0 + 2) % q
    g1 = (v1 + 2) % q
    r = maybe_div(g0, g1, q)
    if r is None:
        stats["h90_zero_denominator"] += 1
        return {}, stats
    ir = inv(r, q)
    if ir is None:
        stats["h90_zero_ratio"] += 1
        return {}, stats
    h = sqrt_mod_square(r, q)
    if h is None:
        stats["h90_ratio_nonsquare"] += 1
        return {}, stats
    ih = inv(h, q)
    if ih is None:
        stats["h90_zero_h"] += 1
        return {}, stats

    h_sym = (h + ih) % q
    h_anti = (h - ih) % q
    r_sym = (r + ir) % q
    h_sym2 = h_sym * h_sym % q
    h_anti2 = h_anti * h_anti % q
    tau = maybe_div(h - 1, h + 1, q)
    tau_sym: Optional[int] = None
    if tau is None:
        stats["h90_tau_denominator_zero"] += 1
    else:
        tau2 = tau * tau % q
        itau2 = inv(tau2, q)
        if itau2 is None:
            stats["h90_tau2_zero"] += 1
        else:
            tau_sym = (tau2 + itau2) % q

    if (r_sym - u) % q:
        stats["h90_rsym_not_u"] += 1
    if (h_sym2 - (u + 2)) % q:
        stats["h90_hsym2_not_uplus2"] += 1
    if (h_anti2 - (u - 2)) % q:
        stats["h90_hanti2_not_uminus2"] += 1

    return {
        "r": int(r),
        "r_sym": int(r_sym),
        "h": int(h),
        "h_inv": int(ih),
        "h_sym": int(h_sym),
        "h_anti": int(h_anti),
        "h_sym2": int(h_sym2),
        "h_anti2": int(h_anti2),
        "tau": None if tau is None else int(tau),
        "tau_sym": None if tau_sym is None else int(tau_sym),
    }, stats


def row_payload(q: int, B: int, u: int, actual_edges: dict[tuple[int, int], set[int]]) -> tuple[dict[str, Any], Counter]:
    stats: Counter = Counter()
    A = (B * B - 2) % q
    generic = sorted(transition_roots(A, u, q))
    actual = sorted(actual_edges.get((B, u), set()))
    missing = [v for v in generic if v not in set(actual)]

    stats[f"generic_roots_{len(generic)}"] += 1
    stats[f"actual_roots_{len(actual)}"] += 1
    stats[f"missing_roots_{len(missing)}"] += 1
    if len(generic) != 4:
        stats["bad_generic_root_count"] += 1
    if len(actual) != 2:
        stats["bad_actual_root_count"] += 1
    if len(missing) != 2:
        stats["bad_missing_root_count"] += 1
    if not set(actual).issubset(set(generic)):
        stats["actual_not_subset_generic"] += 1

    for v in generic:
        if transition_value(A, u, v, q):
            stats["transition_value_nonzero"] += 1

    gamma_signs = [legendre((v + 2) % q, q) for v in generic]
    rho_signs = [legendre((v * v - 4) % q, q) for v in generic]
    orient_signs = [legendre((v + A) % q, q) for v in generic]
    f4_sign = gamma_signs[0] if gamma_signs else 0
    if any(sign != f4_sign for sign in gamma_signs):
        stats["generic_gamma_not_constant"] += 1
    if any(v in actual and rho_signs[i] != 1 for i, v in enumerate(generic)):
        stats["actual_rho_not_square"] += 1
    if any(v in actual and orient_signs[i] != 1 for i, v in enumerate(generic)):
        stats["actual_vplusA_not_square"] += 1
    if any(v in missing and rho_signs[i] != -1 for i, v in enumerate(generic)):
        stats["missing_rho_not_nonsquare"] += 1
    if any(v in missing and orient_signs[i] != -1 for i, v in enumerate(generic)):
        stats["missing_vplusA_not_nonsquare"] += 1

    generic_gamma_norm = product([(v + 2) % q for v in generic], q)
    actual_gamma_norm = product([(v + 2) % q for v in actual], q)
    missing_gamma_norm = product([(v + 2) % q for v in missing], q)
    expected_generic_norm = 16 * (A - 2) * (A - 2) % q
    if generic_gamma_norm != expected_generic_norm:
        stats["generic_gamma_norm_formula_bad"] += 1
    if legendre(actual_gamma_norm, q) != 1:
        stats["actual_gamma_norm_nonsquare"] += 1
    if legendre(missing_gamma_norm, q) != 1:
        stats["missing_gamma_norm_nonsquare"] += 1

    h_roots: list[int] = []
    H2 = (u + 2) % q
    H = sqrt_mod_square(H2, q)
    if H is None:
        stats["H2_nonsquare"] += 1
    else:
        h_roots = sorted({int(H), int((-H) % q)})
        for root in h_roots:
            if root * root % q != H2:
                stats["H_root_bad"] += 1

    h90, h90_stats = h90_payload(actual, u, q)
    stats.update(h90_stats)

    return {
        "B": int(B),
        "A": int(A),
        "u": int(u),
        "H2": int(H2),
        "H_roots": h_roots,
        "generic_v_roots": [int(v) for v in generic],
        "actual_v_roots": [int(v) for v in actual],
        "missing_v_roots": [int(v) for v in missing],
        "f4": sign_label(f4_sign),
        "generic_gamma_signs": [sign_label(sign) for sign in gamma_signs],
        "rho_square_signs": [sign_label(sign) for sign in rho_signs],
        "v_plus_A_signs": [sign_label(sign) for sign in orient_signs],
        "gamma_norms": {
            "generic": int(generic_gamma_norm),
            "actual": int(actual_gamma_norm),
            "missing": int(missing_gamma_norm),
            "expected_generic": int(expected_generic_norm),
        },
        "h90": h90,
    }, stats


def counter_json(stats: Counter) -> dict[str, int]:
    return {str(key): int(value) for key, value in sorted(stats.items(), key=lambda item: str(item[0]))}


def field_payload(q: int, first: dict[str, Any]) -> dict[str, Any]:
    first_field = load_field(first, q)
    actual_edges, _actual_by_b, edge_stats = collect_actual_edges(q)
    stats: Counter = Counter({f"edge_{key}": value for key, value in edge_stats.items()})
    rows: list[dict[str, Any]] = []

    for fixture_row in first_field["rows"]:
        if str(fixture_row["sign"]) != "plus":
            continue
        B = int(fixture_row["B"]) % q
        for raw_u in fixture_row["u_roots"]:
            payload, row_stats = row_payload(q, B, int(raw_u) % q, actual_edges)
            rows.append(payload)
            stats.update(row_stats)

    stats["handoff_rows"] = len(rows)
    stats["f4_plus"] = sum(1 for row in rows if row["f4"] == "plus")
    stats["f4_minus"] = sum(1 for row in rows if row["f4"] == "minus")
    stats["B_count"] = len({row["B"] for row in rows})

    return {
        "field": int(q),
        "row_count": len(rows),
        "stats": counter_json(stats),
        "rows": rows,
    }


def packet_json(fields: list[int], first: dict[str, Any]) -> dict[str, Any]:
    return {
        "name": "p27_b_line_gamma_class_handoff",
        "date": "2026-06-22",
        "target_prime": "1000000000000000000000000103",
        "purpose": (
            "CAS/GPU handoff for the remaining B-line moonshot: extract the "
            "Kummer class of gamma^2=v+2 over the f3-plus reduced layer and "
            "decide whether it is sourceable, recurrent, or a fresh half-cover."
        ),
        "field_signature": {
            "q_mod_16": 7,
            "chi_minus_one": -1,
            "chi_two": 1,
        },
        "equations": {
            "base": "A = B^2 - 2",
            "f3_h90_layer": "H^2 = u + 2; use p27_b_line_reduced_cover_symbolic_packet for the actual B-u source equations",
            "transition": "(v^2 - 4)^2 - 4*u*(v^2 - 4)*(v + A) + 16*(v + A)^2 = 0",
            "materialization": "rho^2 = v^2 - 4; actual selected source keeps chi(v^2-4)=chi(v+A)=+1",
            "gamma_class": "gamma^2 = v + 2",
            "generic_gamma_norm": "Norm_generic(v+2) = 16*(A-2)^2",
            "actual_h90_quotient": "for actual pair v0,v1: r=(v0+2)/(v1+2), r+1/r=u, (h+1/h)^2=u+2 when h^2=r",
        },
        "fixtures": [field_payload(q, first) for q in fields],
        "cas_tasks": [
            {
                "priority": 10,
                "name": "Normalize the f3-plus B-u-H base",
                "compute": [
                    "use the reduced-cover symbolic packet as the source model",
                    "adjoin H^2=u+2 only on the f3-plus component",
                    "record genus, component count, branch support, and visible involutions",
                ],
                "promote_if": "the f3-plus base has a low-genus/sourceable quotient carrying the selected sequence",
                "kill_if": "the base is already generic and high-genus with no useful quotient",
            },
            {
                "priority": 20,
                "name": "Extract gamma divisor/Kummer class",
                "compute": [
                    "on F_A(u,v)=0 over the normalized f3-plus base, compute div(v+2) modulo squares",
                    "test whether gamma is a pullback from B/u/H, an H90 coboundary, a translate, or a quotient class",
                    "separate the generic transition class from the rho materialization orientation",
                ],
                "promote_if": "gamma is pullback/coboundary/low-genus/sourceable or controls more than one selected gate",
                "kill_if": "gamma is a fresh independent half-cover on every useful quotient",
            },
            {
                "priority": 30,
                "name": "Compare with next gate",
                "compute": [
                    "repeat the same transition after f4-plus to obtain the f5/f4 class",
                    "compare branch divisors and Kummer classes against gamma",
                    "ask GPU only for transition telemetry that includes these named class coordinates",
                ],
                "promote_if": "one recurrence/source law couples gamma to the next selected class",
                "kill_if": "f5/f4 is another unrelated fresh half-cover with geometric half-loss",
            },
        ],
        "gpu_task": {
            "run_only_if": "CAS names a quotient/class coordinate, or GPU telemetry can emit these coordinates cheaply",
            "emit": [
                "raw source draw denominator",
                "B,A,u,H2,H_roots",
                "generic_v_roots or compact symmetric functions",
                "actual/missing orientation signs",
                "gamma sign",
                "next-gate f5/f4 analogue",
            ],
            "promote_if": "target survivors per raw source draw improves by at least 1.25x or a direct sampler avoids fresh half-loss",
            "kill_if": "only conditional lift appears after paying a fresh classifier",
        },
        "do_not_run": [
            "more visible B/H/tau relation scans without a new named class",
            "GPU production from gamma buckets before raw-source accounting",
            "treating rho/materialization as the moonshot class",
            "using one-sided small-field f5/f6 tails as recurrence evidence",
        ],
        "sentinel": "p27_b_line_gamma_class_handoff_rows=1/1",
    }


def print_text(packet: dict[str, Any]) -> None:
    print("p27 B-line gamma class handoff")
    print()
    print("Purpose:")
    print("  Package the surviving B-line moonshot as a class-extraction task.")
    print("  The first class to extract is gamma^2=v+2 on the generic transition")
    print("  over the f3-plus B-u-H layer; rho^2=v^2-4 is materialization data.")
    print()
    print("Equations:")
    for key, value in packet["equations"].items():
        print(f"  {key}: {value}")
    print()
    print("Guard-field summaries:")
    for fixture in packet["fixtures"]:
        stats = fixture["stats"]
        print(
            f"  q={fixture['field']}: rows={fixture['row_count']} "
            f"B={stats.get('B_count', 0)} f4={stats.get('f4_plus', 0)}/"
            f"{stats.get('f4_minus', 0)} "
            f"generic4={stats.get('generic_roots_4', 0)} "
            f"actual2={stats.get('actual_roots_2', 0)} "
            f"missing2={stats.get('missing_roots_2', 0)}"
        )
        bad_markers = (
            "formula_bad",
            "not_subset",
            "nonzero",
            "not_square",
            "not_nonsquare",
            "not_constant",
            "nonsquare",
            "zero_denominator",
            "zero_ratio",
            "zero_h",
            "tau_denominator_zero",
            "tau2_zero",
        )
        bad_keys = [
            key for key, value in stats.items()
            if value and (key.startswith("bad_") or any(marker in key for marker in bad_markers))
        ]
        if bad_keys:
            print("    warnings:")
            for key in bad_keys:
                print(f"      {key}={stats[key]}")
    print()
    print("Next concrete tests:")
    for task in packet["cas_tasks"]:
        print(f"  {task['priority']}. {task['name']}")
        print(f"     promote: {task['promote_if']}")
        print(f"     kill: {task['kill_if']}")
    print()
    print("JSON fixture:")
    print("  research/p27/archive/fixtures/p27_b_line_gamma_class_handoff_20260622.json")
    print()
    print(packet["sentinel"])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1607,1847,2087")
    parser.add_argument("--first-fixture", type=Path, default=DEFAULT_FIRST)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    first = json.loads(args.first_fixture.read_text())
    packet = packet_json(parse_ints(args.small_primes), first)
    if args.json:
        print(json.dumps(packet, indent=2, sort_keys=True))
    else:
        print_text(packet)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
