#!/usr/bin/env python3
"""Genus/component pressure from p27 no-R reduced-cover point counts.

This is not a replacement for normalization.  It is a small diagnostic over
the existing localized-cover layer-count output.  If the no-R reduced cover
were a single smooth low-genus component over a tested field, the affine count
would have to satisfy the Hasse-Weil upper bound for its projective completion:

    N_aff <= N_proj <= q + 1 + 2*g*sqrt(q).

Boundary points removed by localization only make N_aff smaller than N_proj,
so a positive excess over q+1 gives a one-component genus lower bound.  If the
one-component assumption is false, the same count is evidence for nontrivial
component/field-of-definition behavior, not a simple genus-0/1 source.
"""

from __future__ import annotations

import argparse
import math
import re
from dataclasses import dataclass
from pathlib import Path


DEFAULT_INPUT = Path("research/p27/archive/probe_outputs/p27_b_line_localized_cover_layer_count_probe_20260622.txt")


@dataclass(frozen=True)
class FieldCount:
    label: str
    q: int
    noR_reduced_U: int
    noR_gamma: int
    full_reduced_U: int


def parse_counts(path: Path) -> list[FieldCount]:
    fields: list[FieldCount] = []
    label = ""
    q: int | None = None
    values: dict[str, int] = {}
    header_re = re.compile(r"^GF\(([^)]+)\) q=(\d+):$")
    value_re = re.compile(r"^  ([A-Za-z0-9_]+) = (\d+)$")

    for raw_line in path.read_text().splitlines():
        line = raw_line.rstrip()
        header = header_re.match(line)
        if header:
            if q is not None:
                fields.append(
                    FieldCount(
                        label=label,
                        q=q,
                        noR_reduced_U=values["noR_reduced_U_points"],
                        noR_gamma=values["noR_gamma_points"],
                        full_reduced_U=values["full_reduced_U_points"],
                    )
                )
            label = header.group(1)
            q = int(header.group(2))
            values = {}
            continue
        match = value_re.match(line)
        if match and match.group(1) in {"noR_reduced_U_points", "noR_gamma_points", "full_reduced_U_points"}:
            values[match.group(1)] = int(match.group(2))

    if q is not None:
        fields.append(
            FieldCount(
                label=label,
                q=q,
                noR_reduced_U=values["noR_reduced_U_points"],
                noR_gamma=values["noR_gamma_points"],
                full_reduced_U=values["full_reduced_U_points"],
            )
        )
    return fields


def genus_lower_bound(count: int, q: int) -> int:
    excess = count - (q + 1)
    if excess <= 0:
        return 0
    return math.ceil(excess / (2 * math.sqrt(q)))


def genus_one_margin(count: int, q: int) -> float:
    return count - (q + 1 + 2 * math.sqrt(q))


def print_table(fields: list[FieldCount]) -> None:
    print("p27 B-line no-R reduced-cover genus/component pressure")
    print("source = localized layer-count output")
    print("interpretation = one-component Hasse-Weil lower bound; otherwise component pressure")
    print()
    print(
        "field q noR_reduced_U noR_per_q excess_over_qplus1 "
        "g_min_if_one_component genus1_margin noR_gamma gamma_per_q full_per_noR"
    )
    for field in fields:
        excess = field.noR_reduced_U - (field.q + 1)
        g_min = genus_lower_bound(field.noR_reduced_U, field.q)
        margin = genus_one_margin(field.noR_reduced_U, field.q)
        full_ratio = field.full_reduced_U / field.noR_reduced_U if field.noR_reduced_U else 0.0
        print(
            f"{field.label} {field.q} {field.noR_reduced_U} "
            f"{field.noR_reduced_U / field.q:.9f} "
            f"{excess} {g_min} {margin:.3f} "
            f"{field.noR_gamma} {field.noR_gamma / field.q:.9f} "
            f"{full_ratio:.9f}"
        )
    print()
    positive = [field for field in fields if field.noR_reduced_U > field.q + 1]
    max_g = max((genus_lower_bound(field.noR_reduced_U, field.q) for field in positive), default=0)
    genus_one_violations = sum(1 for field in fields if genus_one_margin(field.noR_reduced_U, field.q) > 0)
    print(f"positive_excess_fields = {len(positive)}/{len(fields)}")
    print(f"genus_one_violations_if_one_component = {genus_one_violations}/{len(fields)}")
    print(f"max_g_min_if_one_component = {max_g}")
    print("p27_b_line_noR_genus_pressure_probe_rows=1/1")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    args = parser.parse_args()
    print_table(parse_counts(args.input))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
