#!/usr/bin/env python3
"""Emit machine-readable targets for lambda low-genus screens.

The lambda coordinate

    lambda = -K^2/4

is a Belyi-normalized K-line coordinate.  Split degree <=4 branch divisors and
monomial Belyi recurrences are already negative; the remaining bounded
low-genus screen is exact monic cubic/quartic support in lambda.  A hit would
be diagnostic for K-level branch-class extraction and would still need the
rational K-square lift checked before becoming a source.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from typing import Any

from p27_lambda_branch_divisor_probe import collect_rows, parse_ints


def sign_counts(rows: list[dict[str, int]]) -> Counter:
    stats: Counter = Counter()
    for row in rows:
        stats["rows"] += 1
        if row["sign"] == 1:
            stats["plus"] += 1
        elif row["sign"] == -1:
            stats["minus"] += 1
        else:
            stats["other"] += 1
    return stats


def lambda_rows(q: int, family: str) -> tuple[list[dict[str, int]], Counter]:
    ld3, ld4, stats = collect_rows(q)
    if family == "d3_on_lambda":
        rows = [{"lambda": row.lam, "sign": row.target} for row in ld3]
    elif family == "d4_on_lambda_after_d3":
        rows = [{"lambda": row.lam, "sign": row.target} for row in ld4]
    else:
        raise ValueError(f"unknown family {family!r}")
    return rows, Counter(stats)


def family_payload(q: int, family: str) -> dict[str, Any]:
    rows, source_stats = lambda_rows(q, family)
    counts = sign_counts(rows)
    return {
        "field": q,
        "family": family,
        "coordinate": "lambda",
        "sign_convention": "+1 means target/square side; -1 means complement",
        "row_count": counts["rows"],
        "plus_count": counts["plus"],
        "minus_count": counts["minus"],
        "source_stats": dict(sorted(source_stats.items())),
        "rows": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1471,1607,1847")
    parser.add_argument("--families", default="d3_on_lambda,d4_on_lambda_after_d3")
    parser.add_argument("--indent", type=int, default=2)
    args = parser.parse_args()

    families = [part.strip() for part in args.families.split(",") if part.strip()]
    fields = parse_ints(args.small_primes)
    packet = {
        "name": "p27_lambda_lowgenus_targets",
        "purpose": "Exact finite-field lambda rows for monic cubic/quartic low-genus support screens",
        "coordinate": "lambda=-K^2/4",
        "families": families,
        "fields": fields,
        "polynomial_family": "chi(lambda^d+a_{d-1}lambda^{d-1}+...+a_0), d in {3,4}, global polarity allowed",
        "zero_policy": "exclude polynomials that vanish on any listed lambda row",
        "rational_source_warning": "lambda alone is not a rational p27 source quotient; hits must lift to the K-square stratum",
        "targets": [family_payload(q, family) for q in fields for family in families],
        "sentinel": "p27_lambda_lowgenus_target_packet_rows=1/1",
    }
    print(json.dumps(packet, indent=args.indent, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
