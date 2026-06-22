#!/usr/bin/env python3
"""Count the staged p27 A/B/K f4 -> f5 transition over guard fields.

The f3 -> f4 chart count showed that the selected f3-plus-only component
reproduces the prior gamma handoff, while all-chart fibers are staging
bookkeeping.  This probe repeats the same quotient-transition test one layer
later:

    start with B rows where f4=+1,
    use the frozen v=x7+1/x7 roots from the second reduced-fiber fixture,
    count roots W of F_A(v,W)=0,
    compare chi(W+2) with the frozen f5(B) class.

It is a finite-field guard for the CAS question "does f5/f4 reuse the gamma
class, or is it a fresh half-cover?"  Counts alone do not prove a source law.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from p27_b_line_transition_closure_probe import transition_roots
from p27_kline_reverse_z_relation_probe import parse_ints
from p27_label2_alpha_branch_recurrence_probe import legendre


DEFAULT_SECOND = Path("research/p27/archive/fixtures/p27_b_line_second_reduced_fiber_fixture_20260622.json")
DEFAULT_KUMMER = Path("research/p27/archive/fixtures/p27_b_line_kummer_fixture_packet_20260622.json")


def sign_to_int(label: str) -> int:
    if label == "plus":
        return 1
    if label == "minus":
        return -1
    return 0


def int_to_sign(value: int) -> str:
    if value == 1:
        return "plus"
    if value == -1:
        return "minus"
    if value == 0:
        return "zero"
    return f"bad_{value}"


def load_field(packet: dict[str, Any], q: int) -> dict[str, Any]:
    for fixture in packet["fixtures"]:
        if int(fixture["field"]) == q:
            return fixture
    raise KeyError(f"field {q} missing")


def family_sign_map(kummer_field: dict[str, Any], name: str) -> dict[int, int]:
    for family in kummer_field["families"]:
        if family["name"] == name:
            return {int(row["B"]): sign_to_int(str(row["sign"])) for row in family["rows"]}
    raise KeyError(name)


def run_field(q: int, second: dict[str, Any], kummer: dict[str, Any]) -> None:
    second_field = load_field(second, q)
    kummer_field = load_field(kummer, q)
    f5 = family_sign_map(kummer_field, "f5_conditional")
    f4 = family_sign_map(kummer_field, "f4_conditional")
    stats: Counter = Counter()
    by_b: defaultdict[int, Counter] = defaultdict(Counter)

    for row in second_field["rows"]:
        B = int(row["B"]) % q
        row_sign = sign_to_int(str(row["sign"]))
        if f4.get(B) != row_sign:
            stats["second_fixture_f4_mismatch"] += 1
        if row_sign != 1:
            stats["f4_not_plus_rows_skipped"] += 1
            continue
        if B not in f5:
            stats["f4_plus_missing_f5"] += 1
            continue

        target = f5[B]
        A = (B * B - 2) % q
        stats["f4_plus_B_rows"] += 1
        stats[f"f5_target_{target}"] += 1
        by_b[B]["target"] = target

        for v in sorted({int(value) % q for value in row["v_roots"]}):
            roots = sorted(transition_roots(A, v, q))
            stats[f"W_roots_per_v_{len(roots)}"] += 1
            by_b[B][f"W_roots_per_v_{len(roots)}"] += 1
            signs = {legendre((w + 2) % q, q) for w in roots}
            stats[f"W_gamma_sign_set_{tuple(sorted(signs))}"] += 1
            by_b[B][f"W_gamma_sign_set_{tuple(sorted(signs))}"] += 1
            for w in roots:
                gamma = legendre((w + 2) % q, q)
                stats[f"gamma_{gamma}"] += 1
                by_b[B][f"gamma_{gamma}"] += 1
                if gamma == target:
                    stats["gamma_matches_f5"] += 1
                    by_b[B]["gamma_matches_f5"] += 1
                else:
                    stats["gamma_mismatches_f5"] += 1
                    by_b[B]["gamma_mismatches_f5"] += 1
                rho = legendre((w * w - 4) % q, q)
                orient = legendre((w + A) % q, q)
                stats[f"rho_{rho}"] += 1
                stats[f"orient_{orient}"] += 1
                by_b[B][f"rho_{rho}"] += 1
                by_b[B][f"orient_{orient}"] += 1

    for B, row in by_b.items():
        total = row["gamma_matches_f5"] + row["gamma_mismatches_f5"]
        target = row["target"]
        plus = row["gamma_1"]
        minus = row["gamma_-1"]
        zero = row["gamma_0"]
        stats[f"B_gamma_pmz_{(plus, minus, zero)}"] += 1
        if total and row["gamma_mismatches_f5"] == 0:
            stats["B_all_gamma_matches_f5"] += 1
        elif total and row["gamma_matches_f5"] == 0:
            stats["B_all_gamma_opposes_f5"] += 1
        elif total:
            stats["B_gamma_mixed_vs_f5"] += 1
        if target == 1:
            stats[f"B_target_plus_pmz_{(plus, minus, zero)}"] += 1
        elif target == -1:
            stats[f"B_target_minus_pmz_{(plus, minus, zero)}"] += 1

    print(f"q={q}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")
    den = stats["gamma_matches_f5"] + stats["gamma_mismatches_f5"]
    if den:
        print(f"  gamma_matches_f5_rate = {stats['gamma_matches_f5'] / den:.9f}")
        print(f"  gamma_plus_rate = {stats['gamma_1'] / den:.9f}")
        print(f"  gamma_minus_rate = {stats['gamma_-1'] / den:.9f}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1607,1847,2087")
    parser.add_argument("--second-fixture", type=Path, default=DEFAULT_SECOND)
    parser.add_argument("--kummer-fixture", type=Path, default=DEFAULT_KUMMER)
    args = parser.parse_args()

    second = json.loads(args.second_fixture.read_text())
    kummer = json.loads(args.kummer_fixture.read_text())

    print("p27 ABK f4/f5 transition count probe")
    print("chart = f4-plus B rows, F_A(v,W)=0, next gamma chi(W+2)")
    print(f"second_fixture = {args.second_fixture}")
    print(f"kummer_fixture = {args.kummer_fixture}")
    print("question = does f5/f4 reuse gamma or look fresh on the selected component?")
    for q in parse_ints(args.small_primes):
        run_field(q, second, kummer)
    print("p27_abk_f4_f5_transition_count_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
