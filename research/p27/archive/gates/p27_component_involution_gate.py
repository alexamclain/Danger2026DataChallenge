#!/usr/bin/env python3
"""Automorphism ratios for p27 T_line components.

The component norm audit shows that visible norm squareclasses do not explain
T_line.  This gate asks for a sharper invariant: how the component signs
transform under the EK automorphisms, especially the quotient involution
t -> -1/t that preserves (a,b).
"""

from __future__ import annotations

import argparse
from collections import Counter
import importlib.util
from pathlib import Path
import sys


def load_gate(name: str):
    path = Path(__file__).with_name(name)
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


norm_gate = load_gate("p27_component_norm_gate.py")
transfer = norm_gate.transfer
P = transfer.P


COMPONENTS = (
    "pref",
    "h",
    "vq",
    "h_vq",
    "pref_h",
    "pref_vq",
    "D",
    "T",
    "T_line",
    "line_norm",
)

REFERENCE_SIGNS = (
    "chi_t",
    "chi_B",
    "chi_C",
    "chi_R",
    "chi_a_plus_2",
    "chi_a_minus_2",
    "chi_y_minus_2",
    "chi_one_minus_t2",
    "h_norm",
    "h_inner",
    "v_norm",
    "v_inner",
    "a_chi",
    "b_chi",
    "domain_line",
    "line_norm",
    "h",
    "vq",
    "pref",
)

TRANSFORMS = (
    ("neg_inv_t", transfer.transform_neg_inv_t),
    ("inv_t", transfer.transform_inv_t),
    ("neg_t", transfer.transform_neg_t),
)


def sign_name(sign: int) -> str:
    return {1: "+1", -1: "-1", 0: "0"}.get(sign, "?")


def audit_transform(points: list[tuple[int, int]], transform) -> tuple[int, dict[str, Counter[str]], dict[str, Counter[str]]]:
    ratios = {component: Counter() for component in COMPONENTS}
    matches = {component: Counter() for component in COMPONENTS}
    rows = 0
    for y, w in points:
        source = norm_gate.norm_component_values(y, w)
        image_point = transform(y, w)
        if source is None or image_point is None:
            continue
        image = norm_gate.norm_component_values(*image_point)
        if image is None:
            continue
        rows += 1
        for component in COMPONENTS:
            ratio = image[component] * source[component]
            ratios[component][f"ratio_{sign_name(ratio)}"] += 1
            for ref in REFERENCE_SIGNS:
                ref_value = source.get(ref, 0)
                if ref_value == 0:
                    continue
                if ratio == ref_value:
                    matches[component][ref] += 1
                if ratio == -ref_value:
                    matches[component][f"-{ref}"] += 1
    return rows, ratios, matches


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", default="121")
    parser.add_argument("--chunks", default="0,1")
    parser.add_argument("--tids", default="0:64")
    parser.add_argument("--draws-per-thread", type=int, default=256)
    parser.add_argument("--top-matches", type=int, default=8)
    args = parser.parse_args()

    points, stats = transfer.collect_k_points(
        seeds=transfer.parse_range(args.seeds),
        chunks=transfer.parse_range(args.chunks),
        tids=transfer.parse_range(args.tids),
        draws_per_thread=args.draws_per_thread,
    )

    print("p27_component_involution_gate")
    print(f"p={P}")
    print("sample:")
    for key in ("raw_draws", "nonsplit_y", "k_points"):
        print(f"  {key}={stats[key]}")

    for name, transform in TRANSFORMS:
        rows, ratios, matches = audit_transform(points, transform)
        print(f"transform={name}")
        print(f"  comparable_rows={rows}")
        for component in COMPONENTS:
            exact = [
                (label, count)
                for label, count in matches[component].items()
                if count == rows and rows
            ]
            exact.sort(key=lambda item: item[0])
            top = matches[component].most_common(args.top_matches)
            print(
                "  "
                f"component={component} "
                f"ratio_+1={ratios[component]['ratio_+1']} "
                f"ratio_-1={ratios[component]['ratio_-1']} "
                f"exact={','.join(label for label, _count in exact) or 'none'} "
                f"top={','.join(f'{label}:{count}' for label, count in top)}"
            )

    print("p27_component_involution_gate_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
