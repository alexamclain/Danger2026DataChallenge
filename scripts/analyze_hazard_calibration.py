#!/usr/bin/env python3
"""Analyze fixed-budget hazard calibration CSVs.

The calibration runner records each independent search as either a hit at
`trials_to_hit` or a censored miss at `budget`.  This analyzer reports
exponential-process hazard estimates and approximate log-rate confidence
intervals for mode comparisons.
"""

from __future__ import annotations

import argparse
import csv
import math
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Group:
    p: int
    mode: str
    runs: int = 0
    hits: int = 0
    exposure: int = 0
    elapsed: float = 0.0
    trace_mass: float = 0.0

    @property
    def hazard(self) -> float:
        return self.hits / self.exposure if self.exposure else 0.0

    @property
    def rate(self) -> float:
        return self.exposure / self.elapsed if self.elapsed else 0.0

    @property
    def effective_hits_per_s(self) -> float:
        return self.hazard * self.rate


def parse_bool(text: str) -> bool:
    return text.strip().lower() in {"1", "true", "yes", "y"}


def load_groups(path: Path) -> dict[tuple[int, str], Group]:
    groups: dict[tuple[int, str], Group] = {}
    with path.open(newline="") as f:
        for row in csv.DictReader(f):
            p = int(row["p"])
            mode = row["mode"]
            key = (p, mode)
            if key not in groups:
                groups[key] = Group(p=p, mode=mode)
            g = groups[key]
            hit = parse_bool(row["hit"])
            budget = int(row["budget"])
            trials_to_hit = row.get("trials_to_hit", "")
            exposure = int(trials_to_hit) if hit and trials_to_hit else budget
            g.runs += 1
            g.hits += 1 if hit else 0
            g.exposure += exposure
            g.elapsed += float(row["elapsed"])
            g.trace_mass = float(row["trace_mass"])
    return groups


def ratio_interval(ratio: float, hits_a: int, hits_b: int, z: float = 1.96) -> tuple[float, float]:
    if ratio <= 0 or hits_a <= 0 or hits_b <= 0:
        return 0.0, float("inf")
    se = math.sqrt(1.0 / hits_a + 1.0 / hits_b)
    return ratio * math.exp(-z * se), ratio * math.exp(z * se)


def fmt_interval(lo: float, hi: float) -> str:
    if math.isinf(hi):
        return "[0, inf]"
    return f"[{lo:.3f}, {hi:.3f}]"


def summarize(path: Path, baseline: str, compare_modes: list[str] | None) -> str:
    groups = load_groups(path)
    by_p: dict[int, dict[str, Group]] = defaultdict(dict)
    for (p, mode), group in groups.items():
        by_p[p][mode] = group

    lines = [f"csv={path}", f"baseline={baseline}", ""]
    for p in sorted(by_p):
        modes = by_p[p]
        if baseline not in modes:
            lines.append(f"p={p} missing baseline mode {baseline}")
            continue
        base = modes[baseline]
        lines.append(f"p={p}")
        for mode in sorted(modes):
            g = modes[mode]
            lines.append(
                "  mode={mode} runs={runs} hits={hits} exposure={exposure} "
                "hazard={hazard:.6e} rate={rate:.3f}/s eff_hits_s={eff:.6e} "
                "trace_mass={tm:.6e}".format(
                    mode=mode,
                    runs=g.runs,
                    hits=g.hits,
                    exposure=g.exposure,
                    hazard=g.hazard,
                    rate=g.rate,
                    eff=g.effective_hits_per_s,
                    tm=g.trace_mass,
                )
            )

        candidates = compare_modes or [m for m in sorted(modes) if m != baseline]
        for mode in candidates:
            if mode not in modes:
                continue
            g = modes[mode]
            hazard_ratio = g.hazard / base.hazard if base.hazard else 0.0
            rate_ratio = g.rate / base.rate if base.rate else 0.0
            effective_ratio = g.effective_hits_per_s / base.effective_hits_per_s if base.effective_hits_per_s else 0.0
            h_lo, h_hi = ratio_interval(hazard_ratio, g.hits, base.hits)
            e_lo, e_hi = ratio_interval(effective_ratio, g.hits, base.hits)
            lines.append(
                "  compare {mode}/{baseline}: hazard_ratio={hr:.3f} "
                "hazard_ratio_approx95={hci} rate_ratio={rr:.3f} "
                "effective_speed_ratio={er:.3f} effective_ratio_approx95={eci}".format(
                    mode=mode,
                    baseline=baseline,
                    hr=hazard_ratio,
                    hci=fmt_interval(h_lo, h_hi),
                    rr=rate_ratio,
                    er=effective_ratio,
                    eci=fmt_interval(e_lo, e_hi),
                )
            )
        lines.append("")
    return "\n".join(lines).rstrip()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("csv", type=Path)
    ap.add_argument("--baseline", default="generic")
    ap.add_argument("--compare-mode", action="append", default=[])
    args = ap.parse_args()

    print(summarize(args.csv, args.baseline, args.compare_mode or None))


if __name__ == "__main__":
    main()
