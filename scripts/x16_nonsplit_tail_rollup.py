#!/usr/bin/env python3
"""Roll up nonsplit X1(16) v2-tail calibration logs.

The active p23 nonsplit run succeeds when v2(#E(Fp)) reaches the target depth.
For X1(16), the geometric baseline after forced order 16 is

    Pr[v2 >= d] ~= 2^(4-d),  d >= 4.

This helper parses exact FFT/brute logs and sampled BSGS logs, then reports
tail ratios against that baseline.  It is a calibration/reporting helper only.
"""

from __future__ import annotations

import argparse
import re
from collections import Counter, defaultdict
from pathlib import Path


def parse_hist(text: str) -> Counter[int]:
    out: Counter[int] = Counter()
    for part in text.split(","):
        part = part.strip()
        if not part or ":" not in part:
            continue
        k, v = part.rsplit(":", 1)
        out[int(k)] += int(v)
    return out


def parse_class_v2_hist(text: str) -> Counter[int]:
    out: Counter[int] = Counter()
    for part in text.split(","):
        part = part.strip()
        match = re.fullmatch(r"nonsplit:v2=(\d+):(\d+)", part)
        if match:
            out[int(match.group(1))] += int(match.group(2))
    return out


def row_from_log(path: Path) -> tuple[int, str, Counter[int]] | None:
    try:
        text = path.read_text(errors="replace")
    except OSError:
        return None
    p_match = re.search(r"^p=(\d+)$", text, re.MULTILINE)
    p = int(p_match.group(1)) if p_match else 0

    class_match = re.search(r"^class_v2_hist=(.*)$", text, re.MULTILINE)
    if class_match:
        hist = parse_class_v2_hist(class_match.group(1))
        if hist:
            return p, "exact", hist

    v2_match = re.search(r"^v2_hist=(.*)$", text, re.MULTILINE)
    if v2_match:
        hist = parse_hist(v2_match.group(1))
        if hist:
            return p, "bsgs", hist

    return None


def baseline(depth: int) -> float:
    if depth <= 4:
        return 1.0
    return 2.0 ** (4 - depth)


def tail(hist: Counter[int], depth: int) -> int:
    return sum(count for e2, count in hist.items() if e2 >= depth)


def print_row(label: str, hist: Counter[int], depths: list[int]) -> None:
    total = sum(hist.values())
    print(f"row={label} total={total} hist=" + ",".join(f"{k}:{hist[k]}" for k in sorted(hist)))
    for depth in depths:
        hits = tail(hist, depth)
        rate = hits / total if total else 0.0
        base = baseline(depth)
        ratio = rate / base if base else 0.0
        print(
            f"  d={depth:2d} hits={hits}/{total} "
            f"rate={rate:.9f} baseline={base:.9f} ratio={ratio:.3f}"
        )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("logs", nargs="+", type=Path)
    ap.add_argument("--depths", default="5,6,7,8,9,10,11,12,13,14,15")
    ap.add_argument(
        "--min-p",
        type=int,
        default=0,
        help="drop rows with parsed p below this value; rows without p are kept only if min-p=0",
    )
    args = ap.parse_args()
    depths = [int(x) for x in args.depths.split(",") if x]

    rows: list[tuple[int, str, Path, Counter[int]]] = []
    for path in args.logs:
        parsed = row_from_log(path)
        if parsed is None:
            continue
        p, source, hist = parsed
        if args.min_p and (not p or p < args.min_p):
            continue
        rows.append((p, source, path, hist))

    if not rows:
        raise SystemExit("no parseable rows")

    print("X1(16) nonsplit v2-tail rollup")
    print("geometric_baseline=Pr[v2>=d]=2^(4-d) for d>=4")
    print(f"rows={len(rows)} min_p={args.min_p}")
    print()

    aggregate_by_source: dict[str, Counter[int]] = defaultdict(Counter)
    aggregate_all: Counter[int] = Counter()
    for p, source, path, hist in rows:
        label = f"{source}:p={p}:{path}"
        print_row(label, hist, depths)
        aggregate_by_source[source].update(hist)
        aggregate_all.update(hist)
        print()

    for source in sorted(aggregate_by_source):
        print_row(f"aggregate_{source}", aggregate_by_source[source], depths)
        print()
    print_row("aggregate_all", aggregate_all, depths)


if __name__ == "__main__":
    main()
